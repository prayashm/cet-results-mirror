from models import *
from flask import Flask, jsonify, request, send_from_directory
app = Flask(__name__, static_url_path='')

@app.route("/")
def root():
	return app.send_static_file("index.html")

# Serve the Raw Files Directly
@app.route("/raw/<path:path>")
def send_raw(path):
	return send_from_directory('data',path)

@app.route("/<int:regno>")
def getStudentByRegNo(regno):
	student = Student.get(Student.regno == regno)
	semesters = []
	for exam in student.exams:
		semesters.append({'sem':exam.semester.num,'sgpa':exam.sgpa, 'path':'raw/%d/%d/%s.html' % (student.batch, exam.semester.code, student.regno), 'credits':exam.credits})
	print semesters
	return jsonify(name=student.name.title(), regno=student.regno, branch=student.branch.name.title(), batch=student.batch, semesters=semesters)

@app.route("/<partial_name>")
def getStudentByName(partial_name):
	#if partial_name[-1] != '*':
	#	partial_name = partial_name+'*'
	#partial_name = partial_name.replace('*','%%')
	students = []
	records = Student.raw("SELECT * FROM student WHERE name LIKE '%%"+partial_name+"%%' ORDER BY regno DESC")
	for student in records:
		students.append({'name':student.name,'regno':student.regno,'batch':student.batch, 'branch':student.branch.code })
	return jsonify(students=students)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5100,debug=True)
