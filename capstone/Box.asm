// Box.asm - Hack Assembly program for Roll Number K=20 (Shubham Dhar Dwivedi - 2501730420)
// Box starts at Screen Row 20, is 20 rows tall (rows 20 to 39)
// Width = 1 word (16 pixels), moving down 32 words per row
// If KBD != 0: draw black box (-1 in each word)
// If KBD == 0: clear box (0 in each word)
// Simple nested loop (outer: 20 rows, inner: 1 word)
(MAIN_LOOP)          // Main loop: polls keyboard and draws/clears the box continuously
    @KBD             // Load address 24576 (memory-mapped keyboard register) into A
    D=M              // Read current keyboard key code into D register
    @SET_WHITE       // Load target jump address for SET_WHITE label into A
    D;JEQ            // If D == 0 (no key pressed), jump to SET_WHITE
    @color           // Load address of variable 'color' into A
    M=-1             // Set color = -1 (all 16 bits 1 = 16 black pixels per word)
    @START_DRAW      // Load target jump address for START_DRAW label into A
    0;JMP            // Unconditional jump to START_DRAW
(SET_WHITE)          // Branch when no key is pressed: set box color to white/clear
    @color           // Load address of variable 'color' into A
    M=0              // Set color = 0 (all 16 bits 0 = 16 white pixels per word)
(START_DRAW)         // Initialize drawing coordinates and loop counters
    @17024           // Screen start address for row 20: 16384 + (32 * 20) = 17024
    D=A              // Put start address 17024 into D register
    @row_addr        // Load address of variable 'row_addr' into A
    M=D              // Initialize row_addr = 17024 (base address of current row)
    @20              // Box height = 20 rows (row 20 to row 39)
    D=A              // Put row count 20 into D register
    @row_count       // Load address of variable 'row_count' into A
    M=D              // Initialize row_count = 20
(ROW_LOOP)           // Outer loop: iterate through all 20 rows of the box
    @row_count       // Load address of variable 'row_count' into A
    D=M              // Put remaining rows count into D register
    @MAIN_LOOP       // Load target jump address for MAIN_LOOP into A
    D;JLE            // If row_count <= 0, all 20 rows are drawn; loop back to poll keyboard
    @row_addr        // Load address of variable 'row_addr' into A
    D=M              // Put current row starting address into D register
    @col_addr        // Load address of variable 'col_addr' into A
    M=D              // Initialize col_addr = row_addr (start pointer for inner loop)
    @1               // Box width = 1 word per row (1 * 16 = 16 pixels wide)
    D=A              // Put word count 3 into D register
    @col_count       // Load address of variable 'col_count' into A
    M=D              // Initialize col_count = 3
(COL_LOOP)           // Inner loop: fill 3 consecutive 16-bit words in current row
    @col_count       // Load address of variable 'col_count' into A
    D=M              // Put remaining words count into D register
    @END_ROW         // Load target jump address for END_ROW into A
    D;JLE            // If col_count <= 0, row is completed; jump to END_ROW
    @color           // Load address of variable 'color' into A
    D=M              // Put color value (-1 or 0) into D register
    @col_addr        // Load address of variable 'col_addr' into A
    A=M              // Set memory address pointer to current screen word (A = col_addr)
    M=D              // Write color into screen memory at RAM[col_addr]
    @col_addr        // Load address of variable 'col_addr' into A
    M=M+1            // Advance word pointer to next horizontal word (col_addr = col_addr + 1)
    @col_count       // Load address of variable 'col_count' into A
    M=M-1            // Decrement inner loop counter (col_count = col_count - 1)
    @COL_LOOP        // Load target jump address for COL_LOOP into A
    0;JMP            // Jump back to fill next word of the current row
(END_ROW)            // End of inner loop: move to the next screen row
    @32              // Screen width in memory words = 32 words per row (512 / 16)
    D=A              // Put 32 into D register
    @row_addr        // Load address of variable 'row_addr' into A
    M=D+M            // Advance row_addr by 32 words to reach next row (row_addr += 32)
    @row_count       // Load address of variable 'row_count' into A
    M=M-1            // Decrement outer loop counter (row_count = row_count - 1)
    @ROW_LOOP        // Load target jump address for ROW_LOOP into A
    0;JMP            // Jump back to draw the next row of the box
