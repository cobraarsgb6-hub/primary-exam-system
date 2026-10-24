# -*- coding: utf-8 -*-
code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    c = f.read()

target = "let retakeSheet = ss.getSheetByName('Retake_Requests');\n    }"
replacement = "let retakeSheet = ss.getSheetByName('Retake_Requests');\n    }\n\n    restoreAllHistoricalSubmissions();"

if "restoreAllHistoricalSubmissions();" not in c[c.find("function getAdminDashboardData"):c.find("function getAdminDashboardData") + 300]:
    c = c.replace(target, replacement, 1)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Updated getAdminDashboardData successfully.")
