# -*- coding: utf-8 -*-
import json
import re

print("Patching Index.html with UI stability, real analytics, and daily missions...")

with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update STUDENT_DATA starter exams
ali_exams = [
    {"code": "DAILY_Y5_ENG_W1D5", "title": "Ali - Day 5: Compound Adverbials (Today's Mission)", "subject": "English Grammar", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y5_ENG_W1D1", "title": "Ali - Day 1: Adverbs of Manner", "subject": "English Grammar", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y5_ENG_W1D2", "title": "Ali - Day 2: Adverbials of Time", "subject": "English Grammar", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y5_ENG_W1D3", "title": "Ali - Day 3: Adverbials of Place", "subject": "English Grammar", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y5_ENG_W1D4", "title": "Ali - Day 4: Fronted Adverbials & Commas", "subject": "English Grammar", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y5_ENG_W1D6", "title": "Ali - Day 6: Sentence Repair & Error Hunting", "subject": "English Grammar", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "EX_Y5_ENG_W1", "title": "Ali - Week 1 Milestone: Adverbials Mastery", "subject": "English Grammar", "count": 10, "duration": 20, "period": "W1", "type": "Weekly"},
    {"code": "EX_Y5_ENG_W2_CUMULATIVE", "title": "Ali - Week 2 Cumulative Exam (W1 + W2 Balanced)", "subject": "English Grammar", "count": 12, "duration": 25, "period": "W2", "type": "Cumulative"},
    {"code": "EX_Y5_ENG_W3_CUMULATIVE", "title": "Ali - Week 3 Cumulative Exam (W1 + W2 + W3)", "subject": "English Grammar", "count": 15, "duration": 30, "period": "W3", "type": "Cumulative"},
    {"code": "EX_Y5_ENG_M1_CAPSTONE", "title": "Ali - Month 1 Comprehensive Capstone Exam", "subject": "English Grammar", "count": 20, "duration": 40, "period": "M1", "type": "Monthly"}
]

mostafa_exams = [
    {"code": "DAILY_Y6_ARB_W1D5", "title": "Mostafa - Day 5: النكرة والمعرفة (مهمة اليوم)", "subject": "اللغة العربية", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y6_ARB_W1D4", "title": "Mostafa - Day 4: إدارة الوقت وترتيب الأولويات", "subject": "اللغة العربية", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "DAILY_Y6_ARB_W1D6", "title": "Mostafa - Day 6: الهمزة المتوسطة على ألف", "subject": "اللغة العربية", "count": 5, "duration": 10, "period": "W1", "type": "Daily"},
    {"code": "EX_Y6_ARB_W1", "title": "Mostafa - Week 1 Milestone: لغة عربية", "subject": "اللغة العربية", "count": 10, "duration": 20, "period": "W1", "type": "Weekly"},
    {"code": "DAILY_Y6_ARB_W2D8", "title": "Mostafa - Day 8: أنواع الخبر (المفرد)", "subject": "اللغة العربية", "count": 5, "duration": 10, "period": "W2", "type": "Daily"},
    {"code": "DAILY_Y6_ARB_W2D9", "title": "Mostafa - Day 9: أنواع الخبر (الجملة وشبه الجملة)", "subject": "اللغة العربية", "count": 5, "duration": 10, "period": "W2", "type": "Daily"},
    {"code": "DAILY_Y6_ARB_W2D10", "title": "Mostafa - Day 10: الهمزة المتوسطة على واو", "subject": "اللغة العربية", "count": 5, "duration": 10, "period": "W2", "type": "Daily"},
    {"code": "EX_Y6_ARB_W2_CUMULATIVE", "title": "Mostafa - Week 2 Cumulative Exam (W1 + W2)", "subject": "اللغة العربية", "count": 12, "duration": 25, "period": "W2", "type": "Cumulative"},
    {"code": "EX_Y6_ARB_W3_CUMULATIVE", "title": "Mostafa - Week 3 Cumulative Exam (W1 + W2 + W3)", "subject": "اللغة العربية", "count": 15, "duration": 30, "period": "W3", "type": "Cumulative"},
    {"code": "EX_Y6_ARB_M1_CAPSTONE", "title": "Mostafa - Month 1 Comprehensive Capstone Exam", "subject": "اللغة العربية", "count": 20, "duration": 40, "period": "M1", "type": "Monthly"}
]

new_student_data = f"""    const STUDENT_DATA = {{
      'ali': {{
        name: 'Ali Ahmed',
        grade: 'Year 5 (G5)',
        exams: {json.dumps(ali_exams, ensure_ascii=False, indent=8)}
      }},
      'mostafa': {{
        name: 'Mostafa Ahmed',
        grade: 'Grade 6 (G6)',
        exams: {json.dumps(mostafa_exams, ensure_ascii=False, indent=8)}
      }}
    }};"""

html = re.sub(
    r"const STUDENT_DATA = \{[\s\S]*?'mostafa': \{[\s\S]*?\}\s*\}\s*\};",
    new_student_data,
    html,
    count=1
)

# 2. Fix openStudentPortal: Preserve active exam selection, do NOT reset to first exam!
new_open_student_portal = """    /* STUDENT PORTAL LOGIC (100% ISOLATED & STABLE) */
    function openStudentPortal(studentKey, preferredExamCode) {
      currentStudentKey = studentKey;
      initTodayMission(studentKey);
      const student = STUDENT_DATA[studentKey];
      if (!student) {
        showScreen('screen-gateway');
        return;
      }

      document.getElementById('sp-student-title').innerText = `${student.name}'s Assessment Portal`;
      document.getElementById('sp-student-grade').innerText = `${student.grade} • International School`;

      // Determine initial selection: keep activeExamCode if already valid for this student, else preferred, else first
      let selectedCode = activeExamCode;
      if (!selectedCode || !student.exams.some(ex => ex.code === selectedCode)) {
        selectedCode = (preferredExamCode && student.exams.some(ex => ex.code === preferredExamCode))
          ? preferredExamCode
          : (student.exams[0] ? student.exams[0].code : '');
      }

      function renderExamCards() {
        const listEl = document.getElementById('sp-exams-list');
        if (!listEl) return;
        listEl.innerHTML = '';
        student.exams.forEach((ex) => {
          const card = document.createElement('button');
          card.type = 'button';
          card.className = 'exam-item-card' + (ex.code === activeExamCode ? ' active' : '');
          card.id = 'exam-item-' + ex.code;
          card.innerHTML = `
            <div>
              <div class="exam-item-title">${escapeHtml(ex.title)}</div>
              <div class="exam-item-meta">${escapeHtml(ex.subject)} &bull; ${ex.count || 10} Questions &bull; ${ex.duration || 20} Mins</div>
            </div>
            <span class="exam-item-tag">${escapeHtml(ex.period || ex.type || student.grade)}</span>
          `;
          card.addEventListener('click', () => {
            selectStudentExam(ex.code);
          });
          listEl.appendChild(card);
        });
      }

      renderExamCards();
      selectStudentExam(selectedCode);
      showScreen('screen-student');

      // Asynchronously fetch any new server-side exams without overwriting selection
      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(res => {
            if (res && res.success && Array.isArray(res.exams) && res.exams.length > 0) {
              const existingCodes = {};
              student.exams.forEach(e => { existingCodes[e.code] = true; });
              let addedAny = false;
              res.exams.forEach(se => {
                if (!existingCodes[se.code]) {
                  student.exams.push(se);
                  existingCodes[se.code] = true;
                  addedAny = true;
                }
              });
              if (addedAny) {
                renderExamCards();
                // Crucial fix: NEVER reset to index 0! Keep activeExamCode
                if (activeExamCode && student.exams.some(e => e.code === activeExamCode)) {
                  selectStudentExam(activeExamCode);
                }
              }
              if (res.driveVideos) window.DRIVE_VIDEOS = res.driveVideos;
            }
          })
          .getStudentAvailableExams(studentKey);
      }
    }"""

html = re.sub(
    r"function openStudentPortal\(studentKey, preferredExamCode\) \{[\s\S]*?\.getStudentAvailableExams\(studentKey\);\s*\}\s*\}",
    new_open_student_portal,
    html,
    count=1
)

# 3. Fix selectStudentExam to toggle active class properly
new_select_exam = """    function selectStudentExam(code) {
      if (!code) return;
      activeExamCode = code;
      const student = STUDENT_DATA[currentStudentKey];
      if (!student) return;
      const exam = student.exams.find(e => e.code === code) || student.exams[0];
      if (!exam) return;

      activeExamCode = exam.code;

      // Update card visual selection
      document.querySelectorAll('.exam-item-card').forEach(c => {
        c.classList.toggle('active', c.id === ('exam-item-' + exam.code));
      });

      const heroTitle = document.getElementById('sp-hero-title');
      const heroSubject = document.getElementById('sp-hero-subject');
      const heroDuration = document.getElementById('sp-hero-duration');
      const heroCount = document.getElementById('sp-hero-count');

      if (heroTitle) heroTitle.innerText = exam.title;
      if (heroSubject) heroSubject.innerText = exam.subject;
      if (heroDuration) heroDuration.innerText = exam.duration;
      if (heroCount) heroCount.innerText = exam.count;

      renderConceptRefresher(exam.code);
      checkExamStatus(student.name, exam.code);
    }"""

html = re.sub(
    r"function selectStudentExam\(code\) \{[\s\S]*?checkExamStatus\(student\.name, exam\.code\);\s*\}",
    new_select_exam,
    html,
    count=1
)

# 4. Fix launchTodayMission: ACTUALLY START the mission immediately!
new_launch_mission = """    function launchTodayMission() {
      if (!currentTodayMission || !currentTodayMission.examCode) return;
      selectStudentExam(currentTodayMission.examCode);
      // Immediately open the assessment prompt modal for zero-friction launch
      promptStartConfirmation();
    }"""

html = re.sub(
    r"function launchTodayMission\(\) \{[\s\S]*?if \(actionBox\) actionBox\.scrollIntoView[\s\S]*?\}",
    new_launch_mission,
    html,
    count=1
)

# 5. Fix renderAnalyticsUI: REAL ANALYTICS CALCULATIONS
new_analytics_ui = """    function renderAnalyticsUI() {
      const isAli = (activeAdminStudent === 'Ali');
      const titleEl = document.getElementById('ana-student-title');
      const badgeEl = document.getElementById('ana-student-badge');
      const contentEl = document.getElementById('ana-report-content');

      if (titleEl) {
        titleEl.innerText = isAli
          ? '📊 Diagnostic Evaluation Report • Ali Ahmed'
          : '📊 Diagnostic Evaluation Report • Mostafa Ahmed';
      }
      if (badgeEl) {
        badgeEl.innerText = isAli ? 'Year 5 (G5) • Cambridge Curriculum' : 'Grade 6 (G6) • Dual Curriculum';
        badgeEl.className = 'meta-pill ' + (isAli ? 'pill-indigo' : 'pill-green');
      }

      if (!contentEl) return;

      const targetName = isAli ? 'ali ahmed' : 'mostafa ahmed';
      const subs = (cachedAdminData && cachedAdminData.submissions)
        ? cachedAdminData.submissions.filter(s => String(s.studentName || '').trim().toLowerCase() === targetName)
        : [];

      if (subs.length === 0) {
        contentEl.innerHTML = `
          <div style="background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 12px; padding: 36px 20px; text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 10px;">📋</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #1e293b; margin-bottom: 6px;">
              لا توجد محاولات مسجلة حتى الآن لهذا الطالب
            </div>
            <div style="font-size: 0.88rem; color: #64748b; max-width: 520px; margin: 0 auto; line-height: 1.6;">
              بمجرد أن يبدأ الطالب في أداء المهمة اليومية أو أي من الاختبارات المتاحة، سيقوم النظام تلقائياً بتحليل إجاباته بدقة، واستخراج نسب الإتقان، وتحديد المهارات المكتسبة ونقاط الضعف المعرفية.
            </div>
          </div>
        `;
        return;
      }

      // Compute Real Metrics
      const totalAttempts = subs.length;
      let totalEarned = 0;
      let totalMax = 0;
      const questionStats = {};

      subs.forEach(s => {
        totalEarned += Number(s.earnedScore) || 0;
        totalMax += Number(s.totalScore) || 0;

        if (Array.isArray(s.review)) {
          s.review.forEach(r => {
            const qKey = r.questionText || r.questionId;
            if (!questionStats[qKey]) {
              questionStats[qKey] = {
                text: r.questionText || '',
                correctCount: 0,
                wrongCount: 0,
                explanation: r.explanation || ''
              };
            }
            if (r.isCorrect === true || r.isCorrect === 'true') {
              questionStats[qKey].correctCount++;
            } else {
              questionStats[qKey].wrongCount++;
            }
          });
        }
      });

      const avgPercentage = totalMax > 0 ? Math.round((totalEarned / totalMax) * 100) : 0;
      const latestSub = subs[0];

      // Identify Strengths and Deficiencies
      const strengths = [];
      const deficiencies = [];

      Object.keys(questionStats).forEach(k => {
        const item = questionStats[k];
        if (item.wrongCount === 0 && item.correctCount > 0) {
          strengths.push(item);
        } else if (item.wrongCount > 0) {
          deficiencies.push(item);
        }
      });

      let strengthsHtml = '';
      if (strengths.length > 0) {
        strengthsHtml = strengths.slice(0, 5).map(s => `
          <li style="margin-bottom: 8px;">
            <strong>${escapeHtml(plainText(s.text))}</strong>
            <span style="color: #16a34a; font-weight: 700; margin-left: 6px;">(إتقان تام ${s.correctCount}/${s.correctCount})</span>
          </li>
        `).join('');
      } else {
        strengthsHtml = '<li>جاري تجميع بيانات الأسئلة المتقنة مع استمرار حل التدريبات.</li>';
      }

      let deficienciesHtml = '';
      if (deficiencies.length > 0) {
        deficienciesHtml = deficiencies.slice(0, 5).map(d => `
          <div style="background: #fff; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; border-left: 4px solid #e11d48;">
            <div style="font-weight: 700; color: #9f1239; font-size: 0.88rem;">${escapeHtml(plainText(d.text))}</div>
            <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">
              💡 <strong>التحليل التربوي:</strong> ${escapeHtml(d.explanation || 'يُنصح بإعادة مراجعة هذا المفهوم في الدرس والتركيز على مفتاح الإجابة.')}
            </div>
          </div>
        `).join('');
      } else {
        deficienciesHtml = '<div style="color: #16a34a; font-weight: 700;">🌟 أداء ممتاز! لم تُسجل أي أخطاء متكررة في المحاولات المسجلة.</div>';
      }

      contentEl.innerHTML = `
        <!-- Summary Real KPI Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-bottom: 20px;">
          <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 10px; padding: 14px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #15803d;">${avgPercentage}%</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #166534; margin-top: 2px;">متوسط الدرجات العام (Real Avg)</div>
          </div>
          <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 10px; padding: 14px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #1d4ed8;">${totalAttempts}</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #1e40af; margin-top: 2px;">إجمالي الاختبارات المنجزة</div>
          </div>
          <div style="background: #fffbeb; border: 1.5px solid #fde68a; border-radius: 10px; padding: 14px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #b45309;">${latestSub.percentage}</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #92400e; margin-top: 2px;">آخر نتيجة مسجلة (${latestSub.earnedScore}/${latestSub.totalScore})</div>
          </div>
        </div>

        <!-- Section 1: Demonstrated Strengths -->
        <div style="margin-bottom: 18px; background: #ffffff; border: 1px solid var(--border); border-radius: 10px; padding: 16px;">
          <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1rem; color: #15803d; margin-bottom: 10px;">
            <span>🌟</span> Demonstrated Academic Strengths (أوجه التميز والإتقان الفعلي)
          </div>
          <ul style="font-size: 0.88rem; color: #334155; line-height: 1.7; margin: 0; padding-left: 20px;">
            ${strengthsHtml}
          </ul>
        </div>

        <!-- Section 2: Deficiencies & Root Causes -->
        <div style="margin-bottom: 18px; background: #fff1f2; border: 1.5px solid #fecdd3; border-radius: 10px; padding: 16px;">
          <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1rem; color: #be123c; margin-bottom: 10px;">
            <span>⚠️</span> Targeted Deficiencies & Root Causes (أوجه القصور والتحليل الإدراكي الفعلي)
          </div>
          ${deficienciesHtml}
        </div>
      `;
    }"""

html = re.sub(
    r"function renderAnalyticsUI\(\) \{[\s\S]*?contentEl\.innerHTML = `[\s\S]*?\}\s*\}",
    new_analytics_ui,
    html,
    count=1
)

with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Index.html successfully patched and saved!")
