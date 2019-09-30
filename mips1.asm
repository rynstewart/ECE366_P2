addi $8, $0, 1
addi $9, $0, 2
addi $10, $0, 3
addi $11, $0, 4
addi $12, $0, 5

add $13, $8, $9
addiu $14, $8, $9
mult $8, $9
multu $8, $9
srl $13, $8, 1
lb $13, 0 ($8)
sb $13, 1 ($14)
lw $13, 2 ($8)
sw $13, 3 ($14)
beq $8, $9, next
next:
bne $8, $9, next2
next2:
slt $13, $8, $9
sltu $13, $8, $9
j label

addi $8, $0, 1

label:
