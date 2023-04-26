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
    @8192
    D=A
    @cnt    //cnt equals 8192
    M=D    
(MAIN)
    @R0     //R0 is current counter
    M=0
    @KBD // ind of keyboard interrupt
    D=M
    @CLEAR
    D;JEQ
    @PAINT
    D;JNE
(CLEAR)
    @R0     // D=current counter
    D=M     
    @SCREEN
    A=D+A
    D=M     // D=current pixel state
    @MAIN
    D;JEQ
    @R0
    D=M     
    @cnt
    D=M-D   // D=num_words to clear
    @MAIN
    D;JEQ
    @R0
    D=M
    @SCREEN
    A=A+D
    M=0
    @R0
    M=M+1
    @CLEAR
    0;JMP
(PAINT)
    @R0     // D=current counter
    D=M     
    @cnt
    D=M-D   // D=num_words to clear
    @MAIN
    D;JEQ
    @R0
    D=M
    @SCREEN
    A=A+D
    D=0
    M=!D
    @R0
    M=M+1
    @PAINT
    0;JMP
