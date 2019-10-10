lui $8, 0xFA19 #1
ori $8, $8, 0xE366 #2
addi $9, $0, 1 #3
addi $11, $0, 0
addi $12, $0, 20
addi $15, $0, 0x64
addi $16, $0, 0
addi $17, $0, 1

Store_loop:#1
Mult_loop: #5x

multu $8, $9 #might optimize to use $9 differently #4
mflo $13 #5
mfhi $14 #6
xor $9, $13, $14 #7
sw $9, 0x2500($11) #8
#add $9, $0, $9
addi $11, $11, 4
bne $11, $12, Mult_loop #9

addi $17, $17, 1
addi $11, $0, 0
addi $9, $17, 0

lw $13, 0x2510($0) #10
srl $14, $13, 16 #11
andi $13, $13, 0x0000FFFF #12
xor $13, $13, $14
srl $14, $13, 8
andi $13, $13, 0x00FF
xor $13, $13, $14
sb $13, 0x2020($16) #13

#add checking for max here
sltu $18, $13, $19 #14 if $13 is less than $19
bne $18, $0, skip
addi $19, $13, 0
addi $18, $16, 0x2020
sw $18, 0x2000($0)
sb $19, 0x2004($0)

skip:
#checking for 11111 from $13
#Pattern_Check:, $13, $14, $20, $21, $22, $23
addi $14, $0, 0 # number of ones in a row
addi $21, $0, 5 # number of ones to find
addi $22, $0, 1 # const
one_loop:
andi $20, $13, 0x1 # check bottom bit
srl $13, $13, 1 # shift number right by one
bne $20, $22, no_inc # if its not one, skip inc
addi $14, $14, 1 # inc number of ones seen
j prep_next_loop #16
no_inc:
addi $14, $0, 0
prep_next_loop:
bne $14, $21, no_found_ones # if counter isnt 5
j found_ones
no_found_ones:
bne $13, $0, one_loop # more ones left
j skip_3
found_ones:
lw $23, 0x2008($0)
addi $23, $23, 1
sw $23, 0x2008($0)
j skip


skip_3:
addi $16, $16, 1
bne $16, $15, Store_loop





