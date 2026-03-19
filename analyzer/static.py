import re

def analyze(code):
    issues = []
    lines = code.split("\n")

    loop_depth = 0
    max_depth = 0
    brace_stack = []

    for i, line in enumerate(lines):
        s = line.strip()
        if re.search(r'\b(for|while)\s*\(', s):
            loop_depth += 1
            max_depth = max(max_depth, loop_depth)
            brace_stack.append(('loop', i + 1))
        for ch in s:
            if ch == '}':
                if brace_stack:
                    brace_stack.pop()
                    if loop_depth > 0:
                        loop_depth -= 1

    if max_depth >= 2:
        issues.append({"type": "complexity", "message": "O(n^" + str(max_depth) + ") detected - nested loops found", "severity": "warning", "line": None})

    for i, line in enumerate(lines):
        if re.search(r'while\s*\(\s*(true|1)\s*\)', line):
            issues.append({"type": "infinite_loop", "message": "Infinite loop risk - while(true) or while(1) found", "severity": "error", "line": i + 1})

    for i, line in enumerate(lines):
        if re.search(r'if\s*\([^=!<>]*=[^=]', line):
            issues.append({"type": "assignment_in_condition", "message": "Assignment inside if - did you mean == ?", "severity": "error", "line": i + 1})

    bounds_lines = []
    for i, line in enumerate(lines):
        if re.search(r'\w+\[\w+\]', line):
            if '.size()' not in line and '.at(' not in line:
                bounds_lines.append(i + 1)
    if bounds_lines:
        issues.append({"type": "bounds_risk", "message": "Array access without bounds check (lines: " + str(bounds_lines[:3])[1:-1] + ")", "severity": "info", "line": bounds_lines[0]})

    pointer_lines = []
    for i, line in enumerate(lines):
        if re.search(r'\*\w+\s*=', line) or '->' in line:
            pointer_lines.append(i + 1)
    if pointer_lines:
        issues.append({"type": "null_pointer", "message": "Pointer usage detected - check for null (lines: " + str(pointer_lines[:3])[1:-1] + ")", "severity": "warning", "line": pointer_lines[0]})

    return issues
