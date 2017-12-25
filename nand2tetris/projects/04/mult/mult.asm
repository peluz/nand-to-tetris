// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@i
	M=0 // set i to 0
	@R2
	M=0 // set R2 to 0

(LOOP)
	@i
	D=M // D=i
	@R1
	D=D-M // D=i-R1
	@END
	D;JGE // if i >= R1 goto end

	@R2
	D=M // D=R2
	@R0
	D=D+M // R2+=R0
	@R2
	M=D // R2=D
	@i
	M=M+1 // i++
	@LOOP
	0;JMP // goto loop

(END)
	@END
	0;JMP // Finish execution