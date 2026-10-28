import re

with open('Index.html', encoding='utf-8') as f:
    text = f.read()

# Find JS functions
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)', text)
print(f'Total functions found: {len(funcs)}')

keywords = ['quiz', 'exam', 'submit', 'question', 'render', 'retake', 'plan', 'student', 'score', 'modal']
for k in keywords:
    matched = [f'{fn}({args})' for fn, args in funcs if k in fn.lower()]
    print(f'-- Functions with "{k}" ({len(matched)}) --')
    for m in matched[:8]:
        print('  ', m)
