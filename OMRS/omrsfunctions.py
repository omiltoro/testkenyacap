__author__ = 'judyw'

import requests,json,re
from requests.auth import HTTPBasicAuth

#import functions existing in other apps
from OMRS.models import Server
import django.views

#variables
url = str('http://localhost:8081/openmrs-standalone/ws/rest/v1/')
url2 = str('http://162.222.179.9:8080/kenyacaptricity/ws/rest/v1/')
headers = {'content-type': 'application/json'}
username = 'judy'
pw = 'Admin123'

"""
workflow is that the method should receive a users URL

"""

def searchLocations(server,username,password):
    #server = str(server)+ '/ws/rest/v1/'
    p = requests.get(server+'location',headers=headers,auth=HTTPBasicAuth(username,password))
    print p
    #resp = json.loads(p.text)
    #locations = resp['results']  #list of locations returned

    locationDict ={} # holds all searched locations as key/value pairs
    '''

    #get the location uuid and name
    for k,v in enumerate(locations):
        locationUUID = locations[k]['uuid']
        locationName = locations[k]['display']
        locationDict[locationUUID] = locationName
    print locationDict
    '''
    return locationDict


j = searchLocations(url2,'admin','test')

def searchEncounterTypes():
    return 'yaya'

def searchIdentifiers():
    return 'more yaya'

