from __future__ import print_function

# Remember where each of the jump label is, and the target location 
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')


def machineTranslation(program): # Translates the assembly to machine code and stores it back in program []
    PC = 0
    instructionList = {'addi': 1000} # Stores the opcodes of all our assembly instructions
    machineCode = []

    while(PC < len(program)):
        instruction = program[PC]
        print(instruction)

        spaceLocation = 0
        for char in instruction:
            if char == ' ':
                #print("Space location at " + str(spaceLocation))
                break
            else:
                spaceLocation += 1

        opcode = instruction[0:spaceLocation] # Grabs the english string of the opcode
        print(opcode)
        binaryOpcode = instructionList.get(opcode) # Replaces the english text opcode with the binary one
        if binaryOpcode == None: # Gives error if the opcode is not supported by instructionList (for debuging purposes)
            print("Instruction not implemented, please check!")
            print("Error instruction '" + opcode + "' not supported.")
            quit()
        print(binaryOpcode)

        rx = instruction[spaceLocation + 2:spaceLocation + 3] # Grabs the next two bits as an english string
        binaryRx = "{0:2b}".format(int(rx)) # Converts to binary
        print(binaryRx)
        print(rx)

        ry = instruction[spaceLocation + 5:] # Grabs the rest of the data as a english string NOTE: ry can also be imm
        binaryRy = "{0:2b}".format(int(ry))
        for blank in binaryRy:
            blank.replace('', '0')
        print(ry)
        machineCode.append(str(binaryOpcode) + str(binaryRx) + str(binaryRy))
        for blank in machineCode:
            if '' in blank:
                print("yes")
        print(machineCode)
        PC += 4


# Function reads binary code instruction
def sim(program):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 4   # Let's initialize 4 empty registers
    mem = [0] * 12288     # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
                          # But my machine has 16GB of RAM, its ok :)
    DIC = 0               # Dynamic Instr Count

    while(not(finished)):
        if PC == len(program) - 4:
            finished = True
        if PC >= len(program):
            break
        fetch = program[PC]
        DIC += 1


        # HERES WHERE THE INSTRUCTIONS GO!
        #print(hex(int(fetch, 2)), PC)
        # ----------------------------------------------------------------------------------------------- ADDI Done!
        if fetch[0:4] == '1000': # Reads the Opcode
            PC += 4
            rx = int(fetch[4:6], 2) # Reads the next two bits which is rx
            imm = -(256 - int(fetch[6:], 2)) if fetch[6] == '1' else int(fetch[6:], 2) # Reads the immediate
            register[rx] = register[rx] + imm

        else:
            # This is not implemented on purpose
            pass
            #print('Not implemented\n')
        
        #printInfo(register[8:23],DIC,hi,lo,mem[8192:8272], PC)

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    #printInfo(register[8:23],DIC,hi,lo,mem[8192:8272], PC)
    input()


def printInfo(_register, _DIC, _hi, _lo, _mem, _PC):
    num = int(_PC/4)
    #inst = asmCopy[num-1]
    inst = inst.replace("\n",'')
    print('******* Instruction Number ' + str(num) + '. ' + inst + ' : *********\n')
    print('Registers $8 - $23 \n', _register)
    print('\nDynamic Instr Count ', _DIC)
    print('\nMemory contents 0x2000 - 0x2050 ', _mem)
    print('\nhi = ', _hi)
    print('lo = ', _lo)
    print('\nPC = ', _PC)
    print('\nPress enter to continue.......')

    
def ConvertHexToInt(_line):
    i = ""
    for item in _line:
        if "0x" in item:
            ind = _line.index(item)
            if "(" in item:
                i = item.find("(")
                i = item[i:]
                item = item.replace(i,"")
            item = str(int(item, 0))
            item = item + i
            _line[ind]=item
            
    return _line



def main():
    file = open("test.asm", "r") # Opens the file
    asm = file.readlines() # Gets a list of every line in file

    program = [] # Whats this?

    for line in asm:    # For every line in the asm file

         # Not sure what this does.
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        # Removes empty lines from the file
        if line[0] == '\n':
            continue
        line = line.replace('\n','')

        instr = line[0:]
        program.append(instr)       # since PC increment by 4 every cycle,
        program.append(0)           # let's align the program code by every
        program.append(0)           # 4 lines
        program.append(0)
        print(line)

    # We SHALL start the simulation!
    print(program)
    machineCode = machineTranslation(program) # Translates the english assembly code to machine code
    #sim(machineCode)

if __name__ == '__main__':
    main()