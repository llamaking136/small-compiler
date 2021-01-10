import re 
from token import token
from errors import *

def lex(characters, token_exprs, filename):
    line = 0
    pos = 0
    char = 0
    tokens = []
    while (pos < len(characters)):
        if (characters[pos] == "\n"):
            char = 0
            line += 1
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if (match):
                text = match.group(0)
                if (tag):
                    current_token = token(text, tag, char, line)# (text, tag)
                    tokens.append(current_token)
                break
        if (not match):
            if (characters[pos] == "”" or characters[pos] == "“"):
                throw(f"detected unicode quotations", char, line, filename, characters[pos])
                return []
            elif (characters[pos] == "'"):
                throw("please use '\"' for quotations marks only", char, line, filename, characters[pos])
                return []
            elif (characters[pos] == "#"):
                throw(f"illegal character, did you mean '//'?", char, line, filename, characters[pos])
                return []
            else:
                throw(f"illegal character", char, line, filename, characters[pos])
                return []
        else:
            pos = match.end(0)
        char += 1
    return tokens

######### DOCS ABOUT DATA TYPES #########

############### DATATYPES ###############

STR = "STR" # string - a string of characters          # eg. '"hello, world"'
INT = "INT" # integer - an array or single numbers     # eg. '42'
FLO = "FLO" # float - integer, but with decimals(WIP)  # eg. '5.2'
NME = "NME" # name - a name to assign something        # eg. 'pewds'
HEX = "HEX" # hexidecimal code - hex (WIP)             # eg. '0xA455'
BOO = "BOO" # boolean - yes/no on/off true/false       # eg. 'true'
NON = "NON" # nonetype - nothing                       # eg. 'null'
FUN = "FUN" # function - type function                 # eg. 'print()'
OBJ = "OBJ" # object - grab a thing off a thing        # eg. 'sys.stdout'
BIN = "BIN" # binary - only on/off                     # eg. '0b11000000111001'

#########################################

RSV = "RSV" # reserved - cannot be overwritten/builtin # eg. 'typeof'
SEP = "SEP" # seperator - comma, used in functions     # eg. ','
SCO = "SCO" # semi-colon - used to seperate lines      # eg. ';'
MAT = "MAT" # math - any math operator                 # eg. '+'
OPR = "OPR" # operator - returns a bool value          # eg. '!='
LOG = "LOG" # logical operator - used to compare       # eg. '||'
CON = "CON" # continue - continues the current line    # eg. '\'
CMD = "CMD" # repl command - command used during repl  # eg. '!!EXIT'
OCB = "OCB" # open curly bracket - opens func, if      # eg. '{'
CCB = "CCB" # close curly bracket - closes func, if    # eg. '}'
LBR = "LBR" # left brace bracket - opens func args     # eg. '('
RBR = "RBR" # right brace bracket - closes func args   # eg. ')'
LAB = "LAB" # left add bracket - for include           # eg. '['
RAB = "RAB" # right add bracket - for include          # eg. ']'
PPR = "PPR" # pre-processing - pre-stuff               # eg. '#define thingy;'
NSP = "NSP" # namespaces - things under a name (WIP)   # eg. 'stdio::printf();'
ARO = "ARO" # arrow - thing?                           # eg. '->'
DTY = "DTY" # data type - declare type of data         # eg. 'var test: STR;'
EAQ = "EAQ" # eaquals sign - read the name             # eg. '='
BIT = "BIT" # bitwise operators - does things in bin   # eg. '3 | 4;'
UND = "UND" # undefined - what did you say?            # eg. 'not_defined; // should not throw error, rather undefined'

class DEC:  # declarations - convert thing to thing   # eg. 'DEC(\'"I AM THE GOD OF DESTRUCTION!!"\')._TO_STR_()'
    def __init__(self, data):
        self.data = data

    def _FR_INT_(self):
        self.INT = self.data
        return int(self.INT)

    def _FR_STR_(self):
        self.STR = list(self.data)
        del self.STR[0], self.STR[-1]
        return str("".join(self.STR))

    def _TO_INT_(self):
        return str(self.data)

    def _TO_STR_(self):
        final = ['"']
        for i in self.data:
            final.append(i)
        final.append('"')
        return "".join(final)

    def __repr__(self):
        return f"{self.data}"

