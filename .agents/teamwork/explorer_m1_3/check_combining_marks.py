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

with open('Index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

combining_lines = []

for idx, line in enumerate(lines, 1):
    # Check if line has shadda + vowel or vowel + shadda
    chars = [ord(c) for c in line]
    has_shadda = 0x0651 in chars
    has_haraka = any(c in chars for c in [0x064B, 0x064C, 0x064D, 0x064E, 0x064F, 0x0650, 0x0652])
    
    # Check consecutive marks
    pairs = []
    for i in range(len(line) - 1):
        c1, c2 = ord(line[i]), ord(line[i+1])
        if c1 in HARAKAT_AND_SHADDA and c2 in HARAKAT_AND_SHADDA:
            pairs.append((i, line[i], line[i+1], HARAKAT_AND_SHADDA[c1], HARAKAT_AND_SHADDA[c2]))
            
    norm_line = unicodedata.normalize('NFKC', line)
    differs_under_nfkc = (norm_line != line)
    
    if pairs or differs_under_nfkc:
        combining_lines.append((idx, line, pairs, differs_under_nfkc))

print(f"Lines with adjacent combining marks or NFKC diffs: {len(combining_lines)}")
for idx, line, pairs, diff in combining_lines:
    print(f"\nLine {idx} (NFKC diff: {diff}):")
    print(f"  Snippet: {line.strip()[:100]}...")
    for pos, ch1, ch2, name1, name2 in pairs:
        # show surrounding word
        start = max(0, pos - 10)
        end = min(len(line), pos + 10)
        word = line[start:end].strip()
        print(f"  Adjacent marks at pos {pos}: {name1} (U+{ord(ch1):04X}) + {name2} (U+{ord(ch2):04X}) in context: '{word}'")
        # Check canonical ordering:
        # Canonical combining class of ch1 and ch2
        ccc1 = unicodedata.combining(ch1)
        ccc2 = unicodedata.combining(ch2)
        print(f"    CCC({name1}) = {ccc1}, CCC({name2}) = {ccc2}")
        if ccc1 > ccc2:
            print(f"    ⚠️ INVERTED CANONICAL ORDER! Under NFKC, {name2} will precede {name1}.")
        else:
            print(f"    ✅ Canonical order (lower CCC precedes higher CCC).")
