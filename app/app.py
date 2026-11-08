from flask import Flask, request, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/health')
def health():
    return "App Tier is healthy!"

# READ: Saare tasks laao
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM tasks ORDER BY id DESC;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

# CREATE: Naya task banao
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, priority, status) VALUES (%s, %s, %s) RETURNING id;",
        (data['title'], data['priority'], 'Pending')
    )
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "message": "Task created!"}), 201

# UPDATE: Task ka status change karo (Pending <-> Completed)
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status=%s WHERE id=%s;", (data['status'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task updated!"})

# DELETE: Task delete karo
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task deleted!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 