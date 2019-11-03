lui $8, 0xFA19
ori $8, $8, 0xE366
addi $9, $0, 1
addi $10, $0, 0x2020
addi $20, $0, 0x2500
addi $21, $0, 0x2000
addi $22, $0, 0x2004
addi $30, $0, 0x2008
addi $23, $0, 0
addi $26, $0, 0
addi $28, $0, 0
addi $29, $0, 10

loop_part_a:

multu $9, $8
mfhi $11
mflo $12
xor $13, $12, $11

multu $13, $8
mfhi $11
mflo $12
xor $13, $12, $11

multu $13, $8
mfhi $11
mflo $12
xor $13, $12, $11

multu $13, $8
mfhi $11
mflo $12
xor $13, $12, $11

multu $13, $8
mfhi $11
mflo $12
xor $13, $12, $11

sw $13, 0($20)
lhu $14, 0($20)
lhu $15, 2($20)

xor $16, $15, $14
sh $16, 4($20)
lbu $17, 4($20)
lbu $18, 5($20)
xor $19, $17, $18

slt $24, $23, $19
beq $24, 1, new_max
back_to_loop:

j Check
back_again:

sw $19, 0($10)
addi $10, $10, 4

addi $9, $9, 1
bne $9, 101, loop_part_a

sw $28, 0($30)

j end

new_max:
sw $10, 0($21)
sw $19, 0($22)
addi $23, $19, 0
j back_to_loop

Check:
addi $27, $19, 0
again_check:
and  $25, $27, 1
beq $25, $0, next_0
bne $25, $0, next_1

next_1:
srl $27, $27, 1
addi $26, $26, 1
beq $26, 5, got_one
bne $27, $0, again_check
j again_check

next_0:
srl $27, $27, 1
addi $26, $0, 0
bne $27, $0, again_check
j back_again

got_one:
addi $28, $28, 1
addi $26, $0, 0
j back_again


end:
