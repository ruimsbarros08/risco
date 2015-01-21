from django.conf.urls import patterns, url
from jobs import views

urlpatterns = patterns('',

	url(r'^scenario/hazard/$', views.index_scenario_hazard, name='index_scenario_hazard'),
    url(r'^scenario/hazard/add/$', views.add_sceanrio_hazard, name='add_sceanrio_hazard'),
)