from __future__ import print_function

# Start of program
def main():
    file = open("test.asm", "r") # Opens the file
    asm = file.readlines() # Gets a list of every line in file

    program = [] # Whats this?

    for line in asm:    # For every line in the asm file
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        # Removes empty lines from the file
        if line[0] == '\n':
            continue
        line = line.replace('\n','')

        instr = line[0:]
        program.append(instr)
        program.append(0)           # since PC increment by 4 every cycle,
        program.append(0)           # let's align the program code by every 4 lines
        program.append(0)

    # We SHALL start the simulation!
    print("The code that will be converted to binary is ")
    print(program)
    machineCode = machineTranslation(program) # Translates the english assembly code to machine code
    sim(machineCode) # Starts the assembly simulation with the assembly program machine code as input


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


# Translates the assembly to machine code and stores it back in program []
def machineTranslation(program):
    PC = 0 # Used to end the while loop
    instructionList = {'addi': 1000} # Stores the opcodes of all our assembly instructions
    machineCode = [] # Stores the final binary data

    while(PC < len(program)): # Goes through all the instructions in the program
        instruction = program[PC] # Sets instruction to the current instruction we are translating

        # This keeps track of where the opcode ends (Because there would be a space there)
        spaceLocation = 0
        for char in instruction:
            if char == ' ':
                #print("Space location at " + str(spaceLocation))
                break
            else:
                spaceLocation += 1

        # Below code translates the english opcode to binary and checks for errors
        opcode = instruction[0:spaceLocation] # Grabs the english string of the opcode
        binaryOpcode = instructionList.get(opcode) # Replaces the english text opcode with the binary one
        if binaryOpcode == None: # Gives error if the opcode is not supported by instructionList (for debuging purposes)
            print("Instruction not implemented, please check!")
            print("Error instruction '" + opcode + "' not supported.")
            quit()

        # Grabs the english data for the 2 bits after the opcode and translates it to binary
        rx = instruction[spaceLocation + 2:spaceLocation + 3] # Grabs the next two bits as an english string
        binaryRx = "{0:2b}".format(int(rx)) # Converts to binary

        # Grabs the english data for the last 2 bits and translates it to binary
        ry = instruction[spaceLocation + 5:] # Grabs the rest of the data as a english string NOTE: ry can also be imm
        binaryRy = "{0:2b}".format(int(ry))

        # Adds all the binary data into machineCode. NOTE: The data has spaces which need to be fixed by the for loop
        machineCode.append(str(binaryOpcode) + str(binaryRx) + str(binaryRy))
        incompleteMachineCode = machineCode[PC] # This machine code will have spaces in it which will be fixed
        completeMachineCode = '' # This will contain the fixed machineCode
        for char in incompleteMachineCode:
            if char == ' ':
                char = '0'
            else:
                pass
            completeMachineCode += char
        print("The complete machine code for the instruction is " + completeMachineCode)
        machineCode[PC] = completeMachineCode # The correct final binary value is now in machineCode
        machineCode.append(0)  # since PC increment by 4 every cycle,
        machineCode.append(0)  # let's align the program code by every 4 lines
        machineCode.append(0)
        PC += 4 # Used to end the while loop
    print("The machine code for the program is ")
    print(machineCode)
    return machineCode


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
        # ----------------------------------------------------------------------------------------------- ADDI Done!
        if fetch[0:4] == '1000': # Reads the Opcode
            print("Will now addi")
            PC += 4
            rx = int(fetch[4:6], 2) # Reads the next two bits which is rx
            imm = int(fetch[6:], 2) # Reads the immediate
            register[rx] = register[rx] + imm
            print("register " + str(rx) + " is now added by " + str(imm))
            print(register[rx])

        else:
            # This is not implemented on purpose
            print('Not implemented\n')

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    printInfo(register[0:3],DIC,mem[8192:8272], PC)
    input()


def printInfo(_register, _DIC, _mem, _PC):
    num = int(_PC/4)
    #NOTE: I dont know what these 3 lines do so i just left them
    #inst = asmCopy[num-1] #
    #inst = inst.replace("\n",'')
   # print('******* Instruction Number ' + str(num) + '. ' + inst + ' : *********\n')
    print('Registers $8 - $23 \n', _register)
    print('\nDynamic Instr Count ', _DIC)
    print('\nMemory contents 0x2000 - 0x2050 ', _mem)
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


if __name__ == '__main__':
    main()