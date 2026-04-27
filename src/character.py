import talents, attributes
from dice import ROLL_DICE
from helper import remove_non_numbers as rm_NaN

#TODO: All other elements of a char sheet espcially: Heldeninfo, Vor-und-Nachteile, Sonderfertigkeiten, Kampf-stats
class Character():
    def __init__(self, json: dict):
        self.info = {
            'name': json['name'],
            'sex': json['sex']
        }
        for key, val in json['pers'].items():
            self.info[key] = val
        
        self.attributeValues = {}
        #INFO: Optolith .json IS NOT sorted and doesnt contain default values! 
        
        for i in range(8):
            #Attrbut.id -> Attribute()
            #INFO: this means the id is redundantely stored (both as the key of self.attributeValuess AND in the value of AttributeValue)
            #TODO: find a better universal solution?
            self.attributeValues[attributes.DATA[i].id] = attributes.AttributeValue(attributes.DATA[i], 8)
        
        for attr in json['attr']['values']:
            i = int(rm_NaN(attr['id'])) - 1
            id = attributes.DATA[i].id
            self.attributeValues[id].value = attr['value']

        self.talentValues = []
        for i in range(len(talents.DATA)):
            val = 0; an = ""
            id = f"TAL_{i + 1}"
            if id in json['talents']:
                val = json['talents'][id]
            if id in json['talents_notes']:
                an  = json['talents_notes'][id]
            
            self.talentValues.append(talents.TalentValue(talents.DATA[i], val, 0, an))
            
    #TODO: not all info stats implemented yet!
    def showInfo(self) -> str:
        out = ""

        rows = {
            'Name': self.info['name'],
            'Geschlecht': self.info['sex'],
            'Alter': self.info['age'],
            'Gewicht': self.info['weight'],
            'Größe': self.info['size'],
            'Familie': self.info['family'],
            'Geburtsort': self.info['placeofbirth'],
            'Geburtsdatum': self.info['dateofbirth'],
            'Persönlichkeit': self.info['characteristics'],
        }

        columnSize = 0
        for key in rows.keys():
            if len(key) > columnSize:
                columnSize = len(key)
        
        SPACE_CHAR = '.'
        for key, val in rows.items():
            out += f"{key}{SPACE_CHAR*(columnSize - len(key))} {val}\n"        
        return out

    def showAttributes(self, id_range:list=None) -> str:
        out = ''
        
        if id_range is None:
            for key, val in self.attributeValues.items():
                out += val.toStr()
        else:
            keys = []
            for i in range(id_range[0], id_range[1] + 1):
                keys.append(attributes.DATA[i].id)
            for key in keys:
                out += self.attributeValues[key].toStr()
        
        return out

    def showTalente(self, id_range:list=None) -> str:
        out = ''
        
        if id_range is None:
            id_range = range(len(self.talentValues))
        else:
            for id in id_range:
                if id >= len(self.talentValues) or id < (len(self.talentValues)) * -1: #INFO: negative indexiation is an intended feature!
                    raise IndexError(f"Talent ID [{id}] is out of range")
            id_range = range(id_range[0], id_range[1] + 1)
    
        k = ''
        for i in id_range:
            if self.talentValues[i].talent.category != k:
                k = self.talentValues[i].talent.category
                out += self.talentValues[i].getCategorySeperator()
            out += f"[{i:02}] " + self.talentValues[i].toStr(withCat=False) + '\n'
        
        return out

    def doAttributeCheck(self, id:str, mod:int=0) -> attributes.AttributeCheck:
        return attributes.AttributeCheck(self.attributeValues[id], mod)

    def doTalentCheck(self, id:int, mod:int=0) -> talents.TalentCheck:
        attrVals = []
        talentValue = self.talentValues[id]
        for attr_id in talentValue.talent.check:
            attrVals.append(self.attributeValues[attr_id].value)
        return talents.TalentCheck(attrVals, talentValue.value, mod)

    def getCheckValuesText(self, check) -> str:
        return f"{self.attributeValues[check[0]].value}/{self.attributeValues[check[1]].value}/{self.attributeValues[check[2]].value}"