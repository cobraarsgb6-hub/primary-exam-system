# -*- coding: utf-8 -*-
"""
Add explicit Reading Passages to Code.gs and Index.html.
Ensures comprehension questions display the full authentic passage on screen!
"""

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'r', encoding='utf-8') as f:
    code = f.read()

# Passages:
# 1. English Fantasy Passage (The City That Waited - Part 6)
eng_fantasy_passage = """The city was a hush. Pale light crept over the cobbles of the deserted square. In the courtyard, the old stone fountain whispered to itself as thin streams of water trickled into the basin. Its white walls glowed like the inside of a seashell in the twilight. High above, the iron gates closed with a mournful sigh, and shadows stretched along the walls, long and thin as fingers. No one walked the silent streets..."""

# 2. English Sea Turtles Report Draft Passage (Session 7 Homework)
eng_turtle_passage = """Sea turtles are in danger because people throw plastic and rubbish into the sea. People can stop throwing plastic into the sea and join beach clean-ups. People can also ask boats and ships not to dump rubbish into the ocean. Protecting sea turtles matters because they help keep the ocean healthy. If they disappear, marine ecosystems will suffer greatly."""

# 3. Arabic Reading Passage (سلاح التلميذ - إدارة الوقت وتنظيم الأولويات)
arb_passage = """الوقتُ كنزٌ ثمينٌ وعطاءٌ إلهي عظيم، والنجاحُ في الحياة لا يتحقق بالأماني، وإنما بحسن إدارة يومنا وترتيب أولوياتنا. يتطلب إنجاز المهام وقتاً محدداً وتركيزاً حثيثاً، والبدء بالأهم قبل المهم. كما يحذر الخبراء من تبديد الوقت في المشتتات وتأجيل عمل اليوم إلى الغد، فالأشخاص الذين ينظمون أوقاتهم هم الأكثر قدرة على تحقيق طموحاتهم وخدمة وطنهم."""

print("Passages defined.")
