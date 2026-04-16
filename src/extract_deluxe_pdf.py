import pymupdf
import attributes, talents, data
import os, sys, re, json
from os import path
from helper import remove_non_numbers as rm_NaN
from helper import validate_file_name, validator_loop, create_empty_json
import helper

def extract_char_info(pdf: str) -> dict:
    info = {
        'name': '',
        'ap': {'total': 0},
        'sex': '',
        'pers': {
            'family': '',
            'placeofbirth': '',
            'dateofbirth': '',
            'age': 0,
            'size': 0,
            'weight': 0,
            'characteristics': '',
            'cultureAreaKnowledge': ''
        },
    }

    with pymupdf.open(pdf) as doc:
        page = doc[0]

        for widget in page.widgets():
            print(f"{widget.field_name} => {widget.field_value}")
            match widget.field_name:
                case 'Held_Name':
                    info['name'] = str(widget.field_value)
                
                case 'Held_Geschlecht':
                    if widget.field_value.lower() in ['männlich', 'm', 'mann', 'male']:
                        info['sex'] = 'm'
                    elif widget.field_value.lower() in ['weiblich', 'f', 'w', 'frau', 'female']:
                        info['sex'] = 'f'

                case 'Held_Familie':
                    if info['pers']['family'] != '':
                       info['pers']['family'] += ", "
                    info['pers']['family'] += widget.field_value

                case 'Held_Sonstiges_1':
                    if info['pers']['family'] != '':
                        info['pers']['family'] += ", "
                    info['pers']['family'] += widget.field_value

                case 'Held_Titel':
                    if info['pers']['characteristics'] != '':
                        info['pers']['characteristics'] += ", "
                    info['pers']['characteristics'] += widget.field_value
               
                case 'Held_Charakteristika':
                    if info['pers']['characteristics'] != '':
                        info['pers']['characteristics'] += ", "
                    info['pers']['characteristics'] += widget.field_value

                case 'Held_Geburtsort':
                    info['pers']['placeofbirth'] = widget.field_value

                case 'Held_Geburtsdatum':
                    info['pers']['dateofbirth'] = widget.field_value

                case 'Held_Alter':
                    try:
                        info['pers']['age'] = int(rm_NaN(widget.field_value))                    
                    except Exception:
                        print("WARNING: Could not transform age into int!")
                    
                case 'Held_Groesse':
                    try:
                        info['pers']['size'] = int(rm_NaN(widget.field_value))                    
                    except Exception:
                        print("WARNING: Could not transform size into int!")
 
                case 'Held_Gewicht':
                    try:
                        info['pers']['weight'] = int(rm_NaN(widget.field_value))                    
                    except Exception:
                        print("WARNING: Could not transform size into int!")

                case 'AP_gesamt':
                    try:
                        info['ap']['total'] = int(rm_NaN(widget.field_value))
                    except Exception:
                        print("WARNING: Could not transform AP into int!")


    return info

def extract_attribute_values(pdf: str) -> list:
    out = [] 
    with pymupdf.open(pdf) as doc:
        page = doc[0]

        for widget in page.widgets():
            if widget.field_name[:2] in data.ATTRIBUTES:
                out.append(int(widget.field_value))
    return out



#TODO: old extraction functions are now redundant and must be replaced
def sort_raw_talents(table, categories) -> list:
    half1 = []; half2 = []; k1 = ''; k2 = ''
    for i in range(len(table)):
        row = table[i]
        if row[0] in categories.keys():
            k1 = categories[row[0]]
        else:
            half1.append(row[:7] + [k1])
        if row[7] == None:
            continue
        elif row[7] in categories.keys():
            k2 = categories[row[7]]
        else:
            half2.append(row[7:] + [k2])
    return half1 + half2

def extract_raw_talents(pdf: str):
    talents = []
    with pymupdf.open(pdf) as doc:
        #INFO: String Indicators for the german deluxe pdf!
        CATEGORIES = {
            'Körpertalente MU/GE/KK S. 188 - 194': 'Körper',
            'Wissenstalente KL/KL/IN S. 201 - 206': 'Wissen',
            'Gesellschaftstale': 'Gesellschaft',
            'Handwerkstalent': 'Handwerk',
            'Naturtalente': 'Natur'
        }
        PAGE_INDEX = 1
        TABLE_INDEX = 1
   
        page = doc[PAGE_INDEX]
        page_tables = page.find_tables().tables
        
        talents = sort_raw_talents(page_tables[TABLE_INDEX].extract(), CATEGORIES)
    return talents

def filter_raw_talents(raw_talents):
    out = []
    for t in raw_talents:
        out.append([t[4], t[6]])
    return out


def convert_pdf(file_path:str, file_name:str) -> None:
    file_name = file_name.replace('.pdf', '')
    pdf_path = os.path.join(file_path, file_name + '.pdf') 
    json_path = os.path.join(file_path, file_name + '.json')
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError
    
    json_object = create_empty_json()

    for key, val in extract_char_info(pdf_path).items():
        json_object[key] = val 

    i = 0
    for t in filter_raw_talents(extract_raw_talents(pdf_path)):
        i += 1
        json_object['talents'][f"TAL_{i}"] = t[0]
        json_object['talents_notes'][f"TAL_{i}"] = t[1]

    i = 0
    for a in extract_attribute_values(pdf_path):
        i += 1
        json_object['attr']['values'].append({'id': f"ATTR_{i}", 'value': a})  

    while os.path.exists(json_path):
        print(f"WARNING: '{file_name}.json' already exists! Do you wish to overwrite?")
        p = input("[y/n] => ")
        if p == 'y':
            break
        if p == 'n':
            file_name = validator_loop('Enter new json file name => ', 'json')
            file_name = file_name.replace('.json', '')
            json_path = os.path.join(file_path, file_name + '.json')
    
    with open(json_path, 'w') as json_file:
        json.dump(json_object, json_file)


if __name__ == '__main__':
    files = []
    dir_path = helper.DIR_PATH

    #1) Get .pdf from sys args
    if len(sys.argv[1:]) >= 1:
        files = sys.argv[1:]
        dir_path = os.getcwd()
    
    #2) Get .pdf from manual entry within res dir
    else: 
        helper.init_res_dir()
        file_name = validator_loop('Enter pdf file name => ', 'pdf')
        files.append(file_name)

    for file_name in files:
        try:
            convert_pdf(dir_path, file_name)
        except FileNotFoundError as f:
            print(f"ERROR: '{file_name}.pdf' not found!")
            print(f)
        