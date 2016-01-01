from peewee import *

db = MySQLDatabase('results_db', user='root', passwd='trymiracle')

class BaseModel(Model):
    class Meta:
        database = db

class Branch(BaseModel):
    code = FixedCharField(unique=True)
    name = CharField()

class Subject(BaseModel):
    code = CharField(unique=True)
    name = CharField()
    credits = IntegerField()

class Semester(BaseModel):
    code = PrimaryKeyField()
    batch = IntegerField()
    num = IntegerField() # from 1 to 8

class Student(BaseModel):
    regno = IntegerField(unique=True)
    name = CharField()
    branch = ForeignKeyField(Branch, to_field='code', related_name='students')
    batch = IntegerField()
    cgpa = FloatField()
    course = CharField()

    class Meta:
        order_by = ('regno',)

class Exam(BaseModel):
    student = ForeignKeyField(Student, to_field='regno', related_name='exams')
    semester = ForeignKeyField(Semester, to_field='code', related_name='exams')
    sgpa = FloatField()

class Score(BaseModel):
    student = ForeignKeyField(Student, to_field='regno', related_name='scores', on_delete='cascade')
    subject = ForeignKeyField(Subject, to_field='code', related_name='student_scores', on_delete='cascade')
    grade = FixedCharField(max_length=1)
    semester = ForeignKeyField(Semester, to_field='code',related_name='scores', on_delete='cascade')
    recheckGrade = None

def addTo(table, data_source):
    with db.atomic():
        if table == "Branch":
           Branch.insert_many(data_source).execute()
        elif table == "Subject":
            Subject.insert_many(data_source).execute()
        elif table == "Semester":
            Semester.insert_many(data_source).execute()
        elif table == "Student":
            for i in range(0, len(data_source), 1000):
                Student.insert_many(data_source[i:i+1000]).execute()
        elif table == "Score":
            for i in range(0, len(data_source), 1000):
                Score.insert_many(data_source[i:i+1000]).execute()
    print "Done inserting"


db.connect()
db.create_tables([Branch, Semester, Subject, Student, Exam, Score], True)
db.close()