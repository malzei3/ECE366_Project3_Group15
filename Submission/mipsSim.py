from __future__ import print_function
import os


# Start of program
def main():
    file = open(SelectFile("prog.txt"), 'r')  # Opens the file
    asm = file.readlines()  # Gets a list of every line in file

    program = []  # Whats this? list

    for line in asm:  # For every line in the asm file
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        # Removes empty lines from the file
        if line[0] == '\n':
            continue
        line = line.replace('\n', '')

        # If user entered a Hex file
        if line.count("0x"):
            line = ConvertHexToBin(line)

        instr = line[0:]
        program.append(instr)

    # We SHALL start the simulation!
    # machineCode = machineTranslation(program) # Translates the english assembly code to machine code
    sim(program)  # Starts the assembly simulation with the assembly program machine code as # FUNCTION: read input file


# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: Ask user to enter the file name. If user press enter the applicaiton will take the default file.
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
# ---- FUNCTION: Translates the assembly to machine code and stores it back in program []
def machineTranslation(program):
    PC = 0  # Used to end the while loop
    instructionList = {'addi': 1000}  # Stores the opcodes of all our assembly instructions
    machineCode = []  # Stores the final binary data

    while (PC < len(program)):  # Goes through all the instructions in the program
        instruction = program[PC]  # Sets instruction to the current instruction we are translating

        # This keeps track of where the opcode ends (Because there would be a space there)
        spaceLocation = 0
        for char in instruction:
            if char == ' ':
                # print("Space location at " + str(spaceLocation))
                break
            else:
                spaceLocation += 1

        # Below code translates the english opcode to binary and checks for errors
        opcode = instruction[0:spaceLocation]  # Grabs the english string of the opcode
        binaryOpcode = instructionList.get(opcode)  # Replaces the english text opcode with the binary one
        if binaryOpcode == None:  # Gives error if the opcode is not supported by instructionList (for debuging purposes)
            print("Instruction not implemented, please check!")
            print("Error instruction '" + opcode + "' not supported.")
            quit()

        # Grabs the english data for the 2 bits after the opcode and translates it to binary
        rx = instruction[spaceLocation + 2:spaceLocation + 3]  # Grabs the next two bits as an english string
        binaryRx = "{0:2b}".format(int(rx))  # Converts to binary

        # Grabs the english data for the last 2 bits and translates it to binary
        ry = instruction[spaceLocation + 5:]  # Grabs the rest of the data as a english string NOTE: ry can also be imm
        binaryRy = "{0:2b}".format(int(ry))

        # Adds all the binary data into machineCode. NOTE: The data has spaces which need to be fixed by the for loop
        machineCode.append(str(binaryOpcode) + str(binaryRx) + str(binaryRy))
        incompleteMachineCode = machineCode[PC]  # This machine code will have spaces in it which will be fixed
        completeMachineCode = ''  # This will contain the fixed machineCode
        for char in incompleteMachineCode:
            if char == ' ':
                char = '0'
            else:
                pass
            completeMachineCode += char
        print("The complete machine code for the instruction is " + completeMachineCode)
        machineCode[PC] = completeMachineCode  # The correct final binary value is now in machineCode
        machineCode.append(0)  # since PC increment by every cycle,
        machineCode.append(0)  # let's align the program code by every 1 line
        machineCode.append(0)
        PC += 4  # Used to end the while loop
    print("The machine code for the program is ")
    print(machineCode)
    return machineCode


# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: TBD
def sim(program):
    finished = False  # Is the simulation finished?
    PC = 0  # Program Counter
    register = [0] * 4  # Let's initialize 4 empty registers
    mem = [0] * 12288  # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
    # But my machine has 16GB of RAM, its ok :)
    DIC = 0  # Dynamic Instr Count

    while (not (finished)):
        instruction = ""
        instrDescription = ""
        if PC == len(program):
            finished = True
        if PC > len(program) and PC < len(program):
            break
        try:
            fetch = program[PC]
        except:
            break
        DIC += 1

        # HERES WHERE THE INSTRUCTIONS GO!
        # ----------------------------------------------------------------------------------------------- addi
        if fetch[0:4] == '1000':  # Reads the Opcode
            PC += 1
            rx = int(fetch[4:6], 2)  # Reads the next two bits which is rx
            imm = int(fetch[6:], 2)  # Reads the immediate
            register[rx] = register[rx] + imm
            if register[rx] > 255:  # Overflow support
                register[rx] = register[rx] - 255 - 1
            # print out the updates
            instruction = "addi $" + str(rx) + ", " + str(imm)
            instrDescription = "Register " + str(rx) + " is now added by " + str(imm)


        # ----------------------------------------------------------------------------------------------- init
        elif fetch[0:2] == '00':  # Reads the Opcode
            PC += 1
            rx = int(fetch[2:4], 2)  # Reads the next two bits which is rx
            imm = int(fetch[4:], 2)  # Reads the immediate
            register[rx] = imm
            # print out the updates
            instruction = "init $" + str(rx) + ", " + str(imm)
            instrDescription = "Register " + str(rx) + " is now equal to " + str(imm)


        # ----------------------------------------------------------------------------------------------- subi
        elif fetch[0:4] == '0111':  # Reads the Opcode
            PC += 1
            rx = int(fetch[4:6], 2)  # Reads the next two bits which is rx
            ry = int(fetch[6:], 2)  # Reads the immediate
            register[rx] = register[rx] - ry
            if register[rx] <= 0:  # Underflow support
                register[rx] = 255 - abs(register[rx] + 1)
            # print out the updates
            instruction = "sub $" + str(rx) + ", $" + str(ry)
            instrDescription = "Register " + str(rx) + " is now subtracted by " + str(ry)

        # ----------------------------------------------------------------------------------------------- sb
        elif fetch[0:4] == '1001':  # Reads the Opcode
            PC += 1
            rx = int(fetch[4:6], 2)  # Reads the next two bits which is rx
            ry = int(fetch[6:], 2)  # Reads the immediate
            mem[register[ry]] = register[rx]
            # print out the updates
            instruction = "sb $" + str(rx) + ", $" + str(ry)
            instrDescription = "Memory address " + str(register[ry]) + " is now equal to " + str(register[rx])

        # ----------------------------------------------------------------------------------------------- minc (memory increment)
        elif fetch[0:4] == '1010':
            PC += 1
            rx = int(fetch[4:6], 2)  # Reads the next two bits which is rx
            imm = int(fetch[6:], 2)  # Reads the immediate
            mem[register[rx]] += imm

        # ----------------------------------------------------------------------------------------------- hash
        elif fetch[0:4] == '1100':  # Reads the Opcode
            PC += 1
            rx = int(fetch[4:6], 2)  # Reads the next two bits which is rx
            ry = int(fetch[6:8], 2)  # Reads the next two bits which is ry
            A = register[rx]
            B = register[ry]

            instrDescription = "Register " + str(rx) + " is now equal to hash of " + str(A) + " and " + str(B)

            for i in range(1, 6):
                C = bin(A * B).replace("0b", "")
                a = len(C) - 8
                lo = C[a:].zfill(8)
                hi = C[0:a].zfill(8)
                xor = int(hi, 2) ^ int(lo, 2)
                A = xor

            A = bin(A).replace("0b", "").zfill(8)
            lo = A[4:].zfill(4)
            hi = A[0:4].zfill(4)
            C = int(hi, 2) ^ int(lo, 2)
            C = bin(C).replace("0b", "").zfill(4)
            lo = C[2:].zfill(2)
            hi = C[0:2].zfill(2)
            C = int(hi, 2) ^ int(lo, 2)
            register[rx] = C

            instruction = "hash $" + str(rx) + ", $" + str(ry)



        # ----------------------------------------------------------------------------------------------- saal
        elif fetch[0:4] == '1101':  # Reads the Opcode
            PC += 1
            rx = int(fetch[4:5], 2)  # Reads the next bit which is rx (Either r0 or r1)
            imm = int(fetch[5:], 2)  # Reads the immediate (3 bits)
            mem[255 + imm] = register[rx]
            # print out the updates
            instruction = "sb $" + str(rx) + ", $" + str(255 + imm)
            instrDescription = "Memory address " + str(255 + imm) + " is now equal to " + str(register[rx])

        # ----------------------------------------------------------------------------------------------- cpy
        elif fetch[0:4] == '1110':  # Reads the Opcode
            PC += 1
            rx = int(fetch[4:6], 2)  # Reads the next bit which is rx
            ry = int(fetch[6:], 2)  # Reads the register ry
            register[rx] = register[ry]
            # print out the update
            instruction = "cpy $" + str(rx) + ", $" + str(ry)
            instrDescription = "Register " + str(rx) + "is now set to the value of register " + str(ry)

        else:
            # This is not implemented on purpose
            print('Not implemented\n')
            PC += 1
        printInfo(register, DIC, mem[0:259], PC, instruction, instrDescription)

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    printInfo(register, DIC, mem[0:259], PC, instruction, instrDescription)
    #input()


# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: to print out each instruction line is running with its updates
def printInfo(_register, _DIC, _mem, _PC, instr, instrDes):
    num = int(_PC / 1)
    print('******* Instruction Number ' + str(num) + '. ' + instr + ' : *********\n')
    print(instrDes)
    print('\nRegisters $0- $4 \n', _register)
    print('\nDynamic Instr Count ', _DIC)
    print('\nMemory contents 0xff - 0x64 ', _mem)
    print('\nPC = ', _PC)
    print('\nPress enter to continue.......')
    #input()


# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: Convert line from hex into bin
def ConvertHexToBin(_line):
    # remove 0x then convert.
    _line.replace("0x", "")
    _line = str(bin(int(_line, 16)).zfill(8))
    _line = _line.replace("0b", "")
    return _line


# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: Convert the hex into int in an asm instruction. ex: lw $t, offset($s) converts offset to int.
def ConvertHexToInt(_line):
    i = ""
    for item in _line:
        if "0x" in item:
            ind = _line.index(item)
            if "(" in item:
                i = item.find("(")
                i = item[i:]
                item = item.replace(i, "")
            item = str(int(item, 0))
            item = item + i
            _line[ind] = item

    return _line


if __name__ == '__main__':
    main()