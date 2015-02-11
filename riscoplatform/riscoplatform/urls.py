from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'riscoplatform.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^models/', include('eng_models.urls')),
    url(r'^jobs/', include('jobs.urls')),
)
