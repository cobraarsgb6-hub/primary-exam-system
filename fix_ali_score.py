# -*- coding: utf-8 -*-
"""
Correct Ali Ahmed's score from 10/10 to 9/10 (90%) in Code.gs.
"""

import json
import re

# 9 Correct, 1 Incorrect (Q5 on comma after fronted adverbial)
ali_review = []
for i in range(1, 11):
    if i == 5:
        ali_review.append({
            "questionId": "Q_Y5_ENG_005",
            "questionText": "Which sentence is punctuated correctly with a comma after the fronted adverbial?",
            "studentAnswer": "After a long journey the rover touched down.",
            "correctAnswer": "After a long journey, the rover touched down.",
            "isCorrect": False,
            "pointsAwarded": 0,
            "maxPoints": 1,
            "explanation": "💡 Comma Rule: Remember that a fronted adverbial at the start of a sentence must always be followed by a comma."
        })
    else:
        ali_review.append({
            "questionId": f"Q_Y5_ENG_{i:03d}",
            "questionText": f"Adverbials Concept Question {i}",
            "studentAnswer": "Correct Option",
            "correctAnswer": "Correct Option",
            "isCorrect": True,
            "pointsAwarded": 1,
            "maxPoints": 1,
            "explanation": "Correctly identified adverbial concept."
        })

ali_review_json = json.dumps(ali_review)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace 10, 10, '100%' with 9, 10, '90%'
target_sub = """      'EX_Y5_ENG_ADV01',
      10,
      10,
      '100%',
      'Excellent 🌟',
      '7 min 42 sec',
      '10/10 Correct (All questions answered correctly)',"""

replacement_sub = f"""      'EX_Y5_ENG_ADV01',
      9,
      10,
      '90%',
      'Excellent 🌟',
      '7 min 42 sec',
      '9/10 Correct (1 mistake reviewed)',"""

code = code.replace(target_sub, replacement_sub)

# Update the review JSON in sampleSubmissions
sample_sub_pattern = r"(\['[^']+',\s*'Ali Ahmed',\s*'Year 5 \(G5\)',\s*'EX_Y5_ENG_ADV01',\s*9,\s*10,\s*'90%',\s*'Excellent 🌟',\s*'7 min 42 sec',\s*'9/10 Correct[^']*',\s*)(.*?)(?=\s*\]\s*\];)"

def repl_sub(m):
    return m.group(1) + json.dumps(ali_review_json)

code = re.sub(sample_sub_pattern, repl_sub, code, flags=re.DOTALL)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Code.gs successfully updated with Ali's exact 9/10 score!")
