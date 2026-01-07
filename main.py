import os
import json
import subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def kill_brave():
    subprocess.run(
        ["taskkill", "/F", "/IM", "brave.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def screenshot(page, name):
    path = f"screenshots/{name}_{timestamp()}.png"
    page.screenshot(path=path)
    print("Screeshot: ", path)
    
    
with open("secrets.json", "r") as f:
    secrets = json.load(f)
    
BRAVE_PATH = secrets["brave_executable_path"]
USER_DATA_DIR = secrets["brave_user_data_dir"]
PORTAL_URL = secrets["portal_url"]

os.makedirs("screenshots", exist_ok=True)


print('Closing Brave if running...')
kill_brave()

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
    print("Opening portal...")
    page.goto(PORTAL_URL, timeout=600000)
    page.wait_for_timeout(5000)
    screenshot(page, "01_portal_loaded")
    
    
    print("Clicking 'Login with Google'...")
    page.locator("text=Login with Google").click()
    page.wait_for_timeout(4000)
    screenshot(page, "02_google_login_clicked")
    
    print("Selecting corporate Google account...")
    try:
        page.locator("text=@straive.com").first.click(timeout=15000)
    except PlaywrightTimeoutError:
        screenshot(page, "Error_google_account_not_fount")
        raise RuntimeError("Corporate Google account not found")
    
    page.wait_for_timeout(6000)
    screenshot(page, "03_corporate_google_account_selected")
    
    
    print("Handling mood popup (if present)...")
    try:
        page.locator("text=Skip").click(timeout=5000)
        page.wait_for_timeout(3000)
        screenshot(page, "04_mood_skipped")
    except PlaywrightTimeoutError:
        print("No mood popup detected")
        
    print("Step 3 completed successfully")
    input("Press ENTER to close browser...")
    context.close()