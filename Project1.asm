init r2, 250
init r0, 255

hashing:
hash r3, r2, r0

addi r0, 3
sb r3, r1
sub r0, 3
dein r0, 1

bezR0 hashing



