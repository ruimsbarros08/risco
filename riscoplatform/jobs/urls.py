from django.conf.urls import patterns, url
from jobs import views

urlpatterns = patterns('',

    url(r'^$', views.home, name='jobs_home'),

	url(r'^scenario/hazard/$', views.index_scenario_hazard, name='index_scenario_hazard'),
    url(r'^scenario/hazard/add/$', views.add_scenario_hazard, name='add_scenario_hazard'),
    url(r'^scenario/hazard/results/(?P<job_id>\d+)/$', views.results_scenario_hazard, name='results_scenario_hazard'),
    url(r'^scenario/hazard/(?P<job_id>\d+)/start/$', views.start_scenario_hazard, name='start_scenario_hazard'),
    #url(r'^scenario/hazard/results_ajax/(?P<job_id>\d+)/$', views.results_scenario_hazard_ajax, name='results_scenario_hazard_ajax'),
    url(r'^scenario/hazard/results_ajax/(?P<job_id>\d+)/$', views.results_scenario_hazard_ajax, name='results_scenario_hazard_ajax'),

	url(r'^scenario/damage/$', views.index_scenario_damage, name='index_scenario_damage'),
    url(r'^scenario/damage/add/$', views.add_scenario_damage, name='add_scenario_damage'),
    url(r'^scenario/damage/results/(?P<job_id>\d+)/$', views.results_scenario_damage, name='results_scenario_damage'),
    url(r'^scenario/damage/(?P<job_id>\d+)/start/$', views.start_scenario_damage, name='start_scenario_damage'),
    url(r'^scenario/damage/results_ajax/(?P<job_id>\d+)/$', views.results_scenario_damage_ajax, name='results_scenario_damage_ajax'),
    #url(r'^scenario/damage/results/(?P<job_id>\d+)/tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/$', views.geojson_tiles, name='geojson_tiles'),

    url(r'^scenario/risk/$', views.index_scenario_risk, name='index_scenario_risk'),
    url(r'^scenario/risk/add/$', views.add_scenario_risk, name='add_scenario_risk'),
    url(r'^scenario/risk/results/(?P<job_id>\d+)/$', views.results_scenario_risk, name='results_scenario_risk'),
    url(r'^scenario/risk/results_ajax/(?P<job_id>\d+)/$', views.results_scenario_risk_ajax, name='results_scenario_risk_ajax'),
    url(r'^scenario/risk/(?P<job_id>\d+)/start/$', views.start_scenario_risk, name='start_scenario_risk'),

    url(r'^psha/hazard/$', views.index_psha_hazard, name='index_psha_hazard'),
    url(r'^psha/hazard/add/$', views.add_psha_hazard, name='add_psha_hazard'),
    url(r'^psha/hazard/results/(?P<job_id>\d+)/$', views.results_psha_hazard, name='results_psha_hazard'),
    url(r'^psha/hazard/results_maps/(?P<job_id>\d+)/$', views.results_psha_hazard_maps_ajax, name='results_psha_hazard_maps_ajax'),
    url(r'^psha/hazard/results_curves/(?P<job_id>\d+)/$', views.results_psha_hazard_curves_ajax, name='results_psha_hazard_curves_ajax'),
    url(r'^psha/hazard/(?P<job_id>\d+)/start/$', views.start_psha_hazard, name='start_psha_hazard'),

    url(r'^psha/risk/$', views.index_psha_risk, name='index_psha_risk'),
    url(r'^psha/risk/add/$', views.add_psha_risk, name='add_psha_risk'),
    url(r'^psha/risk/results/(?P<job_id>\d+)/$', views.results_psha_risk, name='results_psha_risk'),
    url(r'^psha/risk/results_maps/(?P<job_id>\d+)/$', views.results_psha_risk_maps_ajax, name='results_psha_risk_maps_ajax'),
    url(r'^psha/risk/results_locations/(?P<job_id>\d+)/$', views.results_psha_risk_locations_ajax, name='results_psha_risk_locations_ajax'),
    url(r'^psha/risk/results_curves/(?P<job_id>\d+)/$', views.results_psha_risk_curves_ajax, name='results_psha_risk_curves_ajax'),
    url(r'^psha/risk/(?P<job_id>\d+)/start/$', views.start_psha_risk, name='start_psha_risk'),

    url(r'^event_based/hazard/$', views.index_event_based_hazard, name='index_event_based_hazard'),
    url(r'^event_based/hazard/add/$', views.add_event_based_hazard, name='add_event_based_hazard'),
    url(r'^event_based/hazard/results/(?P<job_id>\d+)/$', views.results_event_based_hazard, name='results_event_based_hazard'),
    # url(r'^event_based/hazard/results_maps/(?P<job_id>\d+)/$', views.results_psha_hazard_maps_ajax, name='results_psha_hazard_maps_ajax'),
    # url(r'^event_based/hazard/results_curves/(?P<job_id>\d+)/$', views.results_psha_hazard_curves_ajax, name='results_psha_hazard_curves_ajax'),
    url(r'^event_based/hazard/(?P<job_id>\d+)/start/$', views.start_event_based_hazard, name='start_event_based_hazard'),


    url(r'^event_based/risk/$', views.index_event_based_risk, name='index_event_based_risk'),
    url(r'^event_based/risk/add/$', views.add_event_based_risk, name='add_event_based_risk'),
    url(r'^event_based/risk/results/(?P<job_id>\d+)/$', views.results_event_based_risk, name='results_event_based_risk'),
    # url(r'^event_based/hazard/results_maps/(?P<job_id>\d+)/$', views.results_psha_hazard_maps_ajax, name='results_psha_hazard_maps_ajax'),
    # url(r'^event_based/hazard/results_curves/(?P<job_id>\d+)/$', views.results_psha_hazard_curves_ajax, name='results_psha_hazard_curves_ajax'),
    url(r'^event_based/risk/(?P<job_id>\d+)/start/$', views.start_event_based_risk, name='start_event_based_risk'),

)