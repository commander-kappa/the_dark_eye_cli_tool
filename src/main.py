from os import path
import traceback
#INFO: own modules
import character, extract_deluxe_pdf
from dice import ROLL_DICE
import cli
from cli import cli_main

EXTRACT_MODE='PDF'

#TODO: I should probably abandon the live PDF approach and instead write a json parser

DIR_PATH = f"{path.dirname(path.abspath(__file__))}"

INI_NAME = 'default.ini'
INI_PATH = path.join(DIR_PATH, INI_NAME)

PDF_NAME = 'default.pdf'

#INFO: ini parser BETA
with open(INI_PATH, 'r') as ini:
    for line in ini:
        try:
            pair = line.split('=', 2)
            pair[1] = pair[1].replace('\n', '')
            
            if pair[0] == 'PDF':
                PDF_NAME = pair[1]
            if pair[0] == 'JSON':
                pass #INFO: JSON NOT YET IMPLEMENTED!
            
        except:
            print("ERROR: INI could not be parsed")
            input("press enter to exit programm...")
            exit()

PDF_PATH = path.join(DIR_PATH, PDF_NAME)

CHAR = character.Abenteurer(
    extract_deluxe_pdf.get_name_value(PDF_PATH),
    extract_deluxe_pdf.get_attribute_values(PDF_PATH),
    extract_deluxe_pdf.get_talent_values(PDF_PATH)
)


#INFO: New CLI in cli.py

print(cli.EYE_ASCII_ART)
cli_main(char=CHAR)