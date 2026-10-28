path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = "<!-- Operations Grid -->"
insertion = """<!-- Google Drive Cloud Video Sync Section -->
            <div style="background: #f8fafc; border: 1.5px solid #0284c7; border-radius: 12px; padding: 18px; margin-bottom: 20px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="font-size: 1.3rem;">☁️</span>
                  <h4 style="margin: 0; font-size: 1.05rem; font-weight: 800; color: #0369a1;">Google Drive Video Cloud Sync</h4>
                </div>
                <span class="meta-pill pill-cyan" id="drive-sync-pill">Ad-Free Cloud Streaming</span>
              </div>
              <p style="font-size: 0.85rem; color: #475569; margin: 0 0 12px 0;">
                Paste your Google Drive shared folder link or folder ID. The assessment portal will automatically stream all uploaded educational videos directly to any tablet, iPad, or mobile phone without YouTube ads.
              </p>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <input type="text" id="drive-folder-url-input" placeholder="https://drive.google.com/drive/folders/..." style="flex: 1; min-width: 280px; padding: 10px 14px; font-size: 0.85rem; border: 1px solid #cbd5e1; border-radius: 8px; background: #fff;" />
                <button type="button" class="btn-primary" style="width: auto; padding: 10px 20px; background: #0284c7;" onclick="syncGoogleDriveVideosAction()">
                  🔄 Sync Drive Videos Now
                </button>
              </div>
              <div id="drive-sync-feedback" style="margin-top: 10px; font-size: 0.84rem; display: none;"></div>
            </div>

            <!-- Operations Grid -->"""

if target in content and "Google Drive Video Cloud Sync" not in content:
    content = content.replace(target, insertion, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESSFULLY INSERTED GOOGLE DRIVE CARD")
else:
    print("ALREADY INSERTED OR TARGET NOT FOUND")
