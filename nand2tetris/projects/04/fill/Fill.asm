// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
	@SCREEN
	D=A // D=endereço da tela
	@pixels
	M=D // pixels=endereço da tela
	@KBD
	D=M // D= tecla apertada

	@LOOP_BLACK
	D;JNE // Se tecla apertada goto loop_black

	

	(LOOP_WHITE)
		@KBD
		D=A // D=endereço de keyboard
		@pixels
		D=D-M // D=endereço de keyboard - endereço de pixels
		@START
		D;JLE // se pixels for maior q kbd pula pro inicio

		@pixels
		A=M 
		M=0 // 16 pixels ficam brancos
		@pixels
		M=M+1 // endereço dos pixels anda
		@LOOP_WHITE
		0;JMP // volta pro loop branco

	(LOOP_BLACK)
		@KBD
		D=A // D=endereço de keyboard
		@pixels
		D=D-M // D=endereço de keyboard - endereço de pixels
		@START
		D;JLE // se pixels for maior q kbd pula pro inicio

		@pixels
		A=M 
		M=-1 // 16 pixels ficam pretos
		@pixels
		M=M+1 // endereço dos pixels anda
		@LOOP_BLACK
		0;JMP // volta pro loop preto