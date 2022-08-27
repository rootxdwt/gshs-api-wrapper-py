import re

class Finder:
    def __init__(self) ->None:
        self.midbracket = re.compile('(?<=\().+?(?=\))')
        self.largebracket = re.compile('(?<=\[).+?(?=\])')
        self.namebracket = re.compile('(?<=\]).+?(?=\()')

    def MatchMidBracket(self, prop:str)->str:
        return re.findall(self.midbracket, prop)
    
    def MatchLargeBracket(self,prop:str)->str:
        return re.findall(self.largebracket, prop)
    
    def MatchName(self,prop:str)->str:
        return re.findall(self.namebracket, prop)