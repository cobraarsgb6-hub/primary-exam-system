import re
import html.parser

with open('Index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

class ButtonAuditor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.onclicks = []
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        line, col = self.getpos()
        
        if tag == 'button':
            self.buttons.append({
                'tag': tag,
                'id': attr_dict.get('id', ''),
                'class': attr_dict.get('class', ''),
                'onclick': attr_dict.get('onclick', ''),
                'line': line,
                'type': attr_dict.get('type', '')
            })
            
        if 'onclick' in attr_dict:
            self.onclicks.append({
                'tag': tag,
                'id': attr_dict.get('id', ''),
                'onclick': attr_dict.get('onclick', ''),
                'line': line
            })

parser = ButtonAuditor()
parser.feed(html_content)

print(f"Total <button> elements in Index.html: {len(parser.buttons)}")
print(f"Total elements with inline 'onclick': {len(parser.onclicks)}")

print("\n--- All <button> Elements ---")
for idx, b in enumerate(parser.buttons, 1):
    print(f"{idx:2d}. Line {b['line']:4d} | id='{b['id']}' | class='{b['class']}' | onclick='{b['onclick']}'")

print("\n--- Non-Button onclick Elements ---")
non_buttons = [o for o in parser.onclicks if o['tag'] != 'button']
for idx, o in enumerate(non_buttons, 1):
    print(f"{idx:2d}. Line {o['line']:4d} | <{o['tag']}> id='{o['id']}' | onclick='{o['onclick']}'")