def lexer(characters, filename):
    return lex(characters.read(), token_exprs, filename)

#########################################

token_exprs = (
    (r"[ \n\t]+",             None),
    (r"//[^\n]*",             None),
    (r"/\*.*\*/",             None),
    (r"#[a-zA-Z]+",            PPR), # stuff to pre-process like in c
    # (r"/\*[0-9A-Za-z #*_]*\*/",     None), # attempt to make a new comment system
    (r"\!\![A-Za-z0-9]*",      CMD), # repl command TODO: remove all traces of input system
    (r"\"[^\"]*\"",            STR), # contains stuff
    (r"0x[0-9A-Fa-f]+",        HEX), 
    (r"0b[0-1]+",              BIN),
    (r"0o[0-1]+",              BIN),
    (r"0X[0-9A-Fa-f]+",        HEX),
    (r"0B[0-1]+",              BIN),
    (r"0O[0-1]+",              BIN),
    # (r"[0-9]+.[0-9]+",         FLO), # positive
    (r"[0-9]+",                INT), # positive
    # (r"-[0-9]+.[0-9]+",        FLO), # negative
    (r"-[0-9]+",               INT), # negative
    (r"\&",                    BIT),
    (r"\|",                    BIT),
    (r"\<\<",                  BIT),
    (r"\>\>",                  BIT),
    (r"\^",                    BIT),
    (r"~",                     BIT),
    (r"\-\>",                  ARO), # no idea what arrows do
    (r"\<\-",                  ARO),
    (r"\+=",                   MAT),
    (r"\-=",                   MAT),
    (r"\*=",                   MAT),
    (r"\/=",                   MAT),
    (r"\(",                    LBR),
    (r"\)",                    RBR),
    (r";",                     SCO),
    (r"\+",                    MAT),
    (r"-",                     MAT),
    (r"\*",                    MAT),
    (r"/",                     MAT),
    (r"\÷",                    MAT),
    (r"<=",                    OPR),
    (r"<",                     OPR),
    (r">=",                    OPR),
    (r">",                     OPR),
    (r"==",                    OPR),
    (r"=",                     OPR),
    (r"!=",                    OPR),
    (r"\&\&",                  LOG),
    (r"\|\|",                  LOG),
    (r"\!",                    LOG),
    (r"else if",               RSV),
    (r"if",                    RSV),
    (r"else",                  RSV),
    (r"while",                 RSV),
    (r"for",                   RSV),
    (r"until",                 RSV), # will become while loops in preprocesser
    (r"continue",              RSV),
    (r"break",                 RSV),
    (r"new",                   RSV), # because java
    (r"var",                   RSV), # because swift
    (r"auto",                  RSV), # because c++
    (r"func",                  RSV), # because swift
    (r"struct",                RSV), # because structs don't need an initalizer
    (r"include",               RSV), # because c
    (r"return",                RSV),
    (r"typeof",                RSV), # because *
    (r"true",                  BOO),
    (r"false",                 BOO),
    (r"NULL",                  NON), # because real languages
    (r"undef",                 UND), # undefined
    (r"represent",             RSV), # because python
    (r"try",                   RSV),
    (r"throw",                 RSV), # unlike python
    (r"catch",                 RSV), # unline python
    (r"finally",               RSV),
    (r"{",                     OCB),
    (r"}",                     CCB),
    (r"\[",                    LAB),
    (r"\]",                    RAB),
    (r"[A-Za-z_][A-Za-z0-9_]*",NME),
    (r"\,",                    SEP),
    (r"\\",                    CON),
    (r"\.",                    OBJ),
    (r"$",                     NSP),
    (r":",                     DTY)
)
