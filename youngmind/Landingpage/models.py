from django.db import models

class Hackathon(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    rules = models.TextField()
    regulations = models.TextField()
    guidelines = models.TextField()

    def __str__(self):
        return self.title
