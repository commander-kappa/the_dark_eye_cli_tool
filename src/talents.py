import pymupdf

def sortTalents(table, categories):
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
        

def GET_TALENTS(pdf):
    talents = []
    with pymupdf.open(pdf) as doc:
        CATEGORIES = {
            'Körpertalente MU/GE/KK S. 188 - 194': 'Körper',
            'Wissenstalente KL/KL/IN S. 201 - 206': 'Wissen',
            'Gesellschaftstale': 'Gesellschaft',
            'Handwerkstalent': 'Handwerk',
            'Naturtalente': 'Natur'
        }
        PAGE_INDEX =1
        TABLE_INDEX = 1
   
        page = doc[PAGE_INDEX]
        page_tables = page.find_tables().tables
        
        talents = sortTalents(page_tables[TABLE_INDEX].extract(), CATEGORIES)
    return talents
       


if __name__ == "__main__":
    TALENTS = GET_TALENTS('herbert.pdf') 
    for e in TALENTS:
        print(e)