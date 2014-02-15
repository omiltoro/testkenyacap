__author__ = 'judyw'

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django.contrib.auth.models import User

from OMRS.models import UserProfile,Server
from OMRS import omrsfunctions

class LoadServerForm(forms.Form):
    """
    Class to load unbound Server onjects to allow for data entry
    """
    serverAddress = forms.URLField(label="Enter OpenMRS Address:",widget=forms.TextInput(attrs={'placeholder':'http://localhost:8080/openmrs'}))
    serverUsername = forms.CharField(label="Enter OpenMRS Username:")
    serverPassword = forms.CharField(label="Enter OpenMRS password:",widget=forms.PasswordInput())

class ServerDetailsForm(forms.Form):
    """
    Class that displays unbound server entry for user to select data
    """
    #Prepopulated fields here
    FAVORITE_COLORS_CHOICES = (('judy', 'Blue'),
                            ('green', 'Green'),
                            ('black', 'Black'))

    serverAddress = forms.URLField(label="You are currently connected to ..")
    location = forms.ChoiceField(choices=FAVORITE_COLORS_CHOICES)
    encounterType = forms.CharField(label="Encounter Type")
    identifier = forms.CharField()
    server = forms.ModelChoiceField(queryset=Server.objects.all())

class serverAuth(forms.Form):
    """
    Method  to populate server username and password
    """
    class Meta:
        model = Server
        fields = ('serverUsername','serverPassword')

class serverParams(forms.Form):
    #need to specify the server details
    class Meta:
        model = Server
        fields = ('serverAddress','serverUsername','serverPassword')
        #serverAddress
        #encounterLocation
        #encounterType
        #defaultIdentifier

class UserForm (forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    DOB = forms.DateField(widget=SelectDateWidget)
    class Meta:
        model = UserProfile
        fields = ('website','middle_name','DOB','sex','country','organisation')

class serverForm(ModelForm):
    """
    This function displays the user details to allow entry of the server name , server username and server password
    should capture user details from the logged in user
    """

    #declare how to deal with errors
    error_css_class = 'error'
    required_css_class = 'required'

    serverPassword = forms.CharField(widget= forms.PasswordInput())

    #change the labels in the forms
    def __init__(self,*args,**kwargs):
        super(serverForm,self).__init__(*args,**kwargs)
        self.fields['serverAddress'].label = "Enter openMRS server address:"
        self.fields['serverUsername'].label = "Enter openMRS server username:"
        self.fields['serverPassword'].label = "Enter openMRS server password:"

    class Meta:
        model = Server
        exclude = ['user']
        #fields = ('serverAddress','serverUsername','serverPassword')


#form to upload file
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        #label='Select a file',
        help_text='File should be in image format like .JPEG'
    )
