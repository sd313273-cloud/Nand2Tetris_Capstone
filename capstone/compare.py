"""
compare.py - Hack Machine Code (.hack) Comparison Tool
Compares student assembler output with official Nand2Tetris .hack files.

Usage:
    python compare.py                       # Runs comparison on all available test files
    python compare.py Add                   # Compares Add.hack with Add_official.hack
    python compare.py my.hack official.hack  # Compares any two specific files
"""

import sys
import os

def compare_hack_files(actual_path, expected_path, test_name=""):
    """
    Compares two .hack files line by line.
    Returns (is_match, total_lines, diff_list).
    """
    name_str = f" [{test_name}]" if test_name else ""
    print(f"\n=======================================================")
    print(f"Comparing{name_str}:")
    print(f"  Actual   : {actual_path}")
    print(f"  Expected : {expected_path}")
    print(f"=======================================================")

    if not os.path.exists(actual_path):
        print(f"[FAIL] Output file not found: {actual_path}")
        return False, 0, [f"Missing file: {actual_path}"]

    if not os.path.exists(expected_path):
        print(f"[SKIP] Official comparison file not found: {expected_path}")
        print(f"       -> Please supply the official file to test against.")
        return None, 0, []

    with open(actual_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    with open(expected_path, "r", encoding="utf-8") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    total_actual = len(actual_lines)
    total_expected = len(expected_lines)

    diffs = []
    max_len = max(total_actual, total_expected)

    for i in range(max_len):
        act = actual_lines[i] if i < total_actual else "<MISSING - EOF>"
        exp = expected_lines[i] if i < total_expected else "<EXTRA LINE>"
        if act != exp:
            diffs.append((i + 1, act, exp))

    if not diffs:
        print(f"[PASS] PERFECT MATCH! All {total_expected} instructions match exactly.")
        return True, total_expected, []
    else:
        print(f"[FAIL] Found {len(diffs)} difference(s) (Total lines: actual={total_actual}, expected={total_expected}):")
        # Print first 10 differences
        for line_num, act, exp in diffs[:10]:
            print(f"  Line {line_num:4d}:")
            print(f"    Your Output    : {act}")
            print(f"    Official Match : {exp}")
        if len(diffs) > 10:
            print(f"  ... and {len(diffs) - 10} more differences.")
        return False, total_expected, diffs


def run_all_tests():
    """
    Runs automated comparisons for Add, Max, Rect, and Pong.
    Searches both current directory and tests/ directory.
    """
    targets = ["Add", "Max", "Rect", "Pong"]
    results = {}

    search_dirs = [".", "tests", "capstone/tests", "capstone"]

    for name in targets:
        # Locate actual .hack
        act_path = None
        for d in search_dirs:
            p = os.path.join(d, f"{name}.hack")
            if os.path.exists(p):
                act_path = p
                break

        # Locate official .hack (supports Name_official.hack, official/Name.hack, etc.)
        exp_path = None
        possible_exp = [
            f"{name}_official.hack",
            f"{name}.cmp",
            f"official_{name}.hack",
            os.path.join("official", f"{name}.hack"),
            os.path.join("tests", f"{name}_official.hack"),
            os.path.join("tests", f"{name}.cmp"),
        ]
        for candidate in possible_exp:
            for d in ["."] + search_dirs:
                p = os.path.join(d, candidate)
                if os.path.exists(p):
                    exp_path = p
                    break
            if exp_path:
                break

        if not act_path:
            # Try assembling if .asm is found
            asm_found = None
            for d in search_dirs:
                p = os.path.join(d, f"{name}.asm")
                if os.path.exists(p):
                    asm_found = p
                    break
            if asm_found:
                print(f"[*] Assembling {asm_found} first...")
                import subprocess
                subprocess.run([sys.executable, "assembler.py", asm_found])
                act_path = os.path.splitext(asm_found)[0] + ".hack"

        if act_path and exp_path:
            matched, total, _ = compare_hack_files(act_path, exp_path, test_name=name)
            results[name] = "PASSED" if matched else "FAILED"
        elif act_path and not exp_path:
            print(f"\n[{name}] Actual output exists ({act_path}), but official reference file not found yet.")
            print(f"       Drop the official {name}.hack as tests/{name}_official.hack to test.")
            results[name] = "WAITING FOR OFFICIAL FILE"
        else:
            print(f"\n[{name}] Neither .hack nor .asm found in workspace.")
            results[name] = "NOT FOUND"

    print("\n" + "=" * 55)
    print("              TEST SUMMARY REPORT")
    print("=" * 55)
    for name, status in results.items():
        print(f"  {name:10s} : {status}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Direct two-file comparison
        compare_hack_files(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        # Single program comparison by name, e.g. python compare.py Add
        target = sys.argv[1].replace(".hack", "").replace(".asm", "")
        compare_hack_files(f"tests/{target}.hack", f"tests/{target}_official.hack", test_name=target)
    else:
        # Default: batch test all 4 standard programs
        run_all_tests()
