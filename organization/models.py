from django.db import models
from user.models import Sender
from django.contrib.auth.models import User

# Create your models here.
class Organization(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=False)
    logo=models.ImageField( upload_to='organization',max_length=None)
    parent_id=models.IntegerField(null=True)
    authenticated_sender=models.BooleanField(default=False)

class Topic(models.Model):
    topic=models.CharField(max_length=20,null=False)
    organization_id=models.ForeignKey('Organization', on_delete=models.CASCADE)

class Feedback(models.Model):
    feedback=models.CharField(max_length=200,null=False)
    date=models.DateTimeField(default=None)
    organization_id=models.ForeignKey('Organization',  on_delete=models.CASCADE)
    sender_id=models.ForeignKey(Sender, on_delete=models.CASCADE,null=True)
    topic_id=models.ForeignKey("Topic",on_delete=models.CASCADE)
    status=models.BooleanField(null=True)

class Response(models.Model):
    response= models.CharField(max_length=200,null=True)
    date=models.DateTimeField(default=None)
    feedback_id=models.ForeignKey('Feedback',on_delete=models.CASCADE)
    date=models.DateTimeField(default=None)
    status=models.BooleanField(null=True)


class Forward(models.Model):
    organization_id=models.ForeignKey('Organization',on_delete=models.CASCADE) 
    feedback_id=models.ForeignKey('Feedback',on_delete=models.CASCADE) 
  

class Similarity(models.Model):
    feedback_id=models.ForeignKey('Feedback',on_delete=models.CASCADE)
    sender_id=models.ForeignKey(Sender, on_delete=models.CASCADE)





