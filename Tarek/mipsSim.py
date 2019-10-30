from __future__ import print_function
import os


# FUNCTION: read input file
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


# Function reads binary code instruction
def sim(program):
    hilo = [0] * 64
    hi = 0
    lo = 0
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 32   # Let's initialize 32 empty registers
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
        #print(hex(int(fetch,2)), PC)
        # ----------------------------------------------------------------------------------------------- ADDI Done!
        if fetch[0:6] == '001000': 
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = register[s] + imm
        
        else:
            # This is not implemented on purpose
            print('Not implemented\n')
        
        printInfo(register[8:23],DIC,hi,lo,mem[8192:8272], PC)

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    printInfo(register[8:23],DIC,hi,lo,mem[8192:8272], PC)
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
    file = open(SelectFile("prog.asm"), r)

    program = []
    for line in file:
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)
        if line[0] == '\n':
            continue
        line = line.replace('\n','')
        instr = line[0:]
        program.append(instr)       # since PC increment by 4 every cycle,
        program.append(0)           # let's align the program code by every
        program.append(0)           # 4 lines
        program.append(0)

    # We SHALL start the simulation! 
    sim(program)

if __name__ == '__main__':
    main()