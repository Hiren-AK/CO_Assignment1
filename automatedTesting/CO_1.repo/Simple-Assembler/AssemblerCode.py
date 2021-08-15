from sys import stdin
from Errorchecker import *
from OpcodeTable import *
from Registers import *

output = []     #the array that will keep storing the outputs generated

variables = {}  #dictionary that will store address of variables as values
num_vars = 0    #number of variables

labels = {}     #dictionary that will store adrress of labels ad values

errors = []     #list that will store a tuple (error, line number)

inp = []        #the inputs are stored as sub_lists in this list

var_end = False #boolean that shows when variable definition is over

for line in stdin:
    if line == '':
        break
    else:
      inp.append(line.split())

n = 0  #the number of commands (non-empty inputs)
last_comm = 0 #the line at which the last command was entered

for line in range(len(inp)):
  if inp[line] != []:
    last_comm = line
    n += 1

halt_error = errorHalt(inp)

tot_var = 0 #total number of variables #######
for i in range(len(inp)):
    if inp[i] != []:
        if inp[i][0] == "var":
            tot_var += 1

for i in range(len(inp)):
    if inp[i][0][-1] == ':':
        labels[inp[i][0][:-1]] = i - tot_var

    labels[inp[i][0][:-1]] = i - tot_var

for i in range(len(inp)):
  if halt_error[0]:
    errors.append((halt_error[1], last_comm + 1))
    break

  if inp[i] == []:
    continue
  
  elif inp[i][0] == "var":
    if var_end:
      errors.append(("Variables not declared at the beginning,", i+1))
      break

    error = errorVar(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    else:
      addr = n - tot_var + num_vars #######
      num_vars += 1
      variables[inp[i][1]] = addr

  elif inp[i][0][-1] == ':':
    var_end = True
    if not len(inp[i]) > 1:
      errors.append(("General Syntax Error,", i+1))
      break

    #labels[inp[i][0][:-1]] = i - tot_var #########
    ############### FLAGS REGISTERS CAN BE USED IN AFTER CHECKING ERRORS S CORRECT THE CODE ACCORDINGLY.
    if inp[i][1] == "add":
      error = errorA(inp[i][1:])
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["add"][0]
      unused = "00"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]] + flag_register[inp[i][4]]
      output.append(out)

  #sub_____________________________
    elif inp[i][1] == "sub":
      error = errorA(inp[i][1:]) ####
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["sub"][0]
      unused = "00"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]] + flag_register[inp[i][4]]
      output.append(out)

    #mov_____________________________
    elif inp[i][1] == "mov":
      if inp[i][3].startswith("$") and inp[i][3][1:].isdigit():
        error = errorB(inp[i][1:])
        if error[0]:
          errors.append((error[1], i+1))
          break
      
        opcode = opcodet["mov"][0][0]
        binary = converttoBinary(inp[i][3][1:])
        out = opcode + flag_register[inp[i][2]] + binary
        output.append(out)
      
      else:
        error = errorC(inp[i][1:])
        if error[0]:
          errors.append((error[1], i+1))
          break
        
        opcode = opcodet["mov"][0][1]
        unused = "00000"
        out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]]
        output.append(out)

    #ld_____________________________
    elif inp[i][1] == "ld":
      error = errorD(inp[i][1:])
      if error[0]:
          errors.append((error[1], i+1))
          break

      if not isBinary(inp[i][3]) or inp[i][3] not in variables.keys():
        if inp[i][3] in labels.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
          break

        elif inp[i][3] not in variables.keys() and not isBinary(inp[i][3]):
          errors.append(("Use of undefined variables", i+1))
          break

        if not isBinary(inp[i][3]):
          errors.append(("General Syntax Error", i+1))
          break
      
      opcode = opcodet["ld"][0]
      if isBinary(inp[i][3]):
        addr = inp[i][3]
      else:
        addr = converttoBinary(variables[inp[i][3]])
      
      out = opcode + flag_register[inp[i][2]] + addr
      output.append(out)

    #st_____________________________
    elif inp[i][1] == "st":
      error = errorD(inp[i][1:]) #check error
      if error[0]: #if error, print error statement
          errors.append((error[1], i+1))
          break
      
      #checking for more errors
      if not isBinary(inp[i][3]) or inp[i][3] not in variables.keys():
        if inp[i][3] in labels.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
          break

        elif inp[i][3] not in variables.keys() and not isBinary(inp[i][3]):
          errors.append(("Use of undefined variables", i+1))
          break

        if not isBinary(inp[i][3]):
          errors.append(("General Syntax Error", i+1))
          break
      
      opcode = opcodet["st"][0] #opcode
      if isBinary(inp[i][3]): #if its already binary
        addr = inp[i][3]
      else:
        addr = converttoBinary(variables[inp[i][3]]) #convert to binary
      
      out = opcode + flag_register[inp[i][2]] + addr #output in format
      output.append(out)
      
    #mul_____________________________
    elif inp[i][1] == "mul":        
      error = errorA(inp[i][1:])
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["mul"][0]
      unused = "00"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]] + flag_register[inp[i][4]]
      output.append(out)

    #div_____________________________
    elif inp[i][1] == "div":
      error = errorC(inp[i][1:]) #check error
      if error[0]: #if error, print error statement
          errors.append((error[1], i+1))
          break

      opcode = opcodet["div"][0]
      unused = "00000"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]]
      output.append(out)

      

    #rs_____________________________
    elif inp[i][1] == "rs":
      error = errorC(inp[i][1:]) #check error
      if error[0]: #if error, print error statement
          errors.append((error[1], i+1))
          break

      opcode = opcodet["rs"][0]
      unused = "00000"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]]
      output.append(out)
    
    #ls_____________________________
    elif inp[i][1] == "ls":
      error = errorC(inp[i][1:]) #check error
      if error[0]: #if error, print error statement
          errors.append((error[1], i+1))
          break

      opcode = opcodet["ls"][0]
      unused = "00000"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]]
      output.append(out)  

    #xor_____________________________
    elif inp[i][1] == "xor":          
      error = errorA(inp[i][1:])
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["xor"][0]
      unused = "00"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]] + flag_register[inp[i][4]]
      output.append(out)

    #or_____________________________
    elif inp[i][1] == "or":
      error = errorA(inp[i][1:])
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["or"][0]
      unused = "00"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]] + flag_register[inp[i][4]]
      output.append(out)

    #and_____________________________
    elif inp[i][1] == "and":
      error = errorA(inp[i][1])
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["and"][0]
      unused = "00"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]] + flag_register[inp[i][4]]
      output.append(out)

    #not_____________________________
    elif inp[i][1] == "not":
      error = errorC(inp[i][1]) #check error
      if error[0]: #if error, print error statement
          errors.append((error[1], i+1))
          break

      opcode = opcodet["not"][0]
      unused = "00000"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]]
      output.append(out)  

    #cmp_____________________________
    elif inp[i][1] == "cmp":
      error = errorC(inp[i][1:]) #check error
      if error[0]: #if error, print error statement
          errors.append((error[1], i+1))
          break

      opcode = opcodet["cmp"][0]
      unused = "00000"
      out = opcode + unused + flag_register[inp[i][2]] + flag_register[inp[i][3]]
      output.append(out)


    #jmp_____________________________(CHECK)
    elif inp[i][1] == "jmp":
      error = errorE(inp[i][1:])
      if error[0]:
          errors.append((error[1], i+1))
          break

      if not isBinary(inp[i][3]) or inp[i][3] not in labels.keys():
        if not isBinary(inp[i][3]):
          errors.append(("General Syntax Error", i+1))
        elif inp[i][3] in variables.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
        else:
          errors.append(("Use of undefined labels", i+1))

      opcode = opcodet["jmp"][0]
      unused = "000"

      if isBinary(inp[i][3]):
        addr = inp[i][3]
      else:
        addr = converttoBinary(labels[inp[i][3]])
      
      out = opcode + unused + addr
      output.append(out)

    #jlt_____________________________(CHECK)
    elif inp[i][1] == "jlt":
      error = errorE(inp[i][1:])
      if error[0]:
          errors.append((error[1], i+1))
          break

      if not isBinary(inp[i][3]) or inp[i][3] not in labels.keys():
        if not isBinary(inp[i][3]):
          errors.append(("General Syntax Error", i+1))
        elif inp[i][3] in variables.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
        else:
          errors.append(("Use of undefined labels", i+1))

      opcode = opcodet["jlt"][0]
      unused = "000"

      if isBinary(inp[i][3]):
        addr = inp[i][3]
      else:
        addr = converttoBinary(labels[inp[i][3]]) 
      
      out = opcode + unused + addr
      output.append(out)

    #jgt_____________________________(CHECK)
    elif inp[i][1] == "jgt":
      error = errorE(inp[i][1:])
      if error[0]:
          errors.append((error[1], i+1))
          break

      if not isBinary(inp[i][3]) or inp[i][3] not in labels.keys():
        if not isBinary(inp[i][3]):
          errors.append(("General Syntax Error", i+1))
        elif inp[i][3] in variables.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
        else:
          errors.append(("Use of undefined labels", i+1))

      opcode = opcodet["jgt"][0]
      unused = "000"

      if isBinary(inp[i][3]):
        addr = inp[i][3]
      else:
        addr = converttoBinary(labels[inp[i][3]]) 
      
      out = opcode + unused + addr
      output.append(out)

    #je_____________________________(CHECK)
    elif inp[i][1] == "je":
      error = errorE(inp[i][1:])
      if error[0]:
          errors.append((error[1], i+1))
          break

      if not isBinary(inp[i][3]) or inp[i][3] not in labels.keys():
        if not isBinary(inp[i][3]):
          errors.append(("General Syntax Error", i+1))
        elif inp[i][3] in variables.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
        else:
          errors.append(("Use of undefined labels", i+1))

      opcode = opcodet["je"][0]
      unused = "000"

      if isBinary(inp[i][3]):
        addr = inp[i][3]
      else:
        addr = converttoBinary(labels[inp[i][3]]) 
      
      out = opcode + unused + addr
      output.append(out)


    #hlt_____________________________(CHECK)
    elif inp[i][1] == "hlt":
      error = errorF(inp[i])
      if error[0]:
          errors.append((error[1], i+1))
          break
      
      output.append("1001100000000000")
    ###############

  #add_____________________________
  elif inp[i][0] == "add":
    var_end = True          #
    error = errorA(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    opcode = opcodet["add"][0]
    unused = "00"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]] + flag_register[inp[i][3]]
    output.append(out)

  #sub_____________________________
  elif inp[i][0] == "sub":
    var_end = True
    error = errorA(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    opcode = opcodet["sub"][0]
    unused = "00"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]] + flag_register[inp[i][3]]
    output.append(out)

  #mov_____________________________
  elif inp[i][0] == "mov":
    var_end = True
    if inp[i][2].startswith("$") and inp[i][2][1:].isdigit():
      error = errorB(inp[i])
      if error[0]:
        errors.append((error[1], i+1))
        break
    
      opcode = opcodet["mov"][0][0]
      binary = converttoBinary(inp[i][2][1:])
      out = opcode + flag_register[inp[i][1]] + binary
      output.append(out)
    
    else:
      error = errorC(inp[i])
      if error[0]:
        errors.append((error[1], i+1))
        break
      
      opcode = opcodet["mov"][0][1]
      unused = "00000"
      out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]]
      output.append(out)

  #ld_____________________________
  elif inp[i][0] == "ld":
    var_end = True
    error = errorD(inp[i])
    if error[0]:
        errors.append((error[1], i+1))
        break

    if not isBinary(inp[i][2]) or inp[i][2] not in variables.keys():
        if inp[i][2] in labels.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
          break

        elif inp[i][2] not in variables.keys() and not isBinary(inp[i][2]):
            errors.append(("Use of undefined variables", i+1))
            break

        if not isBinary(inp[i][2]):
            errors.append(("General Syntax Error", i+1))
            break
    
    opcode = opcodet["ld"][0]
    if isBinary(inp[i][2]):
      addr = inp[i][2]
    else:
      addr = converttoBinary(variables[inp[i][2]]) #variables have to be looked up
    
    out = opcode + flag_register[inp[i][1]] + addr
    output.append(out)

  #st_____________________________
  elif inp[i][0] == "st":
    var_end = True #check if end
    error = errorD(inp[i]) #check error
    if error[0]: #if error, print error statement
        errors.append((error[1], i+1))
        break
    
    #checking for more errors
    if not isBinary(inp[i][2]) or inp[i][2] not in variables.keys():
        if inp[i][2] in labels.keys():
          errors.append(("Misuse of labels as variables or vice-versa", i+1))
          break

        elif inp[i][2] not in variables.keys() and not isBinary(inp[i][2]):
          errors.append(("Use of undefined variables", i+1))
          break

        if not isBinary(inp[i][2]):
          errors.append(("General Syntax Error", i+1))
          break
    
    opcode = opcodet["st"][0] #opcode
    if isBinary(inp[i][2]): #if its already binary
      addr = inp[i][2]
    else:
      addr = converttoBinary(variables[inp[i][2]]) #convert to binary
    
    out = opcode + flag_register[inp[i][1]] + addr #output in format
    output.append(out)
    
  #mul_____________________________
  elif inp[i][0] == "mul":
    var_end = True          #
    error = errorA(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    opcode = opcodet["mul"][0]
    unused = "00"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]] + flag_register[inp[i][3]]
    output.append(out)

  #div_____________________________
  elif inp[i][0] == "div":
    var_end = True #check if end
    error = errorC(inp[i]) #check error
    if error[0]: #if error, print error statement
        errors.append((error[1], i+1))
        break

    opcode = opcodet["div"][0]
    unused = "00000"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]]
    output.append(out)

    

  #rs_____________________________
  elif inp[i][0] == "rs":
    var_end = True #check if end
    error = errorC(inp[i]) #check error
    if error[0]: #if error, print error statement
        errors.append((error[1], i+1))
        break

    opcode = opcodet["rs"][0]
    unused = "00000"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]]
    output.append(out)
  
  #ls_____________________________
  elif inp[i][0] == "ls":
    var_end = True #check if end
    error = errorC(inp[i]) #check error
    if error[0]: #if error, print error statement
        errors.append((error[1], i+1))
        break

    opcode = opcodet["ls"][0]
    unused = "00000"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]]
    output.append(out)  

  #xor_____________________________
  elif inp[i][0] == "xor":
    var_end = True          #
    error = errorA(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    opcode = opcodet["xor"][0]
    unused = "00"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]] + flag_register[inp[i][3]]
    output.append(out)

  #or_____________________________
  elif inp[i][0] == "or":
    var_end = True          #
    error = errorA(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    opcode = opcodet["or"][0]
    unused = "00"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]] + flag_register[inp[i][3]]
    output.append(out)

  #and_____________________________
  elif inp[i][0] == "and":
    var_end = True          #
    error = errorA(inp[i])
    if error[0]:
      errors.append((error[1], i+1))
      break
    
    opcode = opcodet["and"][0]
    unused = "00"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]] + flag_register[inp[i][3]]
    output.append(out)

  #not_____________________________
  elif inp[i][0] == "not":
    var_end = True #check if end
    error = errorC(inp[i]) #check error
    if error[0]: #if error, print error statement
        errors.append((error[1], i+1))
        break

    opcode = opcodet["not"][0]
    unused = "00000"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]]
    output.append(out)  

  #cmp_____________________________
  elif inp[i][0] == "cmp":
    var_end = True #check if end
    error = errorC(inp[i]) #check error
    if error[0]: #if error, print error statement
        errors.append((error[1], i+1))
        break

    opcode = opcodet["cmp"][0]
    unused = "00000"
    out = opcode + unused + flag_register[inp[i][1]] + flag_register[inp[i][2]]
    output.append(out)


  #jmp_____________________________(CHECK)
  elif inp[i][0] == "jmp":
    var_end = True
    error = errorE(inp[i])
    if error[0]:
        errors.append((error[1], i+1))
        break

    if not isBinary(inp[i][1]) or inp[i][1] not in labels.keys():
      if not isBinary(inp[i][1]):
        errors.append(("General Syntax Error", i+1))
      elif inp[i][1] in variables.keys():
        errors.append(("Misuse of labels as variables or vice-versa", i+1))
      else:
        errors.append(("Use of undefined labels", i+1))

    opcode = opcodet["jmp"][0]
    unused = "000"

    if isBinary(inp[i][1]):
      addr = inp[i][1]
    else:
      addr = converttoBinary(labels[inp[i][2]]) #variables have to be looked up
    
    out = opcode + unused + addr
    output.append(out)

  #jlt_____________________________(CHECK)
  elif inp[i][0] == "jlt":
    var_end = True
    error = errorE(inp[i])
    if error[0]:
        errors.append((error[1], i+1))
        break

    if not isBinary(inp[i][1]) or inp[i][1] not in labels.keys():
      if not isBinary(inp[i][1]):
        errors.append(("General Syntax Error", i+1))
      elif inp[i][1] in variables.keys():
        errors.append(("Misuse of labels as variables or vice-versa", i+1))
      else:
        errors.append(("Use of undefined labels", i+1))

    opcode = opcodet["jlt"][0]
    unused = "000"

    if isBinary(inp[i][1]):
      addr = inp[i][1]
    else:
      addr = converttoBinary(labels[inp[i][1]]) #variables have to be looked up
    
    out = opcode + unused + addr
    output.append(out)

  #jgt_____________________________(CHECK)
  elif inp[i][0] == "jgt":
    var_end = True
    error = errorE(inp[i])
    if error[0]:
        errors.append((error[1], i+1))
        break

    if not isBinary(inp[i][1]) or inp[i][1] not in labels.keys():
      if not isBinary(inp[i][1]):
        errors.append(("General Syntax Error", i+1))
      elif inp[i][1] in variables.keys():
        errors.append(("Misuse of labels as variables or vice-versa", i+1))
      else:
        errors.append(("Use of undefined labels", i+1))

    opcode = opcodet["jgt"][0]
    unused = "000"

    if isBinary(inp[i][1]):
      addr = inp[i][1]
    else:
      addr = converttoBinary(labels[inp[i][1]])
    
    out = opcode + unused + addr
    output.append(out)

  #je_____________________________(CHECK)
  elif inp[i][0] == "je":
    var_end = True
    error = errorE(inp[i])
    if error[0]:
        errors.append((error[1], i+1))
        break

    if not isBinary(inp[i][1]) or inp[i][1] not in labels.keys():
      if not isBinary(inp[i][1]):
        errors.append(("General Syntax Error", i+1))
      elif inp[i][1] in variables.keys():
        errors.append(("Misuse of labels as variables or vice-versa", i+1))
      else:
        errors.append(("Use of undefined labels", i+1))

    opcode = opcodet["je"][0]
    unused = "000"

    if isBinary(inp[i][1]):
      addr = inp[i][1]
    else:
      addr = converttoBinary(labels[inp[i][1]]) #variables have to be looked up
    
    out = opcode + unused + addr
    output.append(out)


  #hlt_____________________________(CHECK)
  elif inp[i][0] == "hlt":
    var_end = True
    error = errorF(inp[i])
    if error[0]:
        errors.append((error[1], i+1))
        break
    
    output.append("1001100000000000")

if len(errors) != 0:
  print(errors[0][0] + ",", "line:", errors[0][1])

else:
  for o in output:
    print(o)
