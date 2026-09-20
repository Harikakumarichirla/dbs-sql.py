from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return """
    <h1>Student CRUD Operations</h1>
        <p>Create a student record</p>
        <p>Read all student records</p>
        <p>Update the first student's age</p>
        <p>Delete the first student record</p>
    """
@app.route('/create')
def create():
    new_student = Student(name="harika", age=19)
    db.session.add(new_student)
    db.session.commit()
    return "Student created successfully!"
@app.route('/read')
def read():
    students = Student.query.all()
    if not students:
        return "No students found in the database."  
    result = "<h1>Student List</h1>"
    for s in students:
        result += f"<p>ID: {s.id}, Name: {s.name}, Age: {s.age}</p>"  
    result += "<br><a href='/'>Back to Home</a>"
    return result
@app.route('/update')
def update():
    target_student = Student.query.first()
    if target_student:
        target_student.age = 25
        db.session.commit()
        return f"Student '{target_student.name}' age updated successfully!"
    return "No student data found to update."

@app.route('/delete')
def delete():
    target_student = Student.query.first()
    if target_student:
        name = target_student.name
        db.session.delete(target_student)
        db.session.commit()
        return f"Student '{name}' deleted successfully!"
    return "No student found to delete."

if __name__ == "__main__":
    app.run(debug=True)