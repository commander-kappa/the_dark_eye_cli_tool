import talents, attributes
from dice import ROLL_DICE
from helper import remove_non_numbers as rm_NaN

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

#TODO: All other elements of a char sheet espcially: Heldeninfo, Vor-und-Nachteile, Sonderfertigkeiten, Kampf-stats
class Abenteurer():
    #TODO: Add all Type indicators
    #TODO: No more internal printing?!
    def __init__(self, json: dict):
        self.info = {
            'name': json['name'],
            'sex': json['sex']
        }
        for key, val in json['pers'].items():
            self.info[key] = val
        
        self.attributeValues = {}
        #INFO: Optolith .json IS NOT sorted and doesnt c asontain default values! 
        
        for i in range(8):
            #Attrbut.id -> Attribut()
            #INFO: this means the id is redundantely stored (both as the key of self.attributeValuess AND in the value of AttributWert)
            #TODO: find a better universal solution?
            self.attributeValues[attributes.DATA[i].id] = attributes.AttributWert(attributes.DATA[i], 8)
        
        for attr in json['attr']['values']:
            i = int(rm_NaN(attr['id'])) - 1
            id = attributes.DATA[i].id
            self.attributeValues[id].wert = attr['value']

        self.talentValues = []
        for i in range(len(talents.DATA)):
            val = 0; an = ""
            id = f"TAL_{i + 1}"
            if id in json['talents']:
                val = json['talents'][id]
            if id in json['talents_notes']:
                an  = json['talents_notes'][id]
            
            self.talentValues.append(talents.TalentWert(talents.DATA[i], val, 0, an))
            
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

    def showAttributes(self, id_range=None) -> str:
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

    def showTalente(self, id_range=None) -> str:
        out = ''
        
        if id_range is None:
            id_range = range(len(self.talentValues))
        else:
            for id in id_range:
                if id >= len(self.talentValues) or id < (len(self.talentValues)) * -1: #INFO: negative indexiation is an intended feature!
                    print(f"ERROR: Talent ID [{id}] is out of range")
                    raise IndexError
            id_range = range(id_range[0], id_range[1] + 1)
    
        k = ''
        for i in id_range:
            if self.talentValues[i].talent.kategorie != k:
                k = self.talentValues[i].talent.kategorie
                out += self.talentValues[i].getCategorySeperator()
            out += f"[{i:02}] " + self.talentValues[i].toStr(withCat=False) + '\n'
        
        return out

#TODO: ProbeClass with toStr() instead of returning Output string
    def doProbeAttribut(self, id:int, mod:int=0) -> str:
        r = ROLL_DICE(1, 20)[0]        
        val = self.attributeValues[id].wert

        out = self.attributeValues[id].toStr()
        
        r2_txt = ''
        if r == 1:
            r2 = ROLL_DICE(1, 20)[0]
            if r2 <= val:
                return out + f"(KRITISCHER ERFOLG) [{r}, {r2}]\n"
            else:
                r2_txt = f", {r2}"
        elif r == 20:
            r2 = ROLL_DICE(1, 20)[0]
            if r2 > val:
                return out + f"(KRITISCHER FEHLSCHLAG) [{r}, {r2}]\n"
            else:
                r2_txt = f", {r2}"
        
        if r + mod > val:
            return out + f"(FEHLSCHLAG) [{r}{r2_txt}] {mod:+}\n"
        else:
            return out + f"(ERFOLG) [{r}{r2_txt}] {mod:+}\n"
        
    def getProbeWerte(self, probe) -> str:
        return f"{self.attributeValues[probe[0]].wert}/{self.attributeValues[probe[1]].wert}/{self.attributeValues[probe[2]].wert}"
    
    def doProbeTalent(self, id:int, mod:int=0, control_crit:bool=False) -> talents.TalentProbeErgebnis:
        rolls = ROLL_DICE(3, 20)
        
        if abs(id) + 1 > len(self.talentValues):
            print(f"ERROR: Talent ID [{id}] is out of range")
            #TODO: Find fitting return type
            raise IndexError
        
        tw = self.talentValues[id]
        
        over = 0
        crit = CRIT_NONE

        n1 = 0; n20 = 0; p = 0
        for i in range(3):
            probeAttribut = self.attributeValues[tw.talent.probe[i]]
            if rolls[i] == 1:
                n1 = n1 + 1
                p = i
            elif rolls[i] == 20:
                n20 = n20 + 1
                p = i

            dif = rolls[i] + mod - probeAttribut.wert
            if dif > 0:
                over = over + dif

#INFO: bestätigunswurf is not rule compliant for talents! :( but i'll keep it here for homebrew rules
        bWurf = ''
        if control_crit:
            if n1 == 1 and n20 == 1:
                crit = CRIT_NONE
            elif n1 == 1:
                r = ROLL_DICE(1, 20)[0]
                bWurf = f"Bestätigungswurf [{probeAttribut.attribut.id}]: {probeAttribut.wert} x {r}"
                if probeAttribut.wert >= r:
                    crit = CRIT_WIN
            elif n20 == 1:
                r = ROLL_DICE(1, 20)[0] 
                bWurf = f"Bestätigungswurf [{probeAttribut.attribut.id}]: {probeAttribut.wert} x {r}"
                if probeAttribut.wert < r:
                    crit = CRIT_LOOSE
        
        #elif n1 >= 2:
        if n1 >= 2:
            crit = CRIT_WIN
        elif n20 >= 2:
            crit = CRIT_LOOSE
        
        #TODO: find a solution for bWurf and the return. Maybe return getResultStr() here and dont let cli resolve to str
        print(f"roll on: {tw.toStr(formatName=False)}")
        print(f"{self.getProbeWerte(tw.talent.probe)} x {rolls}{mod:+} = FW:{tw.wert} - {over} = {tw.wert - over}")
        if bWurf != '':
            print(bWurf)
        #Is this class actually needed?! Especially once I'm sold on using one string return.
        return talents.TalentProbeErgebnis(tw.wert - over, crit)