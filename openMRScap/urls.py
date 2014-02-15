from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import django.views

from OMRS import views
from OMRS import omrsfunctions

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openMRScap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',views.index,name='index'),

    #add other projects URLS
    #url(r'^OMRS/',include('OMRS.urls')),

    url(r'^$','OMRS.views.index', name='home'),



    #url(r'^server/',views.jobs.as_view(),name='server'),
    url(r'^jobs/',views.jobs.as_view(),name='jobs'), #looks like a placeholder
    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/$','OMRS.views.server'), #allows user to view all their servers and create new ones
    url(r'^userprofile/$','OMRS.views.userProfile',name='userprofile'),
    url(r'^jobserversettings/$','OMRS.views.userJobSettings'), #lists just the URLS of the servers in the system
    url(r'^restricted/$', 'OMRS.views.restricted', name='restricted'), #not doing anything yet
    url(r'^alerts/$', 'working.views.create_user_alert', name='alerts'), #not doing anything yet



    #server details
    url(r'^setup/$', 'OMRS.views.post_server_details',name='setup'),
    url(r'^server_form/$', 'OMRS.views.server_form',name='server_form'),
    url(r'^server_details/$', 'OMRS.views.server_details_form',name='server_details'),

    #user details
    url(r'^register/$', 'OMRS.views.register', name='register'),
    url(r'^login/$', 'OMRS.views.user_login',name='login'),
    url(r'^logout/$', 'OMRS.views.user_logout', name='logout'),

    #import file
    url(r'^upload/$', 'OMRS.views.upload', name='upload'),

    #testign URLS
    #url(r'^serverauth/$', 'working.views.get_server_auth_details', name='serverauth'),  #deleted this

    url(r'^test/$', 'working.views.server_details_form', name='test'),
    url(r'^test/(?P<server_url>\w{0,500})$','working.views.server_details_form'),
    #http://127.0.0.1:8000/test/?server_url=http://localhost:8081/openmrs-standalone

    url(r'^_test/$','working.views._test',name='_test'),
    url(r'^createjob/$','working.views.createjob',name='createjob'),

    url(r'^userfeed/$','working.views.create_user_feed',name='userfeeds'),
    url(r'^messages/$', 'ajaxmessages.views.messages', name='ajaxmessages'),

    )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         django.views.static.serve,
         {'document_root': settings.MEDIA_ROOT}),
    )
