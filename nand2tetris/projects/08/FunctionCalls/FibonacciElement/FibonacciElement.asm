@256
D=A
@SP
M=D
// CALL SYS.INIT 0
@Return0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@SYS.INIT
0;JMP
(Return0)
// FUNCTION MAIN.FIBONACCI 0
(MAIN.FIBONACCI)
// PUSH ARGUMENT 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH CONSTANT 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// LT
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@TRUE0
D;JLT
@SP
A=M-1
M=0
@END0
0;JMP
(TRUE0)
@SP
A=M-1
M=-1
(END0)
// IF-GOTO IF_TRUE
@SP
M=M-1
A=M
D=M
@MAIN.FIBONACCI$IF_TRUE
D;JNE
// GOTO IF_FALSE
@MAIN.FIBONACCI$IF_FALSE
0;JMP
(MAIN.FIBONACCI$IF_TRUE)
// PUSH ARGUMENT 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// RETURN
@LCL
D=M
@FRAME
M=D
@5
D=A
@FRAME
D=M-D
A=D
D=M
@RET
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FRAME
M=M-1
A=M
D=M
@THAT
M=D
@FRAME
M=M-1
A=M
D=M
@THIS
M=D
@FRAME
M=M-1
A=M
D=M
@ARG
M=D
@FRAME
M=M-1
A=M
D=M
@LCL
M=D
@RET
A=M
0;JMP
(MAIN.FIBONACCI$IF_FALSE)
// PUSH ARGUMENT 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH CONSTANT 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// SUB
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
// CALL MAIN.FIBONACCI 1
@MAIN.FIBONACCI$Return1
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@MAIN.FIBONACCI
0;JMP
(MAIN.FIBONACCI$Return1)
// PUSH ARGUMENT 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH CONSTANT 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// SUB
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
// CALL MAIN.FIBONACCI 1
@MAIN.FIBONACCI$Return2
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@MAIN.FIBONACCI
0;JMP
(MAIN.FIBONACCI$Return2)
// ADD
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M
// RETURN
@LCL
D=M
@FRAME
M=D
@5
D=A
@FRAME
D=M-D
A=D
D=M
@RET
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FRAME
M=M-1
A=M
D=M
@THAT
M=D
@FRAME
M=M-1
A=M
D=M
@THIS
M=D
@FRAME
M=M-1
A=M
D=M
@ARG
M=D
@FRAME
M=M-1
A=M
D=M
@LCL
M=D
@RET
A=M
0;JMP
// FUNCTION SYS.INIT 0
(SYS.INIT)
// PUSH CONSTANT 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// CALL MAIN.FIBONACCI 1
@SYS.INIT$Return3
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@MAIN.FIBONACCI
0;JMP
(SYS.INIT$Return3)
(SYS.INIT$WHILE)
// GOTO WHILE
@SYS.INIT$WHILE
0;JMP
