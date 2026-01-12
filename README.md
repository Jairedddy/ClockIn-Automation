# ClockIn Automation

Automated browser-based solution for clocking in to company attendance portals using Playwright. Features intelligent scheduling, screenshot documentation, and multi-channel notifications.

## ✨ Features

- 🤖 **Automated Clock-In**: Browser automation with persistent session management
- 📅 **Smart Scheduling**: Workday detection, holiday support, and manual skip dates
- 📸 **Screenshot Documentation**: Automatic capture at each step with retention management
- 🔔 **Multi-Channel Notifications**: Email (Gmail) and Telegram notifications
- 🔒 **Duplicate Prevention**: Lock mechanism and daily status tracking
- ⚙️ **Configurable**: JSON-based configuration for easy customization

## 📋 Prerequisites

- Python 3.11+
- Brave Browser (or Chromium-based browser)
- Gmail API credentials (`credentials.json`)
- Telegram Bot Token

## 🚀 Quick Start

### 1. Install Dependencies

```bash
py -3.11 -m pip install -r requirements.txt
playwright install chromium
```

### 2. Set Up Gmail API

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create OAuth 2.0 credentials and download as `credentials.json`
4. Place `credentials.json` in the project root

### 3. Configure Application

```bash
# Copy configuration templates
copy config.example.json config.json
copy secrets.example.json secrets.json
```

### 4. Fill in Configuration

**`secrets.json`** - Required settings:
- `brave_executable_path`: Path to Brave browser executable
- `brave_user_data_dir`: Path to Brave user data directory
- `portal_url`: Company attendance portal URL
- `corporate_email_identifier`: Email domain/identifier for account selection
- `telegram.bot_token`: Telegram bot token
- `telegram.allowed_user_id`: Your Telegram user ID

**`config.json`** - Optional settings:
- `enabled`: Enable/disable automation (default: `true`)
- `workdays`: List of workdays `[1,2,3,4,5]` (Monday-Friday)
- `holidays`: Array of holiday dates in `YYYY-MM-DD` format
- `skip_dates`: Manual skip dates in `YYYY-MM-DD` format
- `screenshot_retention_days`: Days to keep screenshots (default: `7`)

### 5. Authenticate Gmail API

Run the script once to trigger OAuth flow:
```bash
py -3.11 main.py
```

Authorize the application in your browser. Token will be saved to `token.json`.

## 📖 Usage

### Manual Execution

```bash
py -3.11 main.py
```

### Automated Scheduling

Set up a task scheduler for daily execution:

**Windows Task Scheduler:**
- Create a daily task at your preferred time
- Action: Run `py -3.11 main.py` from project directory

**Linux/Mac Cron:**
```bash
# Run at 9:00 AM on weekdays
0 9 * * 1-5 cd /path/to/ClockIn-Automation && py -3.11 main.py
```

## 📁 Project Structure

```
ClockIn-Automation/
├── main.py                 # Core automation script
├── gmail_notifier.py        # Gmail API integration
├── telegram_bot.py          # Telegram bot integration
├── config.json              # Runtime configuration (auto-generated)
├── config.example.json      # Configuration template
├── secrets.json             # Sensitive credentials (not committed)
├── secrets.example.json     # Secrets template
├── credentials.json         # Gmail API credentials (not committed)
├── token.json               # Gmail OAuth token (auto-generated)
├── screenshots/             # Screenshot storage (organized by date)
└── requirements.txt         # Python dependencies
```

## 🔐 Security Notes

⚠️ **Never commit** the following files:
- `config.json`
- `secrets.json`
- `credentials.json`
- `token.json`

These files contain sensitive information and should be kept secure.

## 🛠️ How It Works

1. **Pre-execution Checks**: Validates lock file, configuration, and run eligibility
2. **Browser Automation**: Launches Brave with persistent context, navigates to portal
3. **Authentication**: Clicks Google SAML login, selects corporate account
4. **Clock-In**: Locates and clicks clock-in button with retry logic (3 attempts)
5. **Documentation**: Captures screenshots at each critical step
6. **Notifications**: Sends success/failure notifications via Gmail and Telegram
7. **Cleanup**: Removes old screenshots and lock files

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Clock-in button not found | Verify portal URL and selectors. Check screenshots for visual debugging. |
| Gmail authentication failed | Delete `token.json` and re-authenticate on next run. |
| Telegram notifications not working | Verify bot token and user ID in `secrets.json`. |
| Browser not launching | Check Brave executable path and user data directory in `secrets.json`. |
| Script runs twice | Lock file mechanism prevents concurrent runs. Check for stale lock files. |

## 📝 License

Personal use only. Not intended for distribution.

---

For innovative enhancement ideas, see [IDEAS.md](IDEAS.md).
