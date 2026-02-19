import pymupdf
from os import path
#INFO: own module
from talents import GET_TALENTS
from attributes import GET_ATTRIBUTES
from dice import ROLL_DICE


PDF_NAME = 'herbert.pdf'
DIR_PATH = f"{path.dirname(path.abspath(__file__))}"
PDF_PATH = path.join(DIR_PATH, PDF_NAME)

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

class Attribut():
    def __init__(self, id, name, wert=8):
        self.id = id
        self.name = name
        self.wert = wert
    def toStr(self):
        return f"{self.name}: {self.wert}"
    def doProbe(self):
        return self.wert >= ROLL_DICE(1, 20)[0]


class TalentProbeErgebnis():
    def __init__(self, fw, crit):
        if fw < 0:
            self.qs = 0
        elif fw == 0:
            self.qs = 1
        else:
            fw = fw - 1
            self.qs = fw // 3
        
        self.crit = crit

    def isSuccess(self):
        if self.crit == 1:
            return True
        elif self.crit == 2:
            return False
        elif self.qs > 0:
            return True
        else:
            return False
    
    def getResultStr(self):
        print(f"{self.qs}")
        if self.isSuccess():
            out = f"(ERFOLG) QS: {self.qs}"
            if self.crit != CRIT_NONE:
                out = f"(KRITISCHER {out[1:]}"
            return out
        else:
            out = f"(FEHLSCHLAG) QS: {self.qs}"
            if self.crit != CRIT_NONE:
                out = f"(KRITISCHER {out[1:]}"


class Talent():
    stgDict = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4
    }
    def __init__(self, name, kat, a1, a2, a3, be, stg, fw=0, r=0, an=''):
        self.name = name
        self.kategorie = kat
        self.belastung = be
        self.steigung = stg
        self.probe = [
            ATTRIBUTES[a1], 
            ATTRIBUTES[a2], 
            ATTRIBUTES[a3]
        ] 
        self.wert = int(fw)
        self.routine = r
        self.anmerkung = an
    
    def toStr(self):
        return f"{self.name} ({self.kategorie}) [{self.getProbeText()}] BE:{self.belastung} R:{self.routine} FW:{self.wert} \"{self.anmerkung}\""
    def getAtrWerte(self):
        return [
            self.probe[0].wert,
            self.probe[1].wert,
            self.probe[2].wert
        ]
    def getProbeText(self):
        return f"{self.probe[0].id}/{self.probe[1].id}/{self.probe[2].id}"
    def doProbe(self, mod=0):
        rolls = ROLL_DICE(3, 20)
        print(f"{self.getProbeText()} => {self.getAtrWerte()} x {rolls}")
        over = 0

        crit = CRIT_NONE
        n1 = 0; n20 = 0; p = 0
        for i in range(3):
            if rolls[i] == 1:
                n1 = n1 + 1
                p = i
            elif rolls[i] == 20:
                n20 = n20 + 1
                p = i

            dif = rolls[i] + mod - self.probe[i].wert
            if dif > 0:
                over = over + dif
            
        if n1 == 1 and n20 == 1:
            crit = CRIT_NONE
        elif n1 == 1:
            if self.probe[p].doProbe():
                crit = CRIT_WIN
        elif n20 == 1:
            if self.probe[p].doProbe():
                crit = CRIT_LOOSE
        elif n1 >= 2:
            crit = CRIT_WIN
        elif n20 >= 2:
            crit = CRIT_LOOSE
        
        print(f"FW:{self.wert} - {over} = {self.wert - over}")
        return TalentProbeErgebnis(self.wert - over, crit)
 

HELD_NAME = 'Held_Name'
HELD_MU = 'MU_1'
HELD_KL = 'KL_1'
HELD_IN = 'IN_1'
HELD_CH = 'CH_1'
HELD_FF = 'FF_1'
HELD_GE = 'GE_1'
HELD_KO = 'KO_1'
HELD_KK = 'KK_1'

HELD_TAL = {
    HELD_NAME: '',
    HELD_MU: '',
    HELD_KL: '',
    HELD_IN: '',
    HELD_CH: '',
    HELD_FF: '',
    HELD_GE: '',
    HELD_KO: '',
    HELD_KK: '',
}

ATTRIBUTES = {
    'MU': Attribut('MU', 'Mut'),
    'KL': Attribut('KL', 'Klugheit'),
    'IN': Attribut('IN', 'Intuition'),
    'CH': Attribut('CH', 'Charisma'),
    'FF': Attribut('FF', 'Fingerfertigkeit'),
    'GE': Attribut('GE','Gewandheit'),
    'KO': Attribut('KO','Konstitution'),
    'KK': Attribut('KK','Körperkraft'),
}

def getATR(key):
    if key in ATTRIBUTES.keys():
        return ATTRIBUTES[key]
    else:
        raise Exception

def PARSE_TALENT(talent):
    return Talent(
        talent[0],
        talent[-1],
        talent[1][:2],
        talent[1][3:5],
        talent[1][6:],
        talent[2],
        talent[3],
        talent[4],
        talent[5],
        talent[6]
    )

for key, value in GET_ATTRIBUTES(PDF_PATH).items():
    ATTRIBUTES[key[:2]].wert = value

for k in ATTRIBUTES.keys():
    print(ATTRIBUTES[k].toStr())

TALENTS = {}
for talent in GET_TALENTS(PDF_PATH):
    #print(talent)
    x = PARSE_TALENT(talent)
    TALENTS[x.name] = x

for t in TALENTS.values():
    #print(t.toStr())
    print('\n')
    print(t.doProbe().getResultStr())


print(f"{3 // 3}")