import talents, attributes
from dice import ROLL_DICE

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

#TODO: All other elements of a char sheet espcially: Heldeninfo, Vor-und-Nachteile, Sonderfertigkeiten, Kampf-stats
class Abenteurer():
    #TODO: Add all Type indicators
    #TODO: No more internal printing?!
    def __init__(self, name:str, attributWerte, talentWerte):
        self.name = name
        self.attribute = attributes.parse_attributWerte(attributWerte)
        self.talente = talents.parse_talentWerte(talentWerte)

    def showAttributes(self, id_range=None) -> str:
        out = ''
        
        if id_range is None:
            for key, val in self.attribute.items():
                #out += f"[{key}] {val.attribut.name:<Attribut.LONGEST_NAME_LEN}: {val.wert}\n"
                out += val.toStr()
        else:
            keys = []
            for i in range(id_range[0], id_range[1] + 1):
                keys.append(attributes.IDS[i])
            for key in keys:
                val = self.attribute[key]
                #out += f"[{key}] {val.attribut.name:<Attribut.LONGEST_NAME_LEN} {val.wert}\n"
                out += val.toStr()
        
        return out

    def showTalente(self, id_range=None) -> str:
        out = ''
        
        if id_range is None:
            id_range = range(len(self.talente))
        else:
            for id in id_range:
                if id >= len(self.talente) or id < (len(self.talente)) * -1: #INFO: negative indexiation is an intended feature!
                    return f"ERROR: Talent ID [{id}] is out of range"
            id_range = range(id_range[0], id_range[1] + 1)
    
        k = ''
        for i in id_range:
            if self.talente[i].talent.kategorie != k:
                k = self.talente[i].talent.kategorie
                #out += f"======= [{k}] =======\n"
                out += self.talente[i].getCategorySeperator()
            out += f"[{i:02}] " + self.talente[i].toStr(withCat=False) + '\n'
        
        return out

    def doProbeAttribut(self, id:int, mod:int=0) -> str:
        r = ROLL_DICE(1, 20)

        out = self.attribute[id].toStr() + "\n"
        if r[0] + mod > self.attribute[id].wert:
            out += f"(FEHLSCHLAG) {r[0]} {mod:+}"
        else:
            out += f"(ERFOLG) {r[0]} {mod:+}"
        
        return out

    def getProbeWerte(self, probe) -> str:
        return f"{self.attribute[probe[0]].wert}/{self.attribute[probe[1]].wert}/{self.attribute[probe[2]].wert}"
    
    def doProbeTalent(self, id:int, mod:int=0) -> talents.TalentProbeErgebnis:
        rolls = ROLL_DICE(3, 20)
        
        if abs(id) + 1 > len(self.talente):
            print(f"ERROR: Talent ID [{id}] is out of range")
            #TODO: Find fitting return type
            raise Exception
        
        tw = self.talente[id]
        
        over = 0
        crit = CRIT_NONE

        n1 = 0; n20 = 0; p = 0
        for i in range(3):
            probeAttribut = self.attribute[tw.talent.probe[i]]
            if rolls[i] == 1:
                n1 = n1 + 1
                p = i
            elif rolls[i] == 20:
                n20 = n20 + 1
                p = i

            dif = rolls[i] + mod - probeAttribut.wert
            if dif > 0:
                over = over + dif
        bWurf = ''
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
        elif n1 >= 2:
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
