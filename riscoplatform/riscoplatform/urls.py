from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^$', 'riscoplatform.views.home', name='home'),

    url(r'^accounts/login/$',  'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^models/', include('eng_models.urls')),
    url(r'^jobs/', include('jobs.urls')),
)
