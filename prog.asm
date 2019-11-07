subi r2, 3
subi r2, 3 #r2 is now 250(0xFA) since by subtracting 6 from 0 it underflows.

init r0, 4 # Sets r0 to 4 (Keeps track of where in the loop we are)

init r1, 1 # Sets r1 to 1 (This will store the hash result)

hashing:
hash r1, r2 # Hashes r1 and r2, r1 is set as result.
minc r1

sb r1, r0	# Stores the hash result to the appropriate memory location

addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0
sub r1, 3

bnezR0 hashing	# When r0 == 0 the loop will end

#We still need to store Hash results in mem[256] - mem[259]

init r0, 1
subi r0, 3
subi r0, 1 # r0 = 253
init r1, 1
subi r1, 3
subi r1, 1 # r1 = 253

hash r1, r2
minc r1

saal r1, 1
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

hash r1, r2
minc r1

saal r1, 2
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

hash r1, r2
minc r1

saal r1, 3
addi r0, 1 	# r0 increments 
cpy r1, r0	# r1 is set equal to r0

end








