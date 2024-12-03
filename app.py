from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(_name_)

# Initialize the database
def init_db():
    conn = sqlite3.connect("organ_donation.db")
    cursor = conn.cursor()

    # Donors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood_group TEXT,
        organ TEXT,
        location TEXT,
        status TEXT DEFAULT 'Available'
    )
    ''')

    # Recipients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood_group TEXT,
        organ_required TEXT,
        location TEXT,
        priority INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_donor", methods=["POST"])
def add_donor():
    data = request.json
    conn = sqlite3.connect("organ_donation.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO donors (name, age, blood_group, organ, location)
    VALUES (?, ?, ?, ?, ?)''', (data['name'], data['age'], data['blood_group'], data['organ'], data['location']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Donor added successfully!"}), 200

@app.route("/add_recipient", methods=["POST"])
def add_recipient():
    data = request.json
    conn = sqlite3.connect("organ_donation.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO recipients (name, age, blood_group, organ_required, location, priority)
    VALUES (?, ?, ?, ?, ?, ?)''', (data['name'], data['age'], data['blood_group'], data['organ_required'], data['location'], data['priority']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Recipient added successfully!"}), 200

@app.route("/match_organ", methods=["GET"])
def match_organ():
    conn = sqlite3.connect("organ_donation.db")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT r.name AS recipient_name, r.organ_required, r.blood_group, d.name AS donor_name, d.organ
    FROM recipients r
    JOIN donors d ON r.organ_required = d.organ AND r.blood_group = d.blood_group
    WHERE d.status = 'Available'
    ORDER BY r.priority ASC
    ''')

    matches = cursor.fetchall()
    conn.close()
    return jsonify(matches), 200

if _name_ == "_main_":
    app.run(debug=True)
@app.route('/test')
def test():
    return "Test Page is Working!"