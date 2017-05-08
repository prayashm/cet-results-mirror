import models
import constants
from flask import Flask, jsonify, send_from_directory, request, render_template

import csv


def write_to_csv(data):
    with open("./data/results.csv", "w") as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        for row in data:
            writer.writerow(row)


app = Flask(__name__, static_url_path='')
app.config.from_pyfile('app.cfg')


@app.route("/")
def root():
    return app.send_static_file("index.html")


# Serve the Raw Files Directly
@app.route("/raw/<path:path>")
def send_raw(path):
    return send_from_directory('./data', path)


@app.route("/<int:student_id>")
def getStudentByRegNo(student_id):
    if len(str(student_id)) != 10:
        students = []
        constants.db.connect()
        records = models.Student.select().where(models.Student.student_id.startswith(student_id)).limit(15)

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
        constants.db.close()
        return jsonify(students=students)

    else:
        student = None
        semesters = []
        csv_data = []
        constants.db.connect()
        try:
            student = models.Student.get(models.Student.student_id == student_id)
        except:
            pass
        exams = models.Exam.select().where(models.Exam.student_id == student_id)
        for exam in exams:
            csv_data.append([exam.semester_id])
            subjects = []
            for score in models.Score.select().where(models.Score.student_id == student_id,
                                                     models.Score.semester_id == exam.semester_id):
                subject_details = models.Subject.get(models.Subject.code == score.subject_id)
                subjects.append(
                    {'name': subject_details.name, 'code': '', 'credits': subject_details.credits,
                     'grade': score.grade})
                csv_data.append([subject_details.name, score.subject_id, subject_details.credits, score.grade])

            semesters.append({'sem': exam.semester_id, 'sgpa': exam.sgpa,
                              'path': 'raw/%d/%s/%s.html' % (student.batch, exam.semester_id, student.student_id),
                              'credits': exam.credits, 'subjects': subjects})
        # print semesters
        write_to_csv(csv_data)
        return jsonify(name=student.name.title(), regno=student.student_id, branch=student.branch_id,
                       batch=student.batch, semesters=semesters)


@app.route("/<partial_name>")
def getStudentByName(partial_name):
    constants.db.connect()
    students = []
    records = models.Student.select().where(models.Student.name.contains(partial_name.upper())).limit(15)
    for student in records:
        students.append({'name': student.name.title(), 'regno': student.student_id, 'batch': student.batch,
                         'branch': student.branch_id})
    return jsonify(students=students)


@app.route("/hide/<int:student_id>")
def hideStudent(student_id):
    constants.db.connect()
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
    constants.db.connect()
    student = models.Student.get(models.Student.student_id == student_id)
    if not student.is_visible:
        return jsonify(visible_message="Make your results public")
    else:
        return jsonify(visible_message="Make your results private")


@app.route("/advanced/")
def fill_dropdown_advanced():
    constants.db.connect()
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


@app.route("/advanced/results/<batch_id>/<branch_id>/<sem_id>", methods=['GET', 'POST'])
def show_bulk_result(batch_id, branch_id, sem_id):
    constants.db.connect()
    if batch_id is None or branch_id is None or sem_id is None:
        branch_code = str(request.form['branch']).translate(None, '!=%1234567890')
        batch = str(request.form['batch']).translate(None, '!=%,;')
        semester_query = str(request.form['semester']).translate(None, '!=%,;')
    else:
        branch_code = str(branch_id).translate(None, '!=%1234567890')
        batch = str(batch_id).translate(None, '!=%,;')
        semester_query = str(sem_id).translate(None, '!=%,;')

    if semester_query == "0":
        data = models.BulkQuery.raw(
            "SELECT * FROM student WHERE branch_id = '" + branch_code +
            "' and batch = " + batch + " ORDER BY `cgpa` DESC").execute()
        students = []
        csv_data = []
        for student in data:
            students.append({"name": student.name, "student_id": student.student_id, "sgpa": student.cgpa})
            csv_data.append([student.name, student.student_id, student.cgpa])
        write_to_csv(csv_data)
        return render_template("bulk_results.html", list_size=len(students), student=students, type="CGPA")
    else:
        semester_code = batch + "-" + semester_query
        data = models.BulkQuery.raw('SELECT t1.sgpa, t2.student_id,t2.name FROM `exam` as t1 RIGHT JOIN '
                                    '(SELECT * FROM `student` )as t2 ON t1.student_id = t2.student_id '
                                    'WHERE t2.branch_id ="' + branch_code + '" AND t2.batch =' + batch +
                                    ' AND t1.semester_id ="' + semester_code +
                                    '" ORDER BY `t1`.`sgpa` DESC').execute()
        students = []
        csv_data = []
        for student in data:
            students.append({"name": student.name, "student_id": student.student_id, "sgpa": student.sgpa})
            csv_data.append([student.name, student.student_id, student.sgpa])
        write_to_csv(csv_data)
        return render_template("bulk_results.html", list_size=len(students), student=students, type="SGPA")


@app.route("/internal")
def fill_dropdown_internal():
    constants.db.connect()
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


@app.route("/internal/subjects/", methods=['GET', 'POST'])
def filter_subject():
    partial_subject_name = str(request.json['subject']).translate(None, '!=%1234567890')
    subjects = models.Subject.select().where(models.Subject.name.contains(partial_subject_name.upper())).limit(10)
    subject_list = []
    for subject in subjects:
        subject_list.append({"name": subject.name, "code": subject.code})
    return jsonify(subject_list=subject_list)


@app.route("/internal/display/", methods=['GET', 'POST'])
def generate_internal_form():
    constants.db.connect()
    branch_code = str(request.form['branch']).translate(None, '!=%1234567890')
    batch = str(request.form['batch']).translate(None, '!=%,;')
    semester_query = str(request.form['semester']).translate(None, '!=%,;')
    semester_code = batch + "-" + semester_query
    data = models.BulkQuery.raw(
        'SELECT name, student_id from student where branch_id = "' + branch_code + '" and batch = ' + batch +
        ' order by student_id asc').execute()
    students = []
    csv_data = []
    for student in data:
        students.append({"name": student.name, "student_id": student.student_id})
    write_to_csv(csv_data)
    return jsonify(students=students)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


# @app.route("/download/")
# def download_csv():
#     return send_from_directory('data', 'hello.txt')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
