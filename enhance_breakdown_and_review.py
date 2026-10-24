# -*- coding: utf-8 -*-
"""
Enhance Parent Breakdown and Question Review in Code.gs and Index.html
"""
import json
import re

# 1. Update Ali's seeded review in Code.gs
code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code_content = f.read()

real_review = [
    {
        "questionId": "Q_Y5_ENG_001",
        "questionText": "What is an adverbial?",
        "studentAnswer": "A group of words without a verb that adds detail about time, place, or manner",
        "correctAnswer": "A group of words without a verb that adds detail about time, place, or manner",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb."
    },
    {
        "questionId": "Q_Y5_ENG_002",
        "questionText": "In the sentence: \"The rocket launched at dawn.\", what type of adverbial is \"at dawn\"?",
        "studentAnswer": "Adverbial of Time",
        "correctAnswer": "Adverbial of Time",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"at dawn\" tells us WHEN the rocket launched (Adverbial of Time)."
    },
    {
        "questionId": "Q_Y5_ENG_003",
        "questionText": "Which of the following sentences contains an adverbial of PLACE?",
        "studentAnswer": "The crew slept inside the space station.",
        "correctAnswer": "The crew slept inside the space station.",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"inside the space station\" answers the question WHERE did the crew sleep (Adverbial of Place)."
    },
    {
        "questionId": "Q_Y5_ENG_004",
        "questionText": "An adverbial of MANNER answers which question?",
        "studentAnswer": "How or in what way?",
        "correctAnswer": "How or in what way?",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently)."
    },
    {
        "questionId": "Q_Y5_ENG_005",
        "questionText": "Which sentence is punctuated correctly with a comma after the fronted adverbial?",
        "studentAnswer": "After a long journey the crew landed.",
        "correctAnswer": "After a long journey, the crew landed.",
        "isCorrect": False,
        "pointsAwarded": 0,
        "maxPoints": 1,
        "explanation": "When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma."
    },
    {
        "questionId": "Q_Y5_ENG_006",
        "questionText": "True or False: In the sentence \"The USSR launched Sputnik I in 1957.\", we must put a comma before \"in 1957\".",
        "studentAnswer": "False",
        "correctAnswer": "False",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "When the adverbial is at the END of a sentence, NO comma is needed."
    },
    {
        "questionId": "Q_Y5_ENG_007",
        "questionText": "Choose the sentence that has an adverbial of TIME at the beginning:",
        "studentAnswer": "Before sunrise, the pilot took off.",
        "correctAnswer": "Before sunrise, the pilot took off.",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"Before sunrise\" tells us WHEN the pilot took off."
    },
    {
        "questionId": "Q_Y5_ENG_008",
        "questionText": "Complete the sentence with the best adverbial of manner: \"The engineer repaired the delicate wiring ........\"",
        "studentAnswer": "with great care",
        "correctAnswer": "with great care",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"with great care\" describes HOW the engineer repaired the wires."
    },
    {
        "questionId": "Q_Y5_ENG_009",
        "questionText": "Rewrite \"Astronauts walked on the moon in 1969.\" by moving the adverbial of time to the start:",
        "studentAnswer": "In 1969, astronauts walked on the moon.",
        "correctAnswer": "In 1969, astronauts walked on the moon.",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Move \"In 1969\" to the front and place a comma directly after it."
    },
    {
        "questionId": "Q_Y5_ENG_010",
        "questionText": "Which sentence has BOTH an adverbial of time AND an adverbial of place?",
        "studentAnswer": "In 1969, astronauts walked on the moon.",
        "correctAnswer": "In 1969, astronauts walked on the moon.",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"In 1969\" is Time, and \"on the moon\" is Place."
    }
]

escaped_json = json.dumps(real_review).replace('"', '\\"')

# Pattern for sampleSubmissions
sample_sub_pattern = r"const sampleSubmissions = \[\s*\[[\s\S]*?\]\s*\];"
new_sample_sub = f"""const sampleSubmissions = [
    [
      Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm'),
      'Ali Ahmed',
      'Year 5 (G5)',
      'EX_Y5_ENG_ADV01',
      9,
      10,
      '90%',
      'Excellent 🌟',
      '7 min 42 sec',
      '9/10 Correct (1 mistake reviewed)',
      "{escaped_json}"
    ]
  ];"""

