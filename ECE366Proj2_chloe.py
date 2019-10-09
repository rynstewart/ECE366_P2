            
                       
#####instructions we still need######
"""
lui, ori, mfhi, mflo, slt
andi, bne
special instruction (hash)
   
"""


def saveJumpLabel(asm,labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index\
            labelAddr.append(lineCount*4)
            #asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def regNameInit(regName):
    i = 0
    while i<=23:
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')
    
def rshift(val, n): 
    #x = 1
    return val>>n

    """
    if val >= 0:
        return val>>n
    else:
        #i = (format(val, '032b') + format(0x8000, '032b'))>>n
        while x <= n:
            i = (val)>>1 + 0x8000
            x+=1
        return i
    """

def hash(B, A):

    #first fold (down to 32 bits)
    C = B*A
    C_hi = C << 32
    C_low = C & 0x00000000FFFFFFFF
    C = C_hi^C_low

    C_hi = C << 16
    C_low = C & 0x0000FFFF
    C = C_hi * C_low
    C_hi = C << 16
    C_low = C & 0x0000FFFF
    C = C_hi^C_low


def main():
    
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo, hi
    LO = 24
    HI = 25
    f = open("mc.txt","w+")
    h = open("mips1.asm","r")
    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName, labelAddr) # Save all jump's destinations

    #import pdb; pdb.set_trace()

    #for lineCount in len(asm):
    lineCount = 0
    while(lineCount < len(asm)):

        line = asm[lineCount]
        #import pdb; pdb.set_trace()
        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
                        
        if(line[0:5] == "addiu"): # $t = $s + imm; advance_pc (4); addiu $t, $s, imm
            line = line.replace("addiu","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
        
        elif(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            #f.write(line)
            line = line.replace("addi","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:3] == "add"): # ADD $d = $s + $t; advance_pc (4); add $d, $s, $t
            line = line.replace("add","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
            line = line.replace("xor","")
            line = line.split(",")
            PC = PC + 4
            x = format(int(line[1]),'032b')^format(int(line[2]),'032b')
            regval[int(line[0])] = int(x)
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        
        elif(line[0:5] == "multu"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("multu","")
            line = line.split(",")
            PC = PC + 4
            temp = regval[int(line[0])]*regval[int(line[1])]
            templo = format(temp, '064b')
            templo = temp & 0x0000FFFF
            temphi = temp >> 32
            regval[LO] = int(templo)
            regval[HI] = int(temphi)
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + '$HI = ' + str(regval[HI]) + '\n')
            
        #mult
        elif(line[0:4] == "mult"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("mult","")
            line = line.split(",")
            PC = PC + 4
            temp = regval[int(line[0])]*regval[int(line[1])]
            templo = format(temp, '064b')
            templo = temp & 0x0000FFFF
            temphi = temp >> 32
            regval[LO] = int(templo)
            regval[HI] = int(temphi)
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + '$HI = ' + str(regval[HI]) + '\n')
            

                #srl
        elif(line[0:3] == "srl"): # $d = $t >> h; advance_pc (4); srl $d, $t, h
            line = line.replace("srl","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = rshift(-1, int(line[2]))
            #regval[int(line[0])] = rshift(regval[int(line[1])], int(line[2]))
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' >> ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')            
            
        elif(line[0:2] == "lbu"): # $t = MEM[$s + offset]; advance_pc (4); lb $t, offset($s)
            line = line.replace("lbu","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = format(int(regval[int(line[1])+int(line[2])]),'08b')
            regval[int(line[0])] = abs(format(int(regval[int(line[0])])))
            f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + ' \n')
            
        #lb
        elif(line[0:2] == "lb"): # $t = MEM[$s + offset]; advance_pc (4); lb $t, offset($s)
            line = line.replace("lb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = format(int(regval[int(line[1])+int(line[2])]),'08b')
            regval[int(line[0])] = format(int(regval[int(line[0])]))
            f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + ' \n')
            
        #sb
        elif(line[0:2] == "sb"): # MEM[$s + offset] = (0xff & $t); advance_pc (4); sb $t, offset($s)
            line = line.replace("sb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[2])+int(line[1])] = format(int(line[0]),'08b')
            regval[int(line[2])] = format(int(regval[int(line[2])]))
            f.write('Operation: MEM[$' + line[2] + ' + ' + line[1] + '] = ' + '$' + line[0] + '; \n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(int(line[2])+int(line[1])) + ' = ' + str(regval[int(line[0])]) + ' \n')

            
        #lw
        elif(line[0:2] == "lw"): # ADD
            line = line.replace("lw","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = format(int(regval[int(line[1])+int(line[2])]),'032b')
            regval[int(line[0])] = format(int(regval[int(line[0])]))
            f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + ' \n')
            
        #sw
        elif(line[0:2] == "sw"): # MEM[$s + offset] = $t; advance_pc (4); sw $t, offset($s)
            line = line.replace("sw","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[2])+int(line[1])] = format(int(line[0]),'032b')
            f.write('Operation: MEM[$' + line[2] + ' + ' + line[1] + '] = ' + '$' + line[0] + '; \n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(int(line[2])+int(line[1])) + ' = ' + str(regval[int(line[0])]) + ' \n') 

        #bne
        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            if(regval[int(line[0])]!=regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = line[2]
                    lineCount = line[2]
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')
                continue

        #sltu
        elif(line[0:4] == "sltu"): # ADD
            line = line.replace("sltu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011') + '\n')
           
        #slt
        elif(line[0:3] == "slt"): # ADD
            line = line.replace("slt","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010') + '\n')
            
            
        elif(line[0:1] == "j"): # JUMP
            #import pdb; pdb.set_trace()
            line = line.replace("j","")
            line = line.split(",")
            f.write('Operation: PC = nPC; ' + '\n')
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                 PC = line[0]
                 lineCount = line[0]
                 f.write('PC is now at ' + str(line[0]) + '\n')
            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        PC = labelAddr[i]
                        lineCount = labelIndex[i]
                        f.write('PC is now at ' + str(labelAddr[i]) + '\n')        
            f.write('No Registers have changed. \n')
            continue
        lineCount = lineCount + 1
    f.close()

if __name__ == "__main__":
    main()