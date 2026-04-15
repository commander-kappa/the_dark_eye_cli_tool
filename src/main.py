import os, sys
from os import path
import character, parse_json, helper
from cli import cli_main, EYE_ASCII_ART

if __name__ == '__main__':
    DIR_PATH = f"{path.dirname(path.abspath(__file__))}"
    INI_NAME = 'default.ini'
    INI_PATH = path.join(DIR_PATH, INI_NAME)
    JSON_NAME = 'herbert.json'

    if len(sys.argv[1:]) >= 1:
        JSON_NAME = sys.argv[1]
    else:
        with open(INI_PATH, 'r') as ini:
            for line in ini:
                try:
                    pair = line.split('=', 2)
                    pair[1] = pair[1].replace('\n', '')
                    if pair[0] == 'JSON':
                        JSON_NAME = pair[1]
                except:
                    print("ERROR: INI could not be parsed")
    
    JSON_PATH = path.join(DIR_PATH, JSON_NAME)

    while not path.exists(JSON_PATH):
        print(f"File '{JSON_PATH}' does not exist!")
        JSON_PATH = path.join(
            DIR_PATH,
            helper.validator_loop('Enter new file name => ', 'json')
        )

    CHAR = character.Abenteurer(parse_json.get_json_from_file(JSON_PATH)) 

    print(EYE_ASCII_ART)
    cli_main(char=CHAR)