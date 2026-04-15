import os, sys, json
import helper
from os import path

#TODO: def get_file_name()

#INFO: This .json format is based on the Optolith one
def filter_json(json_object: dict) -> dict:

    '''
    attr = json_object['attr']['values']
    json_object.pop('attr', None)
    json_object['attr'] = {'values': attr}
    
    if not 'talents_notes' in json_object:
        json_object['talents_notes'] = {}

    json_object.pop('dateCreated', None)
    json_object.pop('dateModified', None)
    json_object.pop('id', None)
    json_object.pop('phase', None)
    json_object.pop('locale', None)
    json_object.pop('belongings', None)
    json_object.pop('activatable', None)
    json_object.pop('rules', None)
    json_object.pop('pets', None) 
    '''

    return helper.recursive_dict_copy(
        helper.create_empty_json(),
        json_object 
    )
    
 

def load_file(file_path:str) -> dict:
    json_object = {}
    with open(file_path, 'r') as file:
        json_object = json.loads(file.readline())
    return json_object    

def get_json_from_file(file_path:str) -> dict:
    return filter_json(load_file(file_path))

if __name__ == '__main__':
    #INFO: debugging tool
    file_name = ""
    if len(sys.argv[1:]) >= 1:
        file_name = sys.argv[1]
    else:
        file_name = 'default.json'
    
    DIR_PATH  = path.dirname(path.abspath(__file__))
    FILE_PATH = path.join(DIR_PATH, file_name)
    
    json_object = get_json_from_file(FILE_PATH)

    for key in json_object.keys():
        print(f"{key}: {json_object[key]}")

#pers: {
# 'family': '',
# 'placeofbirth': '', 
# 'dateofbirth': '', 
# 'age': '', 
# 'haircolor': int, 
# 'eyecolor': int, 
# 'size': '', 
# 'weight': '', 
# 'socialstatus': int 
# 'characteristics', 
# 'cultureAreaKnowledge'}

#attr: {
# 'values': [
# {'id': 'ATTR_1', 'value': 14}, #MUT
# {'id': 'ATTR_2', 'value': 10}, #...
# {'id': 'ATTR_3', 'value': 13}, 
# {'id': 'ATTR_5', 'value': 14}, 
# {'id': 'ATTR_6', 'value': 14}, 
# {'id': 'ATTR_7', 'value': 14}, 
# {'id': 'ATTR_8', 'value': 13}
# ], 
# 'attributeAdjustmentSelected': 'ATTR_1', 
# 'ae': 0, 
# 'kp': 0, 'lp': 0, 'permanentAE': {'lost': 0, 'redeemed': 0}, 'permanentKP': {'lost': 0, 'redeemed': 0}, 'permanentLP': {'lost': 0}}

#activatable: {
# 'ADV_37': [{}], 
# 'ADV_31': [{'tier': 1}], 
# 'ADV_15': [], 'ADV_36': [], 'ADV_16': [], 'ADV_4': [], 'ADV_74': [], 'ADV_72': [], 
# 'ADV_17': [{'sid': 'CT_2'}], 
# 'DISADV_48': [{'sid': 'TAL_16'}, {'sid': 'TAL_19'}], 
# 'DISADV_21': [], 
# 'DISADV_14': [{'tier': 1}], 'DISADV_2': [{'tier': 2}], 'DISADV_36': [{'sid': 4}], 'DISADV_37': [{'sid': 5}, {'sid': 8}], 'DISADV_33': [{'sid2': 'Fortschritt', 'sid': 8}, {'sid2': 'Nostrier', 'sid': 7}], 'DISADV_51': [], 'DISADV_5': [], 'DISADV_1': [{'sid': 7, 'tier': 1}], 'DISADV_67': [{}], 'DISADV_70': [], 'DISADV_69': [], 'DISADV_71': [], 'SA_9': [{'sid2': 2, 'sid': 'TAL_10'}, {'sid2': 3, 'sid': 'TAL_24'}], 'SA_27': [{'sid': 9}], 'SA_29': [{'sid': 8, 'tier': 4}], 'SA_1003': [{}], 'SA_18': [{}], 'SA_1088': [{}], 'SA_1101': [{}], 'SA_1098': [{}], 'SA_41': [{'tier': 1}], 'SA_55': [{'tier': 1}], 'SA_153': [{}], 'SA_12': [{'sid': 9}], 'SA_421': [{'tier': 1}], 'SA_60': [{'sid': 2}]}

