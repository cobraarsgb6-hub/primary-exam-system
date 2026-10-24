# -*- coding: utf-8 -*-
"""
Rebuild Code.gs to be 100% Clean English backend (ratings, messages, logs),
with strict student isolation and clean retake workflow.
"""

import csv
import json

# Read clean questions
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

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

questions_js = ",\n".join(formatted_questions)

sample_exams_js = """    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'ACTIVE', '', new Date()],
    ['EX_Y6_ENG_FANTASY01', 'Grade 6 English: Fantasy Reading "The City That Waited" & Grammar', 'Grade 6 (G6)', 'English Literacy', 10, 20, 'ACTIVE', '', new Date()],
    ['EX_Y6_ARB_PRIO01', 'Grade 6 Arabic: Reading Comprehension, Grammar & Spelling (Diagnostic)', 'Grade 6 (G6)', 'Arabic Language', 10, 20, 'ACTIVE', '', new Date()]"""

code_gs = f"""/**
 * ============================================================
 * Primary School Question Bank & Assessment System (G5 & G6)
 * Manaret El-Eman International School (Ali Ahmed & Mostafa Ahmed)
 * Pure English Architecture & Dedicated Student Separation
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
      Logger.log('Could not open sheet with saved ID: ' + e);
    }}
  }}

  // Create new dedicated sheet and store ID
  ss = SpreadsheetApp.create('Manaret El-Eman - Assessment Platform Database');
  props.setProperty('LINKED_SHEET_ID', ss.getId());
  setupDatabase(ss);
  return ss;
}}

function onOpen() {{
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎯 Assessment Management')
    .addItem('⚙️ Reset & Reinitialize Database', 'setupDatabase')
    .addItem('📝 Generate Google Form from Exam', 'generateGoogleFormPrompt')
    .addSeparator()
    .addItem('🔗 Copy Interactive Web App URL', 'copyWebAppUrl')
    .addItem('📊 Open Linked Google Sheet', 'openLinkedSheetUrl')
    .addToUi();
}}

function setupDatabase(targetSs) {{
  const ss = (targetSs && targetSs.getSheetByName) ? targetSs : getSpreadsheet();

  // 1. Question_Bank Sheet
  let qbSheet = ss.getSheetByName('Question_Bank');
  if (!qbSheet) {{
    qbSheet = ss.insertSheet('Question_Bank');
  }}
  qbSheet.clear();
  const qbHeaders = [
    ['Question ID', 'Grade Level', 'Subject', 'Unit / Lesson', 'Question Text', 'Question Type', 'Options (delimited by |)', 'Correct Answer', 'Points', 'Pedagogical Explanation & Mistake Breakdown', 'Exam Code']
  ];
  qbSheet.getRange(1, 1, 1, qbHeaders[0].length).setValues(qbHeaders);
  formatHeaderRow(qbSheet, '#1e3a8a');

  const sampleQuestions = [
{questions_js}
  ];
  qbSheet.getRange(2, 1, sampleQuestions.length, sampleQuestions[0].length).setValues(sampleQuestions);
  qbSheet.autoResizeColumns(1, qbHeaders[0].length);

  // 2. Exams Sheet
  let exSheet = ss.getSheetByName('Exams');
  if (!exSheet) {{
    exSheet = ss.insertSheet('Exams');
  }}
  exSheet.clear();
  const exHeaders = [
    ['Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Question Count', 'Duration (Mins)', 'Status', 'Direct Link', 'Created Date']
  ];
  exSheet.getRange(1, 1, 1, exHeaders[0].length).setValues(exHeaders);
  formatHeaderRow(exSheet, '#047857');

  const sampleExams = [
{sample_exams_js}
  ];
  exSheet.getRange(2, 1, sampleExams.length, sampleExams[0].length).setValues(sampleExams);
  exSheet.autoResizeColumns(1, exHeaders[0].length);

  // 3. Submissions Sheet
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {{
    subSheet = ss.insertSheet('Submissions');
  }}
  if (subSheet.getLastRow() === 0) {{
    const subHeaders = [
      ['Submission Timestamp', 'Student Name', 'School Group', 'Exam Code', 'Score Earned', 'Total Points', 'Percentage', 'Rating', 'Duration Spent', 'Review Details JSON']
    ];
    subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
    formatHeaderRow(subSheet, '#b45309');
    subSheet.autoResizeColumns(1, subHeaders[0].length);
  }}

  // 4. Retake_Requests Sheet
  let retakeSheet = ss.getSheetByName('Retake_Requests');
  if (!retakeSheet) {{
    retakeSheet = ss.insertSheet('Retake_Requests');
  }}
  if (retakeSheet.getLastRow() === 0) {{
    const retakeHeaders = [
      ['Request ID', 'Timestamp', 'Student Name', 'Exam Code', 'Exam Title', 'Previous Score', 'Status', 'Reason', 'Decision Timestamp']
    ];
    retakeSheet.getRange(1, 1, 1, retakeHeaders[0].length).setValues(retakeHeaders);
    formatHeaderRow(retakeSheet, '#7c3aed');
    retakeSheet.autoResizeColumns(1, retakeHeaders[0].length);
  }}

  try {{
    SpreadsheetApp.getUi().alert('✅ Database initialized successfully with clean English schemas.');
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

function doGet(e) {{
  const examCode = (e && e.parameter && e.parameter.exam) ? e.parameter.exam : '';
  const student = (e && e.parameter && e.parameter.student) ? e.parameter.student.toLowerCase() : '';
  const admin = (e && e.parameter && e.parameter.admin === '1') ? '1' : '0';
  
  const template = HtmlService.createTemplateFromFile('Index');
  template.examCode = examCode;
  template.initialStudent = student;
  template.initialAdmin = admin;
  
  return template.evaluate()
    .setTitle('Manaret El-Eman Assessment Portal')
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
    return {{ success: false, message: 'Requested assessment was not found.' }};
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
    
    let rating = 'Needs Practice 🌱';
    if (percentage >= 85) rating = 'Excellent 🌟';
    else if (percentage >= 75) rating = 'Very Good 👏';
    else if (percentage >= 65) rating = 'Good 👍';
    else if (percentage >= 50) rating = 'Satisfactory 📚';

    const timestamp = new Date();
    subSheet.appendRow([
      timestamp,
      studentName,
      schoolGroup || 'General',
      examCode,
      earnedScore,
      totalScore,
      percentage + '%',
      rating,
      durationSpent || 'Not specified',
      JSON.stringify(reviewDetails)
    ]);

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
      message: 'Failed to record student answers: ' + err.toString()
    }};
  }}
}}

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
          retakeStatus = String(rData[i][6]).trim();
          requestId = String(rData[i][0]).trim();
          break;
        }}
      }}
    }}

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
      previousScore || 'N/A',
      'PENDING',
      reason || 'Second attempt requested to review mistakes',
      ''
    ]);

    return {{
      success: true,
      requestId: reqId,
      message: 'Retake request sent to parent dashboard successfully.'
    }};
  }} catch(e) {{
    return {{ success: false, message: 'Failed to send retake request: ' + e.toString() }};
  }}
}}

function approveRetakeRequest(requestId) {{
  try {{
    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) return {{ success: false, message: 'No retake requests found' }};

    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {{
      if (String(data[i][0]).trim() === requestId) {{
        retakeSheet.getRange(i + 1, 7).setValue('APPROVED');
        retakeSheet.getRange(i + 1, 9).setValue(new Date());
        return {{ success: true, message: 'Retake approved. The student can now start their assessment.' }};
      }}
    }}
    return {{ success: false, message: 'Request ID not found' }};
  }} catch(e) {{
    return {{ success: false, message: e.toString() }};
  }}
}}

function rejectRetakeRequest(requestId) {{
  try {{
    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) return {{ success: false, message: 'No retake requests found' }};

    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {{
      if (String(data[i][0]).trim() === requestId) {{
        retakeSheet.getRange(i + 1, 7).setValue('REJECTED');
        retakeSheet.getRange(i + 1, 9).setValue(new Date());
        return {{ success: true, message: 'Retake request declined.' }};
      }}
    }}
    return {{ success: false, message: 'Request ID not found' }};
  }} catch(e) {{
    return {{ success: false, message: e.toString() }};
  }}
}}

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
          status: String(data[i][6] || 'ACTIVE')
        }});
      }}
    }}

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
      message: 'Error loading admin data: ' + err.toString()
    }};
  }}
}}

function generateGoogleFormPrompt() {{
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('Generate Google Form', 'Enter Exam Code (e.g., EX_Y5_ENG_ADV01 or EX_Y6_ENG_FANTASY01):', ui.ButtonSet.OK_CANCEL);
  
  if (response.getSelectedButton() === ui.Button.OK) {{
    const examCode = response.getResponseText().trim();
    if (!examCode) {{
      ui.alert('Please enter an exam code.');
      return;
    }}
    createGoogleFormFromExam(examCode);
  }}
}}

function createGoogleFormFromExam(examCode) {{
  const examDataRes = getExamData(examCode);
  if (!examDataRes.success || examDataRes.questions.length === 0) {{
    try {{ SpreadsheetApp.getUi().alert('No questions found for code: ' + examCode); }} catch(e){{}}
    return;
  }}

  const exam = examDataRes.exam;
  const questions = examDataRes.questions;

  const form = FormApp.create(exam.title + ' - (' + exam.grade + ')');
  form.setDescription('Interactive Assessment for ' + exam.subject + '\\nDuration: ' + exam.duration + ' Minutes\\nPlease complete all questions carefully.')
      .setIsQuiz(true)
      .setAllowResponseEdits(false)
      .setCollectEmail(false);

  form.addTextItem().setTitle('Student Full Name:').setRequired(true);
  form.addTextItem().setTitle('School / Class:').setRequired(false);

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
    SpreadsheetApp.getUi().alert('🎉 Google Form created successfully!\\n\\nStudent link:\\n' + publishedUrl);
  }} catch(e) {{
    Logger.log('Form created: ' + publishedUrl);
  }}
}}

function copyWebAppUrl() {{
  const url = ScriptApp.getService().getUrl();
  try {{
    SpreadsheetApp.getUi().alert('Interactive Web App Link:\\n\\n' + (url || 'Please deploy script as Web App first.'));
  }} catch(e) {{
    Logger.log(url);
  }}
}}

function openLinkedSheetUrl() {{
  const ss = getSpreadsheet();
  try {{
    SpreadsheetApp.getUi().alert('Linked Google Sheet URL:\\n\\n' + ss.getUrl());
  }} catch(e) {{
    Logger.log(ss.getUrl());
  }}
}}
"""

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'w', encoding='utf-8') as f:
    f.write(code_gs)

print("Clean English Code.gs generated successfully.")
