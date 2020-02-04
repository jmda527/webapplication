from django.db import models

# Create your models here.
class Upload_pkl(models.Model):
    category = models.FileField(upload_to='')

