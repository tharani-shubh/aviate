from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=(("male", "Male"), ("female", "Female")))
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=10)
