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
   
    def toStr(self, withCat=True, formatName=True):
        t = self.talent
        spaces = 0
        if formatName:
            spaces = Talent.LONGEST_NAME_LEN + 1
        else:
            sapces = len(t.name) + 1

        out = f"{t.name:<{spaces}}"
        
        if withCat:
            out += f" ({t.kategorie}) "
        
        out += f"[{t.getProbeText()}] BE:{t.belastung:<4} R:{self.routine:<4} FW:{self.wert:<2} \"{self.anmerkung}\""
        return out

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


class TestTPE():
    TEST_ID = 0
    TEST_YES = 0
    TEST_NO = 0

    def runTest(fw, crit, expected_qs, expected_res):
        TestTPE.TEST_ID += 1
        print(f"SOLL-QS:{expected_qs} SOLL-ERGEBNIS:{expected_res} FW:{fw} crit:{crit} ")
        test = TalentProbeErgebnis(fw, crit)
        print(f"IST-QS: {test.qs} IST-ERGEBNIS: {test.isSuccess()}")
        if test.qs == expected_qs and test.isSuccess() == expected_res:
            print(f"[T{TestTPE.TEST_ID:>3}] UNIT Test Sucess\n")
            TestTPE.TEST_YES += 1
            return True
        else:
            print(f"[T{TestTPE.TEST_ID:>3}] UNIT Test Failure\n")
            TestTPE.TEST_NO += 1
            return False

if __name__ == "__main__":
    #INFO: Unit Tests
    TestTPE.runTest(0, CRIT_NONE, 1, True)
    TestTPE.runTest(0, CRIT_WIN, 1, True)
    TestTPE.runTest(-1, CRIT_NONE, 0, False)
    TestTPE.runTest(-19, CRIT_LOOSE, 0, False)
    TestTPE.runTest(0, CRIT_NONE, 1, True)
    TestTPE.runTest(1, CRIT_NONE, 1, True)
    TestTPE.runTest(2, CRIT_NONE, 1, True)
    TestTPE.runTest(3, CRIT_NONE, 1, True)
    TestTPE.runTest(4, 0, 2, True)
    TestTPE.runTest(5, 0, 2, True)
    TestTPE.runTest(6, 0, 2, True)
    TestTPE.runTest(6, CRIT_WIN, 2, True)
    TestTPE.runTest(6, CRIT_LOOSE, 2, False)
    TestTPE.runTest(7, 0, 3, True)
    TestTPE.runTest(8, 0, 3, True)
    TestTPE.runTest(9, 0, 3, True)
    TestTPE.runTest(10, 0, 4, True)
    TestTPE.runTest(-1, CRIT_WIN, 0, True)

    print(f"SUMMARY: {TestTPE.TEST_YES:>3} out of {TestTPE.TEST_ID:>3} SUCESSFULL")