with open(r'C:\Users\co0ob\Projects\primary-exam-system\Index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add currentSessionKey variable
text = text.replace(
    'let cachedAdminData = null;',
    'let cachedAdminData = null;\n    let currentSessionKey = "";'
)

# 2. Store sessionKey on load
text = text.replace(
    'questions = res.questions;',
    'questions = res.questions;\n      currentSessionKey = res.sessionKey || "";'
)

# 3. Send sessionKey on submit
text = text.replace(
    'durationSpent: durationStr',
    'durationSpent: durationStr,\n        sessionKey: currentSessionKey'
)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Index.html successfully updated with dynamic sessionKey!')
