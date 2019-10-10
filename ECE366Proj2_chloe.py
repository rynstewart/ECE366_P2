            
                       
#####instructions we still need######
"""
lui, ori, mfhi, mflo, slt
andi, bne
special instruction



slt - DONE
mfhi, mflo - needs mult rework
ori - DONE
bne - 
lui - 
   
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

def hash(B, MEM):
    A = 0x01
    max = 0
    max_Addr = 0
    pattern_Num = 0
    for A in range(0x65):
        #first fold (down to 32 bits)
        C = B*A
        C_hi = C >> 32
        C_low = C & 0x00000000FFFFFFFF
        C = C_hi^C_low
        
        #Second fold (down to 16 bits)
        C = B*C
        C_hi = C >> 32
        C_low = C & 0x00000000FFFFFFFF
        C = C_hi^C_low

        #third fold
        C = B*C
        C_hi = C >> 32
        C_low = C & 0x00000000FFFFFFFF
        C = C_hi^C_low

        #fourth fold
        C = B*C
        C_hi = C >> 32
        C_low = C & 0x00000000FFFFFFFF
        C = C_hi^C_low

        #fifth fold
        C = B*C
        C_hi = C >> 32
        C_low = C & 0x00000000FFFFFFFF
        C = C_hi^C_low

        #Down to 16 bits
        C_hi = C >> 16
        C_low = C & 0x0000FFFF
        C = C_hi^C_low

        #Down to 8 bits
        C_hi = C >> 8
        C_low = C & 0x00FF
        C = C_hi^C_low

        MEM[0x2020 + (A - 1)] = C

        #find max
        if(max < C):
            max = C
            max_Addr = 0x2020 + (A - 1)

        #pattern match
        if('11111' in str(bin(C))):
            pattern_Num += 1
            #place in memory incremented by one
    
    #storing max and pattern match
    max_Addrlo = max_Addr >> 8
    max_Addrhi = max_Addr & 0x00FF
    MEM[0x2001] = max_Addrlo
    MEM[0x2000] = max_Addrhi
    MEM[0x2004] = max
    MEM[0x2008] = pattern_Num
    



def main():
    
    MEM = [0]*12288 #intialize array to all 0s for 0x3000 indices
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo, hi
    LO = 24
    HI = 25
    good_in = False
    while(good_in == False):
        file_Name = input("Please type file name, enter for default, or q to quit:")
        if(file_Name == "q"):
           print("Bye!")
           return
        if(file_Name == "\n"):
            file_Name = "mips1.asm"
        try:
            f = open(file_Name)
            f.close()
            good_in = True
        except FileNotFoundError:
            print('File does not exist')
    
    f = open("mc.txt","w+")
    h = open(file_Name,"r")

    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName, labelAddr) # Save all jump's destinations

    #import pdb; pdb.set_trace()

    #for lineCount in len(asm):
    lineCount = 0
    while(lineCount < len(asm)):

        line = asm[lineCount]
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
            regval[int(line[0])] = regval[int(line[1])] + int(line[2],16)
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        if(line[0:5] == "addu"): # $t = $s + imm; advance_pc (4); addiu $t, $s, imm
            line = line.replace("addu","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
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
            #x = format(int(line[1]),'032b')^format(int(line[2]),'032b')
            x = format(int(line[1]),'032b')
            y = format(int(line[2]),'032b')
            z = int(x)^int(y)
            regval[int(line[0])] = z
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        elif(line[0:3] == "lui"): # $t = (imm << 16); advance_pc (4); lui $t, imm
            line = line.replace("lui","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = int(line[1],16)
            f.write('Operation: $' + line[0] + ' = ' + '(' + line[1] + ' << 16); ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + line[1] + '\n')            
            
        
        elif(line[0:5] == "multu"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("multu","")
            line = line.split(",")
            PC = PC + 4
            temp = regval[int(line[0])]*regval[int(line[1])]
            templo = format(temp, '064b')
            templo = temp & 0x00000000FFFFFFFF
            temphi = temp >> 32
            regval[LO] = int(templo)
            regval[HI] = int(temphi)
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + ', $HI = ' + str(regval[HI]) + '\n')
            
        #mult
        elif(line[0:4] == "mult"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("mult","")
            line = line.split(",")
            PC = PC + 4
            temp = regval[int(line[0])]*regval[int(line[1])]
            templo = format(temp, '064b')
            templo = temp & 0x00000000FFFFFFFF
            temphi = temp >> 32
            regval[LO] = int(templo)
            regval[HI] = int(temphi)
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + ', $HI = ' + str(regval[HI]) + '\n')
            
        elif(line[0:4] == "mfhi"): # Operation:$d = $HI; advance_pc (4);mfhi $d
            line = line.replace("mfhi","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[HI]
            #regval[int(line[0])] = rshift(regval[int(line[1])], int(line[2]))
            f.write('Operation: $' + line[0] + ' = ' + '$HI; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[HI]) + '\n')            
        
        elif(line[0:4] == "mflo"): # Operation:$d = $LO; advance_pc (4);mflo $d
            line = line.replace("mflo","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[LO]
            #regval[int(line[0])] = rshift(regval[int(line[1])], int(line[2]))
            f.write('Operation: $' + line[0] + ' = ' + '$LO; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[LO]) + '\n')            
        
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
            regval[int(line[0])] = format(int(MEM[regval[int(line[1])]+int(line[2])]),'08b')
            regval[int(line[0])] = abs((int(regval[int(line[0])])))
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
            MEM[regval[int(line[2])]+int(line[1])] = format(int(line[0]),'08b')
            MEM[regval(int(line[2]))+int(line[1])] = int(MEM[regval[int(line[2])]+int(line[1])])
            f.write('Operation: MEM[$' + line[2] + ' + ' + line[1] + '] = ' + '$' + line[0] + '; \n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(int(line[2])+int(line[1])) + ' = ' + str(regval[int(line[0])]) + ' \n')
           
        #slt
        elif(line[0:3] == "slt"): # ADD
            line = line.replace("slt","")
            line = line.split(",")
           
            if(line[1] < line[2]):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n') 
        
        elif(line[0:4] == "andi"):
            line = line.replace("andi", "")
            line = line.split(",")
            PC = PC + 4

            regval[int(line[1])] = format(regval[int(line[2])] & regval[int(line[0])])
            temp_val = format( int(regval[int(line[1])]),'032b')

            f.write('Operation: $' + line[1] + '= $' + line[0] + "&"  + line[2])
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str( int(line[2]) ) + '=' + str(regval[int(line[0])]) + '\n')

        elif(line[0:3] == "ori"):
            line = line.replace("ori", "")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[1])] = format(regval[int(line[2])] | regval[int(line[0])])
            temp_val = format( int(regval[int(line[1])]),'032b')

            # __, 0, 1, 2
            #op, rs, rt, imm
            #6, 5, 5, 16
            #rt = rs | imm()
            f.write('Operation: $' + line[1] + '= $' + line[0] + "|"  + line[2])
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str( int(line[2]) ) + '=' + str(regval[int(line[0])]) + '\n')

        #hash
        elif(line[0:4]=="hash"):
            line = line.replace("hash","")
            line = line.split(",")
            B = int(line[0], 16)
            hash(B, MEM)
            print("hash function")


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
            f.write('No Registers have changed. \n')
        

        #beq
        elif(line[0:3] == "beq"): # Beq
            line = line.replace("beq","")
            line = line.split(",")
            if(regval[int(line[0])]==regval[int(line[1])]):
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
            f.write('No Registers have changed. \n')


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
    #print final results
    #print(hex(MEM[0x2000]))
    #print(hex(MEM[0x2004]))
    #print(hex(MEM[0x2008]))
    print("Used memory values:\n")
    print("            ", end="")
    for x in range(0,8,1):
        print("0x"+ format(x*4,"08x"), end=" ")
    print("\n")
    print("--------------------------------------------------------------------------------------------------",end="")
    count = 0
    print("\n")
    for x in range(0x2003,0x20a0,4):
        #import pdb; pdb.set_trace() 
        if((x-0x3)%0x20==0):
            print("0x"+format(x-0x3,"08x") + '|', end=" ")
        print("0x", end="")
        for y in range(0,4,1):
            #import pdb; pdb.set_trace()
            print(format(MEM[x-y], "02x"), end="")
        print(" ", end = "")
        count += 1
        if(count == 8):
            count = 0
            print("\n")

    f.close()

if __name__ == "__main__":
    main()