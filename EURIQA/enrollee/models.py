from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Enrollee(models.Model):
    enrollee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, blank=False)
    level = models.CharField(max_length = 50, null=True, blank=False)
    pictures = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = 'enrollee'