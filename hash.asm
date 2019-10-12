
addi $9, $0, 101
addi $8, $0, 1
loop:
func $10, $8, 0xFA19E366
bne $8, $9, loop
sb $10, 0x2008($0)