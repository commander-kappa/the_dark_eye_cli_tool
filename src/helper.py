import re

def remove_non_numbers(inStr: str) -> str:
    NON_NUMBER_REGEX = '[^0-9]'
    return re.sub(NON_NUMBER_REGEX, '', inStr)

#FILE_REGEX = '^[\w,\s-]{1,59}(\.pdf)?$'
MAX_FILE_NAME_LENGTH = 255
MIN_FILE_ENDING_LENGTH = 2

def get_filename_regex(file_ending: str) -> str:
    file_ending = file_ending.replace('.', '')
    if not re.match('^[a-zA-Z]+$', file_ending):
        raise ValueError
    
    flen = len(file_ending)
    if flen > MAX_FILE_NAME_LENGTH - MIN_FILE_ENDING_LENGTH:
        raise ValueError
    
    regex = '^[\\w,\\s-]{' 
    regex += f"{1},{MAX_FILE_NAME_LENGTH - flen - 1}" 
    regex += '}(\\.' 
    regex += file_ending 
    regex += ')?$'

    return regex


def validate_file_name(file_name: str, file_ending: str) -> bool:
    try:
        return re.match(get_filename_regex(file_ending), file_name) is not None
    except ValueError as ve:
        print(f"ERROR: Invalid file ending \'{file_ending}\' set!")
        return False

def validator_loop(input_prompt: str, file_ending: str) -> str:
    while True:
        out = input(input_prompt)
        #print(get_filename_regex(file_ending))
        if validate_file_name(out, file_ending):
            return out

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
        'talents_notes': {}, #INFO: Added for Anmerkungen field
        'spells': {},
        'cantrips': {},
        'liturgies': {},
        'blessings': {},
        'attr': {'values': []}
    }

def recursive_dict_copy(originDict: dict, dataDict: dict) -> dict:
    for key in dataDict.keys():
        if isinstance(dataDict[key], dict) and key in originDict:
            originDict[key] = recursive_dict_copy(originDict[key], dataDict[key])
        else:
            originDict[key] = dataDict[key]
    
    return originDict