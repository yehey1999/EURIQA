from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Administrator(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, blank=False)
    department = models.CharField(max_length=50, blank=False)
    
    class Meta:
        db_table = 'administrator'