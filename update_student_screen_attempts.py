# -*- coding: utf-8 -*-
"""
Display both attempts under each other on the Student Portal Screen!
"""
import re

# 1. Update Code.gs to return all attempts in getStudentExamStatus
code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

new_get_student_status = """function getStudentExamStatus(studentName, examCode) {
  try {
    const ss = getSpreadsheet();
    let subSheet = ss.getSheetByName('Submissions');
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    if (!subSheet) {
      setupDatabase(ss);
      subSheet = ss.getSheetByName('Submissions');
    }

    // Auto-seed historical submissions
    restoreAllHistoricalSubmissions();

    let hasSubmitted = false;
    const attempts = [];

    const targetName = String(studentName || '').trim().toLowerCase();
    const targetExam = String(examCode || '').trim().toUpperCase();

    if (subSheet && subSheet.getLastRow() > 1) {
      const sData = subSheet.getDataRange().getValues();
      for (let i = 1; i < sData.length; i++) {
        const rowName = String(sData[i][1] || '').trim().toLowerCase();
        const rowExam = String(sData[i][3] || '').trim().toUpperCase();

        const isStudentMatch = (rowName === targetName) || 
          (targetName.includes('ali') && (rowName.includes('ali') || rowName.includes('علي'))) ||
          (targetName.includes('mostafa') && (rowName.includes('mostafa') || rowName.includes('مصطفى')));
          
        const isExamMatch = (rowExam === targetExam) ||
          (targetExam.includes('ADV01') && (rowExam.includes('ADV') || rowExam.includes('ENG_G5'))) ||
          (targetExam.includes('FANTASY01') && (rowExam.includes('FANTASY') || rowExam.includes('ENG_G6'))) ||
          (targetExam.includes('ARB_PRIO01') && (rowExam.includes('ARB') || rowExam.includes('PRIO')));

        if (isStudentMatch && isExamMatch) {
          hasSubmitted = true;
          const score = Number(sData[i][4]) || 0;
          const total = Number(sData[i][5]) || 0;
          const pct = formatPercentValue(sData[i][6]);
          const rating = String(sData[i][7] || '');
          const duration = String(sData[i][8] || '');
          const summary = String(sData[i][9] || '');
          const dateStr = sData[i][0] instanceof Date ? Utilities.formatDate(sData[i][0], Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm') : String(sData[i][0]);

          let review = [];
          try { review = JSON.parse(sData[i][10] || '[]'); } catch(e) {}

          attempts.push({
            attemptNumber: attempts.length + 1,
            timestamp: dateStr,
            score: score,
            total: total,
            percentage: pct,
            rating: rating,
            duration: duration,
            summary: summary,
            review: review
          });
        }
      }
    }

    let retakeStatus = 'NONE';
    let requestId = '';

    if (retakeSheet && retakeSheet.getLastRow() > 1) {
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = rData.length - 1; i >= 1; i--) {
        const rowName = String(rData[i][2] || '').trim().toLowerCase();
        const rowExam = String(rData[i][3] || '').trim().toUpperCase();

        const isStudentMatch = (rowName === targetName) || 
          (targetName.includes('ali') && (rowName.includes('ali') || rowName.includes('علي'))) ||
          (targetName.includes('mostafa') && (rowName.includes('mostafa') || rowName.includes('مصطفى')));
          
        const isExamMatch = (rowExam === targetExam) ||
          (targetExam.includes('ADV01') && (rowExam.includes('ADV') || rowExam.includes('ENG_G5'))) ||
          (targetExam.includes('FANTASY01') && (rowExam.includes('FANTASY') || rowExam.includes('ENG_G6'))) ||
          (targetExam.includes('ARB_PRIO01') && (rowExam.includes('ARB') || rowExam.includes('PRIO')));

        if (isStudentMatch && isExamMatch) {
          retakeStatus = String(rData[i][6]).trim();
          requestId = String(rData[i][0]).trim();
          break;
        }
      }
    }

    const latestAttempt = attempts.length > 0 ? attempts[attempts.length - 1] : null;
    const lastScore = latestAttempt ? `${latestAttempt.score} / ${latestAttempt.total} (${latestAttempt.percentage})` : '';
    const lastDate = latestAttempt ? latestAttempt.timestamp : '';
    const canAttempt = (attempts.length < 2) || (retakeStatus === 'APPROVED');

    return {
      success: true,
      hasSubmitted: hasSubmitted,
      attemptsCount: attempts.length,
      attempts: attempts,
      lastScore: lastScore,
      lastDate: lastDate,
      canAttempt: canAttempt,
      retakeStatus: retakeStatus,
      requestId: requestId
    };
  } catch(e) {
    return { success: false, message: e.toString() };
  }
}"""

# Replace old getStudentExamStatus
code = re.sub(
    r"function getStudentExamStatus\(studentName, examCode\) \{[\s\S]*?return \{\s*success: false, message: e\.toString\(\) \};\s*\}\s*\}",
    new_get_student_status,
    code
)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)
print("Code.gs updated with multi-attempt support.")

