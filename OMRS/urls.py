__author__ = 'judyw'

from django.conf.urls import patterns, include, url
from OMRS import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openMRScap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #add other projects URLS
    #url(r'^$',views.index,name='index'),
    #url(r'^server/',views.server,name='server'),

)
