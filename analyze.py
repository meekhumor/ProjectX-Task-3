import os

DISALLOWED = ['print(', 'eval(', 'exec(']

def get_python_files():
    folder = 'src_files'
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.py')]

def is_comment(line):
    return line.strip().startswith('# ')

def analyze_line(line):
    violations = 0
    forbidden_used = False

    if len(line.rstrip()) > 80:
        violations += 1

    if '\\' not in line:
        if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
            violations += 1

    if is_comment(line):
        return violations, False

    if '#' in line:
        line = line.split('#')[0]

    if '"' in line or "'" in line:
        return violations, False

    for keyword in DISALLOWED:
        if keyword in line:
            violations += 1
            forbidden_used = True

    return violations, forbidden_used

def analyze_file(filepath):
    total_violations = 0
    forbidden = False

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            v, f_flag = analyze_line(line)
            total_violations += v
            forbidden = forbidden or f_flag

    if total_violations == 0:
        status = "CLEAN"
    elif total_violations <= 5 and not forbidden:
        status = "LOW RISK"
    else:
        status = "HIGH RISK"

    print(f"{filepath}: {status}")

def main():
    files = get_python_files()
    for f in files:
        analyze_file(f)

if __name__ == "__main__":
    main()
