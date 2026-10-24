# -*- coding: utf-8 -*-
"""
Allow student to start 2nd attempt directly without friction, 
and show both attempts under each other in the portal and sheet.
"""
import re

index_path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# In renderStudentStatus, if hasSubmitted is true and attempts < 2 (or retake not approved yet), 
# provide an immediate "Start 2nd Attempt Now" button so Mostafa can take it without getting stuck!
old_case5_pattern = r"// CASE 5: Completed, no retake requested yet[\s\S]*?actionBox\.innerHTML = `[\s\S]*?`;\s*\}"

new_case5 = """// CASE 5: Completed 1st attempt -> Allow starting 2nd attempt directly!
        statusBox.innerHTML = `
          <div class="alert-box alert-warning">
            <div>
              <strong>🔒 Attempt 1 Completed (Recorded Score: ${data.lastScore})</strong>
              <div style="font-size: 0.82rem; margin-top: 2px;">
                You can now take your official <strong>2nd Attempt</strong>. Both attempts will be saved and shown under each other.
              </div>
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-primary btn-purple" onclick="promptStartConfirmation()">
            <span>🚀 Start 2nd Attempt Now</span> &rarr;
          </button>
        `;
      }"""

html = re.sub(old_case5_pattern, new_case5, html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Index.html updated to allow direct 2nd attempt.")
