from os import path
import traceback
#INFO: own modules
import character, extract
from dice import ROLL_DICE

EXTRACT_MODE='PDF'

#INFO: I should probably abandon the live PDF approach and instead write a json parser

DIR_PATH = f"{path.dirname(path.abspath(__file__))}"

INI_NAME = 'default.ini'
INI_PATH = path.join(DIR_PATH, INI_NAME)

PDF_NAME = 'default.pdf'
#INFO: ini parser beta
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
    extract.get_name_value(PDF_PATH),
    extract.get_attribute_values(PDF_PATH),
    extract.get_talent_values(PDF_PATH)
)

EYE_ASCII_ART = """
DAS SCHWARZE AUGE - CLI Tool
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⠁⠀⣠⣶⣿⡿⢿⣷⣦⡀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⠀⠀⢀⣼⣿⣿⣿⣶⣿⣾⣽⣿⡆⠀⠀⠀⠀⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠀⠀⠸⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⠀⠀⠀⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⠀⠀⠀⢿⣿⣿⣿⣿⣿⣯⣿⣿⠏⠀⠀⠀⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⢀⠀⠙⠿⢿⣿⣿⡿⠟⠁⠀⣀⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

MAIN_MENU_TEXT = f"""
Type one of the following options:
[show] Show character stats
[roll] Roll on a selected value
[help] Prints (this) main menu text
[exit] Closes the program"""

SHOW_MENU_TEXT = f"""
Type one of the following options:
[0] Character Info
[1] Attributes
[2] Talents
[help] Prints (this) menu text
[exit] returns to main menu"""

ROLL_MENU_TEXT = f"""
Use the following Syntax to roll:
[roll -a/-t/-d id mod]
roll = mandatory for initiating roll command
-a/-t/-d = you must use either -a for attribute, -t for talent or -d for dice roll
id = id of value to be rolled
mod (optional) = roll modificator, must be valid integer. Can either be negative or positive

Or type one of the following options:
[exam] Get examples for the roll command 
[help] Print (this) menu text
[exit] returns to main menu"""

ROLL_EXAMPLE_TEXT = f"""Examples for roll command:
"Roll on KK"
(roll) => roll -a KK

"Roll on KL easier by 2"
(roll) => roll -a KL 2

"Roll on Klettern"
(roll) => roll -t 2

"Roll on Sinneschärfe harder by 1"
(roll) => roll -t 9 -1

"Roll 1d6"
(roll) => roll -d 6

"Roll 3d20"
(roll) => roll -d 20 3
"""

#TODO: Menu shell rework, no more sepearted loops. i.e. writing roll -t 9 should work from main
def menu_show(char):
    print(SHOW_MENU_TEXT)
    while True:
        p = input(f"(show) => ")
        match p.lower():
            case '0':
                pass
            case '1':
                char.showAttributes()
            case '2':
                char.showTalente()
            case 'help':
                print(SHOW_MENU_TEXT)
            case 'exit':
                print("Returning to main menu")
                break
            case _:
                print("Invalid Input")
                continue

def parse_roll_prompt(p, char) -> bool:
    #TODO: MUST reverse mod positive and negative!
    try:
        if p[:5] != 'roll ':
            print("ERROR: Invalid Input")
            return False
        if p[5:8] not in ['-d ', '-t ', '-a ']:
            print("ERROR: Invalid flag, -a, -t or -d expected") 
            return False
        
        mode = p[6]
        pp = p[8:]
        
        id = ''
        mod = ''
        changeToMod = False

        for c in pp:
            if c == ' ':
                changeToMod = True
            if changeToMod:
                mod += c
            else:
                id += c                
        if mod == '':
            mod = 0
        else:
            try:
                mod = int(mod)
            except:
                print("ERROR: Modificator could not be parsed into int")
                return False

        if mode == 'a':
            id = id.upper()
            if id not in char.attribute.keys():
                print("ERROR: Invalid Attribute ID")
                return False
            char.doProbeAttribut(id, mod)
        elif mode =='t':
            try:
                id = int(id)
            except:
                print("ERROR: Talent ID could not be parsed into int")
                return False
            
            if id not in range(len(char.talente)):
                print("ERROR: Invalid Talent ID")
                return False
            print(char.doProbeTalent(id, mod).getResultStr() + "\n")
        elif mode == 'd':
            try:
                id = int(id)
            except:
                print("ERROR: Dice size could not be parsed into int")
                return False
            
            if mod < 1:
                mod = 1
            try:
                print(f"Roll {mod}d{id} = {ROLL_DICE(mod, id)}")
            except:
                print("ERROR: Dice roll values invalid!")
                return False

        else:
            print("ERROR: this should not happen!")
            return False
        

        return True
    except:
        print("ERROR: SOMETHING WENT WRONG!")
        traceback.print_exc()
        return False    

print(EYE_ASCII_ART)
def roll_menu(char):
    print(ROLL_MENU_TEXT)
    while True:
        p = input(f"(roll) => ")
        match p.lower():
            case 'exam':
                print(ROLL_EXAMPLE_TEXT)
            case 'help':
                print(ROLL_MENU_TEXT)
            case 'exit':
                print("Returning to main menu")
                break
            case _:
                if not parse_roll_prompt(p.lower(), char):
                    print("Roll prompt parsing failed...")
                continue

print(MAIN_MENU_TEXT)
while True:
    p = input(f"(main) => ")
    
    match p.lower():
        case 'show':
            menu_show(CHAR)
        case 'roll':
            roll_menu(CHAR)
        case 'help':
            print(MAIN_MENU_TEXT)
        case 'exit':
            print("Exiting program...")
            break
        case _:
            print("Invalid Input")
            continue