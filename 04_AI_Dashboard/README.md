# 04_AI_Dashboard — website and question bot

- `app.py` reads SQLite, provides the dashboard API, and answers questions from its SQL analysis.
- `static/index.html` is the page layout and styles.
- `static/app.js` handles filters, buttons, charts, and chat requests.

From the main project folder, run `python 04_AI_Dashboard\app.py`, then visit `http://127.0.0.1:8000`. Without an OpenAI key, the bot uses its built-in rule-based answers.
