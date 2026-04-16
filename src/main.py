import os, sys
from os import path
import character, parse_json, helper
from cli import cli_main, EYE_ASCII_ART

if __name__ == '__main__':
    #INFO DIR_PATH changed to 'res'
    DIR_PATH = helper.DIR_PATH
    INI_NAME = 'default.ini'
    INI_PATH = path.join(DIR_PATH, INI_NAME)
    JSON_NAME = 'default.json'

    #1) Get .json from cli arguments
    if len(sys.argv[1:]) >= 1: 
        JSON_NAME = sys.argv[1]
        DIR_PATH = os.getcwd()
    #2) Get .json from default.ini
    else:
        try:
            with open(INI_PATH, 'r') as ini:
                for line in ini:

                    pair = line.split('=', 2)
                    pair[1] = pair[1].replace('\n', '')
                    if pair[0] == 'JSON':
                        JSON_NAME = pair[1]
        except FileNotFoundError:
            helper.init_res_dir()
        except:
            print("ERROR: INI could not be parsed")
    
    JSON_PATH = path.join(DIR_PATH, JSON_NAME)

    #3) Get .json from manual CLI entry 
    while not path.exists(JSON_PATH):
        print(f"File '{JSON_PATH}' does not exist!")
        JSON_PATH = path.join(
            DIR_PATH,
            helper.validator_loop('Enter new file name => ', 'json')
        )

    CHAR = character.Abenteurer(parse_json.get_json_from_file(JSON_PATH)) 

    print(EYE_ASCII_ART)
    cli_main(char=CHAR)