# Create your views here.

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
import requests, json
from requests.auth import HTTPBasicAuth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

#from working.models import Server,UserProfile  --- kept me here for a while
from working.forms import Test2Form, CreateJobForm, CreateFeed, CreateAlert
from OMRS.models import Server, JobErrors

#Declare global variables
headers = {'content-type': 'application/json'}


def create_user_alert(request):
    context = RequestContext(request)
    if request.method == 'GET':
     return render_to_response('jobAlerts.html',{'form': CreateAlert()}, context)
    #return HttpResponseRedirect('/alerts/')


def create_user_feed(request):
    context = RequestContext(request)
    if request.method == 'GET':
        return render_to_response('userfeedback.html', {'form': CreateFeed()}, context)
    else:
        form = CreateFeed(request.POST)
        form.user = request.user
        if form.is_valid():
            _createfeedobj = form.save()
            _createfeedobj.save()
            return HttpResponseRedirect('/userfeed')
    c = {'form':form}
    return render_to_response('userfeedback.html',c,context)


def createjob(request):
    """Method to save the initial job details once created by user"""
    context = RequestContext(request)
    if request.method == 'GET':
        CreateJobForm()
    else:
        # A POST request: Handle Form Upload
        # Bind data from request.POST into a PostForm
        form = CreateJobForm(request.POST)
        form.user = request.user
        if form.is_valid():
            _createjobobj = form.save(commit=False)
            #_createjobobj.user = request.user
            _createjobobj.save()
            return HttpResponseRedirect('/userprofile')
    c = {'form': form}
    return render_to_response('_test.html', c, context)


def _test(request):
    context = RequestContext(request)
    test_url = request.GET.get("server_url")

    test_auth = get_object_or_404(Server, serverAddress=test_url, user=request.user)


    _username = test_auth.serverUsername
    _pw = test_auth.serverPassword

    #format URL to correct REST format expected for OMRS
    _url = str(test_url) + str("/ws/rest/v1/")
    #expected 'http://localhost:8081/openmrs-standalone/ws/rest/v1/'

    #Get default data to populate the fields for location, Identifier and encounter type

    loc_choices = searchLocations(_url, _username, _pw)
    enc_choices = searchEncounterType(_url, _username, _pw)
    id_choices = searchIdentifier(_url, _username, _pw)

    #instantiate form and populate the data
    form = Test2Form()
    form.fields['serverAddress'].initial = test_url
    form.fields['location'].choices = loc_choices
    form.fields['encounterType'].choices = enc_choices
    form.fields['identifier'].choices = id_choices
    #make server address readonly
    form.fields['serverAddress'].widget.attrs['readonly'] = True

    return render_to_response('_test.html', {"form": form}, context)


def server_details_form(request):
    """
      Method to display the server details including location,provider and identifier and allow a user to select them as
      unbound data
      """
    if request.method == 'GET':
        #get URL value
        test_url = request.GET.get("server_url")

        #use URL value to get corresponding username and password
        test_auth = get_object_or_404(Server, serverAddress=test_url)
        _username = test_auth.serverUsername
        _pw = test_auth.serverPassword

        #format URL to correct REST format expected for OMRS
        _url = str(test_url) + str("/ws/rest/v1/")
        #expected 'http://localhost:8081/openmrs-standalone/ws/rest/v1/'
        print _url

        #Get default data to populate the fields for location, Identifier and encounter type

        loc_choices = searchLocations(_url, _username, _pw)
        enc_choices = searchEncounterType(_url, _username, _pw)
        id_choices = searchIdentifier(_url, _username, _pw)

        #instantiate form and populate the data
        data = {'serverAddress': request.GET.get("server_url")}
        form = Test2Form(initial=data)
        form.fields['location'].choices = loc_choices
        form.fields['encounterType'].choices = enc_choices
        form.fields['identifier'].choices = id_choices
    return render_to_response('working/test.html', {'form': form})

#Methods to fetch details from OMRS - Should ideally be later moved to a new module
def searchLocations(server, username, password):
    """
    Method that searches for available locations on an openmrs server and returns choices loaded into a choice object for locations
    """
    p = requests.get(server + 'location', headers=headers, auth=HTTPBasicAuth(username, password))
    resp = json.loads(p.text)
    locations = resp['results']  #list of locations returned

    loclist = []
    loctuple = ()

    for k, v in enumerate(locations):
        locationUUID = locations[k]['uuid']
        locationName = locations[k]['display']
        loctuple = (locationUUID, locationName)
        loclist.append(loctuple)

    return loclist


def searchEncounterType(server, username, password):
    """
    Function to collect all encounterTypes and pass them on into the App as choices
    """
    p = requests.get(server + 'encountertype', headers=headers, auth=HTTPBasicAuth(username, password))
    resp = json.loads(p.text)
    encounterTypes = resp['results']  #list of locations returned

    enclist = []
    enctuple = ()
    for k, v in enumerate(encounterTypes):
        encUUID = encounterTypes[k]['uuid']
        encName = encounterTypes[k]['display']
        enctuple = (encUUID, encName)
        enclist.append(enctuple)

    return enclist


def searchIdentifier(server, username, password):
    """
    Function to collect all encounterTypes and pass them on into the App as choices
    """
    p = requests.get(server + 'patientidentifiertype', headers=headers, auth=HTTPBasicAuth(username, password))
    resp = json.loads(p.text)
    idTypes = resp['results']  #list of locations returned

    idlist = []
    idtuple = ()

    for k, v in enumerate(idTypes):
        idUUID = idTypes[k]['uuid']
        idName = idTypes[k]['display']
        idtuple = (idUUID, idName)
        idlist.append(idtuple)
    return idlist
