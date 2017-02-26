import models
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_url_path='')
app.config.from_pyfile('app.cfg')


@app.route("/")
def root():
    return app.send_static_file("index.html")


# Serve the Raw Files Directly
@app.route("/raw/<path:path>")
def send_raw(path):
    return send_from_directory('data', path)


@app.route("/<int:student_id>")
def getStudentByRegNo(student_id):
    models.db.connect()
    if len(str(student_id)) != 10:
        students = []
        records = models.Student.select().where(models.Student.student_id.startswith(student_id))
        counter = 0
        for student in records:
            students.append({'name': student.name.title(), 'regno': student.student_id, 'batch': student.batch,
                             'branch': student.branch_id})
        """
        stupid hack, as javascript code screws up when len(records) <= 10
        """
        for student in records:
            students.append({'name': student.name.title(), 'regno': student.student_id, 'batch': student.batch,
                             'branch': student.branch_id})
            break
        return jsonify(students=students)

    else:
        student = models.Student.get(models.Student.student_id == student_id)
        semesters = []
        exams = models.Exam.select().where(models.Exam.student_id == student_id)
        for exam in exams:
            subjects = []
            for score in models.Score.select().where(models.Score.student_id == student_id,
                                                     models.Score.semester_id == exam.semester_id):
                subject_details = models.Subject.get(models.Subject.code == score.subject_id)
                subjects.append(
                    {'name': subject_details.name, 'code': '', 'credits': subject_details.credits,
                     'grade': score.grade})

            semesters.append({'sem': exam.semester_id, 'sgpa': exam.sgpa,
                              'path': 'raw/%d/%s/%s.html' % (student.batch, exam.semester_id, student.student_id),
                              'credits': exam.credits, 'subjects': subjects})
        # print semesters
        return jsonify(name=student.name.title(), regno=student.student_id, branch=student.branch_id,
                       batch=student.batch, semesters=semesters)


@app.route("/<partial_name>")
def getStudentByName(partial_name):
    models.db.connect()
    students = []
    records = models.Student.select().where(models.Student.name.startswith(partial_name.upper()))
    for student in records:
        students.append({'name': student.name.title(), 'regno': student.student_id, 'batch': student.batch,
                         'branch': student.branch_id})
    return jsonify(students=students)


@app.route("/hide/<int:student_id>")
def hideStudent(regno):
    models.db.connect()
    student = models.Student.get(models.Student.student_id == regno)
    student.is_visible = False
    if student.save() == 1:
        return jsonify(message="Success in hiding %s - %s" % (student.regno, student.name.title()))
    else:
        return jsonify(message="Failed in hiding %s. It's already hidden from search by name" % student.regno)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    # app.run()
    #debug only, 0.0.0.0
    app.run(host = '0.0.0.0')
