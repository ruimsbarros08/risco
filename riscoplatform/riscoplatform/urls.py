from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'riscoplatform.views.home', name='home'),

    url(r'^countries$', 'riscoplatform.views.countries', name='countries'),
    url(r'^level1$', 'riscoplatform.views.level1', name='level1'),
    url(r'^level2$', 'riscoplatform.views.level2', name='level2'),
    url(r'^level3$', 'riscoplatform.views.level3', name='level3'),

    url(r'^accounts/$',  'riscoplatform.views.account', name='account'),
    url(r'^accounts/login/$',  'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^avatar/', include('avatar.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^models/', include('eng_models.urls')),
    url(r'^jobs/', include('jobs.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
