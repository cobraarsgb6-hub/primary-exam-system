"""
E2E Testing Harness and Browser Lifecycle Utilities
Provides standardized browser creation, mock injection, and assertions.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

base_proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if base_proj_dir not in sys.path:
    sys.path.insert(0, base_proj_dir)
from bundle import build_bundle

INDEX_HTML_PATH = build_bundle().replace('\\', '/')
MOCK_BRIDGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mock_bridge.js')).replace('\\', '/')

class E2EHarness:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.console_errors = []

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        self.page = self.context.new_page()
        
        # Intercept console errors
        self.page.on('console', self._handle_console)
        self.page.on('pageerror', self._handle_pageerror)

        # Inject RPC Mock Bridge and dialog bypass
        self.page.add_init_script(path=MOCK_BRIDGE_PATH)
        self.page.add_init_script("window.prompt = function(msg) { return '1990'; };")
        self.page.goto(f'file:///{INDEX_HTML_PATH}')
        self.page.wait_for_load_state('domcontentloaded')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _handle_console(self, msg):
        if msg.type in ['error']:
            # Filter expected known cross-origin favicon or simulation logs
            text = msg.text
            if 'favicon' not in text.lower():
                self.console_errors.append(f'Console Error: {text}')

    def _handle_pageerror(self, err):
        self.console_errors.append(f'Page Error: {str(err)}')

    def reset_state(self):
        try:
            self.page.evaluate('''() => {
                if (window.__mockBridge) window.__mockBridge.resetState();
                document.querySelectorAll(".modal-overlay.active").forEach(m => m.classList.remove("active"));
            }''')
        except Exception:
            pass
        self.console_errors.clear()

    def set_bridge_flag(self, flag_name, value):
        self.page.evaluate('(arg) => window.__mockBridge.setFlag(arg.key, arg.val)', {'key': flag_name, 'val': value})

    def get_bridge_state(self):
        return self.page.evaluate('() => window.__mockBridge.state')

    def reload_portal(self):
        self.page.goto(f'file:///{INDEX_HTML_PATH}')
        self.page.wait_for_load_state('domcontentloaded')

def run_test_case(name, func, results_list):
    """Executes a single test case with structured output and error capture."""
    start = time.perf_counter()
    print(f'  [RUNNING] {name} ...', end='', flush=True)
    try:
        func()
        duration = (time.perf_counter() - start) * 1000
        print(f'\r  [PASS] {name} ({duration:.1f}ms)')
        results_list.append({'name': name, 'status': 'PASS', 'duration_ms': duration, 'error': None})
        return True
    except Exception as e:
        duration = (time.perf_counter() - start) * 1000
        print(f'\r  [FAIL] {name} ({duration:.1f}ms) -> {str(e)}')
        results_list.append({'name': name, 'status': 'FAIL', 'duration_ms': duration, 'error': str(e)})
        return False
