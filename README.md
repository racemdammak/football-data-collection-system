# HeroScore - Requirements & Launch Instructions

## Requirements

### 1. Python
- Python 3.9 or newer is recommended.
- Download from: https://www.python.org/downloads/

### 2. Required Python Packages
Install these packages using pip:

```sh
pip install customtkinter pillow
```

- `customtkinter` (for the modern UI)
- `Pillow` (for image handling)

### 3. Project Files & Structure

Your project folder should look like this:

```
HeroScore/
│
├── code/
│   ├── system.py
│   ├── event_popup.py
│   ├── video.py
│   ├── rules/
│   │   └── events.txt
│   ├── match/
│   │   ├── home_players.txt
│   │   ├── away_players.txt
│   │   ├── team_names.txt
│   │   └── match_stats.txt
│   └── logo_ico.ico
│
└── README.md
```

- Make sure `logo_ico.ico` is a valid `.ico` file and is in the `code/` directory.
- The `rules/events.txt` file should contain the list of event names, one per line.
- The `match/` folder should contain the required text files for players, teams, and stats.

### 4. Windows Requirements
- The code is designed for Windows (for icon support and file paths).
- If you use another OS, you may need to adjust file paths and icon handling.

---

## How to Launch

1. **Open a terminal** in the `code/` directory.
2. **Run the main script:**

```sh
python system.py
```

---

## Notes

- If you encounter errors about missing modules, double-check your Python and pip installation.
- If the icon does not show, ensure `logo_ico.ico` is a real `.ico` file and not just renamed from another format.
- For any issues with file paths, use absolute paths or check your working directory.

---

Enjoy using