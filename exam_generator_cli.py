#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 Primary 5 & 6 Exam Generator CLI & Google Sheets Bridge
-----------------------------------------------------------
أداة مساعدة لتوليد وتجهيز بنوك الأسئلة والامتحانات للصفين الخامس والسادس الابتدائي،
وتصديرها بصيغة جاهزة للاستيراد المباشر إلى Google Sheets.
"""

import os
import json
import csv
import sys
import unicodedata

def normalize_text(text: str) -> str:
    """تطبيع النصوص العربية والأرقام والتخلص من المحارف الشاذة (NFKC)"""
    if not text:
        return ""
    return unicodedata.normalize('NFKC', str(text)).strip()

# بنك أسئلة نموذجي جاهز للاستخدام الفوري
SAMPLE_CURRICULUM_DATA = [
    # --- الصف الخامس - علوم ---
    {
        "id": "Q_P5_SCI_001",
        "grade": "الصف الخامس",
        "subject": "علوم",
        "unit": "المفهوم الأول: احتياجات النبات",
        "text": "يمتص النبات غاز ........ من الهواء الجوي لصنع غذائه بنفسه في عملية البناء الضوئي.",
        "type": "MCQ",
        "options": ["الأكسجين", "ثاني أكسيد الكربون", "النيتروجين", "الهيدروجين"],
        "correct": "ثاني أكسيد الكربون",
        "points": 1,
        "explanation": "يمتص النبات غاز ثاني أكسيد الكربون عبر فتحات الثغور المنتشرة على الأوراق.",
        "exam_code": "EX_P5_SCI_01"
    },
    {
        "id": "Q_P5_SCI_002",
        "grade": "الصف الخامس",
        "subject": "علوم",
        "unit": "المفهوم الأول: احتياجات النبات",
        "text": "تنتقل المياه والعناصر الغذائية من الجذور إلى الأوراق عبر أوعية الخشب.",
        "type": "TRUE_FALSE",
        "options": ["صح", "خطأ"],
        "correct": "صح",
        "points": 1,
        "explanation": "أوعية الخشب متخصصة في نقل الماء والأملاح صعوداً من الجذر إلى الساق والأوراق.",
        "exam_code": "EX_P5_SCI_01"
    },
    {
        "id": "Q_P5_SCI_003",
        "grade": "الصف الخامس",
        "subject": "علوم",
        "unit": "المفهوم الثاني: سلاسل الغذاء",
        "text": "تبدأ جميع السلاسل الغذائية بكائن ........",
        "type": "MCQ",
        "options": ["مستهلك أول", "محلل", "منتج للغذاء", "مفترس"],
        "correct": "منتج للغذاء",
        "points": 1,
        "explanation": "النبات الأخضر والطحالب كائنات منتجة تعتمد على ضوء الشمس لصنع طاقتها وتعتبر قاعدة السلسلة الغذائية.",
        "exam_code": "EX_P5_SCI_01"
    },

    # --- الصف الخامس - رياضيات ---
    {
        "id": "Q_P5_MATH_001",
        "grade": "الصف الخامس",
        "subject": "رياضيات",
        "unit": "الوحدة الأولى: الكسور العشرية",
        "text": "العدد العشري 3.456 مقرباً لأقرب جزء من مئة هو:",
        "type": "MCQ",
        "options": ["3.4", "3.45", "3.46", "3.5"],
        "correct": "3.46",
        "points": 1,
        "explanation": "خانة الجزء من ألف تحتوي على الرقم 6 (أكبر من أو يساوي 5)، لذا نضيف 1 إلى خانة الجزء من مئة (5 تصبح 6).",
        "exam_code": "EX_P5_MATH_01"
    },
    {
        "id": "Q_P5_MATH_002",
        "grade": "الصف الخامس",
        "subject": "رياضيات",
        "unit": "الوحدة الأولى: الكسور العشرية",
        "text": "قيمة الرقم 7 في العدد العشري 12.375 هي 0.07",
        "type": "TRUE_FALSE",
        "options": ["صح", "خطأ"],
        "correct": "صح",
        "points": 1,
        "explanation": "الرقم 7 يقع في خانة الجزء من مئة، وبالتالي قيمته المكانية هي سبعة أجزاء من مئة (0.07).",
        "exam_code": "EX_P5_MATH_01"
    },

    # --- الصف السادس - علوم ---
    {
        "id": "Q_P6_SCI_001",
        "grade": "الصف السادس",
        "subject": "علوم",
        "unit": "المفهوم الأول: الخلية كنظام",
        "text": "مركز التحكم الرئيسي في الخلية والمسؤول عن انقسامها وتكاثرها هو ........",
        "type": "MCQ",
        "options": ["الغشاء البلازمي", "الميتوكوندريا", "النواة", "السيتوبلازم"],
        "correct": "النواة",
        "points": 1,
        "explanation": "النواة تحتوي على المادة الوراثية وتدير كافة الوظائف الحيوية وعمليات الانقسام الخلوي.",
        "exam_code": "EX_P6_SCI_01"
    },
    {
        "id": "Q_P6_SCI_002",
        "grade": "الصف السادس",
        "subject": "علوم",
        "unit": "المفهوم الأول: الخلية كنظام",
        "text": "تعتبر الميتوكوندريا هي محطة توليد الطاقة في الخلية.",
        "type": "TRUE_FALSE",
        "options": ["صح", "خطأ"],
        "correct": "صح",
        "points": 1,
        "explanation": "تحدث عملية التنفس الخلوي داخل الميتوكوندريا لتحويل السكر إلى طاقة كيميائية قابلة للاستخدام.",
        "exam_code": "EX_P6_SCI_01"
    },

    # --- الصف السادس - لغة عربية ---
    {
        "id": "Q_P6_ARB_001",
        "grade": "الصف السادس",
        "subject": "لغة عربية",
        "unit": "قواعد النحو: الأسماء الخمسة",
        "text": "إن ........ ذو علم وخلق رفيع. (اختر الكلمة الصحيحة إعرابياً)",
        "type": "MCQ",
        "options": ["أباك", "أبوك", "أبيك", "أبوكا"],
        "correct": "أباك",
        "points": 1,
        "explanation": "اسم إن يكون منصوباً، والأسماء الخمسة تُنصب بالألف (أباك).",
        "exam_code": "EX_P6_ARB_01"
    }
]

def export_question_bank_csv(output_path: str = "Question_Bank.csv"):
    """تصدير الأسئلة إلى ملف CSV متوافق تماماً مع Google Sheets"""
    headers = [
        "معرف السؤال", "الصف الدراسي", "المادة", "الوحدة / الدرس", 
        "نص السؤال", "نوع السؤال", "الخيارات (مفصولة بـ |)", 
        "الإجابة الصحيحة", "الدرجة", "الشرح والتوضيح", "كود الامتحان"
    ]
    
    with open(output_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for q in SAMPLE_CURRICULUM_DATA:
            writer.writerow([
                normalize_text(q["id"]),
                normalize_text(q["grade"]),
                normalize_text(q["subject"]),
                normalize_text(q["unit"]),
                normalize_text(q["text"]),
                normalize_text(q["type"]),
                " | ".join([normalize_text(opt) for opt in q["options"]]),
                normalize_text(q["correct"]),
                q["points"],
                normalize_text(q["explanation"]),
                normalize_text(q["exam_code"])
            ])
    print(f"✅ تم تصدير بنك الأسئلة بنجاح إلى: {output_path}")

def export_exams_registry_csv(output_path: str = "Exams.csv"):
    """تصدير سجل الامتحانات المعتمدة"""
    headers = [
        "كود الامتحان", "عنوان الامتحان", "الصف الدراسي", "المادة", 
        "عدد الأسئلة", "المدة (دقائق)", "الحالة", "رابط الحل للطلاب", "تاريخ الإنشاء"
    ]
    exams = [
        ["EX_P5_SCI_01", "اختبار المفهوم الأول: احتياجات النبات وسلاسل الغذاء", "الصف الخامس", "علوم", 3, 15, "نشط", "", "2026-10-24"],
        ["EX_P5_MATH_01", "اختبار الكسور العشرية والقيمة المكانية", "الصف الخامس", "رياضيات", 2, 15, "نشط", "", "2026-10-24"],
        ["EX_P6_SCI_01", "اختبار الوحدة الأولى: الخلية كنظام ومكوناتها", "الصف السادس", "علوم", 2, 15, "نشط", "", "2026-10-24"],
        ["EX_P6_ARB_01", "اختبار النحو: الأسماء الخمسة وإن وأخواتها", "الصف السادس", "لغة عربية", 1, 10, "نشط", "", "2026-10-24"]
    ]
    with open(output_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in exams:
            writer.writerow([normalize_text(item) for item in row])
    print(f"✅ تم تصدير سجل الامتحانات بنجاح إلى: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qb_file = os.path.join(base_dir, "Question_Bank.csv")
    ex_file = os.path.join(base_dir, "Exams.csv")
    
    export_question_bank_csv(qb_file)
    export_exams_registry_csv(ex_file)
    print("\n🎉 تم إنشاء كافة ملفات البيانات بنجاح!")
