from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Administrator(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, blank=False)
    position = models.CharField(max_length=50, blank=False)
    
    class Meta:
        db_table = 'administrator'

class Part(models.Model):
	part_id = models.AutoField(primary_key=True)
	part_name = models.CharField(max_length = 200)
	instructions = models.CharField(max_length = 200)
	overall_points = models.IntegerField()

	class Meta:
		db_table = "exampart"

class Question(models.Model):
	question_id = models.AutoField(primary_key=True)
	question = models.CharField(max_length = 200)
	optionA = models.CharField(max_length = 100)
	optionB = models.CharField(max_length = 100)
	optionC = models.CharField(max_length = 100)
	optionD = models.CharField(max_length = 100)
	answer = models.CharField(max_length = 100)
	points = models.IntegerField()
	part = models.ForeignKey(Part, on_delete=models.CASCADE, default=None, null=True, blank=True)
	created_by = models.ForeignKey(Administrator, on_delete=models.CASCADE, default=None, null=True, blank=True)

	class Meta:
		db_table = "question"

class Exam(models.Model):
	exam_id = models.AutoField(primary_key=True)
	part = models.ForeignKey(Part, on_delete=models.CASCADE, default=None, null=True, blank=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None, null=True, blank=True)
	overall_points = models.IntegerField()
	created_by = models.ForeignKey(Administrator, on_delete=models.CASCADE, default=None, null=True, blank=True)