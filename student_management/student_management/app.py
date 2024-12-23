from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(50), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name, "age": s.age, "grade": s.grade} for s in students])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(name=data['name'], age=data['age'], grade=data['grade'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    student.name = data['name']
    student.age = data['age']
    student.grade = data['grade']
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
