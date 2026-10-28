import os

path = r"C:\Users\co0ob\Projects\primary-exam-system\Index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = """    function openVideoModal(videoId, title) {
      const modal = document.getElementById('video-modal');
      const titleEl = document.getElementById('video-modal-title');
      const iframe = document.getElementById('video-iframe');
      if (titleEl) titleEl.innerText = title || 'فيديو شرح الدرس';
      if (iframe) iframe.src = 'https://www.youtube-nocookie.com/embed/' + videoId + '?autoplay=1&rel=0';
      if (modal) modal.classList.add('active');
    }

    function closeVideoModal() {
      const modal = document.getElementById('video-modal');
      const iframe = document.getElementById('video-iframe');
      if (iframe) iframe.src = '';
      if (modal) modal.classList.remove('active');
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeVideoModal();
    });

  </script>
  <!-- VIDEO LESSON MODAL -->
  <div class="modal-overlay" id="video-modal" role="dialog" aria-modal="true" aria-labelledby="video-modal-title">
    <div class="modal-card" style="max-width: 680px; width: 95%; padding: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 1.3rem;">🎬</span>
          <h3 id="video-modal-title" style="font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin: 0;">فيديو شرح الدرس</h3>
        </div>
        <button type="button" class="portal-btn" onclick="closeVideoModal()" style="padding: 4px 10px; font-weight: 800;">✕ إغلاق</button>
      </div>
      <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px; background: #000; box-shadow: 0 4px 14px rgba(0,0,0,0.2);">
        <iframe id="video-iframe" style="position: absolute; top:0; left: 0; width: 100%; height: 100%; border: 0;" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div style="margin-top: 14px; text-align: center;">
        <button type="button" class="btn-primary" style="width: auto; padding: 10px 24px;" onclick="closeVideoModal()">
          ✓ استوعبت الشرح، العودة للامتحان
        </button>
      </div>
    </div>
  </div>"""

replacement = """    let currentVideoId = null;

    function setVideoPlayerMode(mode) {
      const nativePlayer = document.getElementById('native-video-player');
      const iframe = document.getElementById('video-iframe');
      const btnNative = document.getElementById('btn-mode-native');
      const btnCloud = document.getElementById('btn-mode-cloud');
      const statusText = document.getElementById('video-mode-status');

      if (mode === 'native') {
        if (iframe) { iframe.src = ''; iframe.style.display = 'none'; }
        if (nativePlayer) {
          nativePlayer.src = 'http://127.0.0.1:8085/stream/' + currentVideoId + '.mp4';
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
    }

    function closeVideoModal() {
      const modal = document.getElementById('video-modal');
      const nativePlayer = document.getElementById('native-video-player');
      const iframe = document.getElementById('video-iframe');
      if (nativePlayer) { nativePlayer.pause(); nativePlayer.src = ''; }
      if (iframe) iframe.src = '';
      if (modal) modal.classList.remove('active');
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeVideoModal();
    });

  </script>
  <!-- VIDEO LESSON MODAL -->
  <div class="modal-overlay" id="video-modal" role="dialog" aria-modal="true" aria-labelledby="video-modal-title">
    <div class="modal-card" style="max-width: 720px; width: 95%; padding: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 1.3rem;">🎬</span>
          <h3 id="video-modal-title" style="font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin: 0;">فيديو شرح الدرس المباشر</h3>
        </div>
        <button type="button" class="portal-btn" onclick="closeVideoModal()" style="padding: 4px 10px; font-weight: 800;">✕ إغلاق</button>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: #f1f5f9; padding: 6px 12px; border-radius: 8px; margin-bottom: 10px; font-size: 0.8rem;">
        <span id="video-mode-status" style="color: #334155;">⚡ جاري التحقق من مصدر البث...</span>
        <div style="display: flex; gap: 6px;">
          <button type="button" id="btn-mode-native" onclick="setVideoPlayerMode('native')" style="padding: 3px 10px; font-size: 0.75rem; border-radius: 4px; border: 1px solid #cbd5e1; background: #2563eb; color: #fff; cursor: pointer; font-weight: 700;">⚡ محلي مباشر</button>
          <button type="button" id="btn-mode-cloud" onclick="setVideoPlayerMode('cloud')" style="padding: 3px 10px; font-size: 0.75rem; border-radius: 4px; border: 1px solid #cbd5e1; background: #fff; color: #334155; cursor: pointer; font-weight: 700;">🌐 سحابي بديل</button>
        </div>
      </div>

      <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px; background: #000; box-shadow: 0 4px 14px rgba(0,0,0,0.2);">
        <video id="native-video-player" controls playsinline controlslist="nodownload" preload="metadata" style="position: absolute; top:0; left: 0; width: 100%; height: 100%; border: 0; display: none; background: #000;"></video>
        <iframe id="video-iframe" style="position: absolute; top:0; left: 0; width: 100%; height: 100%; border: 0; display: none;" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div style="margin-top: 14px; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 0.8rem; color: #64748b;">
          💡 تحكم كامل بالسرعة والجودة بدون إعلانات وبدون تشتيت.
        </div>
        <button type="button" class="btn-primary" style="width: auto; padding: 8px 20px;" onclick="closeVideoModal()">
          ✓ استوعبت الشرح، العودة للامتحان
        </button>
      </div>
    </div>
  </div>"""

nc = content.replace("\r\n", "\n")
nt = target.replace("\r\n", "\n")
nr = replacement.replace("\r\n", "\n")

if nt in nc:
    nc = nc.replace(nt, nr, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(nc)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")
