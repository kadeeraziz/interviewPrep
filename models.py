"""
I chose to use Django models because of its simplicity and ease of use.
Its built-in model framework makes it easy to define and manage the database schema,
and the included administration interface saves time by providing a user-friendly way to interact with the data. 
"""


from django.db import models
class EndOfDay(models.Model):
    date = models.DateField()
    cleaning_number = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    margin_type = models.CharField(max_length=100)
    margin = models.IntegerField()

    def __str__(self):
        return f"{self.date} {self.cleaning_number}"
    
class Intraday(models.Model):
    date = models.DateField()
    time = models.TimeField()
    cleaning_number = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    margin_type = models.CharField(max_length=100)
    margin = models.IntegerField()

    def __str__(self):
        return f"{self.date} {self.cleaning_number} {self.time}"