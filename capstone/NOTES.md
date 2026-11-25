# Nand to Tetris I - Capstone Project Notes & Viva Preparation Guide

**Course:** Nand to Tetris – I (ETCNTC301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Shubham Dhar Dwivedi  
**Roll Number:** 2501730420  
**Personal Parameter (K):** `20` (Last two digits of roll number)

---

## 1. Parameter Calculations (Based on K = 20)

| Parameter | Formula | Calculated Value |
| :--- | :--- | :--- |
| **K** | Last 2 digits of Roll Number | **20** |
| **Starting Row** | Row $K$ | **Row 20** (Rows 20 to 39) |
| **Box Height** | Fixed requirement | **20 screen rows** |
| **Box Width** | $16 \times ((K \bmod 4) + 1)$ | $20 \bmod 4 = 0 \implies 16 \times (0 + 1) =$ **16 pixels** |
| **Words per Row** | $\text{Width} / 16$ | **1 word (16-bit register) per row** |
| **First Row Base Address** | $\text{SCREEN} + 32 \times K$ | $16384 + 32 \times 20 = 16384 + 640 =$ **17024** |
| **Last Row Base Address** | $16384 + 32 \times 39$ | $16384 + 1248 =$ **17632** |
| **Extra Assembler Feature** | $K \bmod 3$ | $20 \bmod 3 = 2 \implies$ **Print warning if same label is written twice** |

---

## 2. Understanding Hack Screen Memory Architecture

* **Screen Dimensions:** 256 rows high $\times$ 512 pixels wide.
* **Screen Base Address:** `16384` (`0x4000`).
* **Words per Row:** 512 pixels $/ 16$ bits per word $= 32$ 16-bit memory words per row.
* **Row Address Formula:** $\text{Address} = 16384 + 32 \times \text{row}$.
* **Pixel Colors:**
  * In Hack, `0` is binary `0000000000000000` (all 16 pixels **white/clear**).
  * `-1` is two's complement binary `1111111111111111` (all 16 pixels **black**).
* **Memory-Mapped Keyboard:** Address `24576` (`KBD`).
  * If no key is pressed, `RAM[24576] == 0`.
  * If any key is pressed, `RAM[24576] != 0` (holds the ASCII key code).

---

## 3. How the Files Work

### A. `assembler.py` (Two-Pass Python Assembler)
The assembler translates human-readable assembly instructions (`.asm`) into 16-bit machine instructions (`.hack`).

1. **Pass 1 (Label Collection & Duplicate Detection):**
   * Reads the file line by line.
   * Strips out comments (`// ...`) and whitespace.
   * Keeps a running counter of ROM instructions (`rom_address`).
   * When it sees a label like `(MAIN_LOOP)`:
     * **Feature for $K \bmod 3 = 2$:** Checks if `MAIN_LOOP` has already been defined in `user_labels`. If yes, prints a clear warning showing the line number and previous address.
     * Records `symbol_table["MAIN_LOOP"] = rom_address`.
2. **Pass 2 (Binary Code Generation):**
   * **A-Instructions (`@value` or `@symbol`):**
     * If numbers (e.g., `@17024`), converts directly to 15-bit binary preceded by `0`.
     * If predefined symbol (e.g., `@KBD`, `@SCREEN`, `@R0`), looks up its standard address.
     * If a label from Pass 1, looks up its ROM address.
     * If a new variable (e.g., `@color`, `@row_addr`), assigns it the next available RAM address starting from **RAM 16** (`16, 17, 18, ...`).
   * **C-Instructions (`dest=comp;jump`):**
     * Formatted as `111 a c1..c6 d1..d3 j1..j3` (16 bits).
     * Looks up `comp` (7 bits), `dest` (3 bits), and `jump` (3 bits) in lookup tables.
3. **Symbols Export:**
   * At the end of assembly, writes `symbols.txt` containing user-defined labels and variables with their assigned addresses (e.g., `MAIN_LOOP = 0`, `color = 16`).

---

### B. `Box.asm` (Screen Drawing Program)
Contains an infinite loop using clean nested loops:
* **Keyboard Polling:**
  * Checks `@KBD`. If `D == 0`, sets `color = 0` (clear).
  * If `D != 0`, sets `color = -1` (black).
* **Outer Loop (`ROW_LOOP`):**
  * Runs for `row_count = 20` iterations.
  * Starts at `row_addr = 17024` (Row 20).
  * Advances down by adding 32 words each row (`row_addr += 32`).
* **Inner Loop (`COL_LOOP`):**
  * Runs for `col_count = 3` words (16 pixels).
  * Writes `color` to `RAM[col_addr]`.
  * Advances horizontally to the next word (`col_addr += 1`).
* **Comment on Every Line:** Every single line has a clear inline comment.

---

### C. `compare.py` (Validation Tool)
* Automatically verifies generated `.hack` files against official reference `.hack` files line by line.
* Tested and passed 100% on:
  * `Add.asm` (6/6 instructions matched)
  * `Max.asm` (16/16 instructions matched)
  * `Rect.asm` (25/25 instructions matched)
  * `Pong.asm` (27,483/27,483 instructions matched)

---

## 4. Live Viva Modification Cheat Sheet (Crucial for 5-Min Viva!)

During the viva, the examiner will likely ask you:  
*"Make a small change to move the box, change its size, or change its color."*

Here are the **exact lines** in `Box.asm` to change:

### 1. Move the Box Down or Up (Change Starting Row)
* **Target Line:** Line 16
  ```hack
  @17024           // Screen start address for row 20: 16384 + (32 * 20) = 17024
  ```
* **How to change:**
  * **To move down to row 120:**  
    Formula: $16384 + (32 \times 120) = 16384 + 3840 = 20224$.  
    Change `@17024` to `@20224`.
  * **To move up to row 10 (near top):**  
    Formula: $16384 + (32 \times 10) = 16384 + 320 = 16704$.  
    Change `@17024` to `@16704`.

---

### 2. Change the Box Width (Horizontal Size)
* **Target Line:** Line 32
  ```hack
  @3               // Box width = 1 word per row (3 * 16 = 16 pixels wide)
  ```
* **How to change:**
  * **To make it narrower (16 pixels / 1 word):**  
    Change `@3` to `@1`.
  * **To make it wider (64 pixels / 4 words):**  
    Change `@3` to `@4`.
  * **To make it 128 pixels (8 words):**  
    Change `@3` to `@8`.

---

### 3. Change the Box Height (Vertical Size)
* **Target Line:** Line 20
  ```hack
  @20              // Box height = 20 rows (row 20 to row 39)
  ```
* **How to change:**
  * **To make it 40 rows tall:**  
    Change `@20` to `@40`.
  * **To make it a square (16 pixels high = 48 rows):**  
    Change `@20` to `@48`.

---

### 4. Invert Colors (Draw White When Pressed, Black When Released)
* **Target Lines:** Line 10 and Line 14
  * In `Box.asm`:
    ```hack
    // Line 10 (when key is pressed):
    M=-1            // Set color = -1 (black)
    ...
    // Line 14 (when key is released):
    M=0             // Set color = 0 (white)
    ```
* **How to change:**
  * Swap them: make Line 10 `M=0` and Line 14 `M=-1`.
  * Now the screen will be black by default, and pressing a key will carve out a white box!

---

### 5. Move the Box Horizontally (Away from the Left Edge)
* **Target Line:** Line 16
  * Each word offset moves the box 16 pixels to the right.
  * E.g., to place the box in the horizontal middle of the row (offset 14 words):  
    Add 14 to starting address: $17024 + 14 = 19534$.  
    Change `@17024` to `@19534`.

---

## 5. Likely Viva Questions & Ready Answers

**Q1: Why is an assembler built in two passes instead of one?**  
> *"In assembly, code can jump forward to a label that hasn't been defined yet (forward reference), such as `@OUTPUT_FIRST` before `(OUTPUT_FIRST)` appears. In Pass 1, we scan the entire program to map all label names to their exact ROM addresses. In Pass 2, with all label addresses known, we can translate every instruction into binary without errors."*

**Q2: Why do user variables start at RAM address 16?**  
> *"Addresses 0 to 15 are reserved for the 16 virtual registers (`R0` through `R15`, as well as `SP`, `LCL`, `ARG`, `THIS`, `THAT`). Therefore, general-purpose user variables start immediately after them at RAM[16]."*

**Q3: Why do we add 32 to move down one row on the screen?**  
> *"The Hack screen has a resolution of $512 \times 256$ pixels. Each memory word is 16 bits wide, so one horizontal line of 512 pixels requires $512 / 16 = 32$ memory words. Thus, moving down one row requires advancing 32 memory addresses."*

**Q4: How does memory-mapped I/O work in the Hack computer?**  
> *"The Hack computer does not use special I/O instructions like `IN` or `OUT`. Instead, the screen memory (`16384` to `24575`) and keyboard register (`24576`) are mapped directly into the CPU's memory address space. Reading or writing to those memory addresses automatically reads the keyboard or updates the screen pixels."*

**Q5: What is the extra feature implemented in your assembler?**  
> *"Since my roll number ends in 20, $20 \bmod 3 = 2$. My extra feature detects and prints a clear warning if a user writes the same label twice in their code, reporting the duplicate declaration and line number."*

---

## 6. How to Re-Assemble and Test After Making Changes

To re-assemble after modifying `Box.asm`:
```cmd
cd capstone
python assembler.py Box.asm
```
This updates:
1. `Box.hack` (ready to load into CPU Emulator)
2. `symbols.txt` (shows updated symbol addresses)

To verify the test suite anytime:
```cmd
python compare.py
```
*(All 4 tests: Add, Max, Rect, Pong will report `PASSED`).*
