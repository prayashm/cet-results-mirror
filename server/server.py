import models
from flask import Flask, jsonify, send_from_directory, request
import sys

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

        for student in records:
            branch = models.Branch.get(models.Branch.code == student.branch_id)
            students.append({'name': student.name.title(), 'regno': student.student_id, 'batch': student.batch,
                             'branch': branch.name})
        """
        stupid hack, as javascript code screws up when len(records) <= 10
        """
        for student in records:
            branch = models.Branch.get(models.Branch.code == student.branch_id)
            students.append({'name': student.name.title(), 'regno': student.student_id, 'batch': student.batch,
                             'branch': branch.name})
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
def hideStudent(student_id):
    models.db.connect()
    student = models.Student.get(models.Student.student_id == student_id)
    if student.is_visible:
        student.is_visible = False
        if student.save() == 1:
            return jsonify(message="Success in hiding %s - %s" % (student.student_id, student.name.title()))
        else:
            return jsonify(message="Failed in hiding %s. It's already hidden from search by name" % student.student_id)
    else:
        return jsonify(confirm="The roll is already hidden. Would you like to make it public ?")


@app.route("/hide_data/<int:student_id>")
def change_message(student_id):
    models.db.connect()
    student = models.Student.get(models.Student.student_id == student_id)
    if not student.is_visible:
        return jsonify(visible_message="Make your results public")
    else:
        return jsonify(visible_message="Make your results private")


@app.route("/advanced")
def fill_dropdowns():
    models.db.connect()
    branch_list = []
    year_list = []
    semester_list = []
    for branch in models.Branch.select():
        branch_list.append({"branch": branch.name.split(" ")[0], "code": branch.code})

    for years in models.Student.select(models.Student.batch).distinct():
        year_list.append({"year": years.batch})
    """
    dont be lazy, support other things like B-Arch
    """
    for semester in range(1, 9):
        semester_list.append({"semester": "Semester - " + str(semester)})

    return jsonify(branch=branch_list, batch=year_list, semester=semester_list)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


@app.route("/advanced/results/", methods=['GET', 'POST'])
def show_bulk_result():
    models.db.connect()
    branch_code = str(request.form['branch'])
    batch = str(request.form['batch'])
    semester_code = batch + "-" + str(request.form['semester'])
    data = models.BulkQuery.raw('SELECT t1.sgpa, t2.student_id,t2.name FROM `exam` as t1 RIGHT JOIN '
                                        '(SELECT * FROM `student` )as t2 ON t1.student_id = t2.student_id '
                                        'WHERE t2.branch_id ="' + branch_code + '" AND t2.batch =' + batch +
                                        ' AND t1.semester_id ="' + semester_code +
                                        '" ORDER BY `t1`.`sgpa` DESC').execute()
    students = []
    for student in data:
        students.append({"name": student.name, "student_id" : student.student_id, "sgpa": student.sgpa})
    return jsonify(students=students)


@app.route("/download")
def download_csv():
    pass

if __name__ == '__main__':
    # app.run()
    # debug only, 0.0.0.0
    app.run(host='0.0.0.0')
