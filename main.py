import os
import json
import subprocess

from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from gmail_notifier import send_email


def kill_brave():
    subprocess.run(
        ["taskkill", "/F", "/IM", "brave.exe"],
        stdout=subprocess.DEVNULL,
        sterr=subprocess.DEVNULL
    )

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def screenshot(page, name):
    path = f"screenshots/{name}_{timestamp()}.png"
    page.screenshot(path=path)
    return path

with open("secrets.json", "r") as f:
    
    secrets = json.load(f)
    
    BRAVE_PATH = secrets["brave_executable_path"]
    USER_DATA_DIR = secrets["brave_user_data_dir"]
    PORTAL_URL = secrets["portal_url"]
    CORP_EMAIL_ID = secrets["corporate_email_id"]
    
    os.makedirs("screenshots", exist_ok=True)
    
    screenshots_taken = []
    
    
try:
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
        
        page.goto(PORTAL_URL, timeout=600000)
        page.wait_for_timeout(5000)
        screenshots_taken.append(screenshot(page, "01_portal_loaded"))
        
        page.wait_for_selector("a[data-type='saml']", timeout=15000)
        page.locator(
            "a[data-type='saml']:has-text('Login with Google)"
        ).click()
        page.wait_for_timeout(4000)
        screenshots_taken.append(screenshot(page, "02_google_login_clicked"))
        
        page.locator(f"text={CORP_EMAIL_ID}").first.click(timeout=15000)
        page.wait_for_timeout(6000)
        screenshots_taken.append(screenshot(page, "03_corporate_google_account_selected"))
        
        try:
            page.locator("text=Skip").click(timeout=5000)
            page.wait_for_timeout(3000)
            screenshots_taken.append(screenshot(page, "04_mood_skipped"))
            
        except PlaywrightTimeoutError:
            pass
        
        clocked_in = False
        for attempt in range(1, 3):
            try:
                page.locator("text=Clock In").click(timeout=5000)
                page.wait_for_timeout(4000)
                screenshots_taken.append(screenshot(page, f"05_clockin_attempt_{attempt}"))
                clocked_in = True
                break
            except PlaywrightTimeoutError:
                if attempt == 3:
                    raise RuntimeError('Clock In Failedafter retries')
                
        context.close()
        
    if clocked_in:
        send_email(
            subject="Clock In Successful",
            body="Your Clock-In Automation Ran Successfully",
            attachments=screenshots_taken
        )
except Exception as e:
    send_email(
        subject="Clock In Automation Failed",
        body = str(e),
        attachments=screenshots_taken
    )
    raise