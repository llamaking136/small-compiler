#!/usr/bin/python3

def deletearray(base, finders):
    total = 0
    for i in range(len(base)):
        if base[i - total] in finders: base.pop(i - total)
    return base

import lexer, parser, converter, filewriter, errors
from sys import argv, stderr

def usage():
    print("usage: small_compiler <filename>", file = stderr)
    exit(1)

lexer  = lexer.lexer
parser = parser.parser
conv   = converter.conv 
filew  = filewriter.filew
throwerror = errors.throwerror

try:
    if len(argv) <= 1: usage()
    filename = open(argv[-1])
except IndexError:
    usage()
except (FileNotFoundError, PermissionError, IOError) as e:
    if throwerror(str(e)): exit(2)

internal_functions = {}
internal_variables = {}

def main():
    tokens = lexer(filename, filename.name)
    for i in tokens: print(i)
    parsed = parser(tokens)
    functions, variables = conv(parsed)
    for i in functions:
        internal_functions[i.name] = i.value
    for i in variables:
        internal_variables[i.name] = i.value

    filew(internal_functions, internal_variables)

if __name__ == "__main__":
    main()
