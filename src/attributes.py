from dice import ROLL_DICE
from data import ATTRIBUTES
import constants as const

class Attribute():
    LONGEST_NAME_LEN = 0
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        
        if len(self.name) > Attribut.LONGEST_NAME_LEN:
            Attribut.LONGEST_NAME_LEN = len(self.name)

class AttributeValue():
    def __init__(self, attribut: Attribut, value: int = 8):
        self.attribut = attribut
        self.value = value

    def toStr(self) -> str:
        return f"[{self.attribut.id}] {self.attribut.name}{'.'*(Attribut.LONGEST_NAME_LEN - len(self.attribut.name))} {self.value:>2}"
    
    def doCheck(self, mod:int = 0) -> AttributeCheck:
        return AttributeCheck(self, mod)

class AttributeCheck():
    def __init__(self, attrVal:AttributeValue, mod:int = 0):
        self.attributeValue = attrVal
        self.mod = mod
        self.roll = ROLL_DICE(1, 20)[0]

        self.critConfirm = None
        self.crit = const.CRIT_NONE
        self.success = False

        if self.roll == 1:
            self.critConfirm = ROLL_DICE(1, 20)[0]
            if self.attributeValue.value <= self.critConfirm + mod:
                self.crit = const.CRIT_WIN
                self.success = True
        elif self.roll == 20:
            self.critConfirm = ROLL_DICE(1, 20)[0]
            if self.attributeValue.value > self.critConfirm + mod:
                self.crit = const.CRIT_FAIL
        elif self.attributeValue <= self.roll + mod:
            self.success = True
    
    def toStr(self) -> str:
        out = '('
        roll2 = ''
        if self.crit != const.CRIT_NONE:
            out += 'KRITISCHER' + ' '
            roll2 = f", {self.critConfirm}"
        if self.success:
            out += 'ERFOLG'
        else:
            out += 'FEHLSCHLAG'
        out += f") [{self.roll}{self.critConfirm}]"

DATA = []
for key, val in ATTRIBUTES.items():
    DATA.append(Attribute(key, val))