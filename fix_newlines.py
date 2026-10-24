# -*- coding: utf-8 -*-
code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace any literal newlines inside strings with \\n
# Notice line 2009: explanation: "💡 إتقان القاعدة:\nفي كلمة..."
code = code.replace(
    'explanation: "💡 إتقان القاعدة:\nفي كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف."',
    'explanation: "💡 إتقان القاعدة:\\nفي كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف."'
)
code = code.replace(
    'explanation: "💡 إتقان التضاد اللغوي:\nمضاد التأجيل هو التعجيل والتبكير."',
    'explanation: "💡 إتقان التضاد اللغوي:\\nمضاد التأجيل هو التعجيل والتبكير."'
)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Fixed newlines in string literals.")
