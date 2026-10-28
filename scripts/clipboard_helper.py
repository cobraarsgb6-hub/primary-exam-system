import sys
import os
import win32clipboard
import win32con

def copy_file(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    target_path = os.path.join(project_dir, filename)
    
    if not os.path.exists(target_path):
        print(f"[ERROR] File not found: {target_path}")
        return False
        
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(content, win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    
    line_count = len(content.splitlines())
    char_count = len(content)
    print("=" * 65)
    print(f" [SUCCESS] Copied {filename} to Clipboard! ")
    print(f" Size: {char_count:,} characters ({line_count:,} lines)")
    print("=" * 65)
    print(f"\nNext Steps in Google Apps Script Editor:")
    print(f"1. Click on file '{filename}' in the left sidebar.")
    print(f"2. Press [Ctrl + A] to select all existing code.")
    print(f"3. Press [Backspace] or [Delete] to clear it completely.")
    print(f"4. Press [Ctrl + V] to paste the clean code.")
    print(f"5. Press [Ctrl + S] to save the file.")
    print("=" * 65)
    return True

if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "Code.gs"
    copy_file(fn)
