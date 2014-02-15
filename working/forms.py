__author__ = 'judywawira'

from django import forms
from OMRS.models import Jobs,UserFeed,JobErrors

class Test2Form(forms.Form):
    #Load form fields
    serverAddress = forms.URLField(label="You are currently connected to")
    location = forms.ChoiceField(label="Select location")
    encounterType = forms.ChoiceField(label="Select encounter type")
    identifier = forms.ChoiceField(label="Select Identifier Type")
    jobName = forms.CharField(label="Enter job name")

class CreateJobForm(forms.ModelForm):
    """
    class that binds the create job details form to the Jobs model
    """
    class Meta:
        model = Jobs

class CreateFeed(forms.ModelForm):
    """
    class that allows a user to leave feedback on a form. Bound to UserFeeds model
    """
    class Meta:
        model = UserFeed
        exclude = ['retired','twitterhandle']

class CreateAlert(forms.ModelForm):
    """
    class that allows a user to leave feedback on a form. Bound to UserFeeds model
    """
    class Meta:
        model = JobErrors

