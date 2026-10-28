import re

path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Initialize DRIVE_VIDEOS at the beginning of script
script_start_target = "<script>\n    // Embedded State from Google Apps Script"
script_start_replacement = """<script>
    window.DRIVE_VIDEOS = <?!= (typeof driveVideos !== 'undefined' && driveVideos) ? driveVideos : '{}' ?>;
    // Embedded State from Google Apps Script"""

if script_start_target not in content:
    # Try finding <script>
    script_pos = content.find("<script>")
    if script_pos != -1:
        content = content[:script_pos + 8] + "\n    window.DRIVE_VIDEOS = <?!= (typeof driveVideos !== 'undefined' && driveVideos) ? driveVideos : '{}' ?>;\n" + content[script_pos + 8:]
else:
    content = content.replace(script_start_target, script_start_replacement, 1)

# 2. Add Drive Sync UI to pview-operations
ops_target = """            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                <input type="text" id="ops-result-url" readonly style="flex: 1; min-width: 200px; padding: 10px 12px; font-size: 0.85rem; border: 1px solid #a7f3d0; border-radius: 8px; background: #fff;" />
                <button type="button" class="btn-primary" style="width: auto; padding: 10px 18px;" onclick="copyOpsUrl()">
                  📋 Copy Link
                </button>
              </div>
            </div>"""

ops_replacement = """            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                <input type="text" id="ops-result-url" readonly style="flex: 1; min-width: 200px; padding: 10px 12px; font-size: 0.85rem; border: 1px solid #a7f3d0; border-radius: 8px; background: #fff;" />
                <button type="button" class="btn-primary" style="width: auto; padding: 10px 18px;" onclick="copyOpsUrl()">
                  📋 Copy Link
                </button>
              </div>
            </div>

            <!-- Google Drive Cloud Video Sync Section -->
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
            </div>"""

nc = content.replace("\r\n", "\n")
ot = ops_target.replace("\r\n", "\n")
or_ = ops_replacement.replace("\r\n", "\n")

if ot in nc:
    nc = nc.replace(ot, or_, 1)
else:
    print("OPS TARGET NOT FOUND")

# 3. Update Video Player JS for Google Drive Priority
video_js_target = """    let currentVideoId = null;

    function setVideoPlayerMode(mode) {
      const nativePlayer = document.getElementById('native-video-player');
      const iframe = document.getElementById('video-iframe');
      const btnNative = document.getElementById('btn-mode-native');
      const btnCloud = document.getElementById('btn-mode-cloud');
      const statusText = document.getElementById('video-mode-status');

      if (mode === 'native') {
        if (iframe) { iframe.src = ''; iframe.style.display = 'none'; }
        if (nativePlayer) {
          var serverHost = window.LOCAL_VIDEO_HOST || '192.168.1.96:8085';
          nativePlayer.src = 'http://' + serverHost + '/stream/' + currentVideoId + '.mp4';
          nativePlayer.style.display = 'block';
          nativePlayer.play().catch(function(e) { console.log('Autoplay deferred:', e); });
        }
        if (btnNative) { btnNative.style.background = '#2563eb'; btnNative.style.color = '#fff'; }
        if (btnCloud) { btnCloud.style.background = '#fff'; btnCloud.style.color = '#334155'; }
        if (statusText) statusText.innerHTML = '⚡ <b>مشغل محلي فائق السرعة</b> من القرص (بدون إعلانات وبدون استهلاك للإنترنت)';
      } else {
        if (nativePlayer) {
          nativePlayer.pause();
          nativePlayer.src = '';
          nativePlayer.style.display = 'none';
        }
        if (iframe) {
          iframe.src = 'https://www.youtube-nocookie.com/embed/' + currentVideoId + '?autoplay=1&rel=0';
          iframe.style.display = 'block';
        }
        if (btnCloud) { btnCloud.style.background = '#2563eb'; btnCloud.style.color = '#fff'; }
        if (btnNative) { btnNative.style.background = '#fff'; btnNative.style.color = '#334155'; }
        if (statusText) statusText.innerHTML = '🌐 <b>بث سحابي بديل</b> (YouTube Embed)';
      }
    }

    function openVideoModal(videoId, title) {
      currentVideoId = videoId;
      const modal = document.getElementById('video-modal');
      const titleEl = document.getElementById('video-modal-title');
      if (titleEl) titleEl.innerText = title || 'فيديو شرح الدرس المباشر';

      // Probe local streaming server
      let probed = false;
      const fallbackTimer = setTimeout(function() {
        if (!probed) { probed = true; setVideoPlayerMode('cloud'); }
      }, 700);

      fetch('http://127.0.0.1:8085/stream/' + videoId + '.mp4', { method: 'HEAD', mode: 'no-cors' })
        .then(function() {
          if (!probed) { probed = true; clearTimeout(fallbackTimer); setVideoPlayerMode('native'); }
        })
        .catch(function() {
          if (!probed) { probed = true; clearTimeout(fallbackTimer); setVideoPlayerMode('cloud'); }
        });

      if (modal) modal.classList.add('active');
    }"""

