from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Create Database if not exists
def init_db():
    conn = sqlite3.connect("faculty.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            designation TEXT,
            qualifications TEXT,
            experience TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize DB on startup

# Route to get all faculty members
@app.route("/faculty", methods=["GET"])
def get_faculty():
    conn = sqlite3.connect("faculty.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty")
    data = cursor.fetchall()
    conn.close()
    faculty_list = [{"id": row[0], "name": row[1], "designation": row[2], "qualifications": row[3], "experience": row[4], "email": row[5]} for row in data]
    return jsonify(faculty_list)

# Route to add a new faculty member
@app.route("/faculty", methods=["POST"])
def add_faculty():
    data = request.json
    conn = sqlite3.connect("faculty.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faculty (name, designation, qualifications, experience, email) VALUES (?, ?, ?, ?, ?)",
                   (data["name"], data["designation"], data["qualifications"], data["experience"], data["email"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Faculty added successfully!"})

# Route to delete a faculty member
@app.route("/faculty/<int:id>", methods=["DELETE"])
def delete_faculty(id):
    conn = sqlite3.connect("faculty.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faculty WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Faculty deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
