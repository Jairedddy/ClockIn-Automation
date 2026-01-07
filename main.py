import os
import json
import subprocess
import random
import time
from datetime import datetime, timedelta

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from gmail_notifier import send_email
from telegram_bot import send_telegram_message, send_telegram_photo

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def save_config(cfg):
    with open("config.json", "w") as f:
        json.dump(cfg, f, indent=2)


def should_run_today(cfg):
    today = datetime.now().date()
    today_str = today.isoformat()

    if not cfg["enabled"]:
        return False, "Automation disabled"

    if today.weekday() + 1 not in cfg["workdays"]:
        return False, "Not a workday"

    if today_str in cfg["skip_dates"]:
        return False, "Manually skipped"

    if today_str in cfg["holidays"]:
        return False, "Holiday"

    if cfg.get("already_clocked_today"):
        return False, "Already clocked in"

    return True, "Allowed"


def random_delay_seconds(cfg):
    min_m, max_m = cfg["random_time_window_minutes"]
    return random.randint(min_m * 60, max_m * 60)

def kill_brave():
    subprocess.run(
        ["taskkill", "/F", "/IM", "brave.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def cleanup_old_screenshots(retention_days):
    screenshots_root = "screenshots"
    if not os.path.exists(screenshots_root):
        return
    
    cutoff = datetime.now() - timedelta(days=retention_days)
    
    for folder in os.listdir(screenshots_root):
        folder_path = os.path.join(screenshots_root, folder)
        
        if not os.path.isdir(folder_path):
            continue
        
        try:
            folder_date = datetime.strptime(folder, "%Y%m%d")
        except ValueError:
            continue
        
        if folder_date < cutoff:
            for file in os.listdir(folder_path):
                os.remove(os.path.join(folder_path, file))
            os.rmdir(folder_path)

def screenshot(page, name):
    today_folder = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join("screenshots", today_folder)
    
    os.makedirs(folder_path, exist_ok=True)
    
    path = os.path.join(
        folder_path,
        f"{name}_{timestamp()}.png"
    )
    
    page.screenshot(path=path)
    return path

with open("secrets.json", "r") as f:
    secrets = json.load(f)

BRAVE_PATH = secrets["brave_executable_path"]
USER_DATA_DIR = secrets["brave_user_data_dir"]
PORTAL_URL = secrets["portal_url"]
CORP_EMAIL_ID = secrets["corporate_email_identifier"]
TELEGRAM_TOKEN = secrets["telegram"]["bot_token"]
TELEGRAM_USER_ID = secrets["telegram"]["allowed_user_id"]

os.makedirs("screenshots", exist_ok=True)
screenshots_taken = []

LOCK_FILE = "run.lock"

if os.path.exists(LOCK_FILE):
    if time.time() - os.path.getmtime(LOCK_FILE) > 3600:
        os.remove(LOCK_FILE)
    else:
        exit(0)

with open(LOCK_FILE, "w") as f:
    f.write(str(os.getpid()))


try:
    config = load_config()

    today_str = datetime.now().date().isoformat()
    if config.get("last_run_date") != today_str:
        config["already_clocked_today"] = False
        config["last_run_date"] = today_str
        save_config(config)
        
    cleanup_old_screenshots(config.get("screenshot_retention_days", 7))

    allowed, reason = should_run_today(config)

    if not allowed:
        send_email(
            subject="⏭️ Clock In Skipped",
            body=f"Clock-in skipped today: {reason}"
        )
        
        send_telegram_message(
            TELEGRAM_TOKEN,
            TELEGRAM_USER_ID,
            f" Clock In Skipped: {reason}"
        )
        
        exit(0)

    delay = 0
    #delay = random_delay_seconds(config)
    #time.sleep(delay)

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

        page.goto(PORTAL_URL, timeout=60000)
        page.wait_for_timeout(5000)
        screenshots_taken.append(screenshot(page, "01_portal_loaded"))

        page.wait_for_selector("a[data-type='saml']", timeout=15000)
        page.locator(
            "a[data-type='saml']:has-text('Login with Google')"
        ).click()
        page.wait_for_timeout(4000)
        screenshots_taken.append(screenshot(page, "02_google_login_clicked"))

        page.locator(f"text={CORP_EMAIL_ID}").first.click(timeout=15000)
        page.wait_for_timeout(6000)
        screenshots_taken.append(
            screenshot(page, "03_corporate_account_selected")
        )

        try:
            page.locator("text=Skip").click(timeout=5000)
            page.wait_for_timeout(3000)
            screenshots_taken.append(screenshot(page, "04_mood_skipped"))
        except PlaywrightTimeoutError:
            pass

        clocked_in = False

        for attempt in range(1, 4):
            try:
                page.wait_for_selector(
                    "li.clockinout_btn.prevent-close",
                    timeout=8000
                )
                page.locator(
                    "li.clockinout_btn.prevent-close"
                ).click()

                page.wait_for_timeout(4000)
                screenshots_taken.append(
                    screenshot(page, f"05_clockin_attempt_{attempt}")
                )

                clocked_in = True
                break

            except PlaywrightTimeoutError:
                if attempt == 3:
                    raise RuntimeError(
                        "Clock In button not clickable after retries"
                    )

        context.close()

    if clocked_in:
        config["already_clocked_today"] = True
        save_config(config)

        send_email(
            subject="✅ Clock In Successful",
            body="Your clock-in automation ran successfully.",
            attachments=screenshots_taken
        )
        
        send_telegram_message(
            TELEGRAM_TOKEN,
            TELEGRAM_USER_ID,
            "Clock In Successful"
        )
        
        for i in range(len(screenshots_taken)):
            send_telegram_photo(
                TELEGRAM_TOKEN,
                TELEGRAM_USER_ID,
                screenshots_taken[i]
            )

except Exception as e:
    send_email(
        subject="❌ Clock In Automation Failed",
        body=str(e),
        attachments=screenshots_taken
    )
    raise

finally:
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
