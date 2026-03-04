from dice import ROLL_DICE

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

class Talent():
    LONGEST_NAME_LEN = 0    

    #INFO: not yet in use
    stgDict = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4
    }

    def __init__(self, name, kat, a1, a2, a3, be, stg):
        self.name = name
        self.kategorie = kat
        self.belastung = be
        self.steigung = stg
        self.probe = [
            a1, a2, a3
        ]
        if len(self.name) > Talent.LONGEST_NAME_LEN:
            Talent.LONGEST_NAME_LEN = len(self.name)

    def toStr(self):
        return f"{self.name} ({self.kategorie}) [{self.getProbeText()}] BE:{self.belastung} R:{self.routine} FW:{self.wert} \"{self.anmerkung}\""
    
    def getProbeText(self):
        return f"{self.probe[0]}/{self.probe[1]}/{self.probe[2]}"

class TalentWert():
    def __init__(self, talent, fw=0, r=0, an=''):
        self.talent = talent
        self.wert = int(fw)
        self.routine = r
        self.anmerkung = an
   
    def toStr(self, withCat=True, formatName=True, spaceChar='.'):
        t = self.talent
        '''
        spaces = 0
        if formatName:
            spaces = Talent.LONGEST_NAME_LEN
        else:
            spaces = len(t.name)

        out = f"{t.name:<{spaces}}"
        '''
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

    #INFO: Implementation of a Centered category name. Didn't like how the result looked, but decided to keep it commented in code if I change my mind later
    '''
    def getCategorySeperator(self) -> str:
        cat = self.talent.kategorie
        
        ID_LEN = len('[00] ')
        SBS = 1 #SPACES_BETWEEN_SEPERATOR

        strLen = len(self.toStr(False, True).split('\"', 1)[0]) - len(cat) + ID_LEN - (SBS*2)
        

        return f"{'='*(strLen//2)}{' '*SBS}[{cat}]{' '*SBS}{'='*((strLen//2) + strLen%2)}\n"
    '''
    
    def getCategorySeperator(self, nEOL:int=1) -> str:
        if nEOL < 0:
            nEOL = 0

        cat = self.talent.kategorie
        ID_LEN = len('[00] ') #Default ID Format
        SBS = 1 #SPACES_BETWEEN_SEPERATOR
        strLen = len(self.toStr(False, True).split('\"', 1)[0]) - len(cat) - (SBS*2)

        #Aurichan certified format <3
        return f"{'\n'*nEOL}{'='*(ID_LEN)}{' '*SBS}[{cat}]{' '*SBS}{'='*strLen}{'\n'*(nEOL +1)}"


class TalentProbeErgebnis():
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
        if self.crit == 1:
            return True
        elif self.crit == 2:
            return False
        elif self.qs > 0:
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

def parse_talentWerte(talente):
    out = []
    for t in talente:
        out.append(parse_talentWert(t))
    return out

def parse_talentWert(talent) -> TalentWert:
    t = Talent(
        talent[0],
        talent[-1],
        talent[1][:2],
        talent[1][3:5],
        talent[1][6:],
        talent[2],
        talent[3]
    )
    #INFO: might have to return t later
    tw = TalentWert(t, talent[4], talent[5], talent[6])
    return tw