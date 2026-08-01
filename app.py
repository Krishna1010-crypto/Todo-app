from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "tasks.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


# GET all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])


# CREATE a new task
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    conn = get_db()
    cur = conn.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "title": title, "completed": 0}), 201


# UPDATE a task (edit title or toggle completed)
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", task["title"])
    completed = data.get("completed", task["completed"])
    conn.execute("UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
                 (title, completed, task_id))
    conn.commit()
    conn.close()
    return jsonify({"id": task_id, "title": title, "completed": completed})


# DELETE a task
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
