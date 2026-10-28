"""
Primary Exam System - Apps Script & Offline Bundler
Utility script to validate and assemble modular HTML/JS templates for Google Apps Script and offline deployment.
Includes automatic JavaScript string escaping for // (as \/\/) to prevent Google Apps Script line-cutting truncation.
"""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def escape_double_slash_in_html_scripts(html_text):
    """
    Safely escapes // as \/\/ inside string literals in JavaScript code,
    preventing Google Apps Script from truncating lines at // comments.
    Does NOT touch actual JavaScript comments.
    """
    def script_replacer(match):
        open_tag = match.group(1)
        js_code = match.group(2)
        close_tag = match.group(3)
        
        def string_replacer(m):
            quote = m.group(1)
            content = m.group(2)
            if '//' in content:
                content = content.replace('//', r'\/\/')
            return quote + content + quote

        pattern = r'(["\'`])((?:(?!\1|\\).|\\.)*?)\1'
        escaped_js = re.sub(pattern, string_replacer, js_code)
        return open_tag + escaped_js + close_tag

    return re.sub(r'(<script[^>]*>)([\s\S]*?)(</script>)', script_replacer, html_text, flags=re.IGNORECASE)

def resolve_template(html_path, base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(html_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def repl(m):
        raw_name = m.group(1).strip().strip("'\"")
        clean = raw_name.replace('.html', '')
        candidates = [
            os.path.join(base_dir, clean + '.html'),
            os.path.join(base_dir, raw_name),
            os.path.join(base_dir, raw_name + '.html'),
        ]
        for c in candidates:
            if os.path.exists(c):
                with open(c, 'r', encoding='utf-8') as cf:
                    return cf.read()
        raise FileNotFoundError(f"Could not resolve include: {raw_name} from {base_dir}")

    resolved = re.sub(r'<\?!=\s*include\(([^)]+)\);?\s*\?>', repl, content)
    # Apply automatic Google Apps Script // string escaping
    return escape_double_slash_in_html_scripts(resolved)

def build_bundle(output_path=None):
    template_path = os.path.join(BASE_DIR, 'Index.template.html')
    if not os.path.exists(template_path):
        template_path = os.path.join(BASE_DIR, 'Index.html')

    resolved = resolve_template(template_path, BASE_DIR)
    
    # 1. Primary Index.bundle.html
    if output_path is None:
        output_path = os.path.join(BASE_DIR, 'Index.bundle.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(resolved)

    # 2. Synchronize Index.html as full standalone working file
    full_index_path = os.path.join(BASE_DIR, 'Index.html')
    with open(full_index_path, 'w', encoding='utf-8') as f:
        f.write(resolved)

    # 3. Synchronize Android kiosk assets if directory exists
    android_asset = os.path.join(BASE_DIR, 'android', 'app', 'src', 'main', 'assets', 'www', 'index.html')
    if os.path.exists(os.path.dirname(android_asset)):
        with open(android_asset, 'w', encoding='utf-8') as f:
            f.write(resolved)

    size_kb = os.path.getsize(output_path) / 1024
    lines_count = len(resolved.splitlines())
    print(f"Successfully assembled bundle -> {output_path}")
    print(f"Synchronized full standalone Index.html -> {full_index_path}")
    print(f"Bundle size: {size_kb:.1f} KB | {lines_count} lines")
    return output_path

if __name__ == '__main__':
    build_bundle()
