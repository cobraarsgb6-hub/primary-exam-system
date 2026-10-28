import unicodedata, os

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

files_to_check = ['Index.html', 'Code.gs', 'Question_Bank.csv', 'Exams.csv']

for fname in files_to_check:
    if not os.path.exists(fname): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    norm = unicodedata.normalize('NFKC', content)
    has_diff = (norm != content)
    
    inverted_pairs = 0
    canonical_pairs = 0
    for i in range(len(content) - 1):
        c1, c2 = ord(content[i]), ord(content[i+1])
        if c1 in HARAKAT_AND_SHADDA and c2 in HARAKAT_AND_SHADDA:
            ccc1 = unicodedata.combining(content[i])
            ccc2 = unicodedata.combining(content[i+1])
            if ccc1 > ccc2:
                inverted_pairs += 1
            else:
                canonical_pairs += 1
                
    print(f"File: {fname}")
    print(f"  NFKC diff: {has_diff}")
    print(f"  Inverted pairs (Shadda+Haraka): {inverted_pairs}")
    print(f"  Canonical pairs (Haraka+Shadda): {canonical_pairs}")
