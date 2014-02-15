from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import RequestContext,loader,Context
from django.views.generic import ListView
from django.core.context_processors import csrf
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from ajaxmessages import add_message
from django.core.urlresolvers import reverse


from OMRS.models import JobStatus,Jobs,Authentication,Server,Shredder,Document,JobErrors
from OMRS.forms import UserProfileForm,UserForm,serverParams,DocumentForm,serverAuth
import OMRS.omrsfunctions as OF

#when using modelforms
from OMRS.forms import serverForm,LoadServerForm,ServerDetailsForm

# Create your views here.

def server_details_form(request):
    """
    Method to display the server details including location,provider and identifier and allow a user to select them as
    unbound data
    """
    return render(request,'test_server_auth.html',{'form':ServerDetailsForm()})

def server_form(request):
    """
    Method to display the server form with unbound data
    """
    return render(request,'testserver.html',{'form':LoadServerForm()})

def post_server_details(request):
    context = RequestContext(request)
    if request.method == 'GET':
        form = serverForm()
    else:
        # A POST request: Handle Form Upload
        # Bind data from request.POST into a PostForm
        form = serverForm(request.POST)
        if form.is_valid():
            serverdetails = form.save(commit=False)
            serverdetails.user = request.user
            serverdetails.save()
            return HttpResponseRedirect('/server')
    c = {'serverDetails':form}
    return render_to_response('setup.html',c,context)

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage':"I am bold"}
    return render_to_response('index.html',context_dict,context)

def restricted(request):
    context = RequestContext(request)
    context_dict = {'boldmessage':"I am bold"}
    return render_to_response('index.html',context_dict,context)

def server(request):
    """
    Method that lists all servers available as a user creates a job
    """
    context = RequestContext(request)
    user = request.user
    latest_server_list = Server.objects.filter(user=user)
    c = Context({
        'latest_server_list' : latest_server_list
    })
    return render_to_response('server.html',c,context)

def userProfile(request):
    context = RequestContext(request)
    return render_to_response('userprofile.html',{
        'jobs_list' :  Jobs.objects.filter(user = request.user),
    },context)

class jobs(ListView):
    model = Jobs
    template_name = 'jobs.html'

def userJobSettings(request):
    context = RequestContext(request)
    return render_to_response('serverparams.html',{
        'userjobsettings_list': Server.objects.all(),
    },context)

def setup(request):
     context = RequestContext(request)

     if request.method == 'POST':
         setup_form = serverParams(data=request.POST)
         if setup_form.is_valid():
             new_obj = setup_form.save(commit=False)
             new_obj.save()
             #setup_form.save()
             return HttpResponseRedirect('/jobserversettings')
         else:
             print setup_form.errors

     return render_to_response('/setup', {}, context_instance=RequestContext(request))


def serverDetails(request):
    context = RequestContext(request)

    if request.method == 'POST':
        server_form = serverParams(data = request.POST)  #whats is declared int he forms data
        if server_form.is_valid():
            location_list = OF.searchLocations(server_form.serverAddress,server_form.serverUsername,server_form.serverPassword)
            print location_list
    return render_to_response('serverdetails.html',{
        'userjobsettings_list': Server.objects.all(),
    })

def register(request):
    context = RequestContext(request)
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            #on successful registration move to the login page
            return HttpResponseRedirect('/login')



        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    context_dict = {}
    c = {}
    c.update(csrf(request))

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                auth_login(request, user)
                return HttpResponseRedirect('/userprofile')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Kenya Data Works account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('login.html', context_dict, context)
           # return HttpResponseRedirect('/')
            #return HttpResponse("Invalid login details supplied.")



    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', context_dict, context)



# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

#view to support file upload

def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse(''))  userprofile
            return HttpResponseRedirect('/userprofile')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'upload.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

'''
class servers(ListView):
    model = Server
    template_name = 'server.html'


def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request, *args, **kwargs)
    return new_view


    <!-- <li> Username: {{ username }}</li> -->
        <li> OMRS Server: {{ serverAddress }}</li>
        <li> OMRS Username: {{ serverUsername }}</li>
        <li> Date Added: {{ dateAdded }}</li>
'''

'''

from django.conf.urls.defaults import *
from mysite.views import requires_login, my_view1, my_view2, my_view3

urlpatterns = patterns('',
    (r'^view1/$', requires_login(my_view1)),
    (r'^view2/$', requires_login(my_view2)),
    (r'^view3/$', requires_login(my_view3)),
)
'''