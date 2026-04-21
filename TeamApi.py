from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
app.config["SWAGGER"] = {
    "title": "Students API",
    "uiversion": 3,
}
swagger = Swagger(app)

students = {}
teams = {}

@app.route('/students', methods=['GET'])
def get_students():
    """
    Get all students
    ---
    tags:
      - Students
    responses:
      200:
        description: A dict of students keyed by id
        schema:
          type: object
          additionalProperties:
            $ref: '#/definitions/Student'
    definitions:
      Student:
        type: object
        properties:
          id:
            type: integer
            example: 1
          name:
            type: string
            example: Jane Doe
          age:
            type: integer
            example: 20
    """
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    Get a student by id
    ---
    tags:
      - Students
    parameters:
      - name: student_id
        in: path
        required: true
        type: integer
        description: The student ID
    responses:
      200:
        description: The student
        schema:
          $ref: '#/definitions/Student'
      404:
        description: Student not found
    """
    student = students.get(student_id)
    if student is None:
        abort(404)
    return jsonify(student)

@app.route('/students', methods=['POST'])
def create_student():
    """
    Create a new student
    ---
    tags:
      - Students
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            age:
              type: integer
            email:
              type: string
          example:
            name: "Alice"
            age: 21
    responses:
      201:
        description: Created student
        schema:
          $ref: '#/definitions/Student'
      400:
        description: Invalid payload
    """
    if not request.json or 'name' not in request.json:
        abort(400)
    student_id = len(students) + 1
    student = {
        'id': student_id,
        'name': request.json['name'],
        'age': request.json.get('age', None),
        'email': request.json.get('email', None)
    }
    students[student_id] = student
    return jsonify(student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    Update an existing student
    ---
    tags:
      - Students
    consumes:
      - application/json
    parameters:
      - name: student_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            age:
              type: integer
          example:
            name: "New Name"
            age: 22
    responses:
      200:
        description: Updated student
        schema:
          $ref: '#/definitions/Student'
      400:
        description: Invalid payload
      404:
        description: Student not found
    """
    student = students.get(student_id)
    if student is None:
        abort(404)
    if not request.json:
        abort(400)
    student['name'] = request.json.get('name', student['name'])
    student['age'] = request.json.get('age', student['age'])
    return jsonify(student)

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Delete a student
    ---
    tags:
      - Students
    parameters:
      - name: student_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Deletion result
        schema:
          type: object
          properties:
            result:
              type: boolean
      404:
        description: Student not found
    """
    student = students.pop(student_id, None)
    if student is None:
        abort(404)
    return jsonify({'result': True})

@app.route('/teams', methods=['GET'])
def get_teams():
    """
    Get all teams
    ---
    tags:
      - Teams
    responses:
      200:
        description: A list of teams
        schema:
          type: array
          items:
            $ref: '#/definitions/Team'
    """
    return jsonify(teams)

@app.route('/teams', methods=['POST'])
def create_team():
    """
    Create a new team
    ---
    tags:
      - Teams
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
          example:
            name: "Team A"  
    responses:
      201:
        description: Created team
        schema:
          $ref: '#/definitions/Team'
      400:
        description: Invalid payload
    """
    if not request.json or 'name' not in request.json:
        abort(400)
    team_id = len(teams) + 1
    team = {
        'id': team_id,
        'name': request.json['name'],
        'members': []
    }
    teams[team_id] = team
    return jsonify(team), 201

@app.route('/teams/<int:team_id>/add_member', methods=['POST'])
def add_member_to_team(team_id):
    """
    Add a member to a team
    ---
    tags:
      - Teams
    consumes:
      - application/json
    parameters:
      - name: team_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - student_id
          properties:
            student_id:
              type: integer
          example:
            student_id: 1
    responses:
      200:
        description: Updated team
        schema:
          $ref: '#/definitions/Team'
      400:
        description: Invalid payload
      404:
        description: Team or Student not found
    """
    team = teams.get(team_id)
    if team is None:
        abort(404)
    if not request.json or 'student_id' not in request.json:
        abort(400)
    student_id = request.json['student_id']
    student = students.get(student_id)
    if student is None:
        abort(404)
    team['members'].append(student_id)
    return jsonify(team) 

if __name__ == '__main__':
    app.run(debug=True)
