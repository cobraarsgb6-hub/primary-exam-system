import re
import html.parser

with open('Index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract the script content
script_match = re.search(r'<script\b[^>]*>(.*?)</script>', html_content, re.DOTALL)
script_content = script_match.group(1) if script_match else ""

class ButtonAuditor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        line, col = self.getpos()
        if tag == 'button':
            self.buttons.append({
                'line': line,
                'id': attr_dict.get('id', ''),
                'class': attr_dict.get('class', ''),
                'onclick': attr_dict.get('onclick', ''),
                'type': attr_dict.get('type', '')
            })

parser = ButtonAuditor()
parser.feed(html_content)

print(f"Total buttons: {len(parser.buttons)}\n")

# Find defined functions in script_content
defined_functions = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', script_content))
defined_vars = set(re.findall(r'(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=', script_content))
window_props = set(re.findall(r'window\.([a-zA-Z0-9_$]+)\s*=', script_content))

all_identifiers = defined_functions | defined_vars | window_props

print(f"Total defined functions in script: {len(defined_functions)}")

audit_results = []

for idx, b in enumerate(parser.buttons, 1):
    onclick = b['onclick'].strip()
    btn_id = b['id']
    btn_line = b['line']
    
    status = "OK"
    notes = ""
    
    if onclick:
        # Extract function call name: e.g. openParentPortal(), switchParentView('history')
        fn_match = re.match(r'([a-zA-Z0-9_$]+)\s*\(', onclick)
        if fn_match:
            fn_name = fn_match.group(1)
            if fn_name in defined_functions:
                notes = f"Calls function '{fn_name}()' [DEFINED]"
            elif fn_name in all_identifiers:
                notes = f"Calls identifier '{fn_name}' [EXISTS]"
            else:
                status = "MISSING_FUNCTION"
                notes = f"CRITICAL: Function '{fn_name}' NOT defined in script!"
        else:
            notes = f"Inline JS expression: {onclick}"
    else:
        # No inline onclick - check if ID has dynamic listener in script
        if btn_id:
            has_get_element = f"'{btn_id}'" in script_content or f'"{btn_id}"' in script_content or f"`{btn_id}`" in script_content
            has_listener = re.search(rf"['\"`]{re.escape(btn_id)}['\"`]\)[\s\S]{{0,100}}\.addEventListener", script_content) or \
                           re.search(rf"['\"`]{re.escape(btn_id)}['\"`]\)[\s\S]{{0,100}}\.onclick", script_content) or \
                           re.search(rf"(?:let|const|var)\s+([a-zA-Z0-9_$]+)\s*=\s*document\.getElementById\(['\"`]{re.escape(btn_id)}['\"`]\);[\s\S]{{0,150}}\1\.(?:onclick|addEventListener)", script_content)
            if has_listener:
                notes = f"Dynamic event listener attached to #{btn_id} [ATTACHED]"
            elif has_get_element:
                notes = f"Referenced in script by id #{btn_id}"
            else:
                status = "DEAD_BUTTON"
                notes = f"DEAD BUTTON: No onclick and no ID reference in script!"
        else:
            status = "DEAD_BUTTON"
            notes = "DEAD BUTTON: No onclick and no ID!"
            
    audit_results.append({
        'index': idx,
        'line': btn_line,
        'id': btn_id,
        'class': b['class'],
        'onclick': onclick,
        'status': status,
        'notes': notes
    })

print(f"{'#':2} | {'Line':4} | {'ID':22} | {'Status':16} | {'Handler / Notes'}")
print("-" * 90)
for r in audit_results:
    id_str = f"#{r['id']}" if r['id'] else "(no id)"
    print(f"{r['index']:2d} | {r['line']:4d} | {id_str:22} | {r['status']:16} | {r['notes']}")
