from os import path

#INFO: own modules
import character, extract

PDF_NAME = 'herbert.pdf'
DIR_PATH = f"{path.dirname(path.abspath(__file__))}"
PDF_PATH = path.join(DIR_PATH, PDF_NAME)

#HELD_NAME = 'Held_Name'

CHAR = character.Abenteurer(
    extract.get_name_value(PDF_PATH),
    extract.get_attribute_values(PDF_PATH),
    extract.get_talent_values(PDF_PATH)
)

               
MAIN_MENU_TEXT = f"""
Type one of the following options:
[show] Show character stats
[roll] Roll on a selected value
[mode] Select input mode
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
[roll -a/-t id mod]
roll = mandatory for initiating roll command
-a/-t = you must use either -a for attribute or -t for talent
id = id of value to be rolled
mod (optional) = roll modificator, must be valid integer. Can either be negative or positive

Or type one of the following options:
[exam] Get examples for the roll command 
[help] Print (this) menu text
[exit] returns to main menu
"""

ROLL_EXAMPLE_TEXT = f"""Examples for roll command:
Roll on KK
=> roll -a KK

Roll on KL easier by 2
=> roll -a KL 2

Roll on Klettern
=> roll -t 2

Roll on Sinneschärfe harder by 1
=> roll -t 9 -1
"""

def menu_show(char):
    print(SHOW_MENU_TEXT)
    while True:
        p = input(f"=> ")
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

    try:    
        if p[:5] != 'roll ':
            print("ERROR: Invalid Input")
            return False
        if p[5:8] != '-a ' and p[5:8] != '-t ':
            print("ERROR: Invalid flag, -a or -t expected") 
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
            print(char.doProbeTalent(id, mod).getResultStr())
        else:
            print("ERROR: this should not happen!")
            return False
        

        return True
    except:
        print("SOMETHING WENT WRONG!")
        return False    


def roll_menu(char):
    print(ROLL_MENU_TEXT)
    while True:
        p = input(f"=> ")
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
    p = input(f"=> ")
    
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