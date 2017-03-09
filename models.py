import os
import peewee
import constants


class BaseModel(peewee.Model):
    class Meta:
        database = constants.db


class Branch(BaseModel):
    code = peewee.FixedCharField(unique=True)
    name = peewee.CharField()


class Student(BaseModel):
    student_id = peewee.CharField()
    name = peewee.CharField()
    branch_id = peewee.CharField()
    batch = peewee.IntegerField()
    cgpa = peewee.FloatField()
    course = peewee.CharField(choices = (('reg', 'regular'), ('le', 'lateral-entry')))
    is_visible = peewee.BooleanField(default=True)

    class Meta:
        primary_key = peewee.CompositeKey('student_id', 'batch')
        order_by = ('student_id',)


class Exam(BaseModel):
    student_id = peewee.CharField()
    semester_id = peewee.CharField()
    sgpa = peewee.FloatField()
    credits = peewee.IntegerField()

    class Meta:
        primary_key = peewee.CompositeKey('student_id', 'semester_id')


class Score(BaseModel):
    student_id = peewee.CharField()
    subject_id = peewee.CharField()
    grade = peewee.FixedCharField()
    semester_id = peewee.CharField()

    class Meta:
        primary_key = peewee.CompositeKey('student_id', 'subject_id')


class Semester(BaseModel):
    code = peewee.PrimaryKeyField()
    batch = peewee.IntegerField()
    num = peewee.IntegerField() # from 1 to 8


class Subject(BaseModel):
    code = peewee.CharField()
    name = peewee.CharField()
    credits = peewee.IntegerField()

    class Meta:
        primary_key = peewee.CompositeKey('code')


class BulkQuery(BaseModel):
    student_id = peewee.CharField()
    name = peewee.CharField()
    sgpa = peewee.FloatField()


def addTo(table, data_source):
    with db.atomic():
        if table == "Branch":
           Branch.insert_many(data_source).execute()
        elif table == "Semester":
            Semester.insert_many(data_source).execute()
    print "Done inserting"

