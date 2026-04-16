import os, sys, json
import helper
from os import path

#TODO: def get_file_name()

#INFO: This .json format is based on the Optolith one
def normalize_json(json_object: dict) -> dict:
    #Maybe should I .pop(key, None) unnecesseary keys again?
    return helper.recursive_dict_merge(
        helper.create_empty_json(),
        json_object 
    )
    

def get_json_from_file(file_path:str) -> dict:
    json_object = {}
    with open(file_path, 'r') as file:
        json_object = json.loads(file.readline())      
   
    return normalize_json(json_object)

if __name__ == '__main__':
    #INFO: debugging tool
    file_name = ""
    if len(sys.argv[1:]) >= 1:
        file_name = sys.argv[1]
    else:
        file_name = 'default.json'
    
    DIR_PATH  = os.getcwd()
    FILE_PATH = path.join(DIR_PATH, file_name)
    
    json_object = get_json_from_file(FILE_PATH)

    helper.print_json_tree(json_object)