#PART 1
addi $3, $0, 0x2000
addi $2, $0, 1

loop_1:
sb   $2, 0($3)
addi $2, $2, 1
addi $3, $3, 1
bne  $2, 256, loop_1 

addi $2, $2, -1
sb   $2, 0($3)


#PART 2
addi $4, $0, 0x2000  #address
addi $5, $0, 0	     #the result of what we are asking for, I got 70 as the final asnwers.

loop_2:
lb $10, 0($4)
addi $8, $0, 0      #counter to check if we finished checking all 8 bits in the byte
addi $6, $0, 0      #the counter for how many 1's there are in a byte
HWC:
andi $9, $10, 1
beq $9, $0, skip
addi $6, $6, 1
skip:
srl $10, $10, 1
addi $8, $8, 1
bne $8, 8, HWC

bne $6, 4 , skip_count
addi $5 ,$5, 1

skip_count:
addi $4, $4, 1
bne $4, 8448, loop_2
