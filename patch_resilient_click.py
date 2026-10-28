# -*- coding: utf-8 -*-

with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Code.gs doGet to use createHtmlOutputFromFile
with open(r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs", "r", encoding="utf-8") as f_code:
    code_gs = f_code.read()

old_doget = """function doGet(e) {
  const examCode = (e && e.parameter && e.parameter.exam) ? e.parameter.exam : '';
  const student = (e && e.parameter && e.parameter.student) ? e.parameter.student.toLowerCase() : '';
  const admin = (e && e.parameter && e.parameter.admin === '1') ? '1' : '0';
  
  const template = HtmlService.createTemplateFromFile('Index');
  template.examCode = examCode;
  template.initialStudent = student;
  template.initialAdmin = admin;
  template.driveVideos = JSON.stringify(getDriveVideosMap());
  
  return template.evaluate()
    .setTitle('Manaret El-Eman Assessment Portal')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}"""

new_doget = """function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Manaret El-Eman Assessment Portal')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}"""

if old_doget in code_gs:
    code_gs = code_gs.replace(old_doget, new_doget)
    with open(r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs", "w", encoding="utf-8") as f_out:
        f_out.write(code_gs)
    print("Updated Code.gs doGet to pure createHtmlOutputFromFile.")
else:
    print("old_doget not found directly in Code.gs")

# 2. In Index.html, give IDs to gateway cards:
old_ali_btn = '<button type="button" class="gateway-card" onclick="openStudentPortal(\'ali\')">'
new_ali_btn = '<button type="button" id="btn-gateway-ali" class="gateway-card" onclick="openStudentPortal(\'ali\')">'
if old_ali_btn in html:
    html = html.replace(old_ali_btn, new_ali_btn)
    print("Added id btn-gateway-ali.")

old_mostafa_btn = '<button type="button" class="gateway-card" onclick="openStudentPortal(\'mostafa\')">'
new_mostafa_btn = '<button type="button" id="btn-gateway-mostafa" class="gateway-card" onclick="openStudentPortal(\'mostafa\')">'
if old_mostafa_btn in html:
    html = html.replace(old_mostafa_btn, new_mostafa_btn)
    print("Added id btn-gateway-mostafa.")

# 3. Remove early initPortalNavigation call from line 140
early_init = """    function initPortalNavigation() {
      try {
        const params = new URLSearchParams(window.location.search);
        const studentParam = params.get('student');
        const adminParam = params.get('admin');
        const examParam = params.get('exam');

        if (adminParam === '1') {
          openParentPortal();
          return;
        }

        if (studentParam === 'ali') {
          openStudentPortal('ali', examParam);
        } else if (studentParam === 'mostafa') {
          openStudentPortal('mostafa', examParam);
        } else {
          showScreen('screen-gateway');
        }
      } catch (err) {
        console.error('Portal init error:', err);
        showScreen('screen-gateway');
      }
    }

    if (document.readyState === 'loading') {
      window.addEventListener('DOMContentLoaded', initPortalNavigation);
    } else {
      initPortalNavigation();
    }"""

if early_init in html:
    html = html.replace(early_init, "")
    print("Removed early initPortalNavigation from top of script.")

# 4. Add global function exports, universal event delegation, and bottom initPortalNavigation
resilient_glue = """
    /* ============================================================
     * RESILIENT EVENT DELEGATION & GLOBAL WINDOW EXPORTS
     * Ensures all clicks work in sandboxed iframes & under strict CSP
     * ============================================================ */
    window.openStudentPortal = openStudentPortal;
    window.openParentPortal = openParentPortal;
    window.showScreen = showScreen;
    window.returnToGateway = returnToGateway;
    window.selectStudentExam = selectStudentExam;
    window.startAssessment = startAssessment;
    window.loadAndStartQuiz = loadAndStartQuiz;
    window.openLessonSummaryModal = openLessonSummaryModal;
    window.openVideoModal = openVideoModal;
    window.closeVideoModal = closeVideoModal;
    window.closeLessonSummaryModal = closeLessonSummaryModal;
    window.syncColigoCloudNowAction = syncColigoCloudNowAction;
    window.setupColigoTriggerAction = setupColigoTriggerAction;
    window.loadColigoHubItemsAction = loadColigoHubItemsAction;
    window.filterColigoHubItems = filterColigoHubItems;
    window.switchVideoModalView = switchVideoModalView;
    window.switchSummaryTab = switchSummaryTab;
    window.toggleSummaryAns = toggleSummaryAns;
    window.toggleRefresherBody = toggleRefresherBody;
    window.filterPlanByWeek = filterPlanByWeek;
    window.filterInspectorByExam = filterInspectorByExam;
    window.switchAdminNav = switchAdminNav;
    window.createWeeklyExamAction = createWeeklyExamAction;
    window.createMonthlyExamAction = createMonthlyExamAction;
    window.createMistakesReviewAction = createMistakesReviewAction;
    window.launchTodayMission = launchTodayMission;

    // Global click delegation fallback (immune to inline onclick blocking)
    document.addEventListener('click', function(e) {
      // Gateway Ali
      const aliBtn = e.target.closest('#btn-gateway-ali');
      if (aliBtn) {
        e.preventDefault();
        openStudentPortal('ali');
        return;
      }

      // Gateway Mostafa
      const mosBtn = e.target.closest('#btn-gateway-mostafa');
      if (mosBtn) {
        e.preventDefault();
        openStudentPortal('mostafa');
        return;
      }

      // Parent Portal
      const parentBtn = e.target.closest('#btn-parent-portal-link');
      if (parentBtn) {
        e.preventDefault();
        openParentPortal();
        return;
      }
    });

    // Safe Bottom Initialization (All variables & functions guaranteed loaded)
    function initPortalNavigation() {
      try {
        const params = new URLSearchParams(window.location.search);
        const studentParam = params.get('student');
        const adminParam = params.get('admin');
        const examParam = params.get('exam');

        if (adminParam === '1') {
          openParentPortal();
          return;
        }

        if (studentParam === 'ali') {
          openStudentPortal('ali', examParam);
        } else if (studentParam === 'mostafa') {
          openStudentPortal('mostafa', examParam);
        } else {
          showScreen('screen-gateway');
        }
      } catch (err) {
        console.error('Portal init error:', err);
        showScreen('screen-gateway');
      }
    }

    if (document.readyState === 'loading') {
      window.addEventListener('DOMContentLoaded', initPortalNavigation);
    } else {
      initPortalNavigation();
    }
"""

if "window.openStudentPortal = openStudentPortal" not in html:
    html = html.replace('</script>', resilient_glue + '\n</script>')
    print("Appended resilient glue and bottom initialization.")

with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "w", encoding="utf-8") as f_out:
    f_out.write(html)

print("Saved updated Index.html.")
