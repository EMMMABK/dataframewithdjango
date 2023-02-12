from django.db import models

class File(models.Model):
    fileName = models.CharField(max_length=255,)
    file = models.FileField()
