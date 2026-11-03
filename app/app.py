from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route('/health')
def health():
    return "App Tier is healthy!"

@app.route('/db')
def db_check():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        return "Database connection successful!"
    except Exception as e:
        return f"Database error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
