def saveJumpLabel(asm,labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index\
            labelAddr.append(lineCount*4)
            asm[lineCount] = line[line.index(":")+1:]
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
        

def main():
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo,hi
    LO = 24
    HI = 25
    f = open("mc.txt","w+")
    h = open("mips1.asm","r")
    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName, labelAddr) # Save all jump's destinations
    
    for line in asm:
        
        f.write('------------------------------ \n')
        f.write('MIPS Instruction: ' + line + '\n')
        
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
            
        if(line[0:5] == "addiu"): # $t = $s + imm; advance_pc (4); addiu $t, $s, imm
            line = line.replace("addiu","")
            line = line.split(",")
            PC = PC + 4;
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
        
        elif(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            #f.write(line)
            line = line.replace("addi","")
            line = line.split(",")
            PC = PC + 4;
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:3] == "add"): # ADD $d = $s + $t; advance_pc (4); add $d, $s, $t
            line = line.replace("add","")
            line = line.split(",")
            PC = PC + 4;
            regval[int(line[0])] = regval[int(line[1])] + regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        
        elif(line[0:5] == "multu"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("multu","")
            line = line.split(",")
            PC = PC + 4;
            regval[LO] = regval[int(line[0])]*regval[int(line[1])]
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + '\n')
            
        #mult
        elif(line[0:4] == "mult"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("mult","")
            line = line.split(",")
            PC = PC + 4;
            regval[LO] = regval[int(line[0])]*regval[int(line[1])]
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + '\n')
            
        #srl
        elif(line[0:3] == "srl"): # ADD
            line = line.replace("srl","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            h = format(int(line[2]),'05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(h) + str('000010') + '\n')
            
        #lb
        elif(line[0:2] == "lb"): # ADD
            line = line.replace("lb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            imm = format(int(line[1]),'016b')
            f.write(str('100000') + str(rs) + str(rt) + str(imm) + '\n')
            
        #sb
        elif(line[0:2] == "sb"): # ADD
            line = line.replace("sb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            imm = format(int(line[1]),'016b')
            f.write(str('101000') + str(rs) + str(rt) + str(imm) + '\n')
            
        #lw
        elif(line[0:2] == "lw"): # ADD
            line = line.replace("lw","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            imm = format(int(line[1]),'016b')
            f.write(str('100011') + str(rs) + str(rt) + str(imm) + '\n')
            
        #sw
        elif(line[0:2] == "sw"): # ADD
            line = line.replace("sw","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            imm = format(int(line[1]),'016b')
            f.write(str('101011') + str(rs) + str(rt) + str(imm) + '\n')
            
        #beq
        elif(line[0:3] == "beq"): # ADD
            line = line.replace("beq","")
            line = line.split(",")
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            if(line[2].isdigit()): # First,test to see if it's a label or a integer
                f.write(str('000100') + str(rs) + str(rt) + str(format(int(line[2]),'016b')) + '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                        f.write(str('000100') + str(rs) + str(rt) + str(format(int(labelIndex[i]),'016b')) + '\n')

        #bne
        elif(line[0:3] == "bne"): # ADD
            line = line.replace("bne","")
            line = line.split(",")
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            if(line[2].isdigit()): # First,test to see if it's a label or a integer
                f.write(str('000101') + str(rs) + str(rt) + str(format(int(line[2]),'016b')) + '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                        f.write(str('000101') + str(rs) + str(rt) + str(format(int(labelIndex[i]),'016b')) + '\n')

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
            line = line.replace("j","")
            line = line.split(",")

            f.write('Operation: PC = nPC; ' + '\n')


            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                 PC = line[0]
                 line = line[0]
                 f.write('PC is now at ' + str(line[0]) + '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        PC = labelAddr[i]
                        line = labelIndex[i]
                        f.write('PC is now at ' + str(labelAddr[i]) + '\n')
                
            f.write('No Registers have changed. \n')


    f.close()

if __name__ == "__main__":
    main()