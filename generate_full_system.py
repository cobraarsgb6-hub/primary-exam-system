# -*- coding: utf-8 -*-
"""
Full System Generator:
- Code.gs with Retake_Requests table and Approval API
- Index.html with Request Retake button & Parent Approval Actions
- Clean 30 questions (10 Ali English, 10 Mostafa English, 10 Mostafa Arabic)
- No Science exam
"""

import csv
import json

# 1. Read clean questions from Question_Bank.csv
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

header = rows[0]
questions_data = rows[1:]

formatted_questions = []
for r in questions_data:
    qid = r[0]
    grade = r[1]
    subject = r[2]
    lesson = r[3]
    text = r[4]
    qtype = r[5]
    options = r[6]
    correct = r[7]
    points = int(r[8]) if r[8].isdigit() else 1
    explanation = r[9]
    exam_code = r[10]

    formatted_questions.append(
        f"    [{json.dumps(qid, ensure_ascii=False)}, {json.dumps(grade, ensure_ascii=False)}, {json.dumps(subject, ensure_ascii=False)}, {json.dumps(lesson, ensure_ascii=False)}, {json.dumps(text, ensure_ascii=False)}, {json.dumps(qtype, ensure_ascii=False)}, {json.dumps(options, ensure_ascii=False)}, {json.dumps(correct, ensure_ascii=False)}, {points}, {json.dumps(explanation, ensure_ascii=False)}, {json.dumps(exam_code, ensure_ascii=False)}]"
    )

questions_js_array = ",\n".join(formatted_questions)

sample_exams_js = """    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'نشط', '', new Date()],
    ['EX_Y6_ENG_FANTASY01', 'Grade 6 English: Fantasy Reading "The City That Waited" & Grammar', 'Grade 6 (G6)', 'English Literacy', 10, 20, 'نشط', '', new Date()],
    ['EX_Y6_ARB_PRIO01', 'الصف السادس - لغة عربية: القراءة المتحررة، النكرة والمعرفة، والهمزة المتوسطة', 'Grade 6 (G6)', 'اللغة العربية', 10, 20, 'نشط', '', new Date()]"""

