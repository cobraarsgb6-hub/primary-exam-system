# -*- coding: utf-8 -*-
import re

code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace setupDatabase to NEVER clear submissions
safe_setup_database = """function setupDatabase(targetSs) {
  const ss = (targetSs && targetSs.getSheetByName) ? targetSs : getSpreadsheet();

  // 1. TAB: Submissions (Student Results & Records) - NEVER CLEAR EXISTING ROWS!
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {
    subSheet = ss.insertSheet('Submissions');
  }
  
  const subHeaders = [
    ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON']
  ];

  if (subSheet.getLastRow() === 0) {
    subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
  } else {
    // Just ensure header values match
    subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
  }
  formatHeaderRow(subSheet, '#1e3a8a');

  // Auto-seed Ali Ahmed only if missing, preserving Mostafa and all other submissions
  ensureAliRecord(subSheet);
  styleSubmissionsSheet(subSheet);

  // 2. TAB: Question_Bank (Reference Catalog)"""

code = re.sub(
    r"function setupDatabase\(targetSs\) \{[\s\S]*?// 2\. TAB: Question_Bank \(Reference Catalog\)",
    safe_setup_database,
    code
)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)

print("setupDatabase made non-destructive successfully.")
