import re

path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update doGet
target_doget = """  template.examCode = examCode;
  template.initialStudent = student;
  template.initialAdmin = admin;
  
  return template.evaluate()"""

replacement_doget = """  template.examCode = examCode;
  template.initialStudent = student;
  template.initialAdmin = admin;
  template.driveVideos = JSON.stringify(getDriveVideosMap());
  
  return template.evaluate()"""

# 2. Update getAdminDashboardData return
target_admin_return = """    return {
      success: true,
      sheetUrl: ss.getUrl(),
      submissions: submissions,
      exams: exams,
      allQuestions: allQuestions,
      retakeRequests: retakeRequests,
      studyPlan: studyPlan
    };"""

replacement_admin_return = """    return {
      success: true,
      sheetUrl: ss.getUrl(),
      submissions: submissions,
      exams: exams,
      allQuestions: allQuestions,
      retakeRequests: retakeRequests,
      studyPlan: studyPlan,
      driveVideos: getDriveVideosMap(),
      driveFolderId: PropertiesService.getScriptProperties().getProperty('DRIVE_VIDEOS_FOLDER_ID') || ''
    };"""

# 3. Add Google Drive video sync functions at the end
drive_functions = """

/**
 * ====================================================================
 * GOOGLE DRIVE EDUCATIONAL VIDEO SYNC & STREAMING ENGINE
 * ====================================================================
 */

function syncGoogleDriveVideos(folderIdOrUrl) {
  if (!folderIdOrUrl) {
    return { success: false, message: 'Please provide a valid Google Drive folder URL or ID.' };
  }

  let folderId = String(folderIdOrUrl).trim();
  const match = folderId.match(/folders\\/([a-zA-Z0-9_-]+)/);
  if (match) {
    folderId = match[1];
  }

  try {
    const folder = DriveApp.getFolderById(folderId);
    const files = folder.getFiles();
    const videoMap = {};
    let count = 0;

    while (files.hasNext()) {
      const file = files.next();
      const name = file.getName();
      const fileId = file.getId();

      // Extract bracketed YouTube ID e.g. [WYOD4qXW0SE] or filename without extension
      const idMatch = name.match(/\\[([a-zA-Z0-9_-]+)\\]/);
      const videoKey = idMatch ? idMatch[1] : name.replace(/\\.[^/.]+$/, '');

      videoMap[videoKey] = {
        fileId: fileId,
        fileName: name,
        previewUrl: 'https://drive.google.com/file/d/' + fileId + '/preview',
        streamUrl: 'https://drive.google.com/uc?export=download&id=' + fileId
      };
      count++;
    }

    PropertiesService.getScriptProperties().setProperty('DRIVE_VIDEOS_MAP', JSON.stringify(videoMap));
    PropertiesService.getScriptProperties().setProperty('DRIVE_VIDEOS_FOLDER_ID', folderId);

    return {
      success: true,
      count: count,
      videoMap: videoMap,
      folderId: folderId,
      message: 'Successfully linked ' + count + ' educational videos from Google Drive!'
    };
  } catch (err) {
    return { success: false, message: 'Google Drive folder access error: ' + err.message };
  }
}

function getDriveVideosMap() {
  try {
    const raw = PropertiesService.getScriptProperties().getProperty('DRIVE_VIDEOS_MAP');
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    return {};
  }
}
"""

nc = content.replace("\r\n", "\n")
td = target_doget.replace("\r\n", "\n")
rd = replacement_doget.replace("\r\n", "\n")
ta = target_admin_return.replace("\r\n", "\n")
ra = replacement_admin_return.replace("\r\n", "\n")

if td in nc and ta in nc:
    nc = nc.replace(td, rd, 1)
    nc = nc.replace(ta, ra, 1)
    nc = nc.strip() + drive_functions
    with open(path, "w", encoding="utf-8") as f:
        f.write(nc)
    print("SUCCESSFULLY UPDATED CODE.GS")
else:
    print("MATCH FAILED", "td in nc:", td in nc, "ta in nc:", ta in nc)
