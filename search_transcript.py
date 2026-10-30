import json
import re

transcript_path = r'C:\Users\co0ob\.gemini\antigravity\brain\54d05bb7-093a-4520-bc55-e8fbc272480c\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        content = str(data.get('content', ''))
        if any(k in content for k in ['script.google.com', 'ساعة', 'جدول', 'اونلاين', 'github.io', 'pages.dev', 'vercel', 'coligo']):
            idx = data.get('step_index')
            m = re.findall(r'https?://[^\s\)\"\'>]+', content)
            if m:
                print(f"Step {idx}: URLs ->", m[:3])
            elif 'ساعة' in content or 'جدول' in content:
                print(f"Step {idx}: Text snippet ->", content[:150].replace('\n', ' '))
