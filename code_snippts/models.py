# django model 
from django.db import models

class EndOfDay(models.Model):
    date = models.DateField()
    cleaning_number = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    margin_type = models.CharField(max_length=100)
    margin = models.IntegerField()

    def __str__(self):
        return f"{self.date} {self.cleaning_number}"
    

## intraday has all the same fields as eod, but also has a time field
class Intraday(models.Model):
    date = models.DateField()
    time = models.TimeField()
    cleaning_number = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    margin_type = models.CharField(max_length=100)
    margin = models.IntegerField()

    def __str__(self):
        return f"{self.date} {self.cleaning_number} {self.time}"