import os
from playwright.sync_api import sync_playwright
from PIL import Image

html_path = 'file:///' + os.path.abspath(r'C:/Users/co0ob/Projects/primary-exam-system/resources/coligo/Mostafa/Science 106/Electricity_Mastery_Guide_Stage6.html').replace('\\', '/')
out_dir = r'C:/Users/co0ob/.gemini/antigravity/brain/54d05bb7-093a-4520-bc55-e8fbc272480c'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 1300})
    page.goto(html_path)
    page.wait_for_timeout(800)

    for mat in ['coin', 'eraser', 'pencil', 'ruler']:
        page.evaluate(f"selectMaterial('{mat}')")
        page.wait_for_timeout(400)
        shot_path = os.path.join(out_dir, f'test_{mat}.png')
        page.screenshot(path=shot_path, full_page=True)
        im = Image.open(shot_path)
        im.crop((300, 340, 980, 720)).save(os.path.join(out_dir, f'crop_{mat}.png'))
        print(f'Captured {mat}')
    browser.close()
