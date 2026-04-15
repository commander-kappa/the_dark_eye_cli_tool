from dice import ROLL_DICE
from data import ATTRIBUTES

#INFO: Unsure whether I should stay with german class Names. I feel like i mix those 2 languages too often here
class Attribut():
    LONGEST_NAME_LEN = 0
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        
        if len(self.name) > Attribut.LONGEST_NAME_LEN:
            Attribut.LONGEST_NAME_LEN = len(self.name)

class AttributWert():
    def __init__(self, attribut: Attribut, wert: int = 8):
        self.attribut = attribut
        self.wert = wert

    def toStr(self) -> str:
        return f"[{self.attribut.id}] {self.attribut.name}{'.'*(Attribut.LONGEST_NAME_LEN - len(self.attribut.name))} {self.wert:>2}\n"
    
    def doProbe(self) -> bool:
        return self.wert >= ROLL_DICE(1, 20)[0]

DATA = []
for key, val in ATTRIBUTES.items():
    DATA.append(Attribut(key, val))