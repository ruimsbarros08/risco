from django.conf.urls import patterns, url
from jobs import views

urlpatterns = patterns('',

	url(r'^scenario/hazard/$', views.index_scenario_hazard, name='index_scenario_hazard'),
    url(r'^scenario/hazard/add/$', views.add_scenario_hazard, name='add_scenario_hazard'),
    url(r'^scenario/hazard/results/(?P<job_id>\d+)/$', views.results_scenario_hazard, name='results_scenario_hazard'),
    url(r'^scenario/hazard/results_ajax/(?P<job_id>\d+)/$', views.results_scenario_hazard_ajax, name='results_scenario_hazard_ajax'),
)