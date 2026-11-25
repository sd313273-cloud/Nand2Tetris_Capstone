# Nand to Tetris I - Capstone Project: Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCNTC301)  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Shubham Dhar Dwivedi  
**Roll Number:** 2501730420  
**Personal Parameter (K):** `20` (Last two digits of Roll Number)

---

## 📌 Project Overview
This repository contains the complete implementation for the Nand to Tetris I Capstone Project:
1. **Hack Computer Hardware (HDL):** `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`.
2. **Two-Pass Hack Assembler (Python 3):** `assembler.py` with custom extra feature for $K \bmod 3 = 2$ (Duplicate label declaration warning) and symbol table export.
3. **Interactive Box Program (Hack Assembly):** `Box.asm` compiled to `Box.hack` which continuously polls the keyboard (`RAM[24576]`) and renders a 16-pixel wide, 20-row tall black rectangular box at Screen Row 20 while any key is pressed, erasing it when released.
4. **Validation Tool:** `compare.py` testing against official benchmark files (`Add`, `Max`, `Rect`, `Pong`).

---

## 📐 Personal Parameter Calculations (K = 20)

| Parameter | Formula | Value |
| :--- | :--- | :--- |
| **Roll Number** | `2501730420` | Last two digits = **20** |
| **K** | Personal Number | **20** |
| **Starting Screen Row** | Row $K$ | **Row 20** (Rows 20 to 39) |
| **Box Height** | Fixed specification | **20 screen rows** |
| **Box Width** | $16 \times ((K \bmod 4) + 1)$ | $20 \bmod 4 = 0 \implies 16 \times (0 + 1) =$ **16 pixels** |
| **Words per Row** | $\text{Width} / 16$ | **1 word (16-bit memory register)** |
| **Starting Screen Address** | $\text{SCREEN} + 32 \times K$ | $16384 + 32 \times 20 =$ **17024** |
| **Last Row Address** | $16384 + 32 \times 39$ | $16384 + 1248 =$ **17632** |
| **Extra Assembler Feature** | $K \bmod 3$ | $20 \bmod 3 = 2 \implies$ **Print warning if same label is written twice** |

---

## 📁 Repository Structure

```text
Capstone_nand/
├── README.md                          # Top-level project documentation
└── capstone/
    ├── assembler.py                   # Two-pass Hack Assembler in Python 3
    ├── Box.asm                        # Fully commented Hack Assembly source
    ├── Box.hack                       # Assembled 16-bit binary machine code
    ├── symbols.txt                    # Symbol table export
    ├── compare.py                     # Machine code comparison testing tool
    ├── CPU.hdl                        # Hack CPU implementation
    ├── Memory.hdl                     # Memory-mapped RAM, Screen, Keyboard
    ├── Computer.hdl                   # Top-level Hack Computer chip
    ├── NOTES.md                       # Comprehensive study and viva preparation guide
    ├── visual_preview.html            # Interactive in-browser Hack screen simulator
    ├── run_assembler.bat              # One-click assembler batch launcher
    ├── run_tests.bat                  # One-click test suite launcher
    └── tests/                         # Official benchmark programs (Add, Max, Rect, Pong)
```

---

## 🚀 How to Run and Test

### 1. Assemble `Box.asm`
```bash
cd capstone
python assembler.py Box.asm
```
* Generates `Box.hack` (53 instructions).
* Generates `symbols.txt` (6 labels, 5 variables).

### 2. Run Test Comparisons
```bash
python compare.py
```
* **Output:**
  * `Add.hack` : **PASSED** (100% bit-for-bit match)
  * `Max.hack` : **PASSED** (100% bit-for-bit match)
  * `Rect.hack`: **PASSED** (100% bit-for-bit match)
  * `Pong.hack`: **PASSED** (100% bit-for-bit match, all 27,483 instructions)

### 3. Run the Box Program
* **Option A (Interactive Browser Simulator):** Open `capstone/visual_preview.html` in Chrome/Edge, hold down any key, and watch the box draw in real-time.
* **Option B (Official CPU Emulator):**
  1. Open `CPUEmulator.bat` from your Nand2Tetris tools suite.
  2. Load `capstone/Box.hack`.
  3. Set speed to Fast / No display changes and click Run (`>>`).
  4. Click the keyboard icon and press any key to display the box!

---

## 🎓 Viva Modification Cheat Sheet
See [`capstone/NOTES.md`](capstone/NOTES.md) for detailed line-by-line viva instructions on how to move the box up/down, change width/height, or invert colors live.
