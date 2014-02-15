from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,related_name="myuser")

    #additional models we wish to include
    website = models.URLField(blank=True)
    middle_name = models.CharField(max_length=128, blank=True)
    DOB = models.DateField()
    sex = models.CharField(max_length=128,blank=True)
    country = models.CharField(max_length=128,blank=True)
    organisation = models.CharField(max_length=128)
    #picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

class Server (models.Model):
    idServerDetails = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,related_name="serveruser")
    serverAddress = models.URLField()
    serverUsername = models.CharField(max_length=128)
    serverPassword = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user','serverAddress')