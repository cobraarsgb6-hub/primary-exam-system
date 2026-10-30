import os

file_path = r"C:\Users\co0ob\Projects\primary-exam-system\build_precision_phet_lab.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Fonts replacement: remove Plus Jakarta Sans, use Newsreader + Outfit + JetBrains Mono
old_font = "family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800"
new_font = "family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400&family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800"
code = code.replace(old_font, new_font)

code = code.replace("font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;", "font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;")
code = code.replace(".font-mono { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }", ".font-mono { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }\n    .font-serif { font-family: 'Newsreader', Georgia, serif; }")

# 2. Remove dark-glow colored box-shadow halos
code = code.replace(
    "box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.4), 0 8px 20px -4px rgba(37, 99, 235, 0.2) !important;",
    "box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.12) !important;"
)

# 3. Remove pulsing decorative dot
code = code.replace(
    "w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse",
    "w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"
)

# 4. Enhance typography hierarchy (fix flat-type-hierarchy)
code = code.replace(
    '<h1 class="theme-text-title text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Precision Electric Circuit Laboratory</h1>',
    '<h1 class="theme-text-title text-2xl sm:text-3xl lg:text-4xl font-extrabold font-serif text-slate-900 tracking-tight">Precision Electric Circuit Laboratory</h1>'
)

code = code.replace(
    '<h2 class="theme-text-title text-base sm:text-lg font-black text-slate-900">Cambridge Exam Checkpoint Challenge</h2>',
    '<h2 class="theme-text-title text-xl sm:text-2xl font-bold font-serif text-slate-900 tracking-tight">Cambridge Exam Checkpoint Challenge</h2>'
)

# 5. Flatten nested cards in inspector showcase
code = code.replace(
    'id="inspector-showcase" class="theme-bg-card bg-slate-50 border border-slate-200/90 rounded-2xl p-5 space-y-4"',
    'id="inspector-showcase" class="pt-5 border-t border-slate-200 dark:border-slate-800 space-y-4"'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated build_precision_phet_lab.py successfully!")
