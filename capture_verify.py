import os
from playwright.sync_api import sync_playwright

html_path = 'file:///' + os.path.abspath(r'C:/Users/co0ob/Projects/primary-exam-system/resources/coligo/Mostafa/Science 106/Electricity_Mastery_Guide_Stage6.html').replace('\\', '/')
out_dir = r'C:/Users/co0ob/.gemini/antigravity/brain/54d05bb7-093a-4520-bc55-e8fbc272480c'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 1300})
    page.goto(html_path)
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, 'flawless_day_default.png'), full_page=True)
    
    # 1. Select Pencil Lead in Day Mode
    page.evaluate("selectMaterial('pencil')")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, 'flawless_day_pencil.png'), full_page=True)

    # 2. Select Copper Coin in Day Mode
    page.evaluate("selectMaterial('coin')")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, 'flawless_day_coin.png'), full_page=True)
    
    # 3. Toggle Night Mode with Pencil
    page.evaluate("toggleThemeMode()")
    page.evaluate("selectMaterial('pencil')")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, 'flawless_night_pencil.png'), full_page=True)
    
    browser.close()
print('All 4 Playwright golden verification screenshots saved!')
