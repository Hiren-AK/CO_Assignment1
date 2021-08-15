#opcode table containing tuples as values for the instructions: (opcode, type, number of operands, uses variable, uses label)

opcodet = {"add":("00000", "A", 3, False, False), 
"sub":("00001", "A", 3, False, False),
"mov":(("00010", "00011"), "B", 2, False, False),
"ld":("00100", "D", 2, True, False),
"st":("00101", "D", 2, True, False),
"mul":("00110", "A", 3, False, False),
"div":("00111", "C", 2, False, False), 
"rs":("01000", "B", 2, False, False),
"ls":("01001", "B", 2, False, False),
"xor":("01010", "A", 3, False, False),
"or":("01011", "A", 3, False, False),
"and":("01100", "A", 3, False, False),
"not":("01101", "C", 2, False, False),
"cmp":("01110", "C", 2, False, False), 
"jmp":("01111", "E", 1, False, True),
"jlt":("10000", "E", 1, False, True),
"jgt":("10001", "E", 1, False, True),
"je":("10010", "E", 1, False, True),
"hlt":("10011", "F", 3, False, False),
}