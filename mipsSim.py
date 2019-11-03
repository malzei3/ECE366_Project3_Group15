from __future__ import print_function
import os

# Start of program
def main():
    file = open(SelectFile("prog.txt"), 'r') # Opens the file
    asm = file.readlines() # Gets a list of every line in file

    program = [] # Whats this? list

    for line in asm:    # For every line in the asm file
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        # Removes empty lines from the file
        if line[0] == '\n':
            continue
        line = line.replace('\n','')

        #If user entered a Hex file
        if line.count("0x"):
            line = ConvertHexToBin(line)

        instr = line[0:]
        program.append(instr)
        program.append(0)           # since PC increment by 4 every cycle,
        program.append(0)           # let's align the program code by every 4 lines
        program.append(0)

    # We SHALL start the simulation!
    #machineCode = machineTranslation(program) # Translates the english assembly code to machine code
    sim(program) # Starts the assembly simulation with the assembly program machine code as # FUNCTION: read input file

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Ask user to enter the file name. If user press enter the applicaiton will take the default file.
def SelectFile(defaultFile):

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    # Select  file, default is prog.asm
    while True:
        cktFile = defaultFile
        print("\nRead asm file: use " + cktFile + "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            userInput = defaultFile
            return userInput
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
            else:
                return userInput

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Remember where each of the jump label is, and the target location 
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

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Translates the assembly to machine code and stores it back in program []
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


# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: TBD
def sim(program):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 4   # Let's initialize 4 empty registers
    mem = [0] * 12288     # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
                          # But my machine has 16GB of RAM, its ok :)
    DIC = 0               # Dynamic Instr Count

    while(not(finished)):
        instruction = ""
        instrDescription = ""
        if PC == len(program) - 4:
            finished = True
        if PC >= len(program):
            break
        fetch = program[PC]
        DIC += 1


        # HERES WHERE THE INSTRUCTIONS GO!
        # ----------------------------------------------------------------------------------------------- ADDI
        if fetch[0:4] == '0000': # Reads the Opcode
            PC += 4
            rx = int(fetch[4:6], 2) # Reads the next two bits which is rx
            imm = int(fetch[6:], 2) # Reads the immediate
            register[rx] = register[rx] + imm
            # print out the updates
            instruction = "addi $" + str(rx) + ", " + str(imm)
            instrDescription = "register " + str(rx) + " is now added by " + str(imm)

        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0001': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0010': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0011': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0100': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0101': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0110': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '0111': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '1000': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '1001': # Reads the Opcode
            PC += 4


        # ----------------------------------------------------------------------------------------------- 
        elif fetch[0:4] == '1010': # Reads the Opcode
            PC += 4

        
        else:
            # This is not implemented on purpose
            print('Not implemented\n')
            PC += 4
        printInfo(register,DIC,mem[8192:8272], PC, instruction, instrDescription)

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    printInfo(register,DIC,mem[8192:8272], PC,"","")
    input()

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: to print out each instruction line is running with its updates 
def printInfo(_register, _DIC, _mem, _PC, instr, instrDes):
    num = int(_PC/4)
    print('******* Instruction Number ' + str(num) + '. ' + instr + ' : *********\n')
    print(instrDes)
    print('\nRegisters $0- $4 \n', _register)
    print('\nDynamic Instr Count ', _DIC)
    print('\nMemory contents 0x2000 - 0x2050 ', _mem)
    print('\nPC = ', _PC)
    print('\nPress enter to continue.......')
    input()

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Convert line from hex into bin
def ConvertHexToBin(_line):
    #remove 0x then convert.
    _line.replace("0x","")
    _line = str(bin(int(_line, 16)).zfill(8))
    _line = _line.replace("0b","")
    return _line

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Convert the hex into int in an asm instruction. ex: lw $t, offset($s) converts offset to int.
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