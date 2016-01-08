import os
from peewee import *

DB_HOST = os.environ.get('OPENSHIFT_MYSQL_DB_HOST','localhost')
DB_PORT = os.environ.get('OPENSHIFT_MYSQL_DB_POORT', 3306)
DB_USER = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME', 'root')
DB_PASS = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD', 'trymiracle')

db = MySQLDatabase('results_db', host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS)

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
    regno = CharField(unique=True)
    name = CharField()
    branch = ForeignKeyField(Branch, to_field='code', related_name='students')
    batch = IntegerField()
    cgpa = FloatField(null=True)
    course = CharField(choices = (('reg','regular'),('le','lateral-entry')))
    is_visible = BooleanField(default=True)

    class Meta:
        order_by = ('regno',)

class Exam(BaseModel):
    student = ForeignKeyField(Student, to_field='regno', related_name='exams')
    semester = ForeignKeyField(Semester, to_field='code', related_name='exams')
    sgpa = FloatField()
    credits = IntegerField()

class Score(BaseModel):
    student = ForeignKeyField(Student, to_field='regno', related_name='scores', on_delete='cascade')
    subject = ForeignKeyField(Subject, to_field='code', related_name='student_scores', on_delete='cascade')
    grade = FixedCharField(max_length=1)
    semester = ForeignKeyField(Semester, to_field='code',related_name='scores', on_delete='cascade')
    # updatedGrade = FixedCharField(max_length=1,null=True)

def addTo(table, data_source):
    with db.atomic():
        if table == "Branch":
           Branch.insert_many(data_source).execute()
        elif table == "Semester":
            Semester.insert_many(data_source).execute()
    print "Done inserting"


#db.connect()
#db.create_tables([Branch, Semester, Subject, Student, Exam, Score], True)
#db.close()
