import re

REAL_TYPOS = [
    (r'\bwhil\s*\(', 'while('),
    (r'\bfro\s*\(', 'for('),
    (r'\biff\s*\(', 'if('),
    (r'\besle\b', 'else'),
    (r'\breeturn\b', 'return'),
    (r'\bretrn\b', 'return'),
    (r'\bretrun\b', 'return'),
    (r'\bintt\b', 'int'),
    (r'\bvoud\b', 'void'),
    (r'\bstirng\b', 'string'),
    (r'\bstrign\b', 'string'),
    (r'\bflot\b', 'float'),
    (r'\bdoubel\b', 'double'),
    (r'\bvecotr\b', 'vector'),
    (r'\bvecor\b', 'vector'),
    (r'\bnamepsace\b', 'namespace'),
    (r'\bnamesapce\b', 'namespace'),
    (r'\bclss\b', 'class'),
    (r'\bpulbic\b', 'public'),
    (r'\bpirntf\b', 'printf'),
    (r'\bcotu\b', 'cout'),
    (r'\bswithc\b', 'switch'),
    (r'\bswitc\b', 'switch'),
    (r'\bcotinue\b', 'continue'),
    (r'\bcontiue\b', 'continue'),
    (r'\bpritf\b', 'printf'),
    (r'\bprinft\b', 'printf'),
]

def analyze(code):
    issues = []
    lines = code.split("\n")

    # 1. Nested loop detection
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

    # 2. Infinite loop
    for i, line in enumerate(lines):
        if re.search(r'while\s*\(\s*(true|1)\s*\)', line):
            issues.append({"type": "infinite_loop", "message": "Infinite loop risk - while(true) or while(1) found", "severity": "error", "line": i + 1})

    # 3. Assignment in condition
    for i, line in enumerate(lines):
        if re.search(r'if\s*\([^=!<>]*=[^=]', line):
            issues.append({"type": "assignment_in_condition", "message": "Assignment inside if - did you mean == ?", "severity": "error", "line": i + 1})

    # 4. Array bounds - report once
    bounds_lines = []
    for i, line in enumerate(lines):
        if re.search(r'\w+\[\w+\]', line):
            if '.size()' not in line and '.at(' not in line:
                bounds_lines.append(i + 1)
    if bounds_lines:
        issues.append({"type": "bounds_risk", "message": "Array access without bounds check (lines: " + str(bounds_lines[:3])[1:-1] + ")", "severity": "info", "line": bounds_lines[0]})

    # 5. Null pointer - report once
    pointer_lines = []
    for i, line in enumerate(lines):
        if re.search(r'\*\w+\s*=', line) or '->' in line:
            pointer_lines.append(i + 1)
    if pointer_lines:
        issues.append({"type": "null_pointer", "message": "Pointer usage detected - check for null (lines: " + str(pointer_lines[:3])[1:-1] + ")", "severity": "warning", "line": pointer_lines[0]})

    # 6. Typo detection
    for i, line in enumerate(lines):
        for pattern, suggestion in REAL_TYPOS:
            if re.search(pattern, line):
                issues.append({"type": "typo", "message": "Typo - did you mean: " + suggestion + "?", "severity": "error", "line": i + 1})
                break

    # 7. Mismatched braces
    open_braces = sum(line.count('{') - line.count('}') for line in lines)
    if open_braces > 0:
        issues.append({"type": "brace_mismatch", "message": "Missing closing brace - " + str(open_braces) + " brace(s) not closed", "severity": "error", "line": None})
    elif open_braces < 0:
        issues.append({"type": "brace_mismatch", "message": "Extra closing brace - " + str(abs(open_braces)) + " extra brace(s)", "severity": "error", "line": None})

    # 8. Mismatched parentheses
    open_parens = sum(line.count('(') - line.count(')') for line in lines)
    if open_parens > 0:
        issues.append({"type": "paren_mismatch", "message": "Missing closing parenthesis - " + str(open_parens) + " not closed", "severity": "error", "line": None})
    elif open_parens < 0:
        issues.append({"type": "paren_mismatch", "message": "Extra closing parenthesis - " + str(abs(open_parens)) + " extra", "severity": "error", "line": None})

    # 9. Colon instead of semicolon
    for i, line in enumerate(lines):
        s = line.strip()
        if re.search(r'(int|float|double|char|bool|auto|long|string)\s+\w+.*:$', s):
            if not s.startswith('case') and not s.startswith('default') and '?' not in s:
                issues.append({"type": "colon_instead_semicolon", "message": "Colon at end of line - did you mean semicolon?", "severity": "error", "line": i + 1})

    # 10. Missing semicolon after statement
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith('//') or s.startswith('#') or s.startswith('*'):
            continue
        if re.search(r'^(int|float|double|char|bool|auto|long|string|vector|map|set)\s+\w+.*[^;{},]$', s):
            if not re.search(r'[{(,]$', s) and not s.endswith('\\'):
                issues.append({"type": "missing_semicolon", "message": "Possible missing semicolon", "severity": "warning", "line": i + 1})

    # 11. Return in void function
    void_func = False
    for i, line in enumerate(lines):
        if re.search(r'\bvoid\s+\w+\s*\(', line):
            void_func = True
        if void_func and re.search(r'\breturn\s+\w+', line):
            issues.append({"type": "return_in_void", "message": "Return with value in void function", "severity": "error", "line": i + 1})
            void_func = False

    # 12. Missing return in non-void function
    non_void_funcs = []
    has_return = False
    for i, line in enumerate(lines):
        if re.search(r'\b(int|float|double|char|bool|long)\s+\w+\s*\(', line):
            if 'main' not in line:
                non_void_funcs.append(i + 1)
                has_return = False
        if re.search(r'\breturn\b', line):
            has_return = True
    if non_void_funcs and not has_return:
        issues.append({"type": "missing_return", "message": "Non-void function may be missing return statement", "severity": "warning", "line": non_void_funcs[0]})

    return issues
