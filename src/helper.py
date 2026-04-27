import re
import os; from os import path

def remove_non_numbers(inStr: str) -> str:
    return ''.join(c for c in inStr if c.isdigit())

DIR_PATH = path.join(path.dirname(path.abspath(__file__)), '..', 'res')

def init_res_dir() -> None:
    os.makedirs(DIR_PATH, exist_ok=True)

    file_path = path.join(DIR_PATH, 'default.ini')
    if not path.exists(path.join(file_path)):
        with open(INI_PATH, 'w') as ini:
            ini.writelines(['PDF=default.pdf', 'JSON=default.json'])
    
    file_path = path.join(DIR_PATH, '.gitignore')
    if not path.exists(path.join(file_path)):
        with open(path.join(file_path, '.gitignore'), 'w') as gitignore:
            gitignore.writelines('*.pdf', '*.json')

#FILE_REGEX = '^[\w,\s-]{1,59}(\.pdf)?$'
MAX_FILE_NAME_LENGTH = 255
MIN_FILE_ENDING_LENGTH = 2

#TODO: Too strict regex?
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
        if validate_file_name(out, file_ending):
            return out