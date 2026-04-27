from dice import ROLL_DICE
from data import TALENTS
import constants as const

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

class Talent():
    LONGEST_NAME_LEN = 0    

    #INFO: not yet in use
    stgDict = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    
    #TODO: Replace aN: str wioth a: Attribute()?
    def __init__(self, 
        name: str,
        kat: str, 
        a1 :str, 
        a2 :str, 
        a3 :str, 
        be: str, 
        stg: str
    ):
        self.name = name
        self.category = kat
        self.encumbrance = be
        self.factor = stg
        self.check = [a1, a2, a3]

        if len(self.name) > Talent.LONGEST_NAME_LEN:
            Talent.LONGEST_NAME_LEN = len(self.name)
       
    def toDict(self) -> dict:
        return {
            "name": self.name,
            "kat": self.category,
            "be": self.encumbrance,
            "stg": self.factor,
            "probe": self.check,
        }

    def getCheckText(self) -> str:
        return f"{self.check[0]}/{self.check[1]}/{self.check[2]}"

class TalentValue():
    def __init__(self, talent:Talent, fw=0, r=0, an:str=''):
        self.talent = talent
        self.value = int(fw)
        self.routine = r
        self.notes = an
   
    def toStr(self, withCat=True, formatName=True, spaceChar='.') -> str:
        t = self.talent
        out = ''
        if formatName:
            out = t.name.ljust(Talent.LONGEST_NAME_LEN, spaceChar) 
            #INFO: ljust() is a build-in funciton for str alignment and padding
        else:
            out = t.name

        if withCat:
            out += f" ({t.category})"
        
        out += f" [{t.getCheckText()}] BE:{t.encumbrance:<4} R:{self.routine:<4} FW:{self.value:<2} \"{self.notes}\""
        return out
    
    def toDict(self) -> dict:
        out = self.talent.toDict()
        out['fw'] = self.value
        out['r'] = self.routine
        out['an'] = self.notes
        return out

    def getCategorySeperator(self, nEOL:int=1) -> str:
        if nEOL < 0:
            nEOL = 0

        cat = self.talent.category
        ID_LEN = len('[00] ') #Default ID Format
        SBS = 1 #SPACES_BETWEEN_SEPERATOR
        strLen = len(self.toStr(False, True).split('\"', 1)[0]) - len(cat) - (SBS*2)

        #Aurichan certified format <3
        return f"{'\n'*nEOL}{'='*(ID_LEN)}{' '*SBS}[{cat}]{' '*SBS}{'='*strLen}{'\n'*(nEOL +1)}"


class TalentCheck():
    def __init__(self, attrVals:list, talentPoints:int, mod:int, rolls:list = None):
        if len(attrVals) != 3:
            raise ValueError(f"Attribute Values List does not contain exactly 3 items!")
        if rolls is None:
            rolls = ROLL_DICE(3, 20)
        elif len(rolls) != 3:
            raise ValueError(f"Roll Values List does not contain exactly 3 items")
        if talentPoints < 0:
            raise ValueError(f"Talent Points ({talentPoints}) are less than 0")

        self.attrVals = attrVals
        self.rolls = rolls
        self.talentPoints = talentPoints
        self.mod = mod                

        self.success = False        
        self.crit = const.CRIT_NONE
        self.dif_sum = 0

        n1 = 0; n20 = 0
        for i in range(3):
            if rolls[i] == 1:
                n1 += 1
            elif rolls[i] == 20:
                n20 += 1
            dif = rolls[i] + mod - attrVals[i]
            if dif > 0:
                self.dif_sum += dif
        
        self.qualityPoints = talentPoints - self.dif_sum
        self.qualityLevel = 0
        
        if self.qualityPoints == 0:
            self.qualityLevel = 1
        elif self.qualityPoints >= 1:
            self.qualityLevel = (self.qualityPoints - 1) // 3 + 1
            if self.qualityLevel > 6:
                self.qualityLevel = 6
        
        if n1 >= 2:
            self.crit = const.CRIT_WIN
            self.success = True
        elif n20 >= 2:
            self.crit = const.CRIT_FAIL
        elif self.qualityLevel > 0:
            self.success = True
    
    def toStr(self) -> str:
        out = f"{self.attrVals[0]}/{self.attrVals[1]}/{self.attrVals[2]} x [{self.rolls[0]}, {self.rolls[1]}, {self.rolls[2]}]{self.mod:+} = FW:{self.talentPoints} - {self.dif_sum} = {self.qualityPoints}\n"
        if self.crit == const.CRIT_WIN:
            out += '(KRITISCHER ERFOLG)'
        elif self.crit == const.CRIT_FAIL:
            out += '(KRITISCHER FEHLSCHLAG)'
        elif self.success:
            out += '(ERFOLG)'
        else:
            out += '(FEHLSCHLAG)'
        out += f" QS: {self.qualityLevel}"
        return out

DATA = []
for t in TALENTS:
    DATA.append(Talent(
        t['name'],
        t['kat'],
        t['probe'][0],
        t['probe'][1],
        t['probe'][2],
        t['be'],
        t['stg'],
    ))