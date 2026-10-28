import subprocess

p = subprocess.run(['git', 'log', '-n', '5', '--format=%H %s'], capture_output=True, text=True, encoding='utf-8')
print("Commits:")
print(p.stdout)

commits = [line.split()[0] for line in p.stdout.strip().splitlines() if line]

for c in commits:
    p2 = subprocess.run(['git', 'show', f'{c}:Index.html'], capture_output=True)
    try:
        content = p2.stdout.decode('utf-8')
        import unicodedata
        norm = unicodedata.normalize('NFKC', content)
        print(f"Commit {c[:7]}: len={len(content)}, NFKC diff={content != norm}")
        if content != norm:
            # find lines that differ
            lines = content.splitlines()
            for l_idx, line in enumerate(lines, 1):
                if line != unicodedata.normalize('NFKC', line):
                    print(f"   Line {l_idx} differs under NFKC!")
                    for ch_idx, (c1, c2) in enumerate(zip(line, unicodedata.normalize('NFKC', line))):
                        if c1 != c2:
                            print(f"     char {ch_idx}: {repr(c1)} U+{ord(c1):04X} vs {repr(c2)} U+{ord(c2):04X}")
    except Exception as e:
        print(f"Commit {c[:7]}: error {e}")
