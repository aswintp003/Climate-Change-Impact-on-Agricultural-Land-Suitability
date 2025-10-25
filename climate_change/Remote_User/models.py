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


class predict_climate_change_impact(models.Model):

    Fid= models.CharField(max_length=3000)
    CDate= models.CharField(max_length=3000)
    Precipitation= models.CharField(max_length=3000)
    Humidity= models.CharField(max_length=3000)
    WindSpeed= models.CharField(max_length=3000)
    WeatherCondition= models.CharField(max_length=3000)
    AvgTemp= models.CharField(max_length=3000)
    AvgTempUncertainty= models.CharField(max_length=3000)
    City= models.CharField(max_length=3000)
    Country= models.CharField(max_length=3000)
    Latitude= models.CharField(max_length=3000)
    Longitude= models.CharField(max_length=3000)
    Season= models.CharField(max_length=3000)
    Crop= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



