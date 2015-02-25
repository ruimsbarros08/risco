from django.conf.urls import patterns, url
from eng_models import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='eng_models_home'),

	url(r'^sources/$', views.index_source, name='index_source'),
    url(r'^sources/(?P<model_id>\d+)/$', views.detail_source, name='detail_source'),
    url(r'^sources/add$', views.add_source_model, name='add_source_model'),
    url(r'^sources/(?P<model_id>\d+)/add_source$', views.add_source, name='add_source'),
    url(r'^sources/(?P<model_id>\d+)/ajax$', views.sources_ajax, name='sources_ajax'),

    url(r'^rupture/$', views.index_rupture_model, name='index_rupture_model'),
    url(r'^rupture/add$', views.add_rupture_model, name='add_rupture_model'),
    url(r'^rupture/ajax$', views.ruptures_ajax, name='ruptures_ajax'),

    url(r'^site/$', views.index_site, name='index_site'),
    url(r'^site/(?P<model_id>\d+)/$', views.detail_site, name='detail_site'),
    url(r'^site/(?P<model_id>\d+)/map_grid$', views.detail_site_ajax, name='detail_site_ajax'),
    url(r'^site/add/$', views.add_site_model, name='add_site_model'),

    url(r'^fragility/$', views.index_fragility, name='index_fragility'),
    url(r'^fragility/(?P<model_id>\d+)/$', views.detail_fragility, name='detail_fragility'),
    url(r'^fragility/(?P<model_id>\d+)/taxonomy/(?P<taxonomy_id>\d+)/$', views.fragility_get_taxonomy, name='fragility_get_taxonomy'),
    url(r'^fragility/add/$', views.add_fragility_model, name='add_fragility_model'),

    url(r'^exposure/$', views.index_exposure, name='index_exposure'),
    url(r'^exposure/(?P<model_id>\d+)/$', views.detail_exposure, name='detail_exposure'),
    url(r'^exposure/add/$', views.add_exposure_model, name='add_exposure_model'),
    url(r'^exposure/(?P<model_id>\d+)/tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/$', views.exposure_geojson_tiles, name='exposure_geojson_tiles'),

    url(r'^logictree/$', views.index_logic_tree, name='index_logic_tree'),
    url(r'^logictree/(?P<model_id>\d+)/$', views.detail_logic_tree, name='detail_logic_tree'),
    url(r'^logictree/(?P<model_id>\d+)/ajax$', views.logic_tree_ajax, name='logic_tree_ajax'),
    url(r'^logictree/add/$', views.add_logic_tree, name='add_logic_tree'),

)