#talents: {
# 'TAL_3': 6, 
# 'TAL_4': 5, 'TAL_5': 6, 'TAL_7': 4, 'TAL_8': 6, 'TAL_10': 9, 'TAL_13': 8, 'TAL_24': 10, 'TAL_25': 8, 'TAL_34': 3, 'TAL_50': 6, 'TAL_53': 3, 'TAL_51': 7, 'TAL_27': 10, 'TAL_28': 7, 'TAL_40': 5, 'TAL_29': 8, 'TAL_30': 10, 'TAL_14': 5, 'TAL_17': 5, 'TAL_23': 7, 'TAL_26': 3, 'TAL_31': 3, 'TAL_38': 4, 'TAL_46': 5, 'TAL_47': 3, 'TAL_48': 3, 'TAL_52': 7, 'TAL_59': 4, 'TAL_21': 3, 'TAL_20': 2, 'TAL_18': 2, 'TAL_33': 1, 'TAL_32': 1, 'TAL_37': 1, 'TAL_39': 2, 'TAL_19': 1}

#(Kampftechniken):
#ct: {'CT_2': 13, 'CT_13': 8, 'CT_5': 10, 'CT_9': 8}

#belongings: {
# 'items': {
# 'ITEM_2': {
# 'id': 'ITEM_2', 'name': 'Langbogen', 'gr': 2, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.75, 'price': 80, 'damageDiceNumber': 1, 'damageFlat': 8, 'length': 200, 'reloadTime': 2, 'ammunition': 'ITEMTPL_75', 'combatTechnique': 'CT_2', 'damageDiceSides': 6, 'template': 'ITEMTPL_65', 'range': [20, 100, 160], 'isParryingWeapon': False, 'isTwoHandedWeapon': False}, 
# 'ITEM_4': {
# 'id': 'ITEM_4', 'name': 'Pfeil', 'gr': 3, 'amount': 30, 'isTemplateLocked': True, 'price': 0.4, 'template': 'ITEMTPL_75', 'forArmorZoneOnly': False, 'addPenalties': False}, 'ITEM_5': {'id': 'ITEM_5', 'name': 'Schlafsack', 'gr': 7, 'amount': 1, 'isTemplateLocked': True, 'weight': 2, 'price': 7, 'stp': 7, 'template': 'ITEMTPL_172'}, 'ITEM_6': {'id': 'ITEM_6', 'name': 'Beil/Handaxt', 'gr': 7, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.75, 'price': 20, 'at': -1, 'damageDiceNumber': 1, 'damageFlat': 2, 'length': 40, 'pa': -2, 'stp': 30, 'combatTechnique': 'CT_5', 'damageDiceSides': 6, 'reach': 2, 'template': 'ITEMTPL_145', 'imp': 1, 'primaryThreshold': {'threshold': 14}}, 'ITEM_7': {'id': 'ITEM_7', 'name': 'Zunder, 25 Portionen', 'gr': 8, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.025, 'price': 0.2, 'stp': 1, 'template': 'ITEMTPL_191'}, 'ITEM_8': {'id': 'ITEM_8', 'name': 'Zunderdose (Platz für 25 Portionen)', 'gr': 8, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.2, 'price': 1, 'stp': 10, 'template': 'ITEMTPL_192'}, 'ITEM_9': {'id': 'ITEM_9', 'name': 'Feldflasche', 'gr': 10, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.25, 'price': 6, 'stp': 12, 'template': 'ITEMTPL_199'}, 'ITEM_10': {'id': 'ITEM_10', 'name': 'Feuerstein und Stahl', 'gr': 8, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.25, 'price': 3, 'stp': [4, 12], 'template': 'ITEMTPL_188'}, 'ITEM_11': {'id': 'ITEM_11', 'name': 'Verband, 10 Stück', 'gr': 9, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.05, 'price': 12.5, 'stp': 3, 'template': 'ITEMTPL_197'}, 'ITEM_12': {'id': 'ITEM_12', 'name': 'Normale Kleidung', 'gr': 4, 'amount': 2, 'isTemplateLocked': True, 'weight': 1, 'enc': 0, 'pro': 0, 'template': 'ITEMTPL_78', 'armorType': 1}, 'ITEM_13': {'id': 'ITEM_13', 'name': 'Stoffrüstung', 'gr': 4, 'amount': 1, 'isTemplateLocked': True, 'weight': 3, 'price': 75, 'enc': 1, 'pro': 2, 'template': 'ITEMTPL_82', 'armorType': 3}, 'ITEM_14': {'id': 'ITEM_14', 'name': 'Hängematte', 'gr': 7, 'amount': 1, 'isTemplateLocked': True, 'weight': 2, 'price': 2, 'template': 'ITEMTPL_156'}, 'ITEM_15': {'id': 'ITEM_15', 'name': 'Umhängetasche', 'gr': 10, 'amount': 1, 'isTemplateLocked': True, 'weight': 0.5, 'price': 8.5, 'stp': 6, 'template': 'ITEMTPL_214'}}, 'armorZones': {}, 'purse': {'d': '', 's': '', 'h': '', 'k': ''}}

#rules: {'higherParadeValues': 0, 'attributeValueLimit': False, 'enableAllRuleBooks': True, 'enabledRuleBooks': [], 'enableLanguageSpecializations': False}
#pets: {}
