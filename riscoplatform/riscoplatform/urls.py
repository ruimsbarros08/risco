from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserChangeForm, UserCreationForm



urlpatterns = patterns('',
    url(r'^$', 'riscoplatform.views.home', name='home'),

    # url(r'^accounts/register/$',  'riscoplatform.views.register', name='register'),
    url(r'^accounts/register/$', CreateView.as_view(template_name='registration/register.html',
                                                form_class=UserCreationForm,
                                                success_url='/accounts/login/'), name='register'),
    # url(r'^welcome/$', 'riscoplatform.views.welcome', name='welcome'),
    url(r'^accounts/$',  'riscoplatform.views.account', name='account'),
    # url(r'^accounts/settings/$',  'riscoplatform.views.account_settings', name='account_settings'),
    url(r'^accounts/settings/$', CreateView.as_view(template_name='account_settings.html',
                                                        form_class=UserChangeForm,
                                                        success_url='/accounts/'), name='account_settings'),
    url(r'^profile/(?P<user_id>\d+)/$',  'riscoplatform.views.profile', name='profile'),
    url(r'^accounts/login/$',  'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^avatar/', include('avatar.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^models/', include('eng_models.urls')),
    url(r'^jobs/', include('jobs.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
