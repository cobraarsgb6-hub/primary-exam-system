import unicodedata

fatha = '\u064e'
shadda = '\u0651'

fs = fatha + shadda
sf = shadda + fatha

print(f"fs: {[hex(ord(c)) for c in fs]}")
print(f"sf: {[hex(ord(c)) for c in sf]}")
print(f"norm(fs): {[hex(ord(c)) for c in unicodedata.normalize('NFKC', fs)]}")
print(f"norm(sf): {[hex(ord(c)) for c in unicodedata.normalize('NFKC', sf)]}")
print(f"fs == norm(fs): {fs == unicodedata.normalize('NFKC', fs)}")
print(f"sf == norm(sf): {sf == unicodedata.normalize('NFKC', sf)}")

with open('Index.html', 'r', encoding='utf-8') as f:
    content = f.read()

norm_content = unicodedata.normalize('NFKC', content)
print(f"content == norm_content: {content == norm_content}")

if content != norm_content:
    print(f"Lengths: {len(content)} vs {len(norm_content)}")
    for i in range(len(content)):
        if content[i] != norm_content[i]:
            line_no = content[:i].count('\n') + 1
            print(f"Difference at char {i}, line {line_no}:")
            print(f"  Orig: {repr(content[i])} (U+{ord(content[i]):04X}) {unicodedata.name(content[i], '')}")
            print(f"  Norm: {repr(norm_content[i])} (U+{ord(norm_content[i]):04X}) {unicodedata.name(norm_content[i], '')}")
            # print surrounding 50 chars
            print(f"  Snippet: {repr(content[max(0, i-30):min(len(content), i+30)])}")
            break
