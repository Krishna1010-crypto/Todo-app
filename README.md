# To-Do App (Full-Stack: Python + JavaScript)

A simple full-stack to-do list app — Flask backend, SQLite database, vanilla JavaScript frontend.

## Features
- Add, complete, and delete tasks
- Tasks persist in a SQLite database
- Clean REST API (`/api/tasks`)

## How to run

1. Install Flask:
   ```
   pip install flask
   ```

2. Run the app:
   ```
   python app.py
   ```

3. Open your browser to:
   ```
   http://127.0.0.1:5000
   ```

That's it — the database file (`tasks.db`) is created automatically the first time you run it.

## Project structure
```
todo-app/
├── app.py              # Flask backend + API routes
├── tasks.db             # created automatically on first run
├── templates/
│   └── index.html        # main page
├── static/
│   ├── style.css          # styling
│   └── script.js           # frontend logic (talks to the API)
└── README.md
```

## Next steps to extend it
- Add user login (Flask-Login) so tasks are private per user
- Add due dates and sort by them
- Add categories/tags and filtering
- Deploy it live (Render or PythonAnywhere both have free tiers)

## Putting this on GitHub
```
git init
git add .
git commit -m "Initial commit: full-stack to-do app"
```
Then create a repo on GitHub and push it — this becomes the project you link from your portfolio site.
