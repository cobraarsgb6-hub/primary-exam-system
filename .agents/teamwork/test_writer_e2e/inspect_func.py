import re

with open('Index.html', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

def print_func(fn_name):
    print(f'=== {fn_name} ===')
    start = -1
    for i, line in enumerate(lines):
        if re.search(r'function\s+' + fn_name + r'\s*\(', line):
            start = i
            break
    if start != -1:
        for j in range(start, min(start + 45, len(lines))):
            print(lines[j])
    else:
        print('Not found')
    print()

for fn in ['renderQuizQuestion', 'nextQuestion', 'prevQuestion', 'submitQuiz', 'onSubmissionSuccess', 'openStudentPortal', 'renderStudentStatus', 'requestRetakePrompt']:
    print_func(fn)
