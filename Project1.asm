init r2, 7
sll r2, 3
sll r2, 2
addi r2, 3
addi r2, 3
addi r2, 3
addi r2, 3
addi r2, 3
addi r2, 3
addi r2, 3
addi r2, 3
addi r2, 2

init r0, 8
sll r0, 3
sll r0, 2

hashing:
hash r3, r2, r0

addi r0, 3
sb r3, r1
sub r0, 3
sub r0, 1

bezR0 hashing



