import talents, attributes
from dice import ROLL_DICE

CRIT_NONE = 0
CRIT_WIN = 1
CRIT_LOOSE = 2

class Abenteurer():
    def __init__(self, name, attributWerte, talentWerte):
        self.name = name
        self.attribute = attributes.parse_attributWerte(attributWerte)
        self.talente = talents.parse_talentWerte(talentWerte)

    def showAttributes(self):
        for key, val in self.attribute.items():
            print(f"[{key}] {val.attribut.name}: {val.wert}")

    def showTalente(self):
        k = ''
        for i in range(len(self.talente)):
            if self.talente[i].talent.kategorie != k:
                k = self.talente[i].talent.kategorie
                print(f"======= [{k}] =======")
            print(f"[{i:02}] {self.talente[i].toStr(withCat=False)}")

    def doProbeAttribut(self, id, mod=0):
        r = ROLL_DICE(1, 20)
        print(self.attribute[id].toStr())
        if r[0] > self.attribute[id].wert + mod:
            print(f"(FEHLSCHLAG) {r[0]}")
        else:
            print(f"(ERFOLG) {r[0]}")
    
    def getProbeWerte(self, probe):
        return f"{self.attribute[probe[0]].wert}/{self.attribute[probe[1]].wert}/{self.attribute[probe[2]].wert}"
    
    def doProbeTalent(self, id, mod=0):
        rolls = ROLL_DICE(3, 20)
        tw = self.talente[id]
        print(f"{tw.talent.getProbeText()} => {self.getProbeWerte(tw.talent.probe)} x {rolls}")
        
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

            dif = rolls[i] - mod - self.attribute[tw.talent.probe[i]].wert
            if dif > 0:
                over = over + dif
            
        if n1 == 1 and n20 == 1:
            crit = CRIT_NONE
        elif n1 == 1:
            if self.attribute[tw.talent.probe[i]].doProbe():
                crit = CRIT_WIN
        elif n20 == 1:
            if self.attribute[tw.talent.probe[i]].doProbe():
                crit = CRIT_LOOSE
        elif n1 >= 2:
            crit = CRIT_WIN
        elif n20 >= 2:
            crit = CRIT_LOOSE
        
        print(f"FW:{tw.wert} - {over} = {tw.wert - over}")
        return talents.TalentProbeErgebnis(tw.wert - over, crit)
