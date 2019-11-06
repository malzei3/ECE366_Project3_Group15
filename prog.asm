init r2, 0 #r2 is set to 0		PC = 0
subi r2, 3
subi r2, 3 #r2 is now 250(0xFA) since by subtracting 6 from 0 it underflows.

init r0, 4 # Sets r0 to 5 (Keeps track of where in the loop we are) (We will do a seperate loop for values 1 - 5)

init r1, 4 # Sets r1 to 5 (This will store the hash result)

hashing:
hash r1, r2 # Hashes r1 and r2, r1 is set as result.

sb r1, r0	# Stores the hash result to the appropriate memory location

addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

bezR0 hashing	# When r0 == 0 the loop will end

#We still need to store Hash results in mem[256] - mem[260]

init r0, 1
init r1, 1

hash r1, r2

saal r1, r0
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

hash r1, r2

saal r1, r0
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

hash r1, r2

saal r1, r0
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

hash r1, r2

saal r1, r0
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0







