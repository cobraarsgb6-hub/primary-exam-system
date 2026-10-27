import os
import re

code_path = r'primary-exam-system\Code.gs'
html_path = r'primary-exam-system\Index.html'

with open(code_path, 'r', encoding='utf-8') as f:
    code_content = f.read()
    code_lines = code_content.splitlines()

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
    html_lines = html_content.splitlines()

html_size_kb = os.path.getsize(html_path) / 1024

# Count functions in Code.gs
fn_matches = re.findall(r'^[ \t]*function\s+([a-zA-Z0-9_]+)\s*\(', code_content, re.MULTILINE)

# Find longest function in Code.gs
fn_starts = [(m.group(1), m.start()) for m in re.finditer(r'^[ \t]*function\s+([a-zA-Z0-9_]+)\s*\(', code_content, re.MULTILINE)]
fn_lengths = {}
for i in range(len(fn_starts)):
    name, start = fn_starts[i]
    end = fn_starts[i+1][1] if i + 1 < len(fn_starts) else len(code_content)
    lines_count = code_content[start:end].count('\n')
    fn_lengths[name] = lines_count

sorted_fns = sorted(fn_lengths.items(), key=lambda x: x[1], reverse=True)
longest_fn = sorted_fns[0] if sorted_fns else ('none', 0)

# Check occurrences
onclick_count = len(re.findall(r'onclick\s*=', html_content, re.IGNORECASE))
inline_style_count = len(re.findall(r'style\s*=', html_content, re.IGNORECASE))
innerhtml_count = len(re.findall(r'innerHTML\s*=', html_content))

fake_data_matches = len(re.findall(r'seedAliSubmissionRow|ensureAliRecord|getHistoricalSubmissionsData|restoreAllHistoricalSubmissions', code_content))
correct_answer_html = len(re.findall(r'correctAnswer', html_content))

print(f"=== CURRENT MEASURED METRICS ===")
print(f"Code.gs lines: {len(code_lines)}")
print(f"Index.html size: {html_size_kb:.1f} KB / {len(html_lines)} lines")
print(f"Longest function: {longest_fn[0]} ({longest_fn[1]} lines)")
print(f"Functions in Code.gs: {len(fn_matches)}")
print(f"Fake data in Code.gs: {fake_data_matches}")
print(f"correctAnswer in Index.html: {correct_answer_html}")
print(f"onclick= count in Index.html: {onclick_count}")
print(f"style= count in Index.html: {inline_style_count}")
print(f"innerHTML= count in Index.html: {innerhtml_count}")
