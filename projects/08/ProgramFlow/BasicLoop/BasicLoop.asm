@0
D=A
@R0
A=M
M=D
@R0
M=M+1
@R0
A=M-1
D=M
@top_val
M=D
@R0
M=M-1
@0
D=A
@R1
A=M+D
D=A
@top_to
M=D
@top_val
D=M
@top_to
A=M
M=D
(LOOP_START)
@0
D=A
@R2
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1
@0
D=A
@R1
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
A=M-1
D=M
A=A-1
M=M+D
@R0
M=M-1
@R0
A=M-1
D=M
@top_val
M=D
@R0
M=M-1
@0
D=A
@R1
A=M+D
D=A
@top_to
M=D
@top_val
D=M
@top_to
A=M
M=D
@0
D=A
@R2
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1
@1
D=A
@R0
A=M
M=D
@R0
M=M+1
@R0
A=M-1
D=M
A=A-1
M=M-D
@R0
M=M-1
@R0
A=M-1
D=M
@top_val
M=D
@R0
M=M-1
@0
D=A
@R2
A=M+D
D=A
@top_to
M=D
@top_val
D=M
@top_to
A=M
M=D
@0
D=A
@R2
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
A=M-1
D=M
@top_val
M=D
@R0
M=M-1
@top_val
D=M
@LOOP_START
D;JNE
@0
D=A
@R1
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1
(END)
@END
0;JMP