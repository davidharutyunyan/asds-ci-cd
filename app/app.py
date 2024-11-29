from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection settings
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'testdb')
DB_USER = os.getenv('DB_USER', 'testuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')


# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


@app.route('/users', methods=['GET'])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    user_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]

    return jsonify(user_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
