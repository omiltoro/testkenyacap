from django.db import models
from django.contrib.auth.models import User

# Create your models here.

notify = False

class Server (models.Model):
    idServerDetails = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    serverAddress = models.URLField()
    serverUsername = models.CharField(max_length=128)
    serverPassword = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.serverAddress

    class Meta:
        unique_together = ('user','serverAddress')

class Authentication(models.Model):
    idAuthentication = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    organisation = models.CharField(max_length=128)

    def __unicode__(self):
        return "%s %s" %(self.username,self.organisation)

class Jobs(models.Model):
    idJobs = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    jobName = models.CharField(max_length=128,unique=True)
    serverAddress = models.ForeignKey(Server,related_name='address')
    location = models.CharField(max_length=128)
    identifier = models.CharField(max_length=128)
    encounterType = models.CharField(max_length=128)
    dateCreated = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s %s" %(self.idJobs,self.jobName,self.dateCreated)

class JobStatus(models.Model):
    idJobStatus = models.AutoField(primary_key=True)
    idJobs = models.ForeignKey(Jobs)
    jobStatus = models.CharField(max_length=128)
    dateUpdated = models.DateField()
    retired = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" %(self.idJobs,self.jobStatus)

class JobErrors(models.Model):
    idError = models.AutoField(primary_key=True)
    idJobs  = models.ForeignKey(Jobs)
    Jobname = models.CharField(max_length=128)
    dateCreated = models.DateField(auto_now_add=True)
    user = models.OneToOneField(User)
    Error = models.TextField(max_length=280)

    def __unicode__(self):
        return "%s %s" %(self.idJobs,self.Jobname,self.dateCreated,self.user,self.Error)

class Shredder(models.Model):
    idShredder = models.AutoField(primary_key=True)
    idJobs = models.ForeignKey(Jobs)
    idCSV = models.FileField(upload_to='documents/%Y/%m/%d')
    shredderStatus = models.CharField(max_length=128)

    def __unicode__(self):
        return "%s %s" %(self.idShredder,self.shredderStatus)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

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

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class UserFeed(models.Model):
    idFeed = models.AutoField(primary_key=True)
    feedUser = models.ForeignKey(User)
    comment = models.TextField()
    dateCreated = models.DateField(auto_now_add=True)
    retired = models.BooleanField(default=False,blank=True)
    twitterhandle = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return "%s %s %s" %(self.feedUser,self.comment,self.dateCreated)