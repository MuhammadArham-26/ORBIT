# ORBIT — Productivity Command Center

ORBIT is a clean, dark-themed productivity dashboard built with Python and Streamlit.

## Features
- Dashboard with mission and focus summaries
- Create, complete, filter, and delete missions
- Priority and category labels
- Focus-session logging
- XP and levels
- Achievement milestones
- Simple activity analytics

## Run locally
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

```bash
py -m venv .venv
.venv\Scripts\activate
```

4. Install dependencies and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Note
This starter version stores data in Streamlit session state. Missions and progress are not permanently saved after the session ends or the app restarts.

## Built with
- Python
- Streamlit
- HTML/CSS
