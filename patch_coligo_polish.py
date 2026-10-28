import json

with open(r'primary-exam-system/Index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fonts & Typography Upgrade
old_font = '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800&display=swap" rel="stylesheet">'
new_font = '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
if old_font in content:
    content = content.replace(old_font, new_font)
    print("Replaced font link")

old_root_font = "--font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Cairo', sans-serif;"
new_root_font = "--font-family: 'Cairo', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;"
if old_root_font in content:
    content = content.replace(old_root_font, new_root_font)
    print("Replaced root font")

# 2. Fix 404 on 'فتح الملف' in Curriculum Library
old_link = '<a href="${encodeURI(f.path)}" target="_blank" class="mat-open-btn">'
new_link = '<a href="${f.url || encodeURI(f.path)}" target="_blank" class="mat-open-btn">'
if old_link in content:
    content = content.replace(old_link, new_link)
    print("Replaced mat-open-btn link")

# 3. Polish Parent Analytics & Escape Characters
old_analytics_target = """      let strengthsHtml = '';
      if (strengths.length > 0) {
        strengthsHtml = strengths.slice(0, 5).map(s => `
          <li style="margin-bottom: 8px;">
            <strong>${escapeHtml(plainText(s.text))}</strong>
            <span style="color: #15803d; font-weight: 700; margin-left: 6px;">(إتقان تام ${s.correctCount}/${s.correctCount})</span>
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
        deficienciesHtml = '<div style="color: #15803d; font-weight: 700;">🌟 أداء ممتاز! لم تُسجل أي أخطاء متكررة في المحاولات المسجلة.</div>';
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
      `;"""

new_analytics_replacement = """      function cleanArabicPunctuation(str) {
        if (!str) return '';
        var t = String(str)
          .replace(/&quot;/g, '"')
          .replace(/&apos;/g, "'")
          .replace(/&#39;/g, "'")
          .replace(/&amp;/g, '&')
          .replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>');
        t = t.replace(/"([^"\\n\\r]+)"/g, '«$1»');
        return escapeHtml(t);
      }

      let strengthsHtml = '';
      if (strengths.length > 0) {
        strengthsHtml = strengths.slice(0, 6).map(s => `
          <li style="margin-bottom: 8px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; gap: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); direction: rtl; text-align: right;">
            <div style="flex: 1; font-weight: 700; font-size: 0.88rem; color: #1e293b;">
              <bdi>${cleanArabicPunctuation(plainText(s.text))}</bdi>
            </div>
            <span style="background: #ecfdf5; color: #166534; border: 1px solid #86efac; border-radius: 6px; padding: 3px 10px; font-size: 0.76rem; font-weight: 800; white-space: nowrap;">
              ✓ إتقان تام (${s.correctCount}/${s.correctCount})
            </span>
          </li>
        `).join('');
      } else {
        strengthsHtml = '<li style="color: #64748b; padding: 12px; text-align: center;">جاري تجميع بيانات الأسئلة المتقنة مع استمرار حل التدريبات.</li>';
      }

      let deficienciesHtml = '';
      if (deficiencies.length > 0) {
        deficienciesHtml = deficiencies.slice(0, 6).map(d => `
          <div style="background: #ffffff; border: 1px solid #fecdd3; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; border-right: 4px solid #e11d48; box-shadow: 0 1px 2px rgba(0,0,0,0.02); direction: rtl; text-align: right;">
            <div style="font-weight: 700; color: #9f1239; font-size: 0.9rem;">
              <bdi>${cleanArabicPunctuation(plainText(d.text))}</bdi>
            </div>
            <div style="font-size: 0.84rem; color: #475569; margin-top: 6px; background: #fff1f2; padding: 8px 12px; border-radius: 6px; line-height: 1.6;">
              💡 <strong>التحليل التربوي:</strong> <bdi>${cleanArabicPunctuation(d.explanation || 'يُنصح بإعادة مراجعة هذا المفهوم في الدرس والتركيز على مفتاح الإجابة.')}</bdi>
            </div>
          </div>
        `).join('');
      } else {
        deficienciesHtml = '<div style="color: #15803d; font-weight: 700; padding: 14px; background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; text-align: center;">🌟 أداء ممتاز! لم تُسجل أي أخطاء متكررة في المحاولات المسجلة.</div>';
      }

      contentEl.innerHTML = `
        <!-- Summary Real KPI Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-bottom: 18px;">
          <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; padding: 14px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
            <div style="font-size: 1.55rem; font-weight: 800; color: #15803d;">${avgPercentage}%</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #166534; margin-top: 2px;">متوسط الدرجات العام (Real Avg)</div>
          </div>
          <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 12px; padding: 14px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
            <div style="font-size: 1.55rem; font-weight: 800; color: #1d4ed8;">${totalAttempts}</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #1e40af; margin-top: 2px;">إجمالي الاختبارات المنجزة</div>
          </div>
          <div style="background: #fffbeb; border: 1.5px solid #fde68a; border-radius: 12px; padding: 14px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
            <div style="font-size: 1.55rem; font-weight: 800; color: #b45309;">${latestSub.percentage}</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #92400e; margin-top: 2px;">آخر نتيجة مسجلة (${latestSub.earnedScore}/${latestSub.totalScore})</div>
          </div>
        </div>

        <!-- Section 1: Demonstrated Strengths (Collapsible Coligo Accordion) -->
        <details style="margin-bottom: 14px; background: #ffffff; border: 1.5px solid #dcfce7; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.03);" open>
          <summary style="cursor: pointer; padding: 12px 18px; font-weight: 800; font-size: 0.95rem; color: #166534; display: flex; justify-content: space-between; align-items: center; background: #f0fdf4; border-bottom: 1px solid #dcfce7; user-select: none;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 1.2rem;">🌟</span>
              <span>أوجه التميز والإتقان الفعلي (${strengths.length} أسئلة متقنة)</span>
            </div>
            <span style="font-size: 0.78rem; background: #dcfce7; color: #15803d; padding: 3px 10px; border-radius: 20px; font-weight: 700;">عرض التفاصيل ▾</span>
          </summary>
          <div style="padding: 14px;">
            <ul style="list-style: none; margin: 0; padding: 0;">
              ${strengthsHtml}
            </ul>
          </div>
        </details>

        <!-- Section 2: Deficiencies & Root Causes (Collapsible Coligo Accordion) -->
        <details style="margin-bottom: 18px; background: #ffffff; border: 1.5px solid #fecdd3; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.03);" ${deficiencies.length > 0 ? 'open' : ''}>
          <summary style="cursor: pointer; padding: 12px 18px; font-weight: 800; font-size: 0.95rem; color: #9f1239; display: flex; justify-content: space-between; align-items: center; background: #fff1f2; border-bottom: 1px solid #ffe4e6; user-select: none;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 1.2rem;">⚠️</span>
              <span>أوجه القصور والتحليل الإدراكي (${deficiencies.length} نقاط تحتاج مراجعة)</span>
            </div>
            <span style="font-size: 0.78rem; background: #ffe4e6; color: #be123c; padding: 3px 10px; border-radius: 20px; font-weight: 700;">عرض التحليل ▾</span>
          </summary>
          <div style="padding: 14px;">
            ${deficienciesHtml}
          </div>
        </details>
      `;"""

if old_analytics_target in content:
    content = content.replace(old_analytics_target, new_analytics_replacement)
    print("Replaced analytics section with Coligo accordions & unescaped punctuation")
else:
    print("WARNING: old_analytics_target not found in exact form")

with open(r'primary-exam-system/Index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patching complete.")
