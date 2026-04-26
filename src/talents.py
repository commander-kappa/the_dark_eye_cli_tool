from dice import ROLL_DICE
from data import TALENTS

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

class Talent():
    LONGEST_NAME_LEN = 0    

    #INFO: not yet in use
    stgDict = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    
    #Replace aN: str wioth a: Attribute()?
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
        self.kategorie = kat
        self.belastung = be
        self.steigung = stg
        self.probe = [a1, a2, a3]
        
        if len(self.name) > Talent.LONGEST_NAME_LEN:
            Talent.LONGEST_NAME_LEN = len(self.name)

    def toStr(self) -> str:
        return f"{self.name} ({self.kategorie}) [{self.getProbeText()}] BE:{self.belastung} R:{self.routine} FW:{self.wert} \"{self.anmerkung}\""
        
    def toDict(self) -> dict:
        return {
            "name": self.name,
            "kat": self.kategorie,
            "be": self.belastung,
            "stg": self.steigung,
            "probe": self.probe,
        }

    def getProbeText(self):
        return f"{self.probe[0]}/{self.probe[1]}/{self.probe[2]}"

class TalentValue():
    def __init__(self, talent:Talent, fw=0, r=0, an:str=''):
        self.talent = talent
        self.wert = int(fw)
        self.routine = r
        self.anmerkung = an
   
    def toStr(self, withCat=True, formatName=True, spaceChar='.'):
        t = self.talent
        out = ''
        if formatName:
            out = t.name.ljust(Talent.LONGEST_NAME_LEN, spaceChar) 
            #INFO: ljust() is a build-in funciton for str alignment and padding
        else:
            out = t.name

        if withCat:
            out += f" ({t.kategorie})"
        
        out += f" [{t.getProbeText()}] BE:{t.belastung:<4} R:{self.routine:<4} FW:{self.wert:<2} \"{self.anmerkung}\""
        return out
    
    def toDict(self) -> dict:
        out = self.talent.toDict()
        out['fw'] = self.wert
        out['r'] = self.routine
        out['an'] = self.anmerkung
        return out

    def getCategorySeperator(self, nEOL:int=1) -> str:
        if nEOL < 0:
            nEOL = 0

        cat = self.talent.kategorie
        ID_LEN = len('[00] ') #Default ID Format
        SBS = 1 #SPACES_BETWEEN_SEPERATOR
        strLen = len(self.toStr(False, True).split('\"', 1)[0]) - len(cat) - (SBS*2)

        #Aurichan certified format <3
        return f"{'\n'*nEOL}{'='*(ID_LEN)}{' '*SBS}[{cat}]{' '*SBS}{'='*strLen}{'\n'*(nEOL +1)}"


class TalentCheck():
    def __init__(self, fw, crit):
        if fw < 0:
            self.qs = 0
        elif fw == 0:
            self.qs = 1
        else:
            fw = fw - 1
            self.qs = 1 + fw // 3
        
        self.crit = crit

    def isSuccess(self) -> bool:
        if self.crit == const.CRIT_FAIL:
            return False
        elif self.crit == const.CRIT_WIN or self.qs > 0:
            return True
        else:
            return False
    
    def getResultStr(self) -> str:
        if self.isSuccess():
            out = f"(ERFOLG) QS: {self.qs}"
            if self.crit != CRIT_NONE:
                out = f"(KRITISCHER {out[1:]}"
        else:
            out = f"(FEHLSCHLAG) QS: {self.qs}"
            if self.crit != CRIT_NONE:
                out = f"(KRITISCHER {out[1:]}"
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