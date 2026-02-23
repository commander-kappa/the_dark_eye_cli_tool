from dice import ROLL_DICE

class Attribut():
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class AttributWert():
    def __init__(self, attribut: Attribut, wert: int = 8):
        self.attribut = attribut
        self.wert = wert

    def toStr(self) -> str:
        return f"[{self.attribut.id}] {self.attribut.name}: {self.wert}"
    
    def doProbe(self) -> bool:
        return self.wert >= ROLL_DICE(1, 20)[0]

class AttributCollection():
    def __init__(self, atrWerte):
        self.collection = {}
        for atrWert in atrWerte:
            self.collection[atrWert.attribut.id] = atrWert        


IDS = ['MU','KL','IN','CH','FF','GE','KO','KK']
ATTRIBUTES = {
    'MU': Attribut('MU', 'Mut'),
    'KL': Attribut('KL', 'Klugheit'),
    'IN': Attribut('IN', 'Intuition'),
    'CH': Attribut('CH', 'Charisma'),
    'FF': Attribut('FF', 'Fingerfertigkeit'),
    'GE': Attribut('GE', 'Gewandheit'),
    'KO': Attribut('KO', 'Konstitution'),
    'KK': Attribut('KK', 'Körperkraft'),
}

def parse_attributWerte(werte):
    out = {} 
    for i in range(len(werte)):
        out[IDS[i]] = AttributWert(ATTRIBUTES[IDS[i]], werte[i])
    return out
