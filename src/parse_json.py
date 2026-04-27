import os, sys, json
from os import path

#TODO: def get_file_name() 
#why did I write this?

def create_empty_json() -> dict:
#INFO: This .json format is based on the Optolith one
#Goddammit the Optolith .json format is the most inconsistent fornat i have ever seen
#Maybe I should write my own format and convert the Optolith one
    return {
        'clientVersion': 'dsa_cli_tool',
        'locale': 'de-DE',
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
        'talents': {},
        'talents_notes': {}, #INFO: Added for notes field
        'spells': {},
        'cantrips': {},
        'liturgies': {},
        'blessings': {},
        'attr': {'values': []}
        }

def print_json_tree(json_dict, lvl=0, head='main'):
    #TODO: Output could be a bit prettier, ig
    print(f"----- [{head}] -----")
    stack = []
    for key, val in json_dict.items():
        if isinstance(val, dict):
            stack.append({
                'key': key,
                'val': val
                })
        else:
            print(f"{'='*lvl}>{key}, {val}")
    for item in stack:
        print_json_tree(item['val'], lvl+1, item['key'])

def recursive_dict_merge(originDict: dict, dataDict: dict) -> dict:
    for key in dataDict.keys():
        if isinstance(dataDict[key], dict) and key in originDict:
            originDict[key] = recursive_dict_merge(originDict[key], dataDict[key])
        else:
            originDict[key] = dataDict[key] 
    return originDict


def normalize_json(json_object: dict) -> dict:
    #Maybe should I .pop(key, None) unnecesseary keys again?
    return recursive_dict_merge(
        create_empty_json(),
        json_object 
    )

def get_json_from_file(file_path:str) -> dict:
    json_object = {}
    with open(file_path, 'r') as file:
        json_object = json.loads(file.readline())      
   
    return normalize_json(json_object)

def main():
    #INFO: debugging tool, prints json tree in console
    file_name = ""
    if len(sys.argv[1:]) >= 1:
        file_name = sys.argv[1]
    else:
        file_name = 'default.json'
    
    DIR_PATH  = os.getcwd()
    FILE_PATH = path.join(DIR_PATH, file_name)
    
    json_object = get_json_from_file(FILE_PATH)

    print_json_tree(json_object)

if __name__ == '__main__':
    main()