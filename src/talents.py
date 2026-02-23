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
   
    def toStr(self, withCat=True):
        t = self.talent
        
        out = f"{t.name:<{Talent.LONGEST_NAME_LEN + 1}}"
        
        if withCat:
            out += f" ({t.kategorie}) "
        
        out += f"[{t.getProbeText()}] BE:{t.belastung:<4} R:{self.routine:<4} FW:{self.wert:<2} \"{self.anmerkung}\""
        return out

'''
    def doProbe(self, attributes, mod=0):
        rolls = ROLL_DICE(3, 20)
        print(f"{self.talent.getProbeText()} => {self.getAtrWerte()} x {rolls}")
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
    '''
    

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
def parse_talentWert(talent):
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


#if __name__ == "__main__":
#    TALENTS = GET_TALENTS('herbert.pdf') 
#    for e in TALENTS:
#        print(e)