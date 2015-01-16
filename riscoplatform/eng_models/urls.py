from django.conf.urls import patterns, url
from eng_models import views

urlpatterns = patterns('',

	url(r'^hazard/$', views.index_hazard, name='index_hazard'),
    url(r'^hazard/faults/(?P<model_id>\d+)/$', views.detail_faults, name='detail_faults'),
	url(r'^hazard/add/faults$', views.add_fault_model, name='add_fault_model'),

	url(r'^exposure/$', views.index_exposure, name='index_exposure'),
    url(r'^exposure/(?P<model_id>\d+)/$', views.detail_exposure, name='detail_exposure'),
    url(r'^exposure/add/$', views.add_exposure, name='add_exposure'),

    url(r'^site/$', views.index_site, name='index_site'),
    url(r'^site/(?P<model_id>\d+)/$', views.detail_site, name='detail_site'),
    url(r'^site/(?P<model_id>\d+)/map_grid$', views.detail_site_ajax, name='detail_site_ajax'),
    url(r'^site/add/$', views.add_site_model, name='add_site_model'),
)