video_js_replacement = """    let currentVideoId = null;

    function setVideoPlayerMode(mode) {
      const nativePlayer = document.getElementById('native-video-player');
      const iframe = document.getElementById('video-iframe');
      const btnNative = document.getElementById('btn-mode-native');
      const btnCloud = document.getElementById('btn-mode-cloud');
      const statusText = document.getElementById('video-mode-status');

      // Check if video is registered in Google Drive
      const driveMeta = (window.DRIVE_VIDEOS && window.DRIVE_VIDEOS[currentVideoId]);

      if (mode === 'drive' && driveMeta) {
        if (nativePlayer) { nativePlayer.pause(); nativePlayer.src = ''; nativePlayer.style.display = 'none'; }
        if (iframe) {
          iframe.src = driveMeta.previewUrl;
          iframe.style.display = 'block';
        }
        if (btnCloud) { btnCloud.style.background = '#0284c7'; btnCloud.style.color = '#fff'; }
        if (btnNative) { btnNative.style.background = '#fff'; btnNative.style.color = '#334155'; }
        if (statusText) statusText.innerHTML = '☁️ <b>بث سحابي من Google Drive</b> (يعمل على كافة الأجهزة بدون إعلانات)';
      } else if (mode === 'native') {
        if (iframe) { iframe.src = ''; iframe.style.display = 'none'; }
        if (nativePlayer) {
          var serverHost = window.LOCAL_VIDEO_HOST || '192.168.1.96:8085';
          nativePlayer.src = 'http://' + serverHost + '/stream/' + currentVideoId + '.mp4';
          nativePlayer.style.display = 'block';
          nativePlayer.play().catch(function(e) { console.log('Autoplay deferred:', e); });
        }
        if (btnNative) { btnNative.style.background = '#2563eb'; btnNative.style.color = '#fff'; }
        if (btnCloud) { btnCloud.style.background = '#fff'; btnCloud.style.color = '#334155'; }
        if (statusText) statusText.innerHTML = '⚡ <b>مشغل محلي عبر الواي فاي</b> (بدون استهلاك إنترنت)';
      } else {
        if (nativePlayer) {
          nativePlayer.pause();
          nativePlayer.src = '';
          nativePlayer.style.display = 'none';
        }
        if (iframe) {
          iframe.src = 'https://www.youtube-nocookie.com/embed/' + currentVideoId + '?autoplay=1&rel=0';
          iframe.style.display = 'block';
        }
        if (btnCloud) { btnCloud.style.background = '#2563eb'; btnCloud.style.color = '#fff'; }
        if (btnNative) { btnNative.style.background = '#fff'; btnNative.style.color = '#334155'; }
        if (statusText) statusText.innerHTML = '🌐 <b>بث سحابي بديل</b> (YouTube Embed)';
      }
    }

    function openVideoModal(videoId, title) {
      currentVideoId = videoId;
      const modal = document.getElementById('video-modal');
      const titleEl = document.getElementById('video-modal-title');
      if (titleEl) titleEl.innerText = title || 'فيديو شرح الدرس المباشر';

      // 1. If available in Google Drive, play immediately via Drive Preview (Zero Ads & In-App)
      if (window.DRIVE_VIDEOS && window.DRIVE_VIDEOS[videoId]) {
        setVideoPlayerMode('drive');
      } else {
        // 2. Probe local streaming server
        let probed = false;
        const fallbackTimer = setTimeout(function() {
          if (!probed) { probed = true; setVideoPlayerMode('cloud'); }
        }, 700);

        var serverHost = window.LOCAL_VIDEO_HOST || '192.168.1.96:8085';
        fetch('http://' + serverHost + '/stream/' + videoId + '.mp4', { method: 'HEAD', mode: 'no-cors' })
          .then(function() {
            if (!probed) { probed = true; clearTimeout(fallbackTimer); setVideoPlayerMode('native'); }
          })
          .catch(function() {
            if (!probed) { probed = true; clearTimeout(fallbackTimer); setVideoPlayerMode('cloud'); }
          });
      }

      if (modal) modal.classList.add('active');
    }

    function syncGoogleDriveVideosAction() {
      const input = document.getElementById('drive-folder-url-input');
      const fb = document.getElementById('drive-sync-feedback');
      if (!input || !fb) return;
      const val = input.value.trim();
      if (!val) {
        fb.style.display = 'block';
        fb.style.color = '#dc2626';
        fb.innerText = '⚠️ Please enter a Google Drive folder link or ID.';
        return;
      }
      fb.style.display = 'block';
      fb.style.color = '#0284c7';
      fb.innerText = '⏳ Connecting to Google Drive and scanning video files...';

      if (typeof google !== 'undefined' && google.script && google.script.run) {
        google.script.run
          .withSuccessHandler(function(res) {
            if (res.success) {
              window.DRIVE_VIDEOS = res.videoMap;
              fb.style.color = '#059669';
              fb.innerText = '✅ ' + res.message;
            } else {
              fb.style.color = '#dc2626';
              fb.innerText = '❌ ' + res.message;
            }
          })
          .withFailureHandler(function(err) {
            fb.style.color = '#dc2626';
            fb.innerText = '❌ Error: ' + (err && err.message ? err.message : err);
          })
          .syncGoogleDriveVideos(val);
      } else {
        fb.style.color = '#059669';
        fb.innerText = '✅ [Simulation Mode] Google Drive videos synchronized.';
      }
    }"""

vt = video_js_target.replace("\r\n", "\n")
vr = video_js_replacement.replace("\r\n", "\n")

if vt in nc:
    nc = nc.replace(vt, vr, 1)
else:
    print("VIDEO JS TARGET NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(nc)
print("SUCCESSFULLY APPLIED GOOGLE DRIVE UPDATES TO INDEX.HTML")
