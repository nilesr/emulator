## small assembly interpreter

Made for fun, put assembly code in the file called "instructions" and it will run it

The example "instructions" file I wrote contains three different ways of calculating the factorial of a number (iteratively, recursively and tail call recursively) and a tail call recursive hailstone implementation. It calculates the number of steps to hailstone 73 (0x49), 6!, 5! and 4! and puts them on ax, bx, cx and dx, then exits. The correct answers should be 115, 720, 120 and 24

The registers are ax, bx, cx and dx. The stack pointers are sp and sb (sb is unused), instruction pointer is ip and flags register is fl

The stack starts at zero and grows up, the maximum address in ram is 1023. sp points to the item after the top item on the stack, but if you just use push and pop you won't have to worry about it. 

The lea instruction takes a register that holds an address and a register to put the contents of that address into, leai takes a literal address and loads it into the register specified by the second argument. sea and seai both take their arguments in that order as well

The call function is just the jmp instruction but first it pushes the instruction pointer to the stack. The ret instruction just pops an instruction pointer and jumps to it. 

test and testi set three bits on the flags register, 001 if they are equal, 010 for greater than and 100 for less than. The conditional jumps include je, jne, jl, jg, jle and jge

At any point you can use the debug instruction to print out the contents of the registers and the first ten values in ram, or the abort instruction to debug then exit.

Registers are callee-preserved.

All integer literals are hexadecimal and start with 0x

Comments start with `#` but any unrecognized instruction is treated as a comment