code_content = re.sub(sample_sub_pattern, new_sample_sub, code_content)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code_content)
print("Code.gs updated successfully.")

# 2. Update Index.html
index_path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Enhance renderStudentSubmissions in Index.html
old_render_subs_pattern = r"function renderStudentSubmissions\(subs\) \{[\s\S]*?\}\s*function setupInspectorChips"

new_render_subs = """function renderStudentSubmissions(subs) {
      const container = document.getElementById('admin-submissions-container');
      if (subs.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 30px; color: var(--text-muted);">No submissions recorded for this student yet.</div>';
        return;
      }

      container.innerHTML = '';
      subs.forEach((s, sIdx) => {
        const card = document.createElement('div');
        card.style = 'background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 18px; margin-bottom: 14px; box-shadow: var(--shadow-sm);';
        
        let detailsHtml = '';
        if (s.review && s.review.length > 0) {
          s.review.forEach((r, idx) => {
            const isCorrect = r.isCorrect === true || r.isCorrect === 'true';
            detailsHtml += `
              <div style="font-size: 0.84rem; padding: 10px 12px; margin-top: 8px; border-radius: 8px; background: ${isCorrect ? '#f8fafc' : '#fef2f2'}; border-left: 4px solid ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
                <div style="font-weight: 700; color: var(--text-main); margin-bottom: 4px;">
                  Q${idx + 1}: ${r.questionText}
                </div>
                <div style="font-size: 0.82rem; margin-top: 3px; display: flex; gap: 14px; flex-wrap: wrap;">
                  <span style="color: ${isCorrect ? 'var(--success)' : 'var(--danger)'}; font-weight: 700;">
                    ${isCorrect ? '✓ Correct Choice: ' + (r.studentAnswer || '(Completed)') : '✗ Student Chose: ' + (r.studentAnswer || '(None)')}
                  </span>
                  ${!isCorrect ? `<span style="color: #047857; font-weight: 700;">✓ Correct Answer: ${r.correctAnswer}</span>` : ''}
                </div>
                ${r.explanation ? `<div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 5px; line-height: 1.4;">💡 <strong>Rule Explanation:</strong> ${r.explanation}</div>` : ''}
              </div>
            `;
          });
        } else {
          detailsHtml = `<div style="font-size: 0.82rem; color: var(--text-muted); padding: 10px;">Detailed answers logged in linked Google Sheet. Click 'Open Google Sheet' in the top right to inspect.</div>`;
        }

        const isLatest = sIdx === 0;
        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
            <div>
              <div style="font-size: 1.05rem; font-weight: 800; color: var(--primary);">${s.examCode}</div>
              <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">⏱️ Duration: <strong>${s.durationSpent}</strong> &bull; 📅 Date: ${s.timestamp}</div>
            </div>
            <div style="font-size: 0.95rem; font-weight: 800; padding: 6px 14px; border-radius: 8px; background: #ecfdf5; color: #047857;">
              ${s.earnedScore} / ${s.totalScore} (${s.percentage}) &bull; ${s.rating}
            </div>
          </div>
          <details ${isLatest ? 'open' : ''} style="margin-top: 8px; border-top: 1px solid #f1f5f9; padding-top: 8px;">
            <summary style="font-weight: 700; color: var(--accent); cursor: pointer; padding: 6px 0; font-size: 0.88rem; display: flex; justify-content: space-between; align-items: center;">
              <span>🔍 View Full Question & Answer Breakdown (${(s.review || []).length} Questions)</span>
              <span style="font-size: 0.75rem; text-decoration: underline; font-weight: 600;">(Click to collapse/expand)</span>
            </summary>
            <div style="margin-top: 10px;">${detailsHtml}</div>
          </details>
        `;
        container.appendChild(card);
      });
    }

    function setupInspectorChips"""

index_content = re.sub(old_render_subs_pattern, new_render_subs, index_content)

# Add a direct "🔐 Parent Portal" button inside the student header bar if not present
student_bar_target = '<button class="portal-btn" onclick="returnToGateway()">'
if 'onclick="openParentPortal()"' not in index_content[index_content.find('student-header-bar'):index_content.find('student-header-bar') + 400]:
    index_content = index_content.replace(
        student_bar_target,
        '<button class="portal-btn" onclick="openParentPortal()" style="margin-right: 6px;">🔐 Parent Portal</button>\n            ' + student_bar_target
    )

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_content)
print("Index.html updated successfully.")
