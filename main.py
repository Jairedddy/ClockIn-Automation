from sqlite3.dbapi2 import Timestamp
from webbrowser import Chrome
from playwright.sync_api import sync_playwright
from datetime import datetime
import os

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
USER_DATA_DIR = r"C:\Users\jaish\AppData\Local\BraveSoftware\Brave-Browser\User Data"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        executable_path=BRAVE_PATH,
        channel="chrome",
        headless=False,
        args=[
            "--profile-directory=Default",
            "--disable-blink-features=AutomationControlled"
        ]
    )
    
    page = context.new_page()
    page.goto("https://straive.darwinbox.com/", timeout=600000)
    
    page.wait_for_timeout(5000)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{SCREENSHOT_DIR}/step2_portal_{timestamp}.png"
    page.screenshot(path=screenshot_path)
    
    print("Portal Screenshot Saved: ", screenshot_path)
    
    input("Press ENTER to close the browser...")
    context.close()
    
    