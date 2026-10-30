with open(r'C:\Users\co0ob\Projects\primary-exam-system\build_flawless_cambridge_lab.py', 'r', encoding='utf-8') as f:
    code = f.read()

target1 = '<rect x="0" y="0" width="240" height="115" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>'
repl1 = '<rect x="0" y="0" width="240" height="122" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>'

target2 = '''            <!-- Single Clean Station Diagnostic Label (Completely below the clips!) -->
            <text id="specimen-station-label" x="120" y="98" fill="#f87171" font-size="9" font-weight="700" font-family="monospace" text-anchor="middle">
              Circuit Open: Air is an insulator (0.00 Amps)
            </text>'''

repl2 = '''            <!-- Single Clean Station Diagnostic Label inside OLED Pill -->
            <rect x="12" y="88" width="216" height="24" rx="12" fill="#090d16" stroke="#334155" stroke-width="1.2"/>
            <text id="specimen-station-label" x="120" y="103" fill="#f87171" font-size="8.5" font-weight="700" font-family="monospace" text-anchor="middle">
              Circuit Open: Air is an insulator (0.00 Amps)
            </text>'''

assert target1 in code, 'target1 not found'
assert target2 in code, 'target2 not found'

code = code.replace(target1, repl1, 1).replace(target2, repl2, 1)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\build_flawless_cambridge_lab.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated OLED Pill and height successfully!')
