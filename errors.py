from sys import stderr

def warning(message):
    print(f"warning: {message}", file = stderr)

def throwerror(message, killProgram = True):
    print(f"error: {message}")
    return killProgram

def throw(message, pos, line, filename, data, isWarning = False):
    if isWarning:
        print(f"{filename}:{line + 1}:{pos}: warning: {message}: '{data}'", file = stderr)
    else:
        print(f"{filename}:{line + 1}:{pos}: error: {message}: '{data}'", file = stderr)
