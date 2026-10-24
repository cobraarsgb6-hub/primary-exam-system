# -*- coding: utf-8 -*-
import re

index_path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Enhance checkExamStatus to clear stale UI instantly and show clean loader
old_check_pattern = r"function checkExamStatus\(studentName, examCode\) \{[\s\S]*?if \(typeof google !== 'undefined'"

new_check = """function checkExamStatus(studentName, examCode) {
      const statusBox = document.getElementById('sp-status-container');
      const actionBox = document.getElementById('sp-action-container');

      // INSTANT CLEANUP: Clear stale data immediately upon click so old scores never flash!
      statusBox.innerHTML = `
        <div style="background: #f8fafc; border: 1px dashed var(--border); border-radius: 10px; padding: 14px; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
          <div class="spinner" style="display: inline-block; width: 16px; height: 16px; margin-right: 6px; vertical-align: middle;"></div>
          Fetching live assessment records...
        </div>
      `;
      actionBox.innerHTML = '';

      if (typeof google !== 'undefined'"""

html = re.sub(old_check_pattern, new_check, html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Index.html updated with instant stale UI cleanup.")
