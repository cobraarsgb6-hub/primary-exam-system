import os
from playwright.sync_api import sync_playwright
from PIL import Image

html_path = 'file:///' + os.path.abspath(r'C:/Users/co0ob/Projects/primary-exam-system/resources/coligo/Mostafa/Science 106/Electricity_Mastery_Guide_Stage6.html').replace('\\', '/')
out_dir = r'C:/Users/co0ob/.gemini/antigravity/brain/54d05bb7-093a-4520-bc55-e8fbc272480c'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 1300})
    page.goto(html_path)
    page.wait_for_timeout(1000)
    
    # 1. Default (Empty Air Gap)
    p_empty = os.path.join(out_dir, 'flawless_air_gap_full.png')
    page.screenshot(path=p_empty, full_page=True)
    
    # 2. Pencil
    page.evaluate("selectMaterial('pencil')")
    page.wait_for_timeout(800)
    p_pencil = os.path.join(out_dir, 'flawless_pencil_full.png')
    page.screenshot(path=p_pencil, full_page=True)
    
    browser.close()

# Crop the specimen stage from both images to inspect
im_empty = Image.open(p_empty)
im_empty.crop((350, 360, 950, 680)).save(os.path.join(out_dir, 'crop_air_gap_fixed.png'))

im_pencil = Image.open(p_pencil)
im_pencil.crop((350, 360, 950, 680)).save(os.path.join(out_dir, 'crop_pencil_fixed.png'))

print('Screenshots and crops saved!')
