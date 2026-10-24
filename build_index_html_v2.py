# -*- coding: utf-8 -*-
"""
Generate complete Index.html with Retake Request & Father Approval workflow.
"""

html_content = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <base target="_top">
  <meta charset="UTF-8">
  <title>Primary Assessment Portal - Manaret El-Eman</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --primary-light: #eff6ff;
      --accent: #0ea5e9;
      --success: #10b981;
      --success-bg: #ecfdf5;
      --warning: #f59e0b;
      --warning-bg: #fffbeb;
      --danger: #ef4444;
      --danger-bg: #fef2f2;
      --purple: #7c3aed;
      --purple-bg: #f5f3ff;
      --bg-body: #f8fafc;
      --bg-card: #ffffff;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --border-focus: #3b82f6;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.05);
      --radius: 14px;
      --font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-body);
      color: var(--text-main);
      font-family: var(--font-family);
      line-height: 1.5;
      padding: 16px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .app-container {
      width: 100%;
      max-width: 760px;
      margin: 0 auto;
    }

    /* Top Brand Navigation */
    .top-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 12px 18px;
      background: var(--bg-card);
      border-radius: var(--radius);
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border);
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-icon {
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #2563eb, #0ea5e9);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 10px;
      font-size: 1.25rem;
      font-weight: 800;
    }

    .brand-meta h1 {
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.01em;
    }

    .brand-meta p {
      font-size: 0.76rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    .portal-toggle-btn {
      background: #f1f5f9;
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: 9px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      text-decoration: none;
    }

    .portal-toggle-btn:hover {
      background: #e2e8f0;
      color: var(--primary);
    }

    /* Cards & Containers */
    .card {
      background: var(--bg-card);
      border-radius: var(--radius);
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border);
      padding: 24px;
      margin-bottom: 20px;
    }

    .screen {
      display: none;
      animation: fadeIn 0.25s ease-out forwards;
    }

    .screen.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Student Selector Cards */
    .section-title {
      font-size: 0.88rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 12px;
    }

    .student-chips-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 20px;
    }

    @media (max-width: 500px) {
      .student-chips-grid {
        grid-template-columns: 1fr;
      }
    }

    .chip-btn {
      background: #f8fafc;
      border: 2px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      cursor: pointer;
      text-align: left;
      transition: all 0.18s ease;
      position: relative;
    }

    .chip-btn:hover {
      border-color: #cbd5e1;
      background: #fff;
    }

    .chip-btn.active {
      border-color: var(--primary);
      background: var(--primary-light);
    }

    .chip-name {
      font-size: 1rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .chip-btn.active .chip-name {
      color: var(--primary);
    }

    .chip-grade {
      font-size: 0.78rem;
      color: var(--text-muted);
      font-weight: 600;
      margin-top: 4px;
    }

    .chip-badge {
      display: inline-block;
      margin-top: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
      background: #e2e8f0;
      color: #334155;
    }

    .chip-btn.active .chip-badge {
      background: #dbeafe;
      color: #1e40af;
    }

    /* Assessment Selection Cards */
    .exam-select-card {
      background: #ffffff;
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 10px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }

    .exam-select-card:hover {
      border-color: var(--accent);
      transform: translateY(-1px);
    }

    .exam-select-card.active {
      border-color: var(--primary);
      background: #f0f7ff;
      box-shadow: 0 0 0 1px var(--primary);
    }

    .exam-select-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .exam-select-card.active .exam-select-title {
      color: var(--primary);
    }

    .exam-select-badge {
      font-size: 0.74rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      background: #e0f2fe;
      color: #0369a1;
      white-space: nowrap;
    }

    /* Assessment Hero Info */
    .assessment-hero {
      background: linear-gradient(135deg, #1e3a8a, #2563eb);
      color: #ffffff;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
    }

    .assessment-hero h2 {
      font-size: 1.25rem;
      font-weight: 800;
      margin-bottom: 6px;
    }

    .hero-meta-row {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      font-size: 0.84rem;
      color: #bfdbfe;
      margin-top: 10px;
    }

    .hero-meta-item {
      display: flex;
      align-items: center;
      gap: 5px;
    }

    /* Retake & Single Attempt Alert Boxes */
    .single-attempt-notice {
      background: var(--warning-bg);
      border: 1px solid #fde68a;
      border-left: 4px solid var(--warning);
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 0.84rem;
      color: #92400e;
      margin-bottom: 20px;
      display: flex;
      gap: 10px;
      align-items: flex-start;
    }

    .retake-status-card {
      border-radius: 10px;
      padding: 14px 16px;
      margin-bottom: 18px;
      font-size: 0.88rem;
    }

    .retake-status-card.pending {
      background: var(--warning-bg);
      border: 1.5px solid #fcd34d;
      color: #92400e;
    }

    .retake-status-card.approved {
      background: var(--success-bg);
      border: 1.5px solid #86efac;
      color: #065f46;
    }

    .retake-status-card.rejected {
      background: var(--danger-bg);
      border: 1.5px solid #fca5a5;
      color: #991b1b;
    }

    .retake-status-card.completed {
      background: #f1f5f9;
      border: 1.5px solid var(--border);
      color: var(--text-main);
    }

    /* Buttons */
    .btn-primary {
      width: 100%;
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 15px;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: background 0.15s ease, transform 0.1s ease;
    }

    .btn-primary:hover {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }

    .btn-primary:disabled {
      background: #94a3b8;
      cursor: not-allowed;
      transform: none;
    }

    .btn-purple {
      background: var(--purple);
      color: #fff;
    }
    .btn-purple:hover {
      background: #6d28d9;
    }

    .btn-secondary {
      background: #f1f5f9;
      color: var(--text-main);
      border: 1px solid var(--border);
      padding: 12px;
      border-radius: 10px;
      font-weight: 700;
      cursor: pointer;
    }

    .btn-secondary:hover {
      background: #e2e8f0;
    }

    .btn-success {
      background: var(--success);
      color: #fff;
      border: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.82rem;
      cursor: pointer;
    }
    .btn-success:hover { background: #059669; }

    .btn-danger {
      background: var(--danger);
      color: #fff;
      border: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.82rem;
      cursor: pointer;
    }
    .btn-danger:hover { background: #dc2626; }

    /* Modal Gatekeeper */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 9999;
    }

    .modal-overlay.active {
      display: flex;
      animation: fadeIn 0.2s ease;
    }

    .modal-card {
      background: #fff;
      border-radius: 16px;
      max-width: 480px;
      width: 100%;
      padding: 26px;
      box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.2);
      text-align: center;
    }

    .modal-warning-icon {
      width: 56px;
      height: 56px;
      background: #fef3c7;
      color: #d97706;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.8rem;
      margin: 0 auto 16px;
    }

    .modal-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 8px;
    }

    .modal-desc {
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 20px;
    }

    .modal-highlight-box {
      background: #f8fafc;
      border: 1.5px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      margin-bottom: 20px;
      text-align: left;
      font-size: 0.88rem;
    }

    .modal-highlight-box div { margin-bottom: 4px; }
    .modal-btn-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    /* Quiz Screen Elements */
    .quiz-sticky-header {
      position: sticky;
      top: 10px;
      z-index: 50;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 18px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .quiz-progress-text {
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .quiz-timer {
      font-size: 0.92rem;
      font-weight: 800;
      color: var(--primary);
      background: var(--primary-light);
      padding: 4px 10px;
      border-radius: 8px;
    }

    .progress-bar-container {
      width: 100%;
      height: 6px;
      background: #e2e8f0;
      border-radius: 3px;
      overflow: hidden;
      margin-top: 8px;
    }

    .progress-bar-fill {
      height: 100%;
      background: var(--primary);
      width: 0%;
      transition: width 0.3s ease;
    }

    .question-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 20px;
    }

    .q-meta-tag {
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
      margin-bottom: 8px;
    }

    .q-text {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 20px;
      line-height: 1.6;
    }

    .q-text.rtl-text {
      direction: rtl;
      text-align: right;
      font-family: 'Cairo', sans-serif;
    }

    .options-grid {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .option-item {
      background: #f8fafc;
      border: 1.5px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.15s ease;
      font-size: 0.96rem;
      font-weight: 600;
    }

    .option-item.rtl-opt {
      direction: rtl;
      font-family: 'Cairo', sans-serif;
    }

    .option-item:hover {
      background: #f1f5f9;
      border-color: #cbd5e1;
    }

    .option-item.selected {
      background: #eff6ff;
      border-color: var(--primary);
      color: var(--primary);
    }

    .opt-circle {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 2px solid #cbd5e1;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .option-item.selected .opt-circle {
      border-color: var(--primary);
      background: var(--primary);
    }

    .opt-circle::after {
      content: '';
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #fff;
      display: none;
    }

    .option-item.selected .opt-circle::after {
      display: block;
    }

    .nav-btn-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-top: 24px;
    }

    /* Result Screen */
    .result-score-banner {
      text-align: center;
      padding: 30px 20px;
      background: linear-gradient(135deg, #1e3a8a, #2563eb);
      color: #fff;
      border-radius: var(--radius);
      margin-bottom: 24px;
    }

    .score-circle {
      font-size: 3rem;
      font-weight: 900;
      margin: 10px 0;
    }

    .score-rating {
      font-size: 1.15rem;
      font-weight: 700;
      color: #93c5fd;
    }

    .review-item {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 16px;
    }

    .review-item.correct { border-left: 5px solid var(--success); }
    .review-item.incorrect { border-left: 5px solid var(--danger); }

    .review-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
      gap: 10px;
    }

    .review-q-title {
      font-size: 0.96rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .review-status-badge {
      font-size: 0.74rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      white-space: nowrap;
    }

    .badge-correct { background: var(--success-bg); color: var(--success); }
    .badge-incorrect { background: var(--danger-bg); color: var(--danger); }

    .explanation-box {
      margin-top: 12px;
      padding: 12px 14px;
      background: #f8fafc;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      font-size: 0.86rem;
      line-height: 1.6;
      white-space: pre-wrap;
      color: #334155;
    }

    /* Admin Dashboard */
    .admin-kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }

    .kpi-box {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px;
      text-align: center;
    }

    .kpi-num {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--primary);
      display: block;
    }

    .kpi-label {
      font-size: 0.76rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* Retake Requests Banner in Admin */
    .admin-retake-banner {
      background: var(--purple-bg);
      border: 1.5px solid #c4b5fd;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 20px;
    }

    .admin-retake-title {
      font-size: 0.96rem;
      font-weight: 800;
      color: var(--purple);
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 12px;
    }

    .retake-request-item {
      background: #fff;
      border: 1px solid #ddd6fe;
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }

    .admin-nav-tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      border-bottom: 2px solid var(--border);
      padding-bottom: 8px;
    }

    .admin-tab-btn {
      background: none;
      border: none;
      padding: 8px 16px;
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: 8px;
      transition: all 0.15s ease;
    }

    .admin-tab-btn.active {
      background: var(--primary-light);
      color: var(--primary);
    }

    .filter-bar {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }

    .filter-chip {
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
    }

    .filter-chip.active {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }

    .submission-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 12px;
      box-shadow: var(--shadow-sm);
    }

    .sub-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .sub-student {
      font-size: 1rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .sub-meta {
      font-size: 0.78rem;
      color: var(--text-muted);
    }

    .sub-score-badge {
      font-size: 0.92rem;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 8px;
    }

    .inspect-q-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      margin-bottom: 12px;
    }

    .inspect-correct-badge {
      display: inline-block;
      background: #ecfdf5;
      color: #047857;
      font-weight: 700;
      font-size: 0.8rem;
      padding: 3px 8px;
      border-radius: 6px;
      margin-top: 6px;
    }

    .spinner {
      border: 3px solid rgba(0, 0, 0, 0.1);
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border-left-color: var(--primary);
      animation: spin 0.8s linear infinite;
      display: inline-block;
      vertical-align: middle;
      margin-right: 8px;
    }

    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  </style>
