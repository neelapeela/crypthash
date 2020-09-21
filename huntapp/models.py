from django.db import models

# Create your models here

class Progress(models.Model):
    username= models.CharField(max_length=20, default='none')
    is_playing= models.BooleanField(default=False)
    level= models.TextField(max_length=20 ,default='none')
    points= models.IntegerField(default=0)
    completed= models.IntegerField(default=0)
    completedlist = models.TextField(max_length=30, default="")
    
class Level(models.Model):
    level = models.TextField(max_length=20, default='none')
    question = models.TextField(max_length=150, default='none')
    answer = models.TextField(max_length=50, default='none')
    points = models.IntegerField(default=0)