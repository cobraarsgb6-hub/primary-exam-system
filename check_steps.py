import json

transcript_path = r'C:\Users\co0ob\.gemini\antigravity\brain\54d05bb7-093a-4520-bc55-e8fbc272480c\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in [10659, 10660, 10662, 10891, 10892, 10893]:
            print(f"=== STEP {idx} ===")
            print(str(data.get('content'))[:600])
