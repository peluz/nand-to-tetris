// FUNCTION SYS.INIT 0
(SYS.INIT)
// PUSH CONSTANT 4000	
@4000	
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP POINTER 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// PUSH CONSTANT 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP POINTER 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// CALL SYS.MAIN 0
@SYS.INIT$Return0
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
@SYS.MAIN
0;JMP
(SYS.INIT$Return0)
// POP TEMP 1
@1
D=A
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
(SYS.INIT$LOOP)
// GOTO LOOP
@SYS.INIT$LOOP
0;JMP
// FUNCTION SYS.MAIN 5
(SYS.MAIN)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
// PUSH CONSTANT 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP POINTER 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// PUSH CONSTANT 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP POINTER 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// PUSH CONSTANT 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP LOCAL 1
@1
D=A
@LCL
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// PUSH CONSTANT 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP LOCAL 2
@2
D=A
@LCL
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// PUSH CONSTANT 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP LOCAL 3
@3
D=A
@LCL
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// PUSH CONSTANT 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// CALL SYS.ADD12 1
@SYS.MAIN$Return1
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
@SYS.ADD12
0;JMP
(SYS.MAIN$Return1)
// POP TEMP 0
@0
D=A
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// PUSH LOCAL 0
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH LOCAL 1
@1
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH LOCAL 2
@2
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH LOCAL 3
@3
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH LOCAL 4
@4
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ADD
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M
// ADD
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M
// ADD
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M
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
// FUNCTION SYS.ADD12 0
(SYS.ADD12)
// PUSH CONSTANT 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP POINTER 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// PUSH CONSTANT 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// POP POINTER 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
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
// PUSH CONSTANT 12
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
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
