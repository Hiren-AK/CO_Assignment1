from Registers import *

def converttoBinary(num):   #source: https://www.codegrepper.com/code-examples/python/python+program+to+convert+decimal+to+8+bit+binary
    num = int(num)
    bnr = bin(num).replace('0b','')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

def isBinary(text):
    b = {'0','1'}
    t = set(text)
    
    if (b == t or t == {'0'} or t == {'1'}) and len(text) == 8:
        return True
    return False

def errorVar (comm):
    if len(comm) != 2:
        return (True, "Wrong syntax used for instructions")

    elif not comm[1].replace('_', '').isalnum():
        return (True, "Illegal variable name")         #have to check if this is an error
    
    return (False, None)

def errorA(comm):
    if len(comm) != 4:
        return (True, "Wrong syntax used for instructions")

    elif comm[1] == "FLAGS":
        return (True, "Illegal use of FLAGS register")

    elif comm[1] not in flag_register.keys() or comm[2] not in flag_register.keys() or comm[3] not in flag_register.keys():
        return (True, "Typos in instruction name or register name")
    
    return (False, None)

def errorB(comm):
    if len(comm) != 3:
        return (True, "Wrong syntax used for instructions")

    elif comm[1] == "FLAGS":
        return (True, "Illegal use of FLAGS register")
    
    elif comm[1] not in flag_register.keys():
        return (True, "Typos in instruction name or register name")

    elif not comm[2].startswith("$"):
        return (True, "Wrong syntax used for instructions")

    return (False, None)

def errorC(comm):
    if len(comm) != 3:
        return (True, "Wrong syntax used for instructions")

    elif comm[1] == "FLAGS":
        return (True, "Illegal use of FLAGS register")
    
    elif comm[1] not in flag_register.keys() or comm[2] not in flag_register.keys():
        return (True, "Typos in instruction name or register name")
    
    return (False, None)

def errorD(comm):
    if len(comm) != 3:
        return (True, "Wrong syntax used for instructions")

    #check if second operand is binary or a variable in main
    elif comm[1] == "FLAGS":
        return (True, "Illegal use of FLAGS register")
    
    elif comm[1] not in flag_register.keys():
        return (True, "Typos in instruction name or register name")

    return (False, None)

def errorE(comm):
    if len(comm) != 2:
        return (True, "Wrong syntax used for instructions")

    #check if second operand is binary or a label in main

    return (False, None)

def errorF(comm):
    if len(comm) != 1:
        return (True, "Wrong syntax used for instructions")
    
    return (False, None)

def errorHalt(arr):
    count = 0
    label_halt = 0

    for i in arr:
        if i != [] and i[0] == "hlt":
            count += 1
        
        if i != [] and i[0][-1] == ":" and len(i) > 1 and i[1] == "hlt":
            label_halt += 1
    
    if count == 0 and label_halt == 0:
        return (True, "Missing hlt instruction")
    
    elif count == 0 and label_halt != 0:
        return (False, None)

    elif count == 1:
        for i in range(len(arr)-1, 0, -1):
            if arr[i] != [] and arr[i][0] != "hlt":
                return (True, "hlt not being used as the last instruction")
            elif arr[i] != [] and arr[i][0] == "hlt":
                return (False, None)

    else:
        return(True, "More than one hlt instruction")