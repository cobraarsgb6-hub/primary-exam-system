import unicodedata

HARAKAT_AND_SHADDA = {
    0x064B: 'FATHATAN',
    0x064C: 'DAMMATAN',
    0x064D: 'KASRATAN',
    0x064E: 'FATHA',
    0x064F: 'DAMMA',
    0x0650: 'KASRA',
    0x0651: 'SHADDA',
    0x0652: 'SUKUN',
}

with open('Code.gs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in Code.gs: {len(lines)}")

combining_lines = []
non_canonical_count = 0

for idx, line in enumerate(lines, 1):
    pairs = []
    for i in range(len(line) - 1):
        c1, c2 = ord(line[i]), ord(line[i+1])
        if c1 in HARAKAT_AND_SHADDA and c2 in HARAKAT_AND_SHADDA:
            ccc1 = unicodedata.combining(line[i])
            ccc2 = unicodedata.combining(line[i+1])
            is_inverted = (ccc1 > ccc2)
            if is_inverted:
                non_canonical_count += 1
            pairs.append((i, line[i], line[i+1], HARAKAT_AND_SHADDA[c1], HARAKAT_AND_SHADDA[c2], is_inverted))
            
    norm_line = unicodedata.normalize('NFKC', line)
    differs_under_nfkc = (norm_line != line)
    
    if pairs or differs_under_nfkc:
        combining_lines.append((idx, line, pairs, differs_under_nfkc))

print(f"Total non-canonical inverted combining pairs in Code.gs: {non_canonical_count}")
print(f"Lines with adjacent combining marks in Code.gs: {len(combining_lines)}")
for idx, line, pairs, diff in combining_lines[:15]:
    print(f"\nLine {idx} (NFKC diff: {diff}):")
    print(f"  Snippet: {line.strip()[:80]}...")
    for pos, ch1, ch2, name1, name2, is_inv in pairs:
        print(f"    {'⚠️ INVERTED' if is_inv else '✅ Canonical'}: {name1} (U+{ord(ch1):04X}) + {name2} (U+{ord(ch2):04X})")
