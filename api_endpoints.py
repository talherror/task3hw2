from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_canteens():
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM CANTEEN")
    canteens = c.fetchall()
    conn.close()
    return canteens

def get_canteens_by_time(open_time):
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM CANTEEN WHERE time_open <= ?", (open_time,))
    canteens = c.fetchall()
    conn.close()
    return canteens

@app.route('/api/canteens', methods=['GET'])
def api_get_canteens():
    canteens = get_canteens()
    return jsonify(canteens)

@app.route('/api/canteens/open', methods=['GET'])
def api_get_canteens_by_time():
    open_time = request.args.get('open_time')
    canteens = get_canteens_by_time(open_time)
    return jsonify(canteens)

@app.route('/api/canteens', methods=['POST'])
def api_add_canteen():
    data = request.get_json()
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("INSERT INTO CANTEEN (Name, Location, time_open, time_closed) VALUES (?, ?, ?, ?)",
              (data['Name'], data['Location'], data['time_open'], data['time_closed']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Canteen added successfully"})

@app.route('/api/canteens/<int:canteen_id>', methods=['PUT'])
def api_update_canteen(canteen_id):
    data = request.get_json()
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("UPDATE CANTEEN SET Name=?, Location=?, time_open=?, time_closed=? WHERE ID=?",
              (data['Name'], data['Location'], data['time_open'], data['time_closed'], canteen_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Canteen updated successfully"})

@app.route('/api/canteens/<int:canteen_id>', methods=['DELETE'])
def api_delete_canteen(canteen_id):
    conn = sqlite3.connect('DINERS.db')
    c = conn.cursor()
    c.execute("DELETE FROM CANTEEN WHERE ID=?", (canteen_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Canteen deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
