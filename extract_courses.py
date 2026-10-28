import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\courses_dump.html", "r", encoding="utf-8") as f:
    html = f.read()

# Match <a data-testid="courseRecord" href="/parent/courses/...">...<h4 ...>Title</h4>...<p>Subject</p>...<p>Grade</p>
pattern = re.compile(r'href="(/parent/courses/[a-f0-9]+)"[\s\S]*?<h4[^>]*>([^<]+)</h4>[\s\S]*?<p[^>]*>([^<]+)</p>[\s\S]*?<p[^>]*>([^<]+)</p>')
matches = pattern.findall(html)

print(f"Total courses extracted: {len(matches)}")
for href, title, subject, grade in matches:
    print(f"  * [{title}] ({subject} - {grade})")
    print(f"    URL: https://coligolms.com{href}")
