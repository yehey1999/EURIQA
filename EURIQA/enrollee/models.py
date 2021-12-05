from django.db import models
from django.contrib.auth.models import User
from administrator.models import *

# Create your models here.
class Program(models.Model):
    program_id = models.CharField(max_length=50, primary_key = True)     #ID Format: [college code] - [department code](e.g CCS-IT)
    program_name = models.CharField(max_length=70)
    college = models.CharField(max_length=70)
    num_enrollees = models.IntegerField()

    class Meta:
        db_table = 'program'

class Strand(models.Model):
    strand_id = models.CharField(max_length=50, primary_key = True)     #ID Format: [college code] - [department code](e.g CCS-IT)
    strand_name = models.CharField(max_length=70)
    track = models.CharField(max_length=70)
    num_enrollees = models.IntegerField()

    class Meta:
        db_table = 'strand'

class Enrollee(models.Model):
    enrollee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)       #Password format: Lastname.123456
    middle_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, blank=False)
    level = models.CharField(max_length = 50, null=True, blank=False)
    enrolled_as = models.CharField(max_length = 50, null=True, blank=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=None, null=True, blank=True)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, default=None, null=True, blank=True)
    exam_status = models.CharField(max_length = 10, null=True, blank=False, default="not done")
    pictures = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = 'enrollee'

class ExamAnswers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    enrollee =  models.ForeignKey(Enrollee, on_delete=models.CASCADE)
    answer = models.CharField(max_length = 1)
    exam =  models.ForeignKey(Exam, on_delete=models.CASCADE)
    part =  models.ForeignKey(Part, on_delete=models.CASCADE)
    question =  models.OneToOneField(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=None, null=True)

    class Meta:
        db_table = 'exam_answers'

class ExamResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    enrollee =  models.OneToOneField(Enrollee, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)

    class Meta:
        db_table = 'exam_results'