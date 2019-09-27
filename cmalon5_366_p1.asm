lui $8, 0xFA19
ori $8, $8, 0xE366	#B
addiu $9, $0, 1	#A
addiu $11, $0, 101
addiu $15, $0, 0x2020
addiu $16, $0, 100
addiu $17, $0, 1
addiu $18, $0, 0x21e0
#addi $19, $0, 0xFFFF	#11111111 11111111

hash:

multu $9, $8
mfhi $12
mflo $13
xor $10, $12, $13	#A1

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13	#A2

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13	#A3

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13	#A4

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13	#A5

#multu $10, $17
addu $20, $0, $10
andi $13, $20, 0xFFFF
srl $12, $10, 16

xor $14, $12, $13	#16 bytes
#multu $14, $17

sb $14, 0($18)
lbu $13, 0($18)
srl $12, $14, 8
xor $14, $12, $13	#final C
sb $14, 0($15)

addiu $9, $9, 1
addiu $15, $15, 1
bne $9, $11, hash


addiu $9, $0, 0x2020
addiu $10, $0, 0x2000
addiu $15, $0, 0
addiu $16, $0, 100
addiu $22, $0, 1

find_max:

slt $18, $16, $15
bne $18, $0, done

lbu $12, 0($9)	#curr num
lbu $13, 4($10) #curr max
#subu $14, $12, $13
addu $11, $0, $9
addiu  $9, $9, 1
addiu $15, $15, 1
slt $17, $13, $12
bne $17, $0, store
j find_max

store:

sb $12, 4($10)
sb $11, 0($10)
addu $20, $11, $0
srl $20, $20, 8
sb $20, 1($10)
j find_max

done:

addiu $9, $0, 0x2020
addiu $10, $0, 0x1F	#11111 in dec
addiu $11, $0, 0x2008
addu $14, $0, $0
#sb $14, 0($11)
addu $15, $0, $0
addiu $16, $0, 100
addiu $17, $0, 8
addu $18, $0, $0

pattern_match:

lbu $12, 0($9)

shift:
andi $13, $12, 0x1F
bne $13, $10, pattern_match_cont
j adding

pattern_match_cont:

srl $12, $12, 1
addiu $18, $18, 1
bne $17, $18, shift
j next

adding:

addiu $14, $14, 1
sb $14, 0($11)


#srl $12, $12, 1
#addiu $18, $18, 1
#bne $17, $18, shift
#j next

next:

addiu $15, $15, 1
bne $15, $16, next2
j pre_collision

next2:

addiu $9, $9, 1
addiu $18, $0, 0
j pattern_match

pre_collision:

addiu $9, $0, 0x2020
addiu $10, $0, 0x2010	#value
addiu $11, $0, 0x2014	#count
addiu $13, $9, 1
addiu $14, $0, 0		#current matches
addiu $15, $0, 0x2085
addiu $16, $0, 0		#previous matches
addiu $17, $0, 1

collision:

lbu $20, 0($9)
lbu $21, 0($13)
beq $20, $21, match
addiu $13, $13, 1
beq $13, $15, increment
j collision

match:

addiu $14, $14, 1
addiu $13, $13, 1
beq $13, $15, increment
j collision

increment:

addiu $9, $9, 1
addiu $13, $9, 1
slt $23, $16, $14
bne $23, $17, next3
addu $16, $14, $0
addiu $18, $16, 1
sb $18, 0($11)
sb $20, 0($10)
addu $14, $0, $0
			#change curr to prev if bigger
			#reset curr match
next3:
addu $14, $0, $0
bne $13, $15, collision


