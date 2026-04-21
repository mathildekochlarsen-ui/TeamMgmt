import mysql.connector
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flasgger import Swagger
 
app = Flask(__name__)
CORS(app)
app.config["SWAGGER"] = {
    "title": "Windmills API",
    "uiversion": 1,
}
swagger = Swagger(app)
 
 
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="PASSWORD",
        database="windmill",
        auth_plugin="mysql_native_password"
    )
 
 
@app.route('/windmills', methods=['GET'])
def get_windmills():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM windmills")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)
 
 
@app.route('/windmills', methods=['POST'])
def create_windmill():
    if not request.json or 'name' not in request.json:
        abort(400)
    name = request.json['name']
    sensor = request.json.get('sensor', None)
    email = request.json.get('email', None)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO windmills (name, sensor, email) VALUES (%s, %s, %s)",
        (name, sensor, email)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM windmills WHERE id = %s", (new_id,))
    windmill = cursor.fetchone()
    conn.close()
    return jsonify(windmill), 201
 
 
@app.route('/windmills/<int:windmill_id>', methods=['PUT'])
def update_windmill(windmill_id):
    if not request.json:
        abort(400)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM windmills WHERE id = %s", (windmill_id,))
    windmill = cursor.fetchone()
    if windmill is None:
        conn.close()
        abort(404)
    name = request.json.get('name', windmill['name'])
    sensor = request.json.get('sensor', windmill['sensor'])
    email = request.json.get('email', windmill['email'])
    cursor.execute(
        "UPDATE windmills SET name = %s, sensor = %s, email = %s WHERE id = %s",
        (name, sensor, email, windmill_id)
    )
    conn.commit()
    cursor.execute("SELECT * FROM windmills WHERE id = %s", (windmill_id,))
    updated = cursor.fetchone()
    conn.close()
    return jsonify(updated)
 
 
@app.route('/windmills/<int:windmill_id>', methods=['DELETE'])
def delete_windmill(windmill_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM windmills WHERE id = %s", (windmill_id,))
    windmill = cursor.fetchone()
    if windmill is None:
        conn.close()
        abort(404)
    cursor.execute("DELETE FROM windmills WHERE id = %s", (windmill_id,))
    conn.commit()
    conn.close()
    return jsonify({'result': True})
 
 
@app.route('/parks', methods=['GET'])
def get_parks():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parks")
    parks = cursor.fetchall()
    conn.close()
    return jsonify(parks)
 
 
@app.route('/parks', methods=['POST'])
def create_park():
    if not request.json or 'name' not in request.json:
        abort(400)
    name = request.json['name']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO parks (name) VALUES (%s)", (name,))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM parks WHERE id = %s", (new_id,))
    park = cursor.fetchone()
    conn.close()
    return jsonify(park), 201
 
 
@app.route('/parks/<int:park_id>/add_windmill', methods=['POST'])
def add_windmill_to_park(park_id):
    if not request.json or 'windmill_id' not in request.json:
        abort(400)
    windmill_id = request.json['windmill_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parks WHERE id = %s", (park_id,))
    park = cursor.fetchone()
    if park is None:
        conn.close()
        abort(404)
    cursor.execute("SELECT * FROM windmills WHERE id = %s", (windmill_id,))
    windmill = cursor.fetchone()
    if windmill is None:
        conn.close()
        abort(404)
    cursor.execute(
        "INSERT INTO park_windmills (park_id, windmill_id) VALUES (%s, %s)",
        (park_id, windmill_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'result': True, 'park_id': park_id, 'windmill_id': windmill_id})
 
 
if __name__ == '__main__':
    app.run(debug=True)
 