# 2. Update Index.html renderStudentStatus to display all attempts under each other
index_path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

new_render_student_status = """function renderStudentStatus(data, studentName, examCode) {
      const statusBox = document.getElementById('sp-status-container');
      const actionBox = document.getElementById('sp-action-container');

      const attempts = data.attempts || [];

      if (!data.hasSubmitted || attempts.length === 0) {
        // CASE 1: Fresh attempt (0 attempts)
        statusBox.innerHTML = `
          <div class="alert-box alert-warning">
            <span style="font-size: 1.2rem;">⚠️</span>
            <div>
              <strong>Assessment Policy:</strong>
              <div style="font-size: 0.8rem; margin-top: 2px;">
                You have 2 official attempts for this assessment. Once started, the timer begins immediately.
              </div>
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-primary" onclick="promptStartConfirmation()">
            <span>Start Assessment Now</span> &rarr;
          </button>
        `;
        return;
      }

      // MULTI-ATTEMPT DISPLAY: Render all attempts under each other!
      let attemptsHtml = `
        <div style="margin-top: 6px; margin-bottom: 14px;">
          <div style="font-size: 0.86rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px; display: flex; justify-content: space-between;">
            <span>📋 Recorded Attempts History (${attempts.length} Completed):</span>
            <span style="color: var(--accent); font-weight: 700;">Best Score: ${Math.max(...attempts.map(a => a.score))} / ${attempts[0].total}</span>
          </div>
      `;

      attempts.forEach((att, idx) => {
        const isBest = att.score === Math.max(...attempts.map(a => a.score));
        let detailsHtml = '';
        (att.review || []).forEach((r, qIdx) => {
          const isCorrect = r.isCorrect === true || r.isCorrect === 'true';
          detailsHtml += `
            <div style="font-size: 0.8rem; padding: 6px 8px; margin-top: 4px; border-radius: 6px; background: ${isCorrect ? '#f8fafc' : '#fef2f2'}; border-left: 3px solid ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
              <div><strong>Q${qIdx + 1}:</strong> ${r.questionText}</div>
              <div style="margin-top: 2px; font-size: 0.78rem;">
                <span style="color: ${isCorrect ? 'var(--success)' : 'var(--danger)'}; font-weight: 700;">
                  ${isCorrect ? '✓ ' + (r.studentAnswer || 'Correct') : '✗ Student: ' + (r.studentAnswer || '(None)')}
                </span>
                ${!isCorrect ? ` &bull; <span style="color: #047857; font-weight: 700;">Correct: ${r.correctAnswer}</span>` : ''}
              </div>
            </div>
          `;
        });

        attemptsHtml += `
          <div style="background: #fff; border: 1.5px solid ${isBest ? '#10b981' : 'var(--border)'}; border-radius: 10px; padding: 12px 14px; margin-bottom: 8px; box-shadow: var(--shadow-sm);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
              <div>
                <div style="font-weight: 800; font-size: 0.95rem; color: var(--primary);">
                  🎯 Attempt ${att.attemptNumber || (idx + 1)} ${isBest ? '🌟 (Highest Score)' : ''}
                </div>
                <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 2px;">
                  📅 ${att.timestamp} &bull; ⏱️ ${att.duration}
                </div>
              </div>
              <div style="font-size: 0.95rem; font-weight: 800; padding: 4px 10px; border-radius: 8px; background: ${att.score >= 9 ? '#ecfdf5' : '#fef3c7'}; color: ${att.score >= 9 ? '#047857' : '#b45309'};">
                ${att.score} / ${att.total} (${att.percentage}) &bull; ${att.rating}
              </div>
            </div>
            ${detailsHtml ? `
              <details style="margin-top: 8px; font-size: 0.8rem;">
                <summary style="font-weight: 700; color: var(--accent); cursor: pointer;">🔍 View Questions & Answers Breakdown ↓</summary>
                <div style="margin-top: 6px;">${detailsHtml}</div>
              </details>
            ` : ''}
          </div>
        `;
      });

      attemptsHtml += `</div>`;
      statusBox.innerHTML = attemptsHtml;

      // ACTION BUTTON BASED ON ATTEMPTS COUNT
      if (attempts.length >= 2) {
        actionBox.innerHTML = `
          <div class="alert-box alert-success" style="justify-content: center; text-align: center; font-weight: 700;">
            ✅ Maximum Attempts Completed (2 of 2 Attempts Saved Successfully)
          </div>
        `;
      } else {
        actionBox.innerHTML = `
          <button class="btn-primary btn-purple" onclick="promptStartConfirmation()">
            <span>🚀 Start 2nd Attempt Now</span> &rarr;
          </button>
        `;
      }
    }"""

# Replace old renderStudentStatus
html = re.sub(
    r"function renderStudentStatus\(data, studentName, examCode\) \{[\s\S]*?function requestRetakePrompt",
    new_render_student_status + "\n\n    function requestRetakePrompt",
    html
)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Index.html updated to show both attempts on student screen.")
