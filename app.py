from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    if not os.path.exists('coal_mine.db'):
        conn = sqlite3.connect('coal_mine.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE carbon_emissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mine_name TEXT,
            activity TEXT,
            emission_factor REAL,
            units INTEGER,
            total_emission REAL
        )''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_activity', methods=['POST'])
def add_activity():
    data = request.get_json()
    mine_name = data['mine_name']
    activity = data['activity']
    emission_factor = data['emission_factor']
    units = data['units']
    total_emission = emission_factor * units

    conn = sqlite3.connect('coal_mine.db')
    c = conn.cursor()
    c.execute("INSERT INTO carbon_emissions (mine_name, activity, emission_factor, units, total_emission) VALUES (?, ?, ?, ?, ?)", 
              (mine_name, activity, emission_factor, units, total_emission))
    conn.commit()
    conn.close()

    return jsonify({"message": "Activity added successfully", "total_emission": total_emission})

@app.route('/get_emissions', methods=['GET'])
def get_emissions():
    conn = sqlite3.connect('coal_mine.db')
    c = conn.cursor()
    c.execute("SELECT mine_name, SUM(total_emission) FROM carbon_emissions GROUP BY mine_name")
    data = c.fetchall()
    conn.close()
    emissions = [{'mine_name': row[0], 'total_emission': row[1]} for row in data]
    return jsonify(emissions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
