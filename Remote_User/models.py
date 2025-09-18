from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)


class cardiac_arrest_prediction(models.Model):

    Fid= models.CharField(max_length=3000)
    Age_In_Days= models.CharField(max_length=3000)
    Sex= models.CharField(max_length=3000)
    ChestPainType= models.CharField(max_length=3000)
    RestingBP= models.CharField(max_length=3000)
    RestingECG= models.CharField(max_length=3000)
    MaxHR= models.CharField(max_length=3000)
    ExerciseAngina= models.CharField(max_length=3000)
    Oldpeak= models.CharField(max_length=3000)
    ST_Slope= models.CharField(max_length=3000)
    slp= models.CharField(max_length=3000)
    caa= models.CharField(max_length=3000)
    thall= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



