import character
from dice import ROLL_DICE

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
From the main mode you can access all commands, by writing the [mode] first and then follow up with the corresponding Syntax.
You can also change your Command Line to default to a specific [mode], emitting the necessity of indicating the [mode]
All commands, except [exit]/[quit] can be shortened to its first letter (i.e: (show talent -> s talent)

[show] Show character stats
[roll] Roll on a selected value
[help] Prints help text of (mode)
[exit] Closes the program
"""

SHOW_MENU_TEXT = f"""Type one of the following options:

[i] Character Info
[a] Attributes     [(min)(,max)]
[t] Talents        [(min)(,max)]
[help] Prints help text
[roll] Switches to roll mode
[main] returns to main
[exit] Closes the program
"""

ROLL_HELP_TEXT = f"""Use the following Syntax to roll:

[r/roll a/t/d id mod]
r/roll = Mandatory for initiating roll command
a/t/d  = You must use either a for attribute, t for talent or d for dice roll
id     = ID of value to be rolled
mod    = Optional, roll modificator, must be valid integer. Can either be negative or positive
"""

ROLL_MENU_TEXT = f"""Type one of the following options:

[a] Roll on Attribute [ID] [(Mod)]
[t] Roll on Talent    [ID] [(Mod)]
[d] Roll Dice [Size] [(times) = 1]
[exam] Get examples for the roll command 
[help] Print help text
[show] Switches to show mode
[main] returns to main menu
[exit] Closes the program
"""

ROLL_EXAMPLE_TEXT = f"""Examples for roll command:

"Roll on KK"
(main) => roll attribute KK

"Roll on KL easier by 2"
(main) => r a KL -2

"Roll on Klettern"
(roll) => talent 2

"Roll on Sinneschärfe harder by 1"
(roll) => t 9 -1

"Roll 1d6"
(roll) => dice 6

"Roll 3d20"
(roll) => d 20 3
"""

import traceback

def cli_main(mode='main', char:character.Abenteurer=None) -> None:    
    print(select_help(mode))
    while True:
        p = input(f"({mode}) => ")
        command = parse_cli_prompt(p, mode)
        match command[0]:
            #------------- MODE -------------#
            #Make parser like roll instead?
            #Is having different modes actually necesseary, considering the effort it takes to manage the modes?
            case 'MODE_MAIN':
                mode = 'main'
                print(select_help('MAIN'))
                continue
            case 'MODE_SHOW':
                mode = 'show'
                print(select_help('SHOW'))
                continue
            case 'MODE_ROLL':
                mode = 'roll'
                print(select_help('ROLL_MENU'))
                continue
            #------------- HELP -------------#
            case 'HELP':
                print(select_help(command[1]))
                continue
            #------------- ROLL -------------#
            case 'ROLL':
                try:
                    roll_cmd = parse_roll_prompt(command[1])
                    if roll_cmd:
                        roll, id, mod = roll_cmd
                        match roll:
                            case 'd':
                                print(f"Roll {mod}d{id} = {ROLL_DICE(mod, id)}")
                            case 'a':
                                print(char.doProbeAttribut(id, mod))
                            case 't':
                                print(char.doProbeTalent(id, mod).getResultStr() + "\n")
                            case 'h':
                                print(select_help(id))
                            case _:
                                raise Exception
                except Exception as e:
                    print(e)
                    print("ERROR: Could not execute roll")
                continue
            #------------- SHOW -------------#
            case 'SHOW':
                try:
                    show_cmd = parse_show_prompt(command[1])
                    if show_cmd:
                        show, id_range = show_cmd
                        match show:
                            case 'a':
                                print(char.showAttributes(id_range))
                            case 't':
                                print(char.showTalente(id_range))
                            case 'i':
                                print(char.showInfo())
                            case _:
                                raise Exception
                    continue
                except:
                    print("ERROR: Could not show")
                    print(traceback.print_exc())
                    continue
            #------------- EXIT -------------#
            case 'CLEAR':
                print("\n"*255)
            case 'EXIT':
                print("Exiting program...")
                break
            case 'INVALID':
                print("ERROR: Invalid Input")
                continue
            case _:
                print('ERROR: THIS SHOULD NOT HAPPEN (CLI EXCEPTION)')
                continue

#INFO: Used if command format changes in future, but kinda redundant tbh
def return_command(prefix:str, rest=None):
    if rest is None:
        return [prefix]
    else:
        return [prefix, rest]

def parse_cli_prompt(p:str, mode:str='main'):

    parts = p.split(None, 1) #INFO: None is is equivalent to 1-n mulitple whitespaces
    
    if not parts:
        return return_command('INVALID')
    
    p = parts[0]
    rest = parts[1] if len(parts) > 1 else '' #Used to be None

    if rest == '': #Used to be is None
        match p.lower():
            case 'main' | 'return':
                return return_command('MODE_MAIN')
            case 'show':
                return return_command('MODE_SHOW')
            case 'roll':
                return return_command('MODE_ROLL')
            case 'help':
                return return_command('HELP', mode)
            case 'clear':
                return return_command('CLEAR')
            case 'quit' | 'exit':
                return return_command('EXIT')
            case _:
                if mode == 'main':
                    return return_command('INVALID')
    
#    if mode != 'main':
#        rest = p + ' ' + rest
#        p = mode

    if mode == 'main':
        mode = p.lower()
    else:
        rest = p + ' ' + rest


#TODO: Fix that selecting modes other than main, makes it impossible to use "help [mode]"
#INFO: Fixed by writing a help command in the roll and show parser. Not sure if its the best solution  
#INFO: ^ BAD IDEA still cant cross use modes (i.e. roll in show) MUST find solution HERE. Makes change up ahead redundant
#probably need a dict or smth

    #match p.lower():
    match mode:
        case 'roll' | 'r':
            return return_command('ROLL', rest)
        case 'show' | 's':
            return return_command('SHOW', rest)
        case 'help' | 'h':
            return return_command('HELP', rest)
        case _:
            return return_command('INVALID')

#Should I turn this into a dict?
def select_help(id:str) -> str:
    match id.upper():
        case 'MAIN':
            return MAIN_MENU_TEXT
        case 'SHOW':
            return SHOW_MENU_TEXT
        case 'ROLL_MENU':
            return ROLL_MENU_TEXT
        case 'ROLL':
            return ROLL_HELP_TEXT
        case 'ROLL_EXAMPLE':
            return ROLL_EXAMPLE_TEXT
        case _:
            return f"ERROR: HELP TEXT ID [{id}] DOES NOT EXIST!"


def parse_range_str(r:str):
    parts = r.split(',', 1)
    if not parts:
        print(f"ERROR: Range empty")
        raise Exception
    #TODO: Filter cross selection between talents and attributes?
    for i in range(len(parts)):
        #Needs a more distinct method later, ig.
        if parts[i].upper() in character.attributes.DATA:
            parts[i] = character.attributes.DATA.index(parts[i].upper())
        else:
            try:
                #TODO: add abs() ?
                parts[i] = int(parts[i])
            except:
                print(f"ERROR: [{parts[i]}] could not be parsed into ID")
                return
    
    if len(parts) == 1:
        parts.append(parts[0])
    else:
        parts.sort()

    return parts

#INFO: Not all show features are implemented yet!
def parse_show_prompt(p:str):
    parts = p.split(None, 1) #INFO: None is is equivalent to 1-n mulitple whitespaces
    

    id = None
    if not parts:
        print("ERROR: Missing command specificaiton")
        return
    elif len(parts) == 2:
        id = parts[1]
    p = parts[0]
    
    if id is not None:
        try:
            id = parse_range_str(id)
        except:
            raise Exception

    match p.lower():
        case 'talents' | 't':
            return ['t', id]
        case 'attributes' | 'a':
            return ['a', id]
        case 'info' | 'i':
            return ['i', id]
        case _:
            print(f"ERROR: Invalid show command [{p}]")
            return
   


#TODO: Instead of return False, raise Exception?!
def parse_roll_prompt(p:str):
    
    parts = p.split(None, 2) #INFO: None is is equivalent to 1-n mulitple whitespaces
    
    #TODO: should become redundant once main is fixed
    if len(parts) < 2:
        if parts[0] in ['h', 'help']:
            return ['h', 'ROLL', '0']
        else:
            print("ERROR: Missing command specificaiton")
            return False

    p = parts[0] #INFO: -> mode
    id = parts[1]
    mod = parts[2] if len(parts) > 2 else '0'

    mode = '' 
    #Convert to dictionary?
    match p.lower():
        case 'dice' | 'd':
            mode = 'd'
        case 'talent' | 't':
            mode = 't'
        case 'attribute' | 'a':
            mode = 'a'
        #Not yet satisfied with this help implementation
        case 'help' | 'h':
            mode = 'h'
            return [mode, id, mod]
        case _:
            print(f"ERROR: Invalid roll command [{p}]. Use talent/t attribute/a or dice/d")
            return False
    try:
        mod = int(mod)
    except:
        print(f"ERROR: Modificator [{mod}] could not be parsed into int")
        return False

    match mode:
        case 'a':
            id = id.upper()
            return [mode, id, mod]
        case 't':
            try:
                id = int(id)
                return [mode, id, mod]
            except:
                print(f"ERROR: Talent ID [{id}] could not be parsed into int")
                return False
        case 'd':
            try:
                #Should I check values here or in dice.ROLL_DICE ?!
                id = abs(int(id))
                if mod < 1:
                    mod = 1
                if id < 1:
                    id = 1
                return [mode, id, mod]
            except:
                print(f"ERROR: Dice size [{id}] could not be parsed into int")
                return False
        case _: #Is it even necesseary?
            print(f"ERROR: THIS SHOULD NOT HAPPEN (MODE [{mode}] doesnt match in switch-case)")
            return False     



if __name__ == "__main__":
    print('you are running cli.py')
    cli_main()