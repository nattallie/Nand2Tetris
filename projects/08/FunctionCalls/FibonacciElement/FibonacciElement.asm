@256
D=A
@R0
M=D
@sys.init_ret_0
D=A
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@5
A=-A
D=A
@R0
D=M+D
@R2
M=D
@0
D=A
@R0
D=M+D
@R1
M=D
@SYS.INIT
0;JMP
(sys.init_ret_0)
(MAIN.FIBONACCI)
@0
D=A
@main.fibonacci_num_loc
M=D
@MAIN.FIBONACCI_LOCAL_LOOP_END
D;JLE
(MAIN.FIBONACCI_LOCAL_LOOP)
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
@main.fibonacci_num_loc
M=M-1
D=M
@MAIN.FIBONACCI_LOCAL_LOOP
D;JGT
(MAIN.FIBONACCI_LOCAL_LOOP_END)
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
@2
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
A=M-1
D=M
M=0
@NOT_LESS_0
D;JGE
@1
D=-A
@R0
A=M-1
M=D
(NOT_LESS_0)
@R0
A=M-1
D=M
@top_val
M=D
@R0
M=M-1
@top_val
D=M
@IF_TRUE
D;JNE
@IF_FALSE
0;JMP
(IF_TRUE)
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
D=A
@frame
M=D
@5
A=-A
D=A
@frame
A=M+D
A=M
D=A
@ret_main.fibonacci_1
M=D
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
@1
D=A
@R2
A=M+D
D=A
@R0
M=D
@1
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R4
M=D
@2
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R3
M=D
@3
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R2
M=D
@4
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R1
M=D
@ret_main.fibonacci_1
A=M
0;JMP
(IF_FALSE)
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
@2
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
@main.fibonacci_ret_2
D=A
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@6
A=-A
D=A
@R0
D=M+D
@R2
M=D
@0
D=A
@R0
D=M+D
@R1
M=D
@MAIN.FIBONACCI
0;JMP
(main.fibonacci_ret_2)
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
@main.fibonacci_ret_3
D=A
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@6
A=-A
D=A
@R0
D=M+D
@R2
M=D
@0
D=A
@R0
D=M+D
@R1
M=D
@MAIN.FIBONACCI
0;JMP
(main.fibonacci_ret_3)
@R0
A=M-1
D=M
A=A-1
M=M+D
@R0
M=M-1
@0
D=A
@R1
A=M+D
D=A
@frame
M=D
@5
A=-A
D=A
@frame
A=M+D
A=M
D=A
@ret_main_4
M=D
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
@1
D=A
@R2
A=M+D
D=A
@R0
M=D
@1
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R4
M=D
@2
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R3
M=D
@3
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R2
M=D
@4
A=-A
D=A
@frame
A=M+D
A=M
D=A
@R1
M=D
@ret_main_4
A=M
0;JMP
(SYS.INIT)
@0
D=A
@sys.init_num_loc
M=D
@SYS.INIT_LOCAL_LOOP_END
D;JLE
(SYS.INIT_LOCAL_LOOP)
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
@sys.init_num_loc
M=M-1
D=M
@SYS.INIT_LOCAL_LOOP
D;JGT
(SYS.INIT_LOCAL_LOOP_END)
@4
D=A
@R0
A=M
M=D
@R0
M=M+1
@main.fibonacci_ret_0
D=A
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@6
A=-A
D=A
@R0
D=M+D
@R2
M=D
@0
D=A
@R0
D=M+D
@R1
M=D
@MAIN.FIBONACCI
0;JMP
(main.fibonacci_ret_0)
(WHILE)
@WHILE
0;JMP
(END)
@END
0;JMP
