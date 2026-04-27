from dice import ROLL_DICE
from data import ATTRIBUTES
import constants as const

class Attribute():
    LONGEST_NAME_LEN = 0
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        
        if len(self.name) > Attribute.LONGEST_NAME_LEN:
            Attribute.LONGEST_NAME_LEN = len(self.name)

class AttributeValue():
    def __init__(self, attribut: Attribute, value: int = 8):
        self.attribut = attribut
        self.value = value

    def toStr(self, formatName:bool = True, spaceChar:str = '.') -> str:
        n = Attribute.LONGEST_NAME_LEN - len(self.attribut.name) if formatName else 0
        return f"[{self.attribut.id}] {self.attribut.name}{spaceChar*n} {self.value:>2}\n"
    
    #def doCheck(self, mod:int = 0) -> AttributeCheck:
    #    return AttributeCheck(self, mod)

class AttributeCheck():
    def __init__(self, attrVal:AttributeValue, mod:int = 0, roll:int = None):
        self.attributeValue = attrVal
        self.mod = mod
        if roll is None:
            roll = ROLL_DICE(1, 20)[0]
        self.roll = roll

        self.critConfirm = None
        self.crit = const.CRIT_NONE
        self.success = False
        
        if self.roll + mod <= self.attributeValue.value:
            self.success = True
        
        if self.roll == 1:
            self.critConfirm = ROLL_DICE(1, 20)[0]
            if self.attributeValue.value >= self.critConfirm + mod:
                self.crit = const.CRIT_WIN
                self.success = True
        elif self.roll == 20:
            self.critConfirm = ROLL_DICE(1, 20)[0]
            if self.attributeValue.value < self.critConfirm + mod:
                self.crit = const.CRIT_FAIL
                self.success = False
                
    def toStr(self) -> str:
        out = '('
        roll2 = f", {self.critConfirm}" if self.critConfirm is not None else ''
        if self.crit != const.CRIT_NONE:
            out += 'KRITISCHER' + ' '
        if self.success:
            out += 'ERFOLG'
        else:
            out += 'FEHLSCHLAG'
        out += f") [{self.roll}{roll2}]{self.mod:+}"
        return out

DATA = []
for key, val in ATTRIBUTES.items():
    DATA.append(Attribute(key, val))