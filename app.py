from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="citrus_db"
)

cursor = db.cursor(dictionary=True)

@app.get("/leaves")
def get_leaves():
    cursor.execute("SELECT * FROM citrus_leaves")
    return jsonify(cursor.fetchall())

@app.get("/leaves/<int:leaf_id>")
def get_leaf(leaf_id):
    cursor.execute("SELECT * FROM citrus_leaves WHERE id = %s", (leaf_id,))
    result = cursor.fetchone()
    return jsonify(result or {})

@app.post("/leaves")
def add_leaf():
    data = request.json
    sql = """
        INSERT INTO citrus_leaves (species, image_path, health_status, notes)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data["species"],
        data["image_path"],
        data["health_status"],
        data["notes"]
    ))
    db.commit()
    return jsonify({"id": cursor.lastrowid})

@app.delete("/leaves/<int:leaf_id>")
def delete_leaf(leaf_id):
    cursor.execute("DELETE FROM citrus_leaves WHERE id = %s", (leaf_id,))
    db.commit()
    return jsonify({"message": "Leaf deleted"})

if __name__ == "__main__":
    app.run(debug=True)
