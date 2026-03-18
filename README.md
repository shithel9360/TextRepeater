# Text Repeater App

A simple Python-based application that automatically types whatever message you want, repeatedly, with safety rate limits to avoid bans.

## Features
- Custom message input
- Custom message count
- Changeable delay between messages (rate limit)
- 5 seconds delay before starting
- Fail-safe (move mouse to a corner of the window to force stop)
- Dark UI Theme (CustomTkinter)

## Build Instructions (Windows)
1. Install Python 3
2. Open terminal and run: `pip install -r requirements.txt`
3. Then run: `pip install pyinstaller`
4. Compile to executable: `pyinstaller --noconsole --onefile main.py`
5. Your `.exe` file will be in the `dist/` folder!
