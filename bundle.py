"""
Primary Exam System - Apps Script & Offline Bundler
Utility script to validate and assemble modular HTML/JS templates for Google Apps Script and offline deployment.
"""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

    return re.sub(r'<\?!=\s*include\(([^)]+)\);?\s*\?>', repl, content)

def build_bundle(output_path=None):
    index_path = os.path.join(BASE_DIR, 'Index.html')
    if output_path is None:
        output_path = os.path.join(BASE_DIR, 'Index.bundle.html')

    resolved = resolve_template(index_path, BASE_DIR)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(resolved)

    size_kb = os.path.getsize(output_path) / 1024
    lines_count = len(resolved.splitlines())
    print(f"Successfully assembled bundle -> {output_path}")
    print(f"Bundle size: {size_kb:.1f} KB | {lines_count} lines")
    return output_path

if __name__ == '__main__':
    build_bundle()
