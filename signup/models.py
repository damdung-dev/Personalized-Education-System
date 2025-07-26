from django.db import models

# Create your models here.
class Student(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=50)
    gender=models.IntegerField(max_length=11)
    created_date=models.DateTimeField()

    class Meta:
        db_table='register_student'

    def __str__(self):
        return self.first_name