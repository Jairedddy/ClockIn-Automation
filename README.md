# ClockIn Automation

Personal automation to clock in to a company portal using Playwright

## Setup
1. Install Python 3.11
2. Install dependencies:
`
py -3.11 -m pip install -r requirements.txt
playwright install chromium
`
3. Copy config file:
`
config.example.json -> config.json
`
4. Copy secrets file:
`
secrets.example.json -> secrets.json
`
5. Fill in values in `secrets.json`
6. Run:
`
py -3.11 main.py
`

## Notes
- `config.json` is modified automatically at runtime
- Do NOT commit `config.json` or `secrets.json`