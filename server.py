from models import *
from flask import Flask, jsonify, request, send_from_directory
app = Flask(__name__, static_url_path='')
app.config.from_pyfile('app.cfg')

@app.route("/")
def root():
    return app.send_static_file("index.html")

# Serve the Raw Files Directly
@app.route("/raw/<path:path>")
def send_raw(path):
    return send_from_directory('data',path)

@app.route("/<int:regno>")
def getStudentByRegNo(regno):
    db.connect()
    student = Student.get(Student.regno == regno)
    semesters = []
    for exam in student.exams:
        subjects = []
        for score in Score.select().where(Score.student == student, Score.semester == exam.semester):
            subjects.append({'name': score.subject.name.title(), 'code': score.subject.code, 'credits': score.subject.credits, 'grade': score.grade})
        
        semesters.append({'sem':exam.semester.num,'sgpa':exam.sgpa, 'path':'raw/%d/%d/%s.html' % (student.batch, exam.semester.code, student.regno), 'credits':exam.credits, 'subjects': subjects})
    # print semesters
    db.disconnect()
    return jsonify(name=student.name.title(), regno=student.regno, branch=student.branch.name.title(), batch=student.batch, semesters=semesters)

@app.route("/<partial_name>")
def getStudentByName(partial_name):
    db.connect()
    students = []
    records = Student.raw("SELECT * FROM student WHERE name LIKE '%%"+partial_name+"%%' AND is_visible = TRUE ORDER BY regno DESC")
    for student in records:
        students.append({'name':student.name.title(),'regno':student.regno,'batch':student.batch, 'branch':student.branch.code })
    db.disconnect()
    return jsonify(students=students)

@app.route("/hide/<int:regno>")
def hideStudent(regno):
    db.connect()
    student = Student.get(Student.regno == regno)
    student.is_visible = False
    db.disconnect()
    if student.save() == 1:
        return jsonify(message="Success in hiding %s - %s" % (student.regno,student.name.title()))
    else:
        return jsonify(message="Failed in hiding %s. It's already hidden from search by name" % student.regno)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