</head>
<body>

  <div class="app-container">

    <!-- Top Header -->
    <header class="top-header">
      <div class="brand-group">
        <div class="brand-icon">M</div>
        <div class="brand-meta">
          <h1>Manaret El-Eman Assessment Portal</h1>
          <p>Official Primary Interactive Exam Platform</p>
        </div>
      </div>
      <div style="display: flex; gap: 8px;">
        <button id="btn-open-parent-portal" class="portal-toggle-btn" onclick="openAdminPortal()">
          🔐 Parent Portal (لوحة ولي الأمر)
        </button>
      </div>
    </header>

    <!-- SCREEN 1: WELCOME & STUDENT SELECTOR -->
    <div id="screen-welcome" class="screen active">
      <div class="card">
        
        <div class="section-title">Step 1 &bull; Select Student Profile</div>
        <div class="student-chips-grid">
          <!-- Student 1: Ali Ahmed -->
          <button id="chip-ali" class="chip-btn active" onclick="onStudentSelected('Ali Ahmed', 'Year 5 (G5)')">
            <div class="chip-name">👦 Ali Ahmed</div>
            <div class="chip-grade">Year 5 (G5) &bull; International School</div>
            <span class="chip-badge">1 Exam Available</span>
          </button>

          <!-- Student 2: Mostafa Ahmed -->
          <button id="chip-mostafa" class="chip-btn" onclick="onStudentSelected('Mostafa Ahmed', 'Grade 6 (G6)')">
            <div class="chip-name">👦 Mostafa Ahmed</div>
            <div class="chip-grade">Grade 6 (G6) &bull; International School</div>
            <span class="chip-badge">2 Exams Available</span>
          </button>
        </div>

        <input type="hidden" id="student-name" value="Ali Ahmed">
        <input type="hidden" id="student-group" value="Year 5 (G5)">

        <div class="section-title">Step 2 &bull; Choose Assessment</div>
        <div id="available-exams-container">
          <!-- Populated dynamically via JS -->
        </div>

        <!-- Selected Assessment Preview Card -->
        <div class="assessment-hero" style="margin-top: 16px;">
          <h2 id="hero-exam-title">Loading Assessment...</h2>
          <div class="hero-meta-row">
            <div class="hero-meta-item">📚 <span id="hero-exam-subject">English</span></div>
            <div class="hero-meta-item">⏱️ <span id="hero-exam-duration">20</span> Mins</div>
            <div class="hero-meta-item">❓ <span id="hero-exam-count">10</span> Questions</div>
            <div class="hero-meta-item">🎯 Single Attempt Protected</div>
          </div>
        </div>

        <!-- Status Container (Dynamic: New, Completed, Pending Approval, Approved) -->
        <div id="status-flow-container">
          <div class="single-attempt-notice" id="notice-single-attempt">
            <span style="font-size: 1.2rem;">⚠️</span>
            <div>
              <strong>Strict Single-Attempt Policy (الامتحان يفتح مرة واحدة فقط):</strong>
              <div style="font-size: 0.8rem; margin-top: 2px;">
                Once started, the timer begins immediately. The exam cannot be restarted after submission without parent authorization.
              </div>
            </div>
          </div>
        </div>

        <!-- Start or Request Retake Buttons -->
        <div id="action-buttons-container">
          <button id="btn-start-modal-trigger" class="btn-primary" onclick="promptStartConfirmation()">
            <span>Start Assessment Now</span> &rarr;
          </button>
        </div>

      </div>
    </div>

    <!-- SCREEN 2: ACTIVE QUIZ -->
    <div id="screen-quiz" class="screen">
      <div class="quiz-sticky-header">
        <div>
          <div class="quiz-progress-text" id="quiz-progress-indicator">Question 1 of 10</div>
          <div class="progress-bar-container">
            <div class="progress-bar-fill" id="progress-bar-fill"></div>
          </div>
        </div>
        <div class="quiz-timer" id="quiz-timer-display">⏱️ 20:00</div>
      </div>

      <div class="question-card" id="quiz-question-box">
        <div class="q-meta-tag" id="q-unit-label">Unit Lesson</div>
        <div class="q-text" id="q-text-display">Question Text goes here...</div>
        <div class="options-grid" id="q-options-container">
          <!-- Dynamic Options -->
        </div>

        <div class="nav-btn-row">
          <button id="btn-prev-q" class="btn-secondary" onclick="prevQuestion()" disabled>
            &larr; Previous
          </button>
          <button id="btn-next-q" class="btn-primary" style="width: auto; padding: 12px 24px;" onclick="nextQuestion()">
            Next &rarr;
          </button>
        </div>
      </div>
    </div>

    <!-- SCREEN 3: RESULT & EXPLANATION REVIEW -->
    <div id="screen-result" class="screen">
      <div class="result-score-banner">
        <div style="font-size: 0.95rem; opacity: 0.9;" id="res-student-header">Assessment Report</div>
        <div class="score-circle" id="res-score-display">10 / 10</div>
        <div class="score-rating" id="res-rating-display">Excellent! 🌟</div>
        <div style="font-size: 0.84rem; opacity: 0.85; margin-top: 6px;" id="res-time-spent">Time Spent: 8 mins</div>
      </div>

      <div class="card">
        <h3 style="font-size: 1.1rem; font-weight: 800; margin-bottom: 14px;">Detailed Explanations & Error Correction</h3>
        <p style="font-size: 0.84rem; color: var(--text-muted); margin-bottom: 18px;">
          Review the complete pedagogical breakdown below, including rules, worked examples, and mistake analysis.
        </p>
        <div id="review-items-container">
          <!-- Populated dynamically -->
        </div>

        <div style="margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
          <button class="btn-secondary" style="flex: 1;" onclick="openAdminPortal()">
            🔐 Parent Portal
          </button>
          <button class="btn-primary" style="flex: 1;" onclick="returnToHome()">
            Return to Home
          </button>
        </div>
      </div>
    </div>

    <!-- SCREEN 4: PARENT / TEACHER DASHBOARD -->
    <div id="screen-admin" class="screen">
      <div class="card" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
          <div>
            <h2 style="font-size: 1.25rem; font-weight: 800;">👨‍🏫 Parent & Teacher Portal</h2>
            <p style="font-size: 0.82rem; color: var(--text-muted);">Real-time submissions, retake approvals & exam inspection</p>
          </div>
          <div style="display: flex; gap: 8px;">
            <a id="admin-sheet-link" href="#" target="_blank" class="portal-toggle-btn" style="color: var(--primary);">
              📂 Open Google Sheet
            </a>
            <button class="portal-toggle-btn" onclick="showScreen('screen-welcome')">
              « Back to Assessments
            </button>
          </div>
        </div>

        <!-- Retake Requests Section (Alerts for Father) -->
        <div id="admin-retake-requests-box" class="admin-retake-banner" style="display: none;">
          <div class="admin-retake-title">
            <span>🔔</span> <strong>Retake Requests Pending Your Approval (طلبات إعادة الامتحان بانتظار موافقتك)</strong>
          </div>
          <div id="admin-retake-requests-list">
            <!-- Dynamic Items -->
          </div>
        </div>

        <!-- KPI Boxes -->
        <div class="admin-kpi-grid">
          <div class="kpi-box">
            <span class="kpi-num" id="kpi-total-attempts">0</span>
            <span class="kpi-label">Total Attempts</span>
          </div>
          <div class="kpi-box">
            <span class="kpi-num" id="kpi-ali-score">--</span>
            <span class="kpi-label">Ali Ahmed (Year 5)</span>
          </div>
          <div class="kpi-box">
            <span class="kpi-num" id="kpi-mostafa-score">--</span>
            <span class="kpi-label">Mostafa Ahmed (Grade 6)</span>
          </div>
        </div>

        <!-- Sub Tabs in Admin -->
        <div class="admin-nav-tabs">
          <button id="admin-tab-subs" class="admin-tab-btn active" onclick="switchAdminSubTab('submissions')">
            📊 Submissions History
          </button>
          <button id="admin-tab-inspector" class="admin-tab-btn" onclick="switchAdminSubTab('inspector')">
            📖 Exam Bank Inspector (معاينة الأسئلة)
          </button>
        </div>

        <!-- SECTION A: SUBMISSIONS -->
        <div id="admin-panel-submissions">
          <div class="filter-bar">
            <button class="filter-chip active" id="flt-all" onclick="filterSubmissions('ALL')">All Submissions</button>
            <button class="filter-chip" id="flt-ali" onclick="filterSubmissions('Ali')">👦 Ali Ahmed</button>
            <button class="filter-chip" id="flt-mostafa" onclick="filterSubmissions('Mostafa')">👦 Mostafa Ahmed</button>
            <button class="portal-toggle-btn" style="margin-left: auto;" onclick="clearLocalLocks()">
              🔓 Reset Device Locks
            </button>
          </div>

          <div id="admin-submissions-container">
            <div style="text-align: center; padding: 30px; color: var(--text-muted);">
              Loading student records...
            </div>
          </div>
        </div>

        <!-- SECTION B: EXAM BANK INSPECTOR -->
        <div id="admin-panel-inspector" style="display: none;">
          <p style="font-size: 0.84rem; color: var(--text-muted); margin-bottom: 14px;">
            Select an exam below to inspect all authentic questions and multi-example explanations directly:
          </p>
          <div class="filter-bar">
            <button class="filter-chip active" id="insp-btn-ali-eng" onclick="inspectExam('EX_Y5_ENG_ADV01')">
              📘 Ali (G5) English Grammar
            </button>
            <button class="filter-chip" id="insp-btn-mostafa-eng" onclick="inspectExam('EX_Y6_ENG_FANTASY01')">
              📘 Mostafa (G6) English Literacy
            </button>
            <button class="filter-chip" id="insp-btn-mostafa-arb" onclick="inspectExam('EX_Y6_ARB_PRIO01')">
              📗 Mostafa (G6) اللغة العربية
            </button>
          </div>

          <div id="inspector-questions-container">
            <!-- Rendered via JS -->
          </div>
        </div>

      </div>
    </div>

  </div>

  <!-- GATEKEEPER MODAL -->
  <div class="modal-overlay" id="start-modal">
    <div class="modal-card">
      <div class="modal-warning-icon">⚠️</div>
      <div class="modal-title">Important Confirmation<br><span style="font-size: 0.95rem; font-weight: 600; color: #d97706;">تنبيه هام للبدء</span></div>
      
      <p class="modal-desc">
        This exam can only be opened and submitted <strong>ONCE</strong>.<br>
        الامتحان يفتح <strong>مرة واحدة فقط</strong> ولا يمكن إعادته بعد البدء إلا بإذن ولي الأمر!
      </p>

      <div class="modal-highlight-box">
        <div>👤 <strong>Student Name / اسم الطالب:</strong> <span id="modal-student-name">Ali Ahmed</span></div>
        <div>📘 <strong>Assessment / الامتحان:</strong> <span id="modal-exam-name">English Grammar</span></div>
        <div>⏱️ <strong>Duration / المدة:</strong> <span id="modal-duration">20 Minutes</span></div>
      </div>

      <div class="modal-btn-row">
        <button class="btn-secondary" onclick="closeStartModal()">Cancel / إلغاء</button>
        <button class="btn-primary" style="padding: 12px;" onclick="confirmStartAssessment()">
          Yes, Start Now 🚀
        </button>
      </div>
    </div>
  </div>

  <script>
    // Registered Exams Catalog - ONLY authentic Ali & Mostafa exams (NO SCIENCE)
    const EXAMS_CATALOG = {
      'Ali': [
        { code: 'EX_Y5_ENG_ADV01', title: '📘 English: Adverbials of Time, Place & Manner (Unit 2)', grade: 'Year 5 (G5)', subject: 'English Grammar', count: 10, duration: 20 }
      ],
      'Mostafa': [
        { code: 'EX_Y6_ENG_FANTASY01', title: '📘 English: Fantasy Reading "The City That Waited" & Grammar', grade: 'Grade 6 (G6)', subject: 'English Literacy', count: 10, duration: 20 },
        { code: 'EX_Y6_ARB_PRIO01', title: '📗 لغة عربية: القراءة المتحررة، النكرة والمعرفة، والهمزة المتوسطة', grade: 'Grade 6 (G6)', subject: 'اللغة العربية', count: 10, duration: 20 }
      ]
    };

    let activeStudentName = 'Ali Ahmed';
    let activeStudentGroup = 'Year 5 (G5)';
    let activeExamCode = 'EX_Y5_ENG_ADV01';
    let examData = null;
    let questions = [];
    let currentIdx = 0;
    let studentAnswers = {};
    let timerInterval = null;
    let secondsRemaining = 0;
    let startTime = null;
    let cachedAdminData = null;
    let currentFilter = 'ALL';
    let currentExamStatus = { canAttempt: true, retakeStatus: 'NONE' };

    window.addEventListener('DOMContentLoaded', () => {
      const urlParams = new URLSearchParams(window.location.search);
      const studentParam = urlParams.get('student');
      const adminParam = urlParams.get('admin');
      const examParam = urlParams.get('exam');

      if (adminParam === '1') {
        openAdminPortal();
        return;
      }

      if (studentParam && studentParam.toLowerCase().includes('mostafa')) {
        onStudentSelected('Mostafa Ahmed', 'Grade 6 (G6)');
      } else {
        onStudentSelected('Ali Ahmed', 'Year 5 (G5)');
      }

      if (examParam) {
        activeExamCode = examParam;
        loadExamDetails(activeExamCode);
      }
    });

    function onStudentSelected(name, group) {
      activeStudentName = name;
      activeStudentGroup = group;
      document.getElementById('student-name').value = name;
      document.getElementById('student-group').value = group;

      document.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
      const isAli = name.includes('Ali');
      if (isAli) {
        document.getElementById('chip-ali').classList.add('active');
      } else {
        document.getElementById('chip-mostafa').classList.add('active');
      }

      // Render Available Exams for Selected Student
      const examsList = isAli ? EXAMS_CATALOG['Ali'] : EXAMS_CATALOG['Mostafa'];
      const examContainer = document.getElementById('available-exams-container');
      examContainer.innerHTML = '';

      examsList.forEach((ex, idx) => {
        const card = document.createElement('div');
        card.className = 'exam-select-card' + (idx === 0 ? ' active' : '');
        card.id = 'exam-card-' + ex.code;
        card.innerHTML = `
          <div>
            <div class="exam-select-title">${ex.title}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">Subject: ${ex.subject} &bull; ${ex.count} Questions</div>
          </div>
          <span class="exam-select-badge">${ex.grade}</span>
        `;
        card.onclick = () => {
          document.querySelectorAll('.exam-select-card').forEach(c => c.classList.remove('active'));
          card.classList.add('active');
          activeExamCode = ex.code;
          loadExamDetails(activeExamCode);
        };
        examContainer.appendChild(card);
      });

      activeExamCode = examsList[0].code;
      loadExamDetails(activeExamCode);
    }

    function loadExamDetails(code) {
      const isAli = activeStudentName.includes('Ali');
      const examsList = isAli ? EXAMS_CATALOG['Ali'] : EXAMS_CATALOG['Mostafa'];
      const currentEx = examsList.find(e => e.code === code) || examsList[0];

      document.getElementById('hero-exam-title').innerText = currentEx.title;
      document.getElementById('hero-exam-subject').innerText = currentEx.subject;
      document.getElementById('hero-exam-duration').innerText = currentEx.duration;
      document.getElementById('hero-exam-count').innerText = currentEx.count;

      checkExamStatusAndRetake(code, activeStudentName);
    }

    function checkExamStatusAndRetake(examCode, studentName) {
      const statusBox = document.getElementById('status-flow-container');
      const actionBox = document.getElementById('action-buttons-container');

      // Check local cache first for instant feedback
      const lockKey = 'lock_' + examCode + '_' + studentName.replace(/\\s+/g, '_');
      const localLock = localStorage.getItem(lockKey);

      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(res => {
            if (res.success) {
              renderStatusFlow(res, examCode, studentName);
            }
          })
          .getStudentExamStatus(studentName, examCode);
      } else {
        // Fallback for direct browser preview
        if (localLock) {
          const lData = JSON.parse(localLock);
          renderStatusFlow({
            hasSubmitted: true,
            lastScore: lData.score,
            canAttempt: false,
            retakeStatus: 'NONE'
          }, examCode, studentName);
        } else {
          renderStatusFlow({
            hasSubmitted: false,
            canAttempt: true,
            retakeStatus: 'NONE'
          }, examCode, studentName);
        }
      }
    }

    function renderStatusFlow(statusData, examCode, studentName) {
      currentExamStatus = statusData;
      const statusBox = document.getElementById('status-flow-container');
      const actionBox = document.getElementById('action-buttons-container');

      if (!statusData.hasSubmitted) {
        // CASE 1: Never submitted
        statusBox.innerHTML = `
          <div class="single-attempt-notice">
            <span style="font-size: 1.2rem;">⚠️</span>
            <div>
              <strong>Strict Single-Attempt Policy (الامتحان يفتح مرة واحدة فقط):</strong>
              <div style="font-size: 0.8rem; margin-top: 2px;">
                Once started, the timer begins immediately. The exam cannot be restarted after submission without parent authorization.
              </div>
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-primary" onclick="promptStartConfirmation()">
            <span>Start Assessment Now</span> &rarr;
          </button>
        `;
      } else if (statusData.canAttempt && statusData.retakeStatus === 'APPROVED') {
        // CASE 2: Retake APPROVED by father!
        statusBox.innerHTML = `
          <div class="retake-status-card approved">
            <strong>🎉 Retake Approved by Parent! (تمت موافقة الوالد على إعادة الامتحان)</strong>
            <div style="font-size: 0.82rem; margin-top: 4px;">
              Your father has granted permission for a second attempt. Previous score: <strong>${statusData.lastScore}</strong>.
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-primary btn-purple" onclick="promptStartConfirmation()">
            <span>Start 2nd Attempt Now (ابدأ المحاولة الثانية الآن)</span> &rarr;
          </button>
        `;
      } else if (statusData.retakeStatus === 'PENDING') {
        // CASE 3: Retake PENDING father approval
        statusBox.innerHTML = `
          <div class="retake-status-card pending">
            <strong>⏳ Retake Request Pending Parent Approval (طلبك بانتظار موافقة الوالد)</strong>
            <div style="font-size: 0.82rem; margin-top: 4px;">
              A request for a 2nd attempt was sent to your parent dashboard. Please wait until your father approves it.
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-secondary" style="width: 100%;" onclick="checkExamStatusAndRetake('${examCode}', '${studentName}')">
            🔄 Check Approval Status (تحديث حالة الموافقة)
          </button>
        `;
      } else if (statusData.retakeStatus === 'REJECTED') {
        // CASE 4: Retake REJECTED
        statusBox.innerHTML = `
          <div class="retake-status-card rejected">
            <strong>❌ Retake Request Declined (تم رفض طلب الإعادة من الوالد)</strong>
            <div style="font-size: 0.82rem; margin-top: 4px;">
              Your parent has declined this retake request. Your recorded score remains: <strong>${statusData.lastScore}</strong>.
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-primary btn-purple" onclick="sendRetakeRequest('${examCode}', '${studentName}', '${statusData.lastScore}')">
            🔄 Request Again from Parent (إعادة طلب الإذن من الوالد)
          </button>
        `;
      } else {
        // CASE 5: Exam completed, no retake requested yet
        statusBox.innerHTML = `
          <div class="retake-status-card completed">
            <strong>🔒 Assessment Completed (تم حل الامتحان مسبقاً):</strong>
            <div style="font-size: 0.84rem; margin-top: 4px;">
              ${studentName} has already submitted this assessment. Recorded Score: <strong>${statusData.lastScore}</strong>.
            </div>
          </div>
        `;
        actionBox.innerHTML = `
          <button class="btn-primary btn-purple" onclick="sendRetakeRequest('${examCode}', '${studentName}', '${statusData.lastScore}')">
            <span>🔄 Request 2nd Attempt from Father (طلب محاولة ثانية من الوالد)</span>
          </button>
        `;
      }
    }

    function sendRetakeRequest(examCode, studentName, prevScore) {
      const reason = prompt('Please mention a reason for requesting a 2nd attempt (e.g., to review mistakes):', 'أرغب بمحاولة إضافية لتحسين النتيجة ومراجعة الأخطاء');
      if (reason === null) return;

      const payload = {
        studentName: studentName,
        examCode: examCode,
        examTitle: document.getElementById('hero-exam-title').innerText,
        previousScore: prevScore,
        reason: reason
      };

      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(res => {
            if (res.success) {
              alert('🎉 ' + res.message);
              checkExamStatusAndRetake(examCode, studentName);
            } else {
              alert('Error: ' + res.message);
            }
          })
          .requestExamRetake(payload);
      } else {
        alert('Simulation: Request sent to Parent Portal!');
        renderStatusFlow({
          hasSubmitted: true,
          lastScore: prevScore,
          canAttempt: false,
          retakeStatus: 'PENDING'
        }, examCode, studentName);
      }
    }

    function clearLocalLocks() {
      if (confirm('Are you sure you want to reset device locks for all completed exams on this device?')) {
        Object.keys(localStorage).forEach(k => {
          if (k.startsWith('lock_')) localStorage.removeItem(k);
        });
        alert('All local device locks have been reset! Students can retake assessments now.');
        checkExamStatusAndRetake(activeExamCode, activeStudentName);
      }
    }

    function showScreen(screenId) {
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      const target = document.getElementById(screenId);
      if (target) target.classList.add('active');
    }

    /* GATEKEEPER MODAL LOGIC */
    function promptStartConfirmation() {
      document.getElementById('modal-student-name').innerText = activeStudentName + ' (' + activeStudentGroup + ')';
      document.getElementById('modal-exam-name').innerText = document.getElementById('hero-exam-title').innerText;
      document.getElementById('modal-duration').innerText = document.getElementById('hero-exam-duration').innerText + ' Minutes';

      document.getElementById('start-modal').classList.add('active');
    }

    function closeStartModal() {
      document.getElementById('start-modal').classList.remove('active');
    }

    function confirmStartAssessment() {
      closeStartModal();
      showScreen('screen-quiz');
      fetchAndBeginQuiz(activeExamCode);
    }

    function fetchAndBeginQuiz(code) {
      const qBox = document.getElementById('quiz-question-box');
      qBox.innerHTML = '<div style="text-align: center; padding: 40px;"><div class="spinner"></div>Loading assessment questions...</div>';

      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(onQuestionsLoaded)
          .withFailureHandler(onQuestionsError)
          .getExamData(code);
      } else {
        setTimeout(() => {
          onQuestionsLoaded({
            success: true,
            exam: { title: 'Practice Assessment', duration: 20 },
            questions: [
              { id: 'DEMO_1', text: 'Sample Question for Preview', type: 'MCQ', options: ['Option A', 'Option B', 'Option C'], points: 1 }
            ]
          });
        }, 400);
      }
    }

    function onQuestionsLoaded(res) {
      if (!res.success || !res.questions || res.questions.length === 0) {
        alert(res.message || 'No questions found for this exam.');
        showScreen('screen-welcome');
        return;
      }
      examData = res.exam;
      questions = res.questions;
      currentIdx = 0;
      studentAnswers = {};
      startTime = new Date();

      secondsRemaining = (examData.duration || 20) * 60;
      startTimer();
      renderCurrentQuestion();
    }

    function onQuestionsError(err) {
      alert('Error connecting to assessment server: ' + err.toString());
      showScreen('screen-welcome');
    }

    function startTimer() {
      clearInterval(timerInterval);
      updateTimerUI();
      timerInterval = setInterval(() => {
        secondsRemaining--;
        if (secondsRemaining <= 0) {
          clearInterval(timerInterval);
          alert('Time is up! Submitting answers automatically.');
          submitQuiz();
        } else {
          updateTimerUI();
        }
      }, 1000);
    }

    function updateTimerUI() {
      const mins = Math.floor(secondsRemaining / 60);
      const secs = secondsRemaining % 60;
      const el = document.getElementById('quiz-timer-display');
      if (el) {
        el.innerText = `⏱️ ${mins}:${secs < 10 ? '0' : ''}${secs}`;
      }
    }

    function renderCurrentQuestion() {
      const q = questions[currentIdx];
      const total = questions.length;

      document.getElementById('quiz-progress-indicator').innerText = `Question ${currentIdx + 1} of ${total}`;
      const fillPct = ((currentIdx + 1) / total) * 100;
      document.getElementById('progress-bar-fill').style.width = fillPct + '%';

      const qBox = document.getElementById('quiz-question-box');
      const isArabic = (q.subject && q.subject.includes('العربية')) || (/[\u0600-\u06FF]/.test(q.text));

      let optsHtml = '';
      (q.options || []).forEach(opt => {
        const isSelected = studentAnswers[q.id] === opt;
        optsHtml += `
          <div class="option-item ${isSelected ? 'selected' : ''} ${isArabic ? 'rtl-opt' : ''}" onclick="selectOption('${q.id}', '${opt.replace(/'/g, "\\\\'")}')">
            <div class="opt-circle"></div>
            <span>${opt}</span>
          </div>
        `;
      });

      qBox.innerHTML = `
        <div class="q-meta-tag">${q.unit || q.lesson || 'Core Curriculum'}</div>
        <div class="q-text ${isArabic ? 'rtl-text' : ''}">${q.text}</div>
        <div class="options-grid">
          ${optsHtml}
        </div>
        <div class="nav-btn-row">
          <button class="btn-secondary" onclick="prevQuestion()" ${currentIdx === 0 ? 'disabled' : ''}>
            &larr; Previous
          </button>
          <button class="btn-primary" style="width: auto; padding: 12px 24px;" onclick="${currentIdx === total - 1 ? 'submitQuiz()' : 'nextQuestion()'}">
            ${currentIdx === total - 1 ? 'Finish & Submit 🎯' : 'Next &rarr;'}
          </button>
        </div>
      `;
    }

    function selectOption(qId, val) {
      studentAnswers[qId] = val;
      renderCurrentQuestion();
    }

    function nextQuestion() {
      if (currentIdx < questions.length - 1) {
        currentIdx++;
        renderCurrentQuestion();
      }
    }

    function prevQuestion() {
      if (currentIdx > 0) {
        currentIdx--;
        renderCurrentQuestion();
      }
    }

    function submitQuiz() {
      clearInterval(timerInterval);
      const total = questions.length;
      const answeredCount = Object.keys(studentAnswers).length;

      if (answeredCount < total) {
        if (!confirm(`You have answered ${answeredCount} of ${total} questions. Are you sure you want to finish and submit?`)) {
          startTimer();
          return;
        }
      }

      showScreen('screen-result');
      const resultBox = document.getElementById('review-items-container');
      resultBox.innerHTML = '<div style="text-align: center; padding: 40px;"><div class="spinner"></div>Calculating score & generating explanation report...</div>';

      const endTime = new Date();
      const diffSecs = Math.round((endTime - startTime) / 1000);
      const durationStr = `${Math.floor(diffSecs / 60)} min ${diffSecs % 60} sec`;

      const payload = {
        studentName: activeStudentName,
        schoolGroup: activeStudentGroup,
        examCode: activeExamCode,
        answers: studentAnswers,
        durationSpent: durationStr
      };

      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(onSubmissionSuccess)
          .withFailureHandler(onSubmissionError)
          .submitExamAnswers(payload);
      } else {
        setTimeout(() => {
          onSubmissionSuccess({
            success: true,
            earnedScore: 10,
            totalScore: 10,
            percentage: 100,
            rating: 'Excellent! 🌟',
            review: []
          });
        }, 500);
      }
    }

    function onSubmissionSuccess(res) {
      if (!res.success) {
        alert(res.message || 'Error recording submission.');
        return;
      }

      // Lock single attempt in localStorage
      const lockKey = 'lock_' + activeExamCode + '_' + activeStudentName.replace(/\\s+/g, '_');
      localStorage.setItem(lockKey, JSON.stringify({
        date: new Date().toLocaleDateString(),
        score: `${res.earnedScore}/${res.totalScore} (${res.percentage}%)`
      }));

      document.getElementById('res-student-header').innerText = `${activeStudentName} &bull; ${activeExamCode}`;
      document.getElementById('res-score-display').innerText = `${res.earnedScore} / ${res.totalScore}`;
      document.getElementById('res-rating-display').innerText = `${res.rating} (${res.percentage}%)`;

      const container = document.getElementById('review-items-container');
      container.innerHTML = '';

      (res.review || []).forEach((item, idx) => {
        const isCorrect = item.isCorrect;
        const card = document.createElement('div');
        card.className = `review-item ${isCorrect ? 'correct' : 'incorrect'}`;

        card.innerHTML = `
          <div class="review-header">
            <div class="review-q-title">Q${idx + 1}: ${item.questionText}</div>
            <span class="review-status-badge ${isCorrect ? 'badge-correct' : 'badge-incorrect'}">
              ${isCorrect ? '✓ Correct (+1)' : '✗ Incorrect (0)'}
            </span>
          </div>
          <div style="font-size: 0.88rem; margin-top: 6px;">
            <div><strong>Student's Answer:</strong> <span style="color: ${isCorrect ? 'var(--success)' : 'var(--danger)'};">${item.studentAnswer || '(No answer)'}</span></div>
            ${!isCorrect ? `<div><strong>Correct Answer:</strong> <span style="color: var(--success); font-weight: 700;">${item.correctAnswer}</span></div>` : ''}
          </div>
          <div class="explanation-box">${item.explanation}</div>
        `;
        container.appendChild(card);
      });
    }

    function onSubmissionError(err) {
      alert('Error submitting responses: ' + err.toString());
    }

    function returnToHome() {
      showScreen('screen-welcome');
      checkExamStatusAndRetake(activeExamCode, activeStudentName);
    }

    /* PARENT DASHBOARD LOGIC */
    function openAdminPortal() {
      showScreen('screen-admin');
      loadAdminDashboardData();
    }

    function loadAdminDashboardData() {
      const container = document.getElementById('admin-submissions-container');
      container.innerHTML = '<div style="text-align: center; padding: 30px;"><div class="spinner"></div>Loading latest data from Google Sheets...</div>';

      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(onAdminDataLoaded)
          .withFailureHandler(onAdminDataError)
          .getAdminDashboardData();
      } else {
        setTimeout(() => {
          onAdminDataLoaded({
            success: true,
            sheetUrl: 'https://docs.google.com/spreadsheets/d/sample',
            submissions: [],
            exams: [],
            allQuestions: [],
            retakeRequests: []
          });
        }, 300);
      }
    }

    function onAdminDataLoaded(res) {
      if (!res.success) {
        alert(res.message || 'Error loading dashboard.');
        return;
      }
      cachedAdminData = res;

      const sheetLinkEl = document.getElementById('admin-sheet-link');
      if (sheetLinkEl && res.sheetUrl) {
        sheetLinkEl.href = res.sheetUrl;
      }

      const subs = res.submissions || [];
      document.getElementById('kpi-total-attempts').innerText = subs.length;

      const aliSubs = subs.filter(s => s.studentName.toLowerCase().includes('ali'));
      if (aliSubs.length > 0) {
        const latest = aliSubs[0];
        document.getElementById('kpi-ali-score').innerText = latest.percentage + ' (' + latest.earnedScore + '/' + latest.totalScore + ')';
      } else {
        document.getElementById('kpi-ali-score').innerText = 'No attempts';
      }

      const mostafaSubs = subs.filter(s => s.studentName.toLowerCase().includes('mostafa'));
      if (mostafaSubs.length > 0) {
        const latest = mostafaSubs[0];
        document.getElementById('kpi-mostafa-score').innerText = latest.percentage + ' (' + latest.earnedScore + '/' + latest.totalScore + ')';
      } else {
        document.getElementById('kpi-mostafa-score').innerText = 'No attempts';
      }

      // Render Pending Retake Requests
      renderRetakeRequests(res.retakeRequests || []);

      renderFilteredSubmissions();
      inspectExam('EX_Y5_ENG_ADV01');
    }

    function renderRetakeRequests(requests) {
      const box = document.getElementById('admin-retake-requests-box');
      const list = document.getElementById('admin-retake-requests-list');
      const pending = requests.filter(r => r.status === 'PENDING');

      if (pending.length === 0) {
        box.style.display = 'none';
        return;
      }

      box.style.display = 'block';
      list.innerHTML = '';

      pending.forEach(r => {
        const item = document.createElement('div');
        item.className = 'retake-request-item';
        item.innerHTML = `
          <div>
            <div style="font-weight: 800; font-size: 0.95rem;">👦 ${r.studentName} &bull; <span style="color: var(--primary);">${r.examTitle}</span></div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">
              Previous Score: <strong>${r.previousScore}</strong> &bull; Reason: <em>"${r.reason}"</em> &bull; ${r.timestamp}
            </div>
          </div>
          <div style="display: flex; gap: 6px;">
            <button class="btn-success" onclick="approveRetake('${r.id}')">
              ✅ Approve Retake (موافقة)
            </button>
            <button class="btn-danger" onclick="rejectRetake('${r.id}')">
              ❌ Decline (رفض)
            </button>
          </div>
        `;
        list.appendChild(item);
      });
    }

    function approveRetake(requestId) {
      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(res => {
            alert(res.message);
            loadAdminDashboardData();
          })
          .approveRetakeRequest(requestId);
      } else {
        alert('Simulation: Approved!');
        loadAdminDashboardData();
      }
    }

    function rejectRetake(requestId) {
      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(res => {
            alert(res.message);
            loadAdminDashboardData();
          })
          .rejectRetakeRequest(requestId);
      } else {
        alert('Simulation: Declined!');
        loadAdminDashboardData();
      }
    }

    function onAdminDataError(err) {
      document.getElementById('admin-submissions-container').innerHTML = 
        '<div style="text-align: center; color: var(--danger); padding: 20px;">Failed to load data: ' + err.toString() + '</div>';
    }

    function switchAdminSubTab(tab) {
      document.getElementById('admin-tab-subs').classList.remove('active');
      document.getElementById('admin-tab-inspector').classList.remove('active');
      document.getElementById('admin-panel-submissions').style.display = 'none';
      document.getElementById('admin-panel-inspector').style.display = 'none';

      if (tab === 'submissions') {
        document.getElementById('admin-tab-subs').classList.add('active');
        document.getElementById('admin-panel-submissions').style.display = 'block';
      } else {
        document.getElementById('admin-tab-inspector').classList.add('active');
        document.getElementById('admin-panel-inspector').style.display = 'block';
      }
    }

    function filterSubmissions(type) {
      currentFilter = type;
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      if (type === 'ALL') document.getElementById('flt-all').classList.add('active');
      else if (type === 'Ali') document.getElementById('flt-ali').classList.add('active');
      else if (type === 'Mostafa') document.getElementById('flt-mostafa').classList.add('active');

      renderFilteredSubmissions();
    }

    function renderFilteredSubmissions() {
      if (!cachedAdminData) return;
      let subs = cachedAdminData.submissions || [];

      if (currentFilter === 'Ali') {
        subs = subs.filter(s => s.studentName.toLowerCase().includes('ali'));
      } else if (currentFilter === 'Mostafa') {
        subs = subs.filter(s => s.studentName.toLowerCase().includes('mostafa'));
      }

      const container = document.getElementById('admin-submissions-container');
      if (subs.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 30px; color: var(--text-muted);">No student submission records found for this view.</div>';
        return;
      }

      container.innerHTML = '';
      subs.forEach((sub, idx) => {
        const card = document.createElement('div');
        card.className = 'submission-card';

        let reviewList = '';
        (sub.review || []).forEach((r, qIdx) => {
          reviewList += `
            <div style="font-size: 0.8rem; padding: 6px 0; border-top: 1px dashed #e2e8f0;">
              <div><strong>Q${qIdx + 1}:</strong> ${r.questionText}</div>
              <div style="color: ${r.isCorrect ? 'var(--success)' : 'var(--danger)'};">
                ${r.isCorrect ? '✓' : '✗'} Student: ${r.studentAnswer || '(None)'} | Correct: ${r.correctAnswer}
              </div>
            </div>
          `;
        });

        card.innerHTML = `
          <div class="sub-card-header">
            <div>
              <div class="sub-student">👦 ${sub.studentName} <span style="font-size: 0.82rem; color: var(--text-muted);">(${sub.schoolGroup})</span></div>
              <div class="sub-meta">📝 ${sub.examCode} &bull; ⏱️ ${sub.durationSpent} &bull; 📅 ${sub.timestamp}</div>
            </div>
            <div class="sub-score-badge" style="background: ${sub.percentage.startsWith('100') || sub.percentage.startsWith('9') ? '#ecfdf5; color: #047857;' : '#eff6ff; color: #1e40af;'}">
              ${sub.earnedScore} / ${sub.totalScore} (${sub.percentage})
            </div>
          </div>
          <details style="font-size: 0.84rem; color: var(--text-muted); cursor: pointer; margin-top: 8px;">
            <summary style="font-weight: 700; color: var(--primary);">View Question by Question Details &darr;</summary>
            <div style="margin-top: 8px;">${reviewList}</div>
          </details>
        `;
        container.appendChild(card);
      });
    }

    function inspectExam(code) {
      document.querySelectorAll('#admin-panel-inspector .filter-chip').forEach(b => b.classList.remove('active'));
      if (code === 'EX_Y5_ENG_ADV01') document.getElementById('insp-btn-ali-eng').classList.add('active');
      else if (code === 'EX_Y6_ENG_FANTASY01') document.getElementById('insp-btn-mostafa-eng').classList.add('active');
      else if (code === 'EX_Y6_ARB_PRIO01') document.getElementById('insp-btn-mostafa-arb').classList.add('active');

      const container = document.getElementById('inspector-questions-container');
      if (!cachedAdminData || !cachedAdminData.allQuestions) {
        container.innerHTML = '<div style="text-align: center; padding: 20px;">Questions are available in the linked Google Sheet.</div>';
        return;
      }

      const qList = cachedAdminData.allQuestions.filter(q => q.examCode === code);
      if (qList.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 20px;">No questions found for this exam code.</div>';
        return;
      }

      container.innerHTML = '';
      qList.forEach((q, idx) => {
        const card = document.createElement('div');
        card.className = 'inspect-q-card';
        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--accent); font-weight: 700;">
            <span>Q${idx + 1} &bull; ${q.id}</span>
            <span>${q.lesson || q.unit}</span>
          </div>
          <div style="font-size: 0.98rem; font-weight: 700; margin: 8px 0; color: var(--text-main);">${q.text}</div>
          <div style="font-size: 0.84rem; color: var(--text-muted); margin-bottom: 6px;">
            <strong>Options:</strong> ${q.options.join(' &bull; ')}
          </div>
          <div>
            <span class="inspect-correct-badge">✓ Correct: ${q.correctAnswer}</span>
          </div>
          <div class="explanation-box" style="margin-top: 8px;">${q.explanation}</div>
        `;
        container.appendChild(card);
      });
    }
  </script>
</body>
</html>
"""

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Index.html v2 generated successfully with Retake Approval UI!")
