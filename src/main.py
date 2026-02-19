import pymupdf
import random
from os import path
#INFO: own module
from talents import GET_TALENTS

PDF_NAME = 'herbert.pdf'
DIR_PATH = f"{path.dirname(path.abspath(__file__))}"
PDF_PATH = path.join(DIR_PATH, PDF_NAME)

class Attribut():
    def __init__(self, id, name, wert=8):
        self.id = id
        self.name = name
        self.wert = wert


class Talent():
    stgDict = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4
    }
    def __init__(self, name, kat, a1, a2, a3, be, stg, fw=0, r=0, an=''):
        print(f"{a1} {a2} {a3}")
        self.name = name
        self.kategorie = kat
        self.belastung = be
        self.steigung = stg
        self.probe = [
            getATR(a1),
            getATR(a2),
            getATR(a3)
        ]
        self.wert = fw
        self.routine = r
        self.anmerkung = an
    
    def parseStr(self):
        return f"{self.name} ({self.kategorie}) [{self.probe[0].id}/{self.probe[1].id}/{self.probe[2].id}] BE:{self.belastung} R:{self.routine} FW:{self.wert} \"{self.anmerkung}\""

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
    'IN': Attribut('IN', 'Intuitiom'),
    'CH': Attribut('CH', 'Charisma'),
    'FF': Attribut('FF', 'Fingerfertigkeit'),
    'GE': Attribut('GE', 'Gewandheit'),
    'KO': Attribut('KO', 'Konstitution'),
    'KK': Attribut('KK', 'Körperkraft'),
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

TALENTS = []

for talent in GET_TALENTS(PDF_PATH):
    print(talent)
    TALENTS.append(PARSE_TALENT(talent))

for t in TALENTS:
    print(t.parseStr())

'''
#reader
with pymupdf.open(PDF_NAME) as doc:
    MIN = 2    
    MAX = 2

    for i in range(MIN - 1, MAX):
        page = doc[i]
        
        for widget in page.widgets():
            out = f"Widget: {widget.field_type}, {widget.field_name}, {widget.field_value}\n"
            print(out)
            if widget.field_name in HELD_TAL.keys():
                HELD_TAL[widget.field_name] = widget.field_value
'''

class Char():
    def __init__(
        self,
        name = ''
    ):
        self.name = name
        self.attributes = {
    }
        