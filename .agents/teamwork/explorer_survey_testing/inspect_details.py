import re
import csv

all_28 = [
    'DAILY_Y5_ENG_W1D1', 'DAILY_Y5_ENG_W1D2', 'DAILY_Y5_ENG_W1D3', 'DAILY_Y5_ENG_W1D4',
    'DAILY_Y5_ENG_W1D5', 'DAILY_Y5_ENG_W1D6', 'DAILY_Y5_ENG_W2D8', 'DAILY_Y5_ENG_W2D9',
    'DAILY_Y5_ENG_W2D10', 'EX_Y5_ENG_W1', 'EX_Y5_ENG_W2_CUMULATIVE', 'EX_Y5_ENG_W3_CUMULATIVE',
    'EX_Y5_ENG_W4_CUMULATIVE', 'EX_Y5_ENG_M1_CAPSTONE', 'EX_Y5_ENG_ADV01',
    'DAILY_Y6_ARB_W1D4', 'DAILY_Y6_ARB_W1D5', 'DAILY_Y6_ARB_W1D6', 'DAILY_Y6_ARB_W2D8',
    'DAILY_Y6_ARB_W2D9', 'DAILY_Y6_ARB_W2D10', 'EX_Y6_ARB_W1', 'EX_Y6_ARB_W2_CUMULATIVE',
    'EX_Y6_ARB_W3_CUMULATIVE', 'EX_Y6_ARB_W4_CUMULATIVE', 'EX_Y6_ARB_M1_CAPSTONE',
    'EX_Y6_ARB_PRIO01', 'EX_Y6_ENG_FANTASY01'
]

# Check presence in Exams.csv
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Exams.csv', 'r', encoding='utf-8') as f:
    ex_csv_codes = set(row[0] for row in csv.reader(f))

# Check presence in Question_Bank.csv
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv', 'r', encoding='utf-8') as f:
    qb_csv_codes = set(row[10] for row in csv.reader(f) if len(row) > 10)

# Check presence in Code.gs
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'r', encoding='utf-8') as f:
    code_gs = f.read()

# Check presence in Index.html
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

print(f"{'Exam Code':<26} | In Exams.csv | In QB.csv | In Code.gs | In Index.html")
print("-" * 75)
for code in all_28:
    in_ex = 'YES' if code in ex_csv_codes else 'MISSING'
    in_qb = 'YES' if code in qb_csv_codes else 'MISSING'
    in_gs = 'YES' if code in code_gs else 'MISSING'
    in_html = 'YES' if code in index_html else 'MISSING'
    print(f"{code:<26} | {in_ex:<12} | {in_qb:<9} | {in_gs:<10} | {in_html:<13}")
