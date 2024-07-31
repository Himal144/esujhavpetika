from django.db import models

# Create your models here.
class Sender(models.Model):
    name=models.CharField(max_length=30,null=True)
    email=models.EmailField(null=True)
