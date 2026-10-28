import json

# Read current token from local_storage.json
with open(r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\local_storage.json", "r", encoding="utf-8") as f:
    ls = json.load(f)

active_token = ls.get("token", "")
semester_id = "6aa6b7d7382ba9a416a84790"
parent_id = "68da691317e1492e0ffcd878"

code_to_append = f"""

/**
 * ====================================================================
 * COLIGO CLOUD AUTOMATED SYNC & INGESTION ENGINE
 * Runs 100% Online on Google Cloud (24/7 without requiring local PC)
 * ====================================================================
 */

var COLIGO_CONFIG_DEFAULT = {{
  baseUrl: 'https://prod-api.coligolms.com/api',
  semesterId: '{semester_id}',
  parentId: '{parent_id}',
  defaultToken: '{active_token}',
  students: [
    {{ name: 'Ali', id: '68da68c843e7498ddb5573ba', grade: 'Year 5A' }},
    {{ name: 'Mostafa', id: '68e6ac96b5f1511f61d47eea', grade: 'Year 6A' }}
  ]
}};

function getColigoToken_() {{
  var prop = PropertiesService.getScriptProperties().getProperty('COLIGO_JWT_TOKEN');
  return prop || COLIGO_CONFIG_DEFAULT.defaultToken;
}}

function saveColigoToken(newToken) {{
  if (!newToken || !newToken.trim()) {{
    return {{ success: false, message: 'Invalid token provided.' }};
  }}
  PropertiesService.getScriptProperties().setProperty('COLIGO_JWT_TOKEN', newToken.trim());
  return {{ success: true, message: 'Coligo cloud authentication token updated successfully!' }};
}}

function getOrCreateColigoFolder_(folderName, parentFolder) {{
  var parent = parentFolder || DriveApp.getRootFolder();
  var folders = parent.getFoldersByName(folderName);
  if (folders.hasNext()) {{
    return folders.next();
  }}
  var newFolder = parent.createFolder(folderName);
  newFolder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  return newFolder;
}}

/**
 * Main Online Coligo Cloud Synchronization
 * Can be called manually from Parent Portal or automatically via Time-driven Trigger
 */
function syncColigoOnline(manualTrigger) {{
  var token = getColigoToken_();
  if (!token) {{
    return {{ success: false, message: 'Coligo token is missing. Please set it in Settings.' }};
  }}

  var headers = {{
    'Authorization': 'JWT ' + token,
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  }};

  var ss = getSpreadsheet();
  var sheet = ss.getSheetByName('Coligo_Hub');
  if (!sheet) {{
    sheet = ss.insertSheet('Coligo_Hub');
    sheet.appendRow([
      'Timestamp', 'Student', 'Grade', 'Course', 'Item Type', 'Title', 
      'Cloud File URL / Link', 'Note Content / Details', 'Drive File ID', 'Original URL'
    ]);
    sheet.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#0284c7').setFontColor('#ffffff');
    sheet.setFrozenRows(1);
  }}

  // Read existing IDs/URLs to avoid duplicate downloads
  var existingMap = {{}};
  if (sheet.getLastRow() > 1) {{
    var sheetData = sheet.getDataRange().getValues();
    for (var r = 1; r < sheetData.length; r++) {{
      var origUrl = String(sheetData[r][9] || sheetData[r][6] || '');
      var titleKey = String(sheetData[r][1] || '') + '_' + String(sheetData[r][3] || '') + '_' + String(sheetData[r][5] || '');
      if (origUrl) existingMap[origUrl] = true;
      if (titleKey) existingMap[titleKey] = true;
    }}
  }}

  var rootDrive = getOrCreateColigoFolder_('Coligo_School_Materials');
  var totalNewFiles = 0;
  var totalNewLinks = 0;
  var totalNewNotes = 0;
  var syncedItems = [];

  var students = COLIGO_CONFIG_DEFAULT.students;

  for (var s = 0; s < students.length; s++) {{
    var student = students[s];
    var studentFolder = getOrCreateColigoFolder_(student.name + ' (' + student.grade + ')', rootDrive);

    // 1. Fetch Student Courses
    var coursesUrl = COLIGO_CONFIG_DEFAULT.baseUrl + '/v1/semesters/' + COLIGO_CONFIG_DEFAULT.semesterId + '/users/' + student.id + '/courses';
    var courses = [];
    try {{
      var cResp = UrlFetchApp.fetch(coursesUrl, {{ headers: headers, muteHttpExceptions: true }});
      if (cResp.getResponseCode() === 200) {{
        var cData = JSON.parse(cResp.getContentText());
        courses = cData.data || cData;
      }}
    }} catch (e) {{
      Logger.log('Error fetching courses for ' + student.name + ': ' + e);
      continue;
    }}

    for (var c = 0; c < courses.length; c++) {{
      var course = courses[c];
      var courseId = course._id;
      var courseTitle = course.title || course.name || 'Course';
      
      // 2. Fetch Course Materials
      var matUrl = COLIGO_CONFIG_DEFAULT.baseUrl + '/v2/courses/' + courseId + '/materials';
      var materials = [];
      try {{
        var mResp = UrlFetchApp.fetch(matUrl, {{ headers: headers, muteHttpExceptions: true }});
        if (mResp.getResponseCode() === 200) {{
          materials = JSON.parse(mResp.getContentText());
        }}
      }} catch (e) {{
        continue;
      }}

      var courseFolder = null; // Lazy create folder only if new files exist

      for (var m = 0; m < materials.length; m++) {{
        var item = materials[m];
        var itemType = item.type;
        var title = item.title || 'Untitled';
        var itemUrl = item.url || item.link || '';
        var content = item.content || item.description || '';
        var titleKey = student.name + '_' + courseTitle + '_' + title;

        if (itemUrl && existingMap[itemUrl]) continue;
        if (existingMap[titleKey]) continue;

        var driveUrl = '';
        var driveFileId = '';
        var nowStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');

        // Handle File Download directly to Google Drive
        if (itemType === '@material-type/file' && itemUrl) {{
          try {{
            if (!courseFolder) {{
              courseFolder = getOrCreateColigoFolder_(courseTitle, studentFolder);
            }}
            var fResp = UrlFetchApp.fetch(itemUrl, {{ muteHttpExceptions: true }});
            if (fResp.getResponseCode() === 200) {{
              var blob = fResp.getBlob();
              var ext = itemUrl.indexOf('.pdf') !== -1 ? '.pdf' : (itemUrl.indexOf('.docx') !== -1 ? '.docx' : (itemUrl.indexOf('.pptx') !== -1 ? '.pptx' : ''));
              var cleanFileName = title.replace(/[\\\\/*?:\"<>|]/g, '_');
              if (ext && cleanFileName.indexOf(ext) === -1) cleanFileName += ext;
              blob.setName(cleanFileName);

              var dFile = courseFolder.createFile(blob);
              dFile.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
              driveFileId = dFile.getId();
              driveUrl = dFile.getUrl();
              totalNewFiles++;
            }}
          }} catch (err) {{
            Logger.log('Drive file upload error: ' + err);
          }}
        }} else if (itemType === '@material-type/link' || (itemUrl && itemUrl.indexOf('youtube') !== -1)) {{
          driveUrl = itemUrl;
          totalNewLinks++;
        }} else if (itemType === '@material-type/note' || content) {{
          totalNewNotes++;
        }}

        sheet.appendRow([
          nowStr, student.name, student.grade, courseTitle, itemType, title,
          driveUrl, content, driveFileId, itemUrl
        ]);
        existingMap[itemUrl] = true;
        existingMap[titleKey] = true;

        syncedItems.push({{
          student: student.name,
          course: courseTitle,
          type: itemType,
          title: title,
          url: driveUrl || itemUrl,
          content: content
        }});
      }}
    }}
  }}

  var resultMessage = 'مزامنة سحابية ناجحة! تم رصد وتحميل (' + totalNewFiles + ') ملف جديد إلى Google Drive، و(' + totalNewLinks + ') رابط جديد، و(' + totalNewNotes + ') ملاحظة رسمية.';
  return {{
    success: true,
    message: resultMessage,
    totalNewFiles: totalNewFiles,
    totalNewLinks: totalNewLinks,
    totalNewNotes: totalNewNotes,
    rootFolderUrl: rootDrive.getUrl(),
    items: syncedItems
  }};
}}

/**
 * Configure Daily Autonomous Trigger on Google Cloud (Runs 24/7 without laptop)
 */
function setupColigoAutoSyncTrigger() {{
  // Delete previous triggers if exist
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {{
    if (triggers[i].getHandlerFunction() === 'syncColigoOnline') {{
      ScriptApp.deleteTrigger(triggers[i]);
    }}
  }}
  // Create daily trigger at 15:30 (3:30 PM Cairo Time)
  ScriptApp.newTrigger('syncColigoOnline')
    .timeBased()
    .everyDays(1)
    .atHour(15)
    .nearMinute(30)
    .create();

  return {{ success: true, message: 'تم تفعيل المجدول السحابي اليومي بنجاح! سيعمل تلقائياً الساعة 3:30 عصراً حتى لو كان جهازك مغلقاً.' }};
}}

function getColigoCloudStatus() {{
  var triggers = ScriptApp.getProjectTriggers();
  var isAutoActive = false;
  for (var i = 0; i < triggers.length; i++) {{
    if (triggers[i].getHandlerFunction() === 'syncColigoOnline') {{
      isAutoActive = true;
      break;
    }}
  }}
  var ss = getSpreadsheet();
  var sheet = ss.getSheetByName('Coligo_Hub');
  var itemsCount = sheet ? Math.max(0, sheet.getLastRow() - 1) : 0;

  return {{
    isAutoActive: isAutoActive,
    itemsCount: itemsCount,
    hasToken: Boolean(getColigoToken_())
  }};
}}
"""

path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(path, "r", encoding="utf-8") as f:
    orig = f.read()

if "COLIGO CLOUD AUTOMATED SYNC" not in orig:
    with open(path, "w", encoding="utf-8") as f:
        f.write(orig.strip() + "\n" + code_to_append)
    print("SUCCESSFULLY APPENDED COLIGO CLOUD ENGINE TO CODE.GS")
else:
    print("ALREADY PRESENT")
