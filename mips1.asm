addi $8, $0, 1
addi $9, $0, 2
addi $10, $0, 3
addi $11, $0, 4
addi $12, $0, 5

add $13, $8, $9
addiu $14, $8, 9
mult $8, $9
multu $8, $9
srl $13, $8, 1
slt $13, $8, $9
sltu $13, $8, $9
j label

label:
addi $8, $0, 3
loop:
addi $8, $8, -1
bne $8, $0, loop


beq $8, $0, end

mult $8, $9
multu $8, $9
end:
addi $9, $0, 100



