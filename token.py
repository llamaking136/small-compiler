class token:
    def __init__(self, name = None, type_ = None, char = None, line = None):
        self.name = name
        self.type_ = type_
        self.char = char
        self.line = line
    
    def __repr__(self):
        return f"`token: '{self.name}', {self.type_}, {self.char}, {self.line}`"

