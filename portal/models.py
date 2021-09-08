from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
'''PORTAL APP, MODELS, data structure for teacher portal'''
#clss is a teachers class of students
class clss(models.Model):
    ID = models.PositiveIntegerField(primary_key=True, editable=False, validators=[MinValueValidator(111111), MaxValueValidator(999999)])
    name = models.CharField(max_length=10)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clss-detail', kwargs={'pk':self.pk})

#Topic object 
class topic(models.Model):
    title = models.CharField(max_length=30)
    Clss = models.ForeignKey(clss, on_delete=models.CASCADE, editable=False)
    green = models.PositiveIntegerField(default=0)
    amber = models.PositiveIntegerField(default=0)
    red = models.PositiveIntegerField(default=0)
    live = models.BooleanField(default=False, editable=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('clss-detail', kwargs={'pk':self.Clss.ID})

#Response comment object
class comment(models.Model):
    topic = models.ForeignKey(topic, on_delete=models.CASCADE, editable=False)
    body = models.CharField(max_length=280)
    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('clss-detail', kwargs={'pk':self.topic.Clss.ID})