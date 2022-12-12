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
  @KBD 
  D = M
  @BLACK
  D;JNE
  @WHITE 
  D;JEQ

(BLACK)
  @color 
  M = -1
  @PAINT
  0;JMP

(WHITE)
  @color
  M = 0
  @PAINT
  0;JMP

(PAINT)
  @SCREEN 
  D = A 
  @pixel 
  M = D 
  @rownumber 
  M = 1
  @ROWS
  0;JMP

(ROWS)
  @rownumber 
  D = M
  @256
  D = D - A
  @START 
  D;JGT
  @colnumber 
  M = 1
  @COLS 
  0;JMP
  

(COLS)
  @colnumber 
  D = M
  @32 
  D = D - A
  @ROWINC 
  D;JGT

  @color
  D = M
  @pixel 
  A = M 
  M = D

  @pixel 
  M = M + 1

  @colnumber 
  M = M + 1

  @COLS 
  0;JMP

(ROWINC) 
  @rownumber
  M = M + 1
  @ROWS 
  0;JMP