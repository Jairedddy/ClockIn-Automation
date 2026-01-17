# ClockIn Automation

## Description

A sophisticated automation tool designed to streamline the daily clock-in process for company attendance portals. This solution eliminates the need for manual, repetitive attendance logging by automating the entire workflow through intelligent browser automation. The system intelligently handles authentication flows, navigates complex portal interfaces, manages session persistence, and provides comprehensive documentation through automated screenshot capture. With built-in scheduling intelligence, the tool automatically detects workdays, respects holidays, and prevents duplicate clock-ins, ensuring reliable and compliant attendance tracking without human intervention.

## Tech

**Core Technologies:**
- Python 3.11+
- Playwright (Browser Automation Framework)
- Chromium/Brave Browser (Browser Engine)
- Google Gmail API (Email Notifications)
- Telegram Bot API (Telegram Notifications)

**Python Libraries:**
- `playwright` - Browser automation and web scraping
- `google-api-python-client` - Gmail API integration
- `google-auth` - Google OAuth2 authentication
- `google-auth-oauthlib` - OAuth2 flow management
- `google-auth-httplib2` - HTTP transport for Google APIs
- `requests` - HTTP library for Telegram API communication

**Browser & Automation:**
- Brave Browser (Chromium-based) with persistent user data directory
- Playwright Chromium engine for headless/headed browser control

## Features

### Core Automation
- **Automated Clock-In**: Intelligent browser automation with persistent session management using Brave browser's user data directory, eliminating the need for repeated logins
- **Smart Element Detection**: Advanced selector strategies with retry logic (up to 3 attempts) to handle dynamic page loads and network latency
- **Modal Handling**: Automatic detection and dismissal of survey modals and pop-ups that may interrupt the clock-in process
- **SAML Authentication**: Seamless integration with Google SAML login flows, including automatic corporate account selection

### Scheduling & Logic
- **Smart Scheduling**: Intelligent workday detection based on configurable weekday patterns (Monday-Friday by default)
- **Holiday Management**: Built-in holiday calendar support with date-based exclusion
- **Manual Skip Dates**: Flexible date-based skipping for personal time off or special circumstances
- **Duplicate Prevention**: Multi-layered protection including lock file mechanism and daily status tracking to prevent concurrent runs and duplicate clock-ins
- **Random Time Windows**: Configurable random delay windows to simulate human-like behavior (optional)

### Documentation & Monitoring
- **Screenshot Documentation**: Automatic capture at each critical step (portal load, login, account selection, clock-in attempts) with timestamped filenames
- **Organized Storage**: Screenshots organized by date in dedicated folders for easy tracking and debugging
- **Retention Management**: Automatic cleanup of old screenshots based on configurable retention period (default: 7 days)

### Notifications
- **Multi-Channel Notifications**: Dual notification system via Gmail and Telegram for redundancy
- **Rich Email Reports**: Gmail notifications with embedded screenshots as attachments for complete audit trail
- **Telegram Integration**: Real-time Telegram bot notifications with photo sharing for quick mobile access
- **Status Reporting**: Detailed notifications for success, failure, and skip scenarios with contextual information

### Configuration & Security
- **JSON-Based Configuration**: Simple, human-readable configuration files for easy customization without code changes
- **Separated Secrets**: Sensitive credentials isolated in separate configuration files (not committed to version control)
- **OAuth2 Security**: Secure Gmail API authentication using OAuth2 with automatic token refresh

## Prerequisites

### Software Requirements
- **Python 3.11 or higher** - Core runtime environment
- **Brave Browser** - Chromium-based browser with persistent user profile (or any Chromium-based browser)
- **Playwright Chromium** - Browser automation engine (installed via `playwright install chromium`)

### API Credentials
- **Gmail API Credentials** - OAuth2 credentials file (`credentials.json`) from Google Cloud Console
- **Telegram Bot Token** - Bot token from [@BotFather](https://t.me/botfather) on Telegram
- **Telegram User ID** - Your personal Telegram user ID for receiving notifications

### System Requirements
- **Windows/Linux/macOS** - Cross-platform support (Windows-specific process management in current implementation)
- **Internet Connection** - Required for portal access, Gmail API, and Telegram API
- **Sufficient Disk Space** - For screenshot storage (automatically managed with retention policies)

## Quick Start

### 1. Install Dependencies

```bash
py -3.11 -m pip install -r requirements.txt
playwright install chromium
```

### 2. Set Up Gmail API

1. **Create Google Cloud Project**
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Gmail API**
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials file and rename it to `credentials.json`

4. **Place Credentials File**
   - Move `credentials.json` to the project root directory
   - **Important**: Never commit this file to version control

### 3. Configure Application

**Windows:**
```bash
# Copy configuration templates
copy config.example.json config.json
copy secrets.example.json secrets.json
```

**Linux/macOS:**
```bash
# Copy configuration templates
cp config.example.json config.json
cp secrets.example.json secrets.json
```

### 4. Fill in Configuration

**`secrets.json`** - Required sensitive settings (never commit this file):

```json
{
  "brave_executable_path": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
  "brave_user_data_dir": "C:\\Users\\YourUsername\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data",
  "portal_url": "https://your-company-attendance-portal.com",
  "corporate_email_identifier": "@yourcompany.com",
  "telegram": {
    "bot_token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
    "allowed_user_id": 123456789
  }
}
```

- `brave_executable_path`: Full path to Brave browser executable (use forward slashes `/` or escaped backslashes `\\` on Windows)
- `brave_user_data_dir`: Full path to Brave user data directory (contains your browser profile and saved sessions)
- `portal_url`: Complete URL of your company's attendance/clock-in portal
- `corporate_email_identifier`: Email domain or identifier used to select the correct Google account during SAML login
- `telegram.bot_token`: Token obtained from [@BotFather](https://t.me/botfather) when creating your Telegram bot
- `telegram.allowed_user_id`: Your Telegram user ID (use [@userinfobot](https://t.me/userinfobot) to find your ID)

**`config.json`** - Runtime configuration (auto-generated, can be edited):

```json
{
  "enabled": true,
  "random_time_window_minutes": [-10, 20],
  "workdays": [1, 2, 3, 4, 5],
  "holidays": ["2024-12-25", "2025-01-01"],
  "skip_dates": ["2024-12-24"],
  "screenshot_retention_days": 7,
  "already_clocked_today": false,
  "last_run_date": "2024-01-15"
}
```

- `enabled`: Master switch to enable/disable automation (default: `true`)
- `random_time_window_minutes`: Time window for random delays `[min, max]` in minutes (currently disabled in code)
- `workdays`: Array of weekday numbers where `1=Monday, 2=Tuesday, ..., 7=Sunday` (default: `[1,2,3,4,5]` for weekdays)
- `holidays`: Array of holiday dates in `YYYY-MM-DD` format (e.g., `["2024-12-25", "2025-01-01"]`)
- `skip_dates`: Manual skip dates in `YYYY-MM-DD` format for personal time off
- `screenshot_retention_days`: Number of days to keep screenshots before automatic deletion (default: `7`)
- `already_clocked_today`: Internal flag (auto-managed) to prevent duplicate clock-ins
- `last_run_date`: Internal tracking (auto-managed) for daily reset logic

### 5. Authenticate Gmail API

Run the script once to trigger OAuth flow:
```bash
py -3.11 main.py
```

**First Run Authentication:**
1. A browser window will automatically open
2. Sign in with your Google account (the one you want to send notifications from)
3. Grant permissions for Gmail API access
4. The OAuth token will be automatically saved to `token.json`
5. Subsequent runs will use the saved token (auto-refreshed when expired)

**Note**: If authentication fails, delete `token.json` and run again to re-authenticate.

## Usage

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

## Project Structure

```
ClockIn-Automation/
├── main.py                      # Core automation script with browser control, scheduling logic, and orchestration
├── gmail_notifier.py             # Gmail API integration for email notifications with OAuth2 authentication
├── telegram_bot.py               # Telegram Bot API integration for text and photo notifications
├── config.json                   # Runtime configuration file (auto-generated, user-editable)
├── config.example.json           # Configuration template with default values and documentation
├── secrets.json                  # Sensitive credentials and API keys (NEVER commit to version control)
├── secrets.example.json          # Secrets template showing required fields and structure
├── credentials.json              # Gmail API OAuth2 credentials from Google Cloud Console (NEVER commit)
├── token.json                    # Gmail OAuth2 access token (auto-generated, auto-refreshed)
├── run.lock                      # Lock file preventing concurrent executions (auto-managed)
├── screenshots/                  # Screenshot storage directory
│   └── YYYY-MM-DD/              # Date-organized folders containing timestamped screenshots
│       ├── 01_portal_loaded_TIMESTAMP.png
│       ├── 02_google_login_clicked_TIMESTAMP.png
│       └── ...
├── requirements.txt              # Python package dependencies with version specifications
└── README.md                     # This comprehensive documentation file
```

### File Descriptions

- **`main.py`**: Main entry point containing browser automation logic, scheduling checks, screenshot capture, error handling, and notification triggers
- **`gmail_notifier.py`**: Handles Gmail API authentication, token management, and email composition with attachment support
- **`telegram_bot.py`**: Provides functions for sending text messages and photos via Telegram Bot API
- **`config.json`**: User-configurable runtime settings (workdays, holidays, retention policies) - auto-generated on first run
- **`secrets.json`**: Contains all sensitive information (browser paths, portal URLs, API tokens) - must be created manually
- **`credentials.json`**: Google OAuth2 credentials downloaded from Google Cloud Console
- **`token.json`**: OAuth2 access token automatically generated during first authentication
- **`run.lock`**: Temporary lock file created during execution to prevent concurrent runs

## Security Notes

### Sensitive Files (Never Commit to Version Control)

**CRITICAL WARNING**: The following files contain sensitive information and must **NEVER** be committed to version control (Git, SVN, etc.):

- **`secrets.json`**: Contains browser paths, portal URLs, Telegram bot tokens, and user IDs
- **`credentials.json`**: Contains Google OAuth2 client credentials with client ID and secret
- **`token.json`**: Contains OAuth2 access and refresh tokens for Gmail API
- **`config.json`**: May contain sensitive configuration data (though less critical)

### Security Best Practices

1. **Git Ignore**: Ensure `.gitignore` includes:
   ```
   config.json
   secrets.json
   credentials.json
   token.json
   run.lock
   screenshots/
   ```

2. **File Permissions**: On Linux/macOS, restrict file permissions:
   ```bash
   chmod 600 secrets.json credentials.json token.json
   ```

3. **Credential Rotation**: Regularly rotate Telegram bot tokens and Google OAuth credentials if compromised

4. **Local Storage Only**: Keep sensitive files only on your local machine or secure, encrypted storage

5. **Token Security**: OAuth tokens in `token.json` are automatically refreshed but should be protected from unauthorized access

6. **Telegram Bot Security**: Limit Telegram bot access to only your user ID; never share bot tokens publicly

## How It Works

### Execution Flow

1. **Pre-execution Checks**
   - Validates lock file existence and age (prevents concurrent runs)
   - Loads and validates configuration files (`config.json`, `secrets.json`)
   - Checks if automation is enabled
   - Verifies run eligibility based on workdays, holidays, and skip dates
   - Resets daily status flags if it's a new day
   - Cleans up old screenshots based on retention policy

2. **Browser Initialization**
   - Terminates any existing Brave browser processes to ensure clean state
   - Launches Brave browser with persistent user data directory (maintains login sessions)
   - Creates new browser context with automation detection disabled
   - Opens new page and navigates to configured portal URL

3. **Portal Navigation & Modal Handling**
   - Waits for portal to fully load (60-second timeout)
   - Captures initial screenshot (`01_portal_loaded.png`)
   - Detects and dismisses survey modals (e.g., "How are you feeling at work today?")
   - Uses multiple selector strategies and keyboard shortcuts (Escape key) for modal dismissal

4. **Authentication Flow**
   - Detects SAML login button (`a[data-type='saml']`) if user is not authenticated
   - Clicks "Login with Google" button
   - Waits for Google account selection screen
   - Automatically selects corporate account based on email identifier
   - Handles post-login survey modals if they appear
   - Captures screenshots at each authentication step

5. **Clock-In Process**
   - Locates clock-in button using selector `li.clockinout_btn.prevent-close`
   - Implements retry logic with 3 attempts (8-second timeout per attempt)
   - Clicks clock-in button and waits for confirmation
   - Captures screenshot after each attempt for debugging
   - Raises error if button not found after all retries

6. **Documentation & Notifications**
   - Collects all screenshots taken during execution
   - Sends success email via Gmail API with all screenshots as attachments
   - Sends Telegram text notification
   - Sends each screenshot individually via Telegram Bot API
   - Updates configuration with `already_clocked_today` flag

7. **Error Handling & Cleanup**
   - Catches and logs any exceptions during execution
   - Sends failure notification with error details and available screenshots
   - Removes lock file in `finally` block to ensure cleanup
   - Closes browser context and terminates browser processes

### Key Technical Details

- **Lock File Mechanism**: Prevents concurrent script executions using `run.lock` file with process ID and timestamp validation
- **Persistent Sessions**: Uses Brave's user data directory to maintain login state across runs
- **Screenshot Organization**: Screenshots stored in `screenshots/YYYY-MM-DD/` folders with timestamped filenames
- **Selector Strategies**: Multiple fallback selectors for modal dismissal to handle UI variations
- **Timeout Management**: Configurable timeouts for page loads, element detection, and network operations

## Troubleshooting

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Clock-in button not found** | Script fails with "Clock In button not clickable after retries" | 1. Verify `portal_url` in `secrets.json` is correct<br>2. Check if portal UI has changed (inspect screenshots)<br>3. Verify selector `li.clockinout_btn.prevent-close` still matches<br>4. Check if page fully loaded (review `01_portal_loaded.png`) |
| **Gmail authentication failed** | Error: "Invalid credentials" or OAuth flow errors | 1. Delete `token.json` file<br>2. Verify `credentials.json` exists and is valid<br>3. Re-run script to trigger OAuth flow<br>4. Ensure Gmail API is enabled in Google Cloud Console |
| **Telegram notifications not working** | No Telegram messages received | 1. Verify `telegram.bot_token` in `secrets.json`<br>2. Verify `telegram.allowed_user_id` matches your Telegram ID<br>3. Test bot token with: `curl https://api.telegram.org/bot<TOKEN>/getMe`<br>4. Ensure bot is not blocked or deleted |
| **Browser not launching** | Error: "Executable doesn't exist" or browser fails to start | 1. Verify `brave_executable_path` points to actual Brave executable<br>2. Check `brave_user_data_dir` path is correct<br>3. Ensure Brave browser is installed<br>4. Try running Brave manually to verify it works |
| **Script runs twice** | Duplicate clock-ins or concurrent execution errors | 1. Check for stale `run.lock` file (older than 1 hour)<br>2. Manually delete `run.lock` if script crashed previously<br>3. Verify no other instances are running<br>4. Check Task Scheduler for duplicate scheduled tasks |
| **Survey modal blocking login** | Script stuck or fails at authentication step | 1. Review screenshots to see modal appearance<br>2. Check if modal text/selectors have changed<br>3. Script handles common modals automatically<br>4. If new modal type appears, update selectors in `main.py` |
| **Screenshots not being captured** | Missing screenshot files or empty folders | 1. Verify `screenshots/` directory has write permissions<br>2. Check disk space availability<br>3. Review script logs for screenshot errors<br>4. Ensure Playwright is properly installed |
| **Portal timeout errors** | "Navigation timeout" or "Page load timeout" | 1. Check internet connection<br>2. Verify portal URL is accessible<br>3. Increase timeout values in code if portal is slow<br>4. Check if portal requires VPN or special network access |
| **Already clocked in error** | Script skips with "Already clocked in" message | 1. This is expected behavior (duplicate prevention)<br>2. If you need to run again, set `already_clocked_today: false` in `config.json`<br>3. Flag resets automatically at midnight |

### Debugging Tips

1. **Review Screenshots**: Check the `screenshots/` directory for visual debugging of each step
2. **Check Configuration**: Verify all paths and URLs in `secrets.json` are correct
3. **Test Manually**: Run the portal login flow manually to identify UI changes
4. **Enable Verbose Logging**: Add print statements or logging to track execution flow
5. **Verify Dependencies**: Run `pip list` to ensure all packages from `requirements.txt` are installed

## License

Personal use only. Not intended for distribution.

---

For innovative enhancement ideas, see [IDEAS.md](IDEAS.md).
