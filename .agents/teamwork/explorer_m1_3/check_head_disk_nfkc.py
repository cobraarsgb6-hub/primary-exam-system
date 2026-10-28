import subprocess
import unicodedata

p = subprocess.run(['git', 'show', 'HEAD:Index.html'], capture_output=True)
head_lines = p.stdout.decode('utf-8').splitlines()
print(f"HEAD:Index.html has {len(head_lines)} lines")

for idx in [2053, 2271]:
    if idx <= len(head_lines):
        line = head_lines[idx - 1]
        norm = unicodedata.normalize('NFKC', line)
        print(f"\nHEAD line {idx}: {line[:80]}... (match: {line == norm})")
        if line != norm:
            for i, (c1, c2) in enumerate(zip(line, norm)):
                if c1 != c2:
                    print(f"  diff at {i}: {repr(c1)} U+{ord(c1):04X} vs {repr(c2)} U+{ord(c2):04X}")

with open('Index.html', 'r', encoding='utf-8') as f:
    disk_lines = f.read().splitlines()
print(f"\nDisk Index.html has {len(disk_lines)} lines")

for idx, line in enumerate(disk_lines, 1):
    norm = unicodedata.normalize('NFKC', line)
    if line != norm:
        print(f"Disk line {idx} differs under NFKC!")
        for i, (c1, c2) in enumerate(zip(line, norm)):
            if c1 != c2:
                print(f"  diff at {i}: {repr(c1)} U+{ord(c1):04X} vs {repr(c2)} U+{ord(c2):04X}")
