import re
from django.db import models

# Create your models here.

class Doc(models.Model):


    upload = models.ImageField(upload_to='datas/')

    def __str__(self):
        return str(self.pk)