code_gs = f"""/**
 * ============================================================
 * منظومة بنك الأسئلة والامتحانات التفاعلية - الصف الخامس والسادس
 * Primary School Question Bank & Assessment System (G5 & G6)
 * المدارس الدولية: منارة الإيمان (Ali Ahmed & Mostafa Ahmed)
 * ============================================================
 */

function getSpreadsheet() {{
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  if (ss) return ss;

  const props = PropertiesService.getUserProperties();
  const savedId = props.getProperty('LINKED_SHEET_ID');
  if (savedId) {{
    try {{
      ss = SpreadsheetApp.openById(savedId);
      if (ss) return ss;
    }} catch(e) {{
      Logger.log('تعذر فتح الشيت بالمعرف المحفوظ: ' + e);
    }}
  }}

  // إنشاء شيت جديد وتخزين معرفه
  ss = SpreadsheetApp.create('منظومة امتحانات الابتدائي - الصف الخامس والسادس');
  props.setProperty('LINKED_SHEET_ID', ss.getId());
  setupDatabase(ss);
  return ss;
}}

function onOpen() {{
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎯 إدارة الامتحانات والتقييم')
    .addItem('⚙️ إعادة تهيئة بنك الأسئلة بالكامل', 'setupDatabase')
    .addItem('📝 إنشاء Google Form من امتحان', 'generateGoogleFormPrompt')
    .addSeparator()
    .addItem('🔗 نسخ رابط منصة الطلاب التفاعلية', 'copyWebAppUrl')
    .addItem('📊 فتح رابط الشيت المربوط', 'openLinkedSheetUrl')
    .addToUi();
}}

function setupDatabase(targetSs) {{
  const ss = (targetSs && targetSs.getSheetByName) ? targetSs : getSpreadsheet();

  // 1. جدول بنك الأسئلة (Question_Bank)
  let qbSheet = ss.getSheetByName('Question_Bank');
  if (!qbSheet) {{
    qbSheet = ss.insertSheet('Question_Bank');
  }}
  qbSheet.clear();
  const qbHeaders = [
    ['كود السؤال', 'الصف الدراسي', 'المادة', 'الوحدة / الدرس', 'نص السؤال', 'نوع السؤال', 'الخيارات (مفصولة بـ |)', 'الإجابة النموذجية', 'الدرجة', 'التفسير ونفي الشبهة والشرح الشامل', 'كود الامتحان المرتبط']
  ];
  qbSheet.getRange(1, 1, 1, qbHeaders[0].length).setValues(qbHeaders);
  formatHeaderRow(qbSheet, '#1e3a8a');

  const sampleQuestions = [
{questions_js_array}
  ];
  qbSheet.getRange(2, 1, sampleQuestions.length, sampleQuestions[0].length).setValues(sampleQuestions);
  qbSheet.autoResizeColumns(1, qbHeaders[0].length);

  // 2. جدول الامتحانات (Exams)
  let exSheet = ss.getSheetByName('Exams');
  if (!exSheet) {{
    exSheet = ss.insertSheet('Exams');
  }}
  exSheet.clear();
  const exHeaders = [
    ['كود الامتحان', 'عنوان الامتحان', 'الصف الدراسي', 'المادة', 'عدد الأسئلة', 'المدة (دقائق)', 'الحالة', 'رابط الحل للطلاب', 'تاريخ الإنشاء']
  ];
  exSheet.getRange(1, 1, 1, exHeaders[0].length).setValues(exHeaders);
  formatHeaderRow(exSheet, '#047857');

  const sampleExams = [
{sample_exams_js}
  ];
  exSheet.getRange(2, 1, sampleExams.length, sampleExams[0].length).setValues(sampleExams);
  exSheet.autoResizeColumns(1, exHeaders[0].length);

  // 3. جدول نتائج الطلاب (Submissions)
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {{
    subSheet = ss.insertSheet('Submissions');
  }}
  if (subSheet.getLastRow() === 0) {{
    const subHeaders = [
      ['وقت التسليم', 'اسم الطالب', 'المدرسة / المجموعة', 'كود الامتحان', 'الدرجة المحصلة', 'الدرجة الكلية', 'النسبة المئوية', 'التقدير', 'المدة المستغرقة', 'تفاصيل الإجابات']
    ];
    subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
    formatHeaderRow(subSheet, '#b45309');
    subSheet.autoResizeColumns(1, subHeaders[0].length);
  }}

  // 4. جدول طلبات إعادة المحاولة والموافقة (Retake_Requests)
  let retakeSheet = ss.getSheetByName('Retake_Requests');
  if (!retakeSheet) {{
    retakeSheet = ss.insertSheet('Retake_Requests');
  }}
  if (retakeSheet.getLastRow() === 0) {{
    const retakeHeaders = [
      ['كود الطلب', 'وقت الطلب', 'اسم الطالب', 'كود الامتحان', 'عنوان الامتحان', 'الدرجة السابقة', 'حالة الطلب', 'سبب الطلب', 'وقت اتخاذ القرار']
    ];
    retakeSheet.getRange(1, 1, 1, retakeHeaders[0].length).setValues(retakeHeaders);
    formatHeaderRow(retakeSheet, '#7c3aed'); // Purple
    retakeSheet.autoResizeColumns(1, retakeHeaders[0].length);
  }}

  try {{
    SpreadsheetApp.getUi().alert('✅ تم بنجاح تهيئة بنك الأسئلة والامتحانات وجدول طلبات الإعادة!');
  }} catch(e) {{
    Logger.log('Database initialized successfully.');
  }}
}}

function formatHeaderRow(sheet, bgColor) {{
  const range = sheet.getRange(1, 1, 1, sheet.getLastColumn());
  range.setBackground(bgColor)
       .setFontColor('#ffffff')
       .setFontWeight('bold')
       .setHorizontalAlignment('center')
       .setVerticalAlignment('middle');
  sheet.setRowHeight(1, 40);
  sheet.setFrozenRows(1);
}}

// ============================================================
// 2. محرك واجهة الويب للطالب (Web App: doGet)
// ============================================================

function doGet(e) {{
  const examCode = (e && e.parameter && e.parameter.exam) ? e.parameter.exam : '';
  const student = (e && e.parameter && e.parameter.student) ? e.parameter.student.toLowerCase() : '';
  const admin = (e && e.parameter && e.parameter.admin === '1') ? '1' : '0';
  
  const template = HtmlService.createTemplateFromFile('Index');
  template.examCode = examCode;
  template.initialStudent = student;
  template.initialAdmin = admin;
  
  return template.evaluate()
    .setTitle('Primary Assessment Portal - Manaret El-Eman')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}}

function getExamData(examCode) {{
  const ss = getSpreadsheet();
  let exSheet = ss.getSheetByName('Exams');
  let qbSheet = ss.getSheetByName('Question_Bank');

  if (!exSheet || !qbSheet) {{
    setupDatabase(ss);
    exSheet = ss.getSheetByName('Exams');
    qbSheet = ss.getSheetByName('Question_Bank');
  }}

  const exData = exSheet.getDataRange().getValues();
  let examInfo = null;
  for (let i = 1; i < exData.length; i++) {{
    if (String(exData[i][0]).trim() === examCode) {{
      examInfo = {{
        code: exData[i][0],
        title: exData[i][1],
        grade: exData[i][2],
        subject: exData[i][3],
        questionsCount: exData[i][4],
        duration: exData[i][5],
        status: exData[i][6]
      }};
      break;
    }}
  }}

  if (!examInfo && exData.length > 1) {{
    examInfo = {{
      code: exData[1][0],
      title: exData[1][1],
      grade: exData[1][2],
      subject: exData[1][3],
      questionsCount: exData[1][4],
      duration: exData[1][5],
      status: exData[1][6]
    }};
    examCode = examInfo.code;
  }}

  if (!examInfo) {{
    return {{ success: false, message: 'لم يتم العثور على الامتحان المطلوب' }};
  }}

  const qbData = qbSheet.getDataRange().getValues();
  const questions = [];

  for (let i = 1; i < qbData.length; i++) {{
    const row = qbData[i];
    const qExamCode = String(row[10]).trim();
    if (qExamCode === examCode || examCode === 'ALL') {{
      let optionsList = [];
      if (row[6]) {{
        optionsList = String(row[6]).split('|').map(opt => opt.trim()).filter(Boolean);
      }}

      questions.push({{
        id: row[0],
        grade: row[1],
        subject: row[2],
        unit: row[3],
        text: row[4],
        type: row[5],
        options: optionsList,
        points: row[8] || 1
      }});
    }}
  }}

  return {{
    success: true,
    exam: examInfo,
    questions: questions
  }};
}}

function submitExamAnswers(payload) {{
  try {{
    const ss = getSpreadsheet();
    const qbSheet = ss.getSheetByName('Question_Bank');
    const subSheet = ss.getSheetByName('Submissions');
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    const data = (typeof payload === 'string') ? JSON.parse(payload) : payload;
    const {{ studentName, schoolGroup, examCode, answers, durationSpent }} = data;

    const qbData = qbSheet.getDataRange().getValues();
    const answerKey = {{}};
    for (let i = 1; i < qbData.length; i++) {{
      const qId = String(qbData[i][0]).trim();
      answerKey[qId] = {{
        correctAnswer: String(qbData[i][7] || '').trim(),
        points: Number(qbData[i][8]) || 1,
        explanation: String(qbData[i][9] || '').trim(),
        text: qbData[i][4]
      }};
    }}

    let earnedScore = 0;
    let totalScore = 0;
    const reviewDetails = [];

    for (const qId in answers) {{
      const studentAns = String(answers[qId] || '').trim();
      const meta = answerKey[qId] || {{ correctAnswer: '', points: 1, explanation: '', text: '' }};
      
      const isCorrect = (studentAns.toLowerCase() === meta.correctAnswer.toLowerCase());
      if (isCorrect) {{
        earnedScore += meta.points;
      }}
      totalScore += meta.points;

      reviewDetails.push({{
        questionId: qId,
        questionText: meta.text,
        studentAnswer: studentAns,
        correctAnswer: meta.correctAnswer,
        isCorrect: isCorrect,
        pointsAwarded: isCorrect ? meta.points : 0,
        maxPoints: meta.points,
        explanation: meta.explanation
      }});
    }}

    const percentage = totalScore > 0 ? Math.round((earnedScore / totalScore) * 100) : 0;
    
    let rating = 'يحتاج إلى تحسين 🌱';
    if (percentage >= 85) rating = 'ممتاز 🌟';
    else if (percentage >= 75) rating = 'جيد جداً 👏';
    else if (percentage >= 65) rating = 'جيد 👍';
    else if (percentage >= 50) rating = 'مقبول 📚';

    const timestamp = new Date();
    subSheet.appendRow([
      timestamp,
      studentName,
      schoolGroup || 'عام',
      examCode,
      earnedScore,
      totalScore,
      percentage + '%',
      rating,
      durationSpent || 'غير محدد',
      JSON.stringify(reviewDetails)
    ]);

    // إذا كانت هذه محاولة معتمدة مسبقاً، نقوم بتحديث حالة الطلب إلى CONSUMED
    if (retakeSheet && retakeSheet.getLastRow() > 1) {{
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = 1; i < rData.length; i++) {{
        if (rData[i][2] === studentName && rData[i][3] === examCode && rData[i][6] === 'APPROVED') {{
          retakeSheet.getRange(i + 1, 7).setValue('CONSUMED');
        }}
      }}
    }}

    return {{
      success: true,
      earnedScore: earnedScore,
      totalScore: totalScore,
      percentage: percentage,
      rating: rating,
      review: reviewDetails
    }};

  }} catch (err) {{
    return {{
      success: false,
      message: 'حدث خطأ أثناء رصد الإجابات: ' + err.toString()
    }};
  }}
}}

// ============================================================
// 3. نظام طلب المحاولة الثانية والموافقة عليها (Retake Workflow)
// ============================================================

/**
 * فحص حالة الطالب للامتحان (هل سبق الحل وهل يوجد طلب إعادة معتمد)
 */
function getStudentExamStatus(studentName, examCode) {{
  try {{
    const ss = getSpreadsheet();
    const subSheet = ss.getSheetByName('Submissions');
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    let hasSubmitted = false;
    let lastScore = '';
    let lastDate = '';

    if (subSheet && subSheet.getLastRow() > 1) {{
      const sData = subSheet.getDataRange().getValues();
      for (let i = sData.length - 1; i >= 1; i--) {{
        if (String(sData[i][1]).trim() === studentName && String(sData[i][3]).trim() === examCode) {{
          hasSubmitted = true;
          lastScore = sData[i][4] + ' / ' + sData[i][5] + ' (' + sData[i][6] + ')';
          lastDate = sData[i][0] instanceof Date ? Utilities.formatDate(sData[i][0], Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm') : String(sData[i][0]);
          break;
        }}
      }}
    }}

    let retakeStatus = 'NONE';
    let requestId = '';

    if (retakeSheet && retakeSheet.getLastRow() > 1) {{
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = rData.length - 1; i >= 1; i--) {{
        if (String(rData[i][2]).trim() === studentName && String(rData[i][3]).trim() === examCode) {{
          retakeStatus = String(rData[i][6]).trim(); // PENDING, APPROVED, REJECTED, CONSUMED
          requestId = String(rData[i][0]).trim();
          break;
        }}
      }}
    }}

    // يمكن للطالب الدخول إذا: لم يسبق له الحل، أو إذا وافق والده وحالة الطلب APPROVED
    const canAttempt = (!hasSubmitted) || (retakeStatus === 'APPROVED');

    return {{
      success: true,
      hasSubmitted: hasSubmitted,
      lastScore: lastScore,
      lastDate: lastDate,
      canAttempt: canAttempt,
      retakeStatus: retakeStatus,
      requestId: requestId
    }};
  }} catch(e) {{
    return {{ success: false, message: e.toString() }};
  }}
}}

/**
 * إرسال طلب محاولة ثانية من الطالب إلى ولي الأمر
 */
function requestExamRetake(payload) {{
  try {{
    const ss = getSpreadsheet();
    let retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet) {{
      setupDatabase(ss);
      retakeSheet = ss.getSheetByName('Retake_Requests');
    }}

    const data = (typeof payload === 'string') ? JSON.parse(payload) : payload;
    const {{ studentName, examCode, examTitle, previousScore, reason }} = data;

    const reqId = 'REQ_' + Utilities.formatDate(new Date(), 'GMT', 'yyyyMMdd_HHmmss');
    const timestamp = new Date();

    retakeSheet.appendRow([
      reqId,
      timestamp,
      studentName,
      examCode,
      examTitle || examCode,
      previousScore || 'غير متوفر',
      'PENDING',
      reason || 'طلب محاولة ثانية لتحسين النتيجة',
      ''
    ]);

    return {{
      success: true,
      requestId: reqId,
      message: 'تم إرسال طلب المحاولة بنجاح إلى ولي الأمر!'
    }};
  }} catch(e) {{
    return {{ success: false, message: 'فشل إرسال الطلب: ' + e.toString() }};
  }}
}}

/**
 * موافقة ولي الأمر على طلب الإعادة
 */
function approveRetakeRequest(requestId) {{
  try {{
    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) return {{ success: false, message: 'لا توجد طلبات' }};

    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {{
      if (String(data[i][0]).trim() === requestId) {{
        retakeSheet.getRange(i + 1, 7).setValue('APPROVED');
        retakeSheet.getRange(i + 1, 9).setValue(new Date());
        return {{ success: true, message: 'تمت الموافقة بنجاح على إعادة الامتحان للطالب!' }};
      }}
    }}
    return {{ success: false, message: 'لم يتم العثور على كود الطلب' }};
  }} catch(e) {{
    return {{ success: false, message: e.toString() }};
  }}
}}

/**
 * رفض ولي الأمر لطلب الإعادة
 */
function rejectRetakeRequest(requestId) {{
  try {{
    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) return {{ success: false, message: 'لا توجد طلبات' }};

    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {{
      if (String(data[i][0]).trim() === requestId) {{
        retakeSheet.getRange(i + 1, 7).setValue('REJECTED');
        retakeSheet.getRange(i + 1, 9).setValue(new Date());
        return {{ success: true, message: 'تم رفض طلب الإعادة' }};
      }}
    }}
    return {{ success: false, message: 'لم يتم العثور على كود الطلب' }};
  }} catch(e) {{
    return {{ success: false, message: e.toString() }};
  }}
}}

// ============================================================
// 4. لوحة تحكم ولي الأمر الشاملة (Parent Dashboard Data)
// ============================================================

function getAdminDashboardData() {{
  try {{
    const ss = getSpreadsheet();
    const subSheet = ss.getSheetByName('Submissions');
    const exSheet = ss.getSheetByName('Exams');
    const qbSheet = ss.getSheetByName('Question_Bank');
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    const submissions = [];
    if (subSheet && subSheet.getLastRow() > 1) {{
      const data = subSheet.getDataRange().getValues();
      for (let i = 1; i < data.length; i++) {{
        let review = [];
        try {{
          review = JSON.parse(data[i][9] || '[]');
        }} catch(e) {{}}

        const rawDate = data[i][0];
        let dateStr = '';
        if (rawDate instanceof Date) {{
          dateStr = Utilities.formatDate(rawDate, Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
        }} else {{
          dateStr = String(rawDate || '');
        }}

        submissions.push({{
          id: i,
          timestamp: dateStr,
          studentName: String(data[i][1] || 'Unknown'),
          schoolGroup: String(data[i][2] || ''),
          examCode: String(data[i][3] || ''),
          earnedScore: Number(data[i][4]) || 0,
          totalScore: Number(data[i][5]) || 0,
          percentage: String(data[i][6] || '0%'),
          rating: String(data[i][7] || ''),
          durationSpent: String(data[i][8] || ''),
          review: review
        }});
      }}
      submissions.reverse();
    }}

    const exams = [];
    if (exSheet && exSheet.getLastRow() > 1) {{
      const data = exSheet.getDataRange().getValues();
      for (let i = 1; i < data.length; i++) {{
        exams.push({{
          code: String(data[i][0] || ''),
          title: String(data[i][1] || ''),
          grade: String(data[i][2] || ''),
          subject: String(data[i][3] || ''),
          questionsCount: Number(data[i][4]) || 0,
          duration: Number(data[i][5]) || 0,
          status: String(data[i][6] || 'نشط')
        }});
      }}
    }}

    // All Question Bank details for the Parent / Teacher Inspector
    const allQuestions = [];
    if (qbSheet && qbSheet.getLastRow() > 1) {{
      const qbData = qbSheet.getDataRange().getValues();
      for (let i = 1; i < qbData.length; i++) {{
        const row = qbData[i];
        let opts = [];
        if (row[6]) {{
          opts = String(row[6]).split('|').map(o => o.trim()).filter(Boolean);
        }}
        allQuestions.push({{
          id: String(row[0] || ''),
          grade: String(row[1] || ''),
          subject: String(row[2] || ''),
          lesson: String(row[3] || ''),
          text: String(row[4] || ''),
          type: String(row[5] || 'MCQ'),
          options: opts,
          correctAnswer: String(row[7] || ''),
          points: Number(row[8]) || 1,
          explanation: String(row[9] || ''),
          examCode: String(row[10] || '')
        }});
      }}
    }}

    // Retake Requests list
    const retakeRequests = [];
    if (retakeSheet && retakeSheet.getLastRow() > 1) {{
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = 1; i < rData.length; i++) {{
        const rawDate = rData[i][1];
        let dateStr = '';
        if (rawDate instanceof Date) {{
          dateStr = Utilities.formatDate(rawDate, Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
        }} else {{
          dateStr = String(rawDate || '');
        }}

        retakeRequests.push({{
          id: String(rData[i][0] || ''),
          timestamp: dateStr,
          studentName: String(rData[i][2] || ''),
          examCode: String(rData[i][3] || ''),
          examTitle: String(rData[i][4] || ''),
          previousScore: String(rData[i][5] || ''),
          status: String(rData[i][6] || 'PENDING'),
          reason: String(rData[i][7] || '')
        }});
      }}
      retakeRequests.reverse();
    }}

    return {{
      success: true,
      sheetUrl: ss.getUrl(),
      submissions: submissions,
      exams: exams,
      allQuestions: allQuestions,
      retakeRequests: retakeRequests
    }};

  }} catch (err) {{
    return {{
      success: false,
      message: 'خطأ في جلب بيانات لوحة التحكم: ' + err.toString()
    }};
  }}
}}

function generateGoogleFormPrompt() {{
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('إنشاء Google Form تلقائياً', 'أدخل كود الامتحان (مثال: EX_Y5_ENG_ADV01 أو EX_Y6_ENG_FANTASY01):', ui.ButtonSet.OK_CANCEL);
  
  if (response.getSelectedButton() === ui.Button.OK) {{
    const examCode = response.getResponseText().trim();
    if (!examCode) {{
      ui.alert('يرجى إدخال كود الامتحان!');
      return;
    }}
    createGoogleFormFromExam(examCode);
  }}
}}

function createGoogleFormFromExam(examCode) {{
  const examDataRes = getExamData(examCode);
  if (!examDataRes.success || examDataRes.questions.length === 0) {{
    try {{ SpreadsheetApp.getUi().alert('تعذر العثور على أسئلة لهذا الكود: ' + examCode); }} catch(e){{}}
    return;
  }}

  const exam = examDataRes.exam;
  const questions = examDataRes.questions;

  const form = FormApp.create(exam.title + ' - (' + exam.grade + ')');
  form.setDescription('امتحان تفاعلي لمادة: ' + exam.subject + '\\nزمن الاختبار: ' + exam.duration + ' دقيقة\\nأجب عن جميع الأسئلة بعناية.')
      .setIsQuiz(true)
      .setAllowResponseEdits(false)
      .setCollectEmail(false);

  form.addTextItem().setTitle('اسم الطالب بالكامل:').setRequired(true);
  form.addTextItem().setTitle('المدرسة / المجموعة:').setRequired(false);

  questions.forEach((q, idx) => {{
    const qTitle = '(' + (idx + 1) + ') ' + q.text;
    if (q.type === 'MCQ' || q.type === 'TRUE_FALSE') {{
      const item = form.addMultipleChoiceItem().setTitle(qTitle).setRequired(true);
      const choices = q.options.map(opt => item.createChoice(opt));
      item.setChoices(choices);
    }} else {{
      form.addTextItem().setTitle(qTitle).setRequired(true);
    }}
  }});

  const publishedUrl = form.getPublishedUrl();
  try {{
    SpreadsheetApp.getUi().alert('🎉 تم إنشاء Google Form بنجاح!\\n\\nرابط حل الطلاب:\\n' + publishedUrl);
  }} catch(e) {{
    Logger.log('Form created: ' + publishedUrl);
  }}
}}

function copyWebAppUrl() {{
  const url = ScriptApp.getService().getUrl();
  try {{
    SpreadsheetApp.getUi().alert('🔗 رابط منصة الاختبارات التفاعلية:\\n\\n' + (url || 'يرجى نشر السكريبت كـ Web App أولاً'));
  }} catch(e) {{
    Logger.log(url);
  }}
}}

function openLinkedSheetUrl() {{
  const ss = getSpreadsheet();
  try {{
    SpreadsheetApp.getUi().alert('📊 رابط الشيت المربوط:\\n\\n' + ss.getUrl());
  }} catch(e) {{
    Logger.log(ss.getUrl());
  }}
}}
"""

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'w', encoding='utf-8') as f:
    f.write(code_gs)

print("Code.gs generated successfully with Retake Request & Approval APIs!")
