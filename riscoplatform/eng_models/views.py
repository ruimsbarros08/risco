from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from eng_models.models import *
from world.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parsers import exposure_parser, site_model_parser, source_parser, fragility_parser, vulnerability_parser, sm_logic_tree_parser, gmpe_logic_tree_parser
from django.core import serializers
from django.db import connection
from django.db import transaction
from django.contrib.gis.geos import Point

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

#from django.db.models import Q
#from django.db.models import F
import json
import requests

from riscoplatform.local_settings import *

def pagination(list, n, page):
	paginator = Paginator(list, n)
	try:
		new_list = paginator.page(page)
	except PageNotAnInteger:
		new_list = paginator.page(1)
	except EmptyPage:
		new_list = paginator.page(paginator.num_pages)
	return new_list


#MODELS HOME

def home(request):
	return render(request, 'eng_models/home.html')

def get_geojson_countries(features_list):
	features = list(dict(type='Feature',
						id=cell[0],
						properties=dict(id=cell[0],
										name=cell[2]),
						geometry=json.loads(cell[1])) for cell in features_list)

	return {'type': 'FeatureCollection', 'features': features}

############################
##     TAXONOMY SOURCE    ##
############################

@login_required
def index_taxonomy(request):
	models = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
	page = request.GET.get('page')
	return render(request, 'eng_models/index_taxonomy.html', {'models': pagination(models, 10, page)})

@login_required
def detail_taxonomy(request, model_id):
	model = get_object_or_404(Building_Taxonomy_Source ,pk=model_id, building_taxonomy_source_contributor__contributor=request.user)
	taxonomies = Building_Taxonomy.objects.filter(source=model)
	return render(request, 'eng_models/detail_taxonomy.html', {'model': model, 'taxonomies':taxonomies})



#####################
##     EXPOSURE    ##
#####################

exposure_form_categories = {'general': ['name', 'description', 'deductible', 'insurance_limit', 'taxonomy_source', 'add_tax_source',
										'tax_source_name', 'tax_source_desc', 'xml'],
							'area': ['area_type', 'area_unit'],
							'structural': ['struct_cost_type', 'struct_cost_currency'],
							'nonstructural': ['non_struct_cost_type', 'non_struct_cost_currency'],
							'contents': ['contents_cost_type', 'contents_cost_currency'],
							'business_int': ['business_int_cost_type', 'business_int_cost_currency']}

class ExposureForm(forms.ModelForm):
	add_tax_source = forms.BooleanField(required=False)
	tax_source_name = forms.CharField(required=False)
	tax_source_desc = forms.CharField(required=False)
	class Meta:
		model = Exposure_Model
		fields = ['name', 'description', 'taxonomy_source', 'area_type', 'area_unit', 'deductible', 'insurance_limit', 'struct_cost_type', 'struct_cost_currency', 'non_struct_cost_type', 'non_struct_cost_currency', 'contents_cost_type', 'contents_cost_currency', 'business_int_cost_type', 'business_int_cost_currency', 'xml']
     
class AssetForm(forms.ModelForm):
	class Meta:
		model = Asset
		exclude = ['model', 'parish']
		widgets = {
			'location': forms.HiddenInput(),
		}

			
@login_required
def index_exposure(request):
	models = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	form = ExposureForm()
	form.fields["taxonomy_source"].queryset = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
	# page = request.GET.get('page')
	return render(request, 'eng_models/index_exposure.html', {'models': models, 'form': form, 'categories': exposure_form_categories})


@login_required
def ajax_exposure_models(request):
	user_id = request.user.id
	cursor = connection.cursor()

	cursor.execute('SELECT list.country_id, ST_AsGeoJSON(world_country.geom_simp), list.country_name, list.sum \
					FROM (SELECT world_country.id AS country_id, world_country.name AS country_name, count(eng_models_asset.id) AS sum \
						FROM eng_models_exposure_model_contributor, \
							eng_models_asset, world_adm_2, world_adm_1, world_country \
						WHERE eng_models_exposure_model_contributor.contributor_id = %s \
						AND eng_models_asset.model_id = eng_models_exposure_model_contributor.model_id \
						AND eng_models_asset.adm_2_id = world_adm_2.id \
						AND world_adm_2.adm_1_id = world_adm_1.id \
						AND world_adm_1.country_id = world_country.id \
						GROUP BY world_country.id) AS list, world_country \
					WHERE list.country_id = world_country.id', [user_id])
	data = cursor.fetchall()

	features = list()

	for country in data:
		cursor.execute('SELECT eng_models_exposure_model.id, eng_models_exposure_model.name \
						FROM eng_models_exposure_model, eng_models_asset, world_adm_2, world_adm_1 \
						WHERE eng_models_asset.model_id = eng_models_exposure_model.id \
						AND eng_models_asset.adm_2_id = world_adm_2.id \
						AND world_adm_2.adm_1_id = world_adm_1.id \
						AND world_adm_1.country_id = %s \
						GROUP BY eng_models_exposure_model.id', [country[0]])

		feature = dict(type='Feature',
							id=country[0],
							properties=dict(id=country[0],
											name=country[2],
											n_assets = country[3],
											models = list(dict(id=model[0],
																name=model[1]) for model in cursor.fetchall())),
							geometry=json.loads(country[1]))

		features.append(feature)

	countries = {'type': 'FeatureCollection', 'features': features}

	return HttpResponse(json.dumps({'countries': countries}), content_type="application/json")


@login_required
def detail_exposure(request, model_id):
	model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
	form = AssetForm()
	form.fields["taxonomy"].queryset = Building_Taxonomy.objects.filter(source=model.taxonomy_source)
	return render(request, 'eng_models/detail_exposure.html', {'model': model, 'form': form})


@login_required
def ajax_assets(request, model_id):

	model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
	model_json = serializers.serialize("json", [model])
	model_json = json.loads(model_json)

	if request.GET.get('taxonomy') != 'undefined':
		taxonomies_json = []

	else:
		taxonomies = Building_Taxonomy.objects.filter(source = model.taxonomy_source)
		taxonomies_json = serializers.serialize("json", taxonomies)
		taxonomies_json = json.loads(taxonomies_json)

	cursor = connection.cursor()
	
	if request.method == 'GET':
		
		region = request.GET.get('region')

		if int(request.GET.get('level')) == 3:

			regions = []

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy = request.GET.get('taxonomy')

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_building_taxonomy.id = %s \
							AND eng_models_asset.adm_2_id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, taxonomy, region])

			else:

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_asset.adm_2_id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, region])


		elif int(request.GET.get('level')) == 2:

			cursor.execute('SELECT DISTINCT world_adm_2.id, world_adm_2.name \
							FROM eng_models_asset, world_adm_2 \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = %s', [model.id, region])

			regions = [ {'id': r[0], 'name': r[1]} for r in cursor.fetchall() ]

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy = request.GET.get('taxonomy')

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, world_adm_2, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_building_taxonomy.id = %s \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, taxonomy, region])

			else:

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, world_adm_2, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, region])


		elif int(request.GET.get('level')) == 1:

			cursor.execute('SELECT DISTINCT world_adm_1.id, world_adm_1.name \
							FROM eng_models_asset, world_adm_1, world_adm_2 \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = world_adm_1.id \
							AND world_adm_1.country_id = %s', [model.id, region])

			regions = [ {'id': r[0], 'name': r[1]} for r in cursor.fetchall() ]

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy = request.GET.get('taxonomy')

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, world_adm_2, world_adm_1, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_building_taxonomy.id = %s \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = world_adm_1.id \
							AND world_adm_1.country_id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, taxonomy, region])

			else:

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, world_adm_2, world_adm_1, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = world_adm_1.id \
							AND world_adm_1.country_id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, region])


		else:

			cursor.execute('SELECT DISTINCT world_country.id, world_country.name \
							FROM eng_models_asset, world_country, world_adm_1, world_adm_2 \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.adm_2_id = world_adm_2.id \
							AND world_adm_2.adm_1_id = world_adm_1.id \
							AND world_adm_1.country_id = world_country.id', [model.id])

			regions = [ {'id': r[0], 'name': r[1]} for r in cursor.fetchall() ]

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy = request.GET.get('taxonomy')

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							AND eng_models_building_taxonomy.id = %s \
							ORDER BY eng_models_asset.id ASC', [model.id, taxonomy])

			else:

				cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
							eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
							eng_models_asset.n_buildings, eng_models_asset.area, \
							eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
							eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
							eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
							eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
							eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
							FROM eng_models_asset, eng_models_building_taxonomy \
							WHERE eng_models_asset.model_id = %s \
							AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
							ORDER BY eng_models_asset.id ASC', [model.id])
			
		assets = [ {'lat': asset[0],
					'lon': asset[1],
					'id': asset[2],
					'name': asset[3],
					'taxonomy': asset[4],
					'n_buildings': asset[5],
					'area': asset[6],
					'struct_cost': asset[7],
					'struct_deductible': asset[8],
					'struct_insurance_limit': asset[9],
					'retrofitting_cost': asset[10],
					'non_struct_cost': asset[11],
					'non_struct_deductible': asset[12],
					'non_struct_insurance_limit': asset[13],
					'contents_cost': asset[14],
					'contents_deductible': asset[15],
					'contents_insurance_limit': asset[16],
					'business_int_cost': asset[17],
					'business_int_deductible': asset[18],
					'business_int_insurance_limit': asset[19],
					'oc_day': asset[20],
					'oc_night': asset[21],
					'oc_transit': asset[22],
					'selected': False} for asset in cursor.fetchall()]
				

	elif request.method == 'POST':
		assets = json.loads(request.body)
		with transaction.atomic():
			for asset in assets:
				try:
					tax = Building_Taxonomy.objects.get(source=model.taxonomy_source, name=asset['taxonomy'])
				except:
					tax = Building_Taxonomy(source=model.taxonomy_source, name=asset['taxonomy'])
					tax.save()

				try:
					a = Asset.objects.get(name=asset['name'], model=model)

					try:
						loc = Point(float( asset['lon']), float( asset['lat']))
					except:
						asset['error'] = 'Invalid location'
						break

					try:
						adm_2 = Adm_2.objects.get(geom__intersects=loc)
					except:
						adm_2 = None

					try:
						a.name = asset['name']
						a.taxonomy = tax
						a.adm_2 = adm_2
						a.n_buildings = asset['n_buildings']
						a.area = asset['area']
						a.struct_cost = asset['struct_cost']
						a.struct_deductible = asset['struct_deductible']
						a.struct_insurance_limit = asset['struct_insurance_limit']
						a.retrofitting_cost = asset['retrofitting_cost']
						a.non_struct_cost = asset['non_struct_cost']
						a.non_struct_deductible = asset['non_struct_deductible']
						a.non_struct_insurance_limit = asset['non_struct_insurance_limit']
						a.contents_cost = asset['contents_cost']
						a.contents_deductible = asset['contents_deductible']
						a.contents_insurance_limit = asset['contents_insurance_limit']						
						a.business_int_cost = asset['business_int_cost']
						a.business_int_deductible = asset['business_int_deductible']
						a.business_int_insurance_limit = asset['business_int_insurance_limit']
						a.location = loc
						a.model = model
						a.oc_day = asset['oc_day']
						a.oc_night = asset['oc_night']
						a.oc_transit = asset['oc_transit']

						a.save()
						
					except Exception, e:
						asset['error'] = e


				except Exception as e:
					if asset['name'] != None:

						try:
							loc = Point(float( asset['lon']), float( asset['lat']))
						except:
							asset['error'] = 'Invalid location'
							break

						try:
							adm_2 = Adm_2.objects.get(geom__intersects=loc)
						except:
							adm_2 = None

						try:
							a = Asset(name = asset['name'],
									taxonomy = tax,
									adm_2 = adm_2,
									n_buildings = asset['n_buildings'],
									area = asset['area'],
									struct_cost = asset['struct_cost'],
									struct_deductible = asset['struct_deductible'],
									struct_insurance_limit = asset['struct_insurance_limit'],
									retrofitting_cost = asset['retrofitting_cost'],
									non_struct_cost = asset['non_struct_cost'],
									non_struct_deductible = asset['non_struct_deductible'],
									non_struct_insurance_limit = asset['non_struct_insurance_limit'],
									contents_cost = asset['contents_cost'],
									contents_deductible = asset['contents_deductible'],
									contents_insurance_limit = asset['contents_insurance_limit'],						
									business_int_cost = asset['business_int_cost'],
									business_int_deductible = asset['business_int_deductible'],
									business_int_insurance_limit = asset['business_int_insurance_limit'],
									location = loc,
									model = model,
									oc_day = asset['oc_day'],
									oc_night = asset['oc_night'],
									oc_transit = asset['oc_transit'])

							a.save()
						except Exception as e:

							asset['error'] = e

					else:
						if asset['id']:
							a = Asset.objects.get(pk=asset['id'])
							a.delete()




		cursor.execute('SELECT DISTINCT world_country.id, world_country.name \
						FROM eng_models_asset, world_country, world_adm_1, world_adm_2 \
						WHERE eng_models_asset.model_id = %s \
						AND eng_models_asset.adm_2_id = world_adm_2.id \
						AND world_adm_2.adm_1_id = world_adm_1.id \
						AND world_adm_1.country_id = world_country.id', [model.id])

		regions = [ {'id': r[0], 'name': r[1]} for r in cursor.fetchall() ]


	elif request.method == 'DELETE':

		cursor.execute('SELECT DISTINCT world_country.id, world_country.name \
						FROM eng_models_asset, world_country, world_adm_1, world_adm_2 \
						WHERE eng_models_asset.model_id = %s \
						AND eng_models_asset.adm_2_id = world_adm_2.id \
						AND world_adm_2.adm_1_id = world_adm_1.id \
						AND world_adm_1.country_id = world_country.id', [model.id])

		regions = [ {'id': r[0], 'name': r[1]} for r in cursor.fetchall() ]


		assets = json.loads(request.body)
		with transaction.atomic():
			for asset in assets:
				try:
					a = Asset.objects.get(name=asset, model=model)
					a.delete()
				except:
					pass

		taxonomies = Building_Taxonomy.objects.filter(source = model.taxonomy_source)
		taxonomies_json = serializers.serialize("json", taxonomies)
		taxonomies_json = json.loads(taxonomies_json)

		cursor.execute('SELECT st_y(eng_models_asset.location), st_x(eng_models_asset.location), \
					eng_models_asset.id, eng_models_asset.name, eng_models_building_taxonomy.name, \
					eng_models_asset.n_buildings, eng_models_asset.area, \
					eng_models_asset.struct_cost, eng_models_asset.struct_deductible, eng_models_asset.struct_insurance_limit, eng_models_asset.retrofitting_cost, \
					eng_models_asset.non_struct_cost, eng_models_asset.non_struct_deductible, eng_models_asset.non_struct_insurance_limit, \
					eng_models_asset.contents_cost, eng_models_asset.contents_deductible, eng_models_asset.contents_insurance_limit, \
					eng_models_asset.business_int_cost, eng_models_asset.business_int_deductible, eng_models_asset.business_int_insurance_limit, \
					eng_models_asset.oc_day, eng_models_asset.oc_night, eng_models_asset.oc_transit \
					FROM eng_models_asset, eng_models_building_taxonomy \
					WHERE eng_models_asset.model_id = %s \
					AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
					ORDER BY eng_models_asset.id ASC', [model.id])
			
		assets = [ {'lat': asset[0],
					'lon': asset[1],
					'id': asset[2],
					'name': asset[3],
					'taxonomy': asset[4],
					'n_buildings': asset[5],
					'area': asset[6],
					'struct_cost': asset[7],
					'struct_deductible': asset[8],
					'struct_insurance_limit': asset[9],
					'retrofitting_cost': asset[10],
					'non_struct_cost': asset[11],
					'non_struct_deductible': asset[12],
					'non_struct_insurance_limit': asset[13],
					'contents_cost': asset[14],
					'contents_deductible': asset[15],
					'contents_insurance_limit': asset[16],
					'business_int_cost': asset[17],
					'business_int_deductible': asset[18],
					'business_int_insurance_limit': asset[19],
					'oc_day': asset[20],
					'oc_night': asset[21],
					'oc_transit': asset[22],
					'selected': False} for asset in cursor.fetchall()]



	return HttpResponse(json.dumps({'model': model_json,
									'assets': assets,
									'taxonomies': taxonomies_json,
									'regions': regions}), content_type="application/json")



@login_required
def add_exposure_model(request):
	if request.method == 'POST':
		form = ExposureForm(request.POST, request.FILES)
		form.fields["taxonomy_source"].queryset = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			if 'add_tax_source' in request.POST:
				new_tax_source = Building_Taxonomy_Source(name=request.POST['tax_source_name'],
															description=request.POST['tax_source_desc'],
															date_created=timezone.now())
				new_tax_source.save()
				Building_Taxonomy_Source_Contributor.objects.create(contributor=request.user, source=new_tax_source, date_joined=new_tax_source.date_created, author=True)
				model.taxonomy_source = new_tax_source
			if request.FILES:
				try:
					exposure_parser.start(model)
				except Exception as e:
					model.delete()
					return render(request, 'eng_models/index_exposure.html', {'form': form, 'parse_error': e, 'categories': exposure_form_categories})
			Exposure_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			return redirect('detail_exposure', model_id=model.id)
		else:
			models = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_exposure.html', {'models': pagination(models, 10, 1), 'form': form, 'categories': exposure_form_categories})
	else:
		form = ExposureForm()
		return render(request, 'eng_models/index_exposure.html', {'form': form, 'categories': exposure_form_categories})


@login_required
def add_asset(request, model_id):
	if request.method == 'POST':
		model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
		form = AssetForm(request.POST)
		form.fields["taxonomy"].queryset = Building_Taxonomy.objects.filter(source=model.taxonomy_source)
		if form.is_valid():
			asset = form.save(commit=False)
			asset.model_id = model_id
			asset.save()
			return redirect('detail_exposure', model_id=model_id)
		else:
			model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
			try:
				asset_list = Asset.objects.filter(model_id=model_id)[1:50]
			except:
				asset_list = []
			return render(request, 'eng_models/detail_exposure.html', {'model': model, 'form': form, 'assets': asset_list})
	else:
		model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
		form = AssetForm()
		return render(request, 'eng_models/detail_exposure.html', {'model': model, 'form': form})




############################
##     SITE CONDITIONS    ##
############################


class SiteForm(forms.ModelForm):
	class Meta:
		model = Site_Model
		fields = ['name', 'description', 'xml']

@login_required
def index_site(request):
	models = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
	form = SiteForm()
	page = request.GET.get('page')

	return render(request, 'eng_models/index_site.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_site(request, model_id):
	model = get_object_or_404(Site_Model ,pk=model_id, site_model_contributor__contributor=request.user)
	site_list = Site.objects.filter(model_id=model_id)
	#page = request.GET.get('page')
	return render(request, 'eng_models/detail_site.html', {'model': model, 'sites': site_list})

@login_required
def detail_site_ajax(request, model_id):

	cursor = connection.cursor()
	cursor.execute('select ST_AsGeoJSON(cell), avg(vs30), avg(z1pt0), avg(z2pt5), world_fishnet.id \
					from world_fishnet, eng_models_site \
					where eng_models_site.model_id = %s \
					and eng_models_site.cell_id = world_fishnet.id \
					group by world_fishnet.id', [model_id])

	features = [dict(type='Feature', id=cell[4], properties=dict(color='#FF0000', vs30="{0:.4f}".format(cell[1]),
																z1pt0="{0:.4f}".format(cell[2]),
																z2pt5="{0:.4f}".format(cell[3])),
				geometry=json.loads(cell[0])) for cell in cursor.fetchall()]
	geojson = {'type': 'FeatureCollection', 'features': features}

	return HttpResponse(json.dumps(geojson), content_type="application/json")

@login_required
def add_site_model(request):
	if request.method == 'POST':
		form = SiteForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			Site_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			if request.FILES:
				try:
					site_model_parser.start(model)
				except Exception as e:
					model.delete()
					return render(request, 'eng_models/index_site.html', {'form': form, 'parse_error': e})
			return redirect('detail_site', model_id=model.id)
		else:
			models = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_site.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = SiteForm()
		return render(request, 'eng_models/index_site.html', {'form': form})



###################
##     SOURCE    ##
###################


class SourceModelForm(forms.ModelForm):

	class Meta:
		model = Source_Model
		fields = ['name', 'description', 'xml']


source_categories = {'general': ['name', 'tectonic_region', 'mag_scale_rel', 'rupt_aspect_ratio'],
					'mag_freq_dist': ['mag_freq_dist_type', 'a', 'b', 'min_mag', 'max_mag', 'bin_width', 'occur_rates'],
					'geometry': ['source_type', 'point', 'upper_depth', 'lower_depth', 'nodal_plane_dist', 'hypo_depth_dist', 'area', 'fault', 'dip', 'rake']} 


class SourceForm(forms.ModelForm):

	def clean(self):
		form_data = self.cleaned_data

		if 'b' in form_data:
			if form_data['b'] < 0:
				self._errors["b"] = "This parameter must be a float greater than 0"
				del form_data['b']

		if form_data['source_type'] != 'SIMPLE_FAULT':
			if 'nodal_plane_dist' in form_data:
				nodal_plane_dist = [[]]
				for e in form_data['nodal_plane_dist']:
					value = float(e.replace('[', '').replace(']', ''))
					if len(nodal_plane_dist[-1]) != 4:  
						pass
					else:
						nodal_plane_dist.append([])
					nodal_plane_dist[-1].append(value)

				prob_sum = 0
				for e in nodal_plane_dist:
					prob_sum += e[0]

				if prob_sum != 1:
					self.add_error(None, 'The sum of the probabilisties must be equal to 1')


			form_data['nodal_plane_dist'] = nodal_plane_dist

			if 'hypo_depth_dist' in form_data:
				hypo_depth_dist = [[]]
				for e in form_data['hypo_depth_dist']:
					value = float(e.replace('[', '').replace(']', ''))
					if len(hypo_depth_dist[-1]) != 2:  
						pass
					else:
						hypo_depth_dist.append([])
					hypo_depth_dist[-1].append(value)

				prob_sum = 0
				for e in hypo_depth_dist:
					if 'lower_depth' in form_data and 'upper_depth' in form_data:
						if e[1] < form_data['lower_depth'] or e[1] > form_data['upper_depth']:
							self._errors["lower_depth"] = "All hypocenter depths specified must be between the lower and the upper depth"
							self._errors["upper_depth"] = "All hypocenter depths specified must be between the lower and the upper depth"
					prob_sum += e[0]
				
				if prob_sum != 1:
					self.add_error(None, 'The sum of the probabilities must be equal to 1')

				form_data['hypo_depth_dist'] = hypo_depth_dist



		if 'lower_depth' in form_data and 'upper_depth' in form_data:
			if form_data['lower_depth'] <= form_data['upper_depth']:
				self._errors["lower_depth"] = "Lower depth value must be higher than upper depth"
				self._errors["upper_depth"] = "Lower depth value must be higher than upper depth"
				del form_data['lower_depth']
				del form_data['upper_depth']
		if 'max_mag' in form_data and 'min_mag' in form_data:
			if form_data['max_mag'] <= form_data['min_mag']:
				self._errors["max_mag"] = "Max magnitude value must be higher than min magnitude"
				self._errors["min_mag"] = "Max magnitude value must be higher than min magnitude"
				del form_data['max_mag']
				del form_data['min_mag']
		return form_data

	class Meta:
		model = Source
		fields = ['name', 'tectonic_region', 'mag_scale_rel', 'rupt_aspect_ratio', 'mag_freq_dist_type', 'a', 'b', 'min_mag', 'max_mag', 'bin_width', 'occur_rates', 'source_type', 'upper_depth', 'lower_depth', 'nodal_plane_dist', 'hypo_depth_dist', 'dip', 'rake', 'point', 'area', 'fault']
		widgets = {
					'point': forms.HiddenInput(),
					'area': forms.HiddenInput(),
					'fault': forms.HiddenInput(),
					'occur_rates': forms.HiddenInput(),
					'nodal_plane_dist': forms.HiddenInput(),
					'hypo_depth_dist': forms.HiddenInput()
					}
		
@login_required
def index_source(request):
	models = Source_Model.objects.filter(source_model_contributor__contributor=request.user).order_by('-date_created')
	form = SourceModelForm()
	page = request.GET.get('page')

	return render(request, 'eng_models/index_source.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_source(request, model_id):
	model = get_object_or_404(Source_Model ,pk=model_id, source_model_contributor__contributor=request.user)
	sources = Source.objects.filter(model_id=model_id)
	# page = request.GET.get('page')
	form = SourceForm()
	return render(request, 'eng_models/detail_source.html', {'model': model, 'form': form, 'sources': sources, 'source_categories': source_categories})

@login_required
def add_source(request, model_id):
	model = get_object_or_404(Source_Model ,pk=model_id)
	sources = Source.objects.filter(model_id=model_id)
	if request.method == 'POST':
		form = SourceForm(request.POST)
		if form.is_valid():
			source = form.save(commit=False)
			source.model_id = model_id
			source.save()
			return redirect('detail_source', model_id=model_id)
		else:

			return render(request, 'eng_models/detail_source.html', {'model': model, 'sources': sources ,'form': form, 'source_categories': source_categories})
	else:
		form = SourceForm()
		return render(request, 'eng_models/detail_source.html', {'model': model, 'sources': sources, 'form': form, 'source_categories': source_categories})

@login_required
def add_source_model(request):
	if request.method == 'POST':
		form = SourceModelForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			Source_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			if request.FILES:
				try:
					source_parser.start(model)
				except Exception as e:
					model.delete()
					return render(request, 'eng_models/index_source.html', {'form': form, 'parse_error': e})
			return redirect('detail_source', model_id=model.id)
		else:
			models = Source_Model.objects.filter(source_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_source.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = SourceModelForm()
		return render(request, 'eng_models/index_source.html', {'form': form})

def get_sources(model_id):
	#model = Source_Model.objects.get(id=model_id)

	point_sources = Source.objects.filter(model_id=model_id, source_type='POINT')
	point_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name,
																		tectonic_region=source.tectonic_region,
																		mag_scale_rel=source.mag_scale_rel,
																		rupt_aspect_ratio=source.rupt_aspect_ratio,
																		mag_freq_dist_type=source.mag_freq_dist_type,
																		a=source.a,
																		b=source.b,
																		min_mag=source.min_mag,
																		max_mag=source.max_mag,
																		bin_width=source.bin_width,
																		occur_rates=source.occur_rates,
																		source_type=source.source_type,
																		upper_depth=source.upper_depth,
																		lower_depth=source.lower_depth,
																		nodal_plane_dist=source.nodal_plane_dist,
																		hypo_depth_dist=source.hypo_depth_dist),
				geometry = json.loads(source.point.json) ) for source in point_sources]

	area_sources = Source.objects.filter(model_id=model_id, source_type='AREA')
	area_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name,
																		tectonic_region=source.tectonic_region,
																		mag_scale_rel=source.mag_scale_rel,
																		rupt_aspect_ratio=source.rupt_aspect_ratio,
																		mag_freq_dist_type=source.mag_freq_dist_type,
																		a=source.a,
																		b=source.b,
																		min_mag=source.min_mag,
																		max_mag=source.max_mag,
																		bin_width=source.bin_width,
																		occur_rates=source.occur_rates,
																		source_type=source.source_type,																		
																		upper_depth=source.upper_depth,
																		lower_depth=source.lower_depth,
																		nodal_plane_dist=source.nodal_plane_dist,
																		hypo_depth_dist=source.hypo_depth_dist),
				geometry = json.loads(source.area.json) ) for source in area_sources]

	fault_sources = Source.objects.filter(model_id=model_id, source_type='SIMPLE_FAULT')
	fault_features = [dict(type='Feature', id=source.id, properties=dict(  name = source.name,
																		tectonic_region=source.tectonic_region,
																		mag_scale_rel=source.mag_scale_rel,
																		rupt_aspect_ratio=source.rupt_aspect_ratio,
																		mag_freq_dist_type=source.mag_freq_dist_type,
																		a=source.a,
																		b=source.b,
																		min_mag=source.min_mag,
																		max_mag=source.max_mag,
																		bin_width=source.bin_width,
																		occur_rates=source.occur_rates,
																		source_type=source.source_type,																		
																		upper_depth=source.upper_depth,
																		lower_depth=source.lower_depth,
																		dip=source.dip,
																		rake=source.rake ),
				geometry = json.loads(source.fault.json) ) for source in fault_sources]	

	return {'pointSource': {'type': 'FeatureCollection', 'features': point_features},
			'areaSource': {'type': 'FeatureCollection', 'features': area_features},
			'faultSource': {'type': 'FeatureCollection', 'features': fault_features}}
			#'name': model.name}

@login_required
def sources_ajax(request, model_id):
	model = get_object_or_404(Source_Model ,pk=model_id, source_model_contributor__contributor=request.user)
	data = get_sources(model_id)
	return HttpResponse(json.dumps(data), content_type="application/json")


####################
##     RUPTURE    ##
####################


class RuptureForm(forms.ModelForm):

	def clean(self):
		form_data = self.cleaned_data
		if 'lower_depth' in form_data and 'upper_depth' in form_data:
			if form_data['lower_depth'] <= form_data['upper_depth']:
				self._errors["lower_depth"] = "Lower depth value must be higher than upper depth"
				self._errors["upper_depth"] = "Lower depth value must be higher than upper depth"
				del form_data['lower_depth']
				del form_data['upper_depth']
		return form_data

	class Meta:
		model = Rupture_Model
		exclude = ['user', 'date_created']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'location': forms.HiddenInput(),
					'rupture_geom': forms.HiddenInput(),
					}

@login_required
def index_rupture_model(request):
	models = Rupture_Model.objects.filter(user=request.user).order_by('-date_created')
	form = RuptureForm()
	return render(request, 'eng_models/index_rupture_model.html', {'models': models, 'form': form})

@login_required
def add_rupture_model(request):
	if request.method == 'POST':
		form = RuptureForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.user = request.user
			model.save()
			if request.FILES:
				pass
				#create parser
			return redirect('index_rupture_model')
		else:
			models = Rupture_Model.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_rupture_model.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = RuptureForm()
		return render(request, 'eng_models/index_rupture_model.html', {'form': form})

@login_required
def ruptures_ajax(request):
	point_sources = Rupture_Model.objects.filter(rupture_type='POINT', user=request.user)
	point_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
				geometry = json.loads(source.location.json) ) for source in point_sources]


	fault_sources = Rupture_Model.objects.filter(rupture_type='FAULT', user=request.user)
	fault_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
				geometry = json.loads(source.rupture_geom.json) ) for source in fault_sources]	

	data = {'pointSource': {'type': 'FeatureCollection', 'features': point_features},
			'faultSource': {'type': 'FeatureCollection', 'features': fault_features}}

	return HttpResponse(json.dumps(data), content_type="application/json")


######################
##     FRAGILITY    ##
######################

class FragilityForm(forms.ModelForm):
	add_tax_source = forms.BooleanField(required=False)
	tax_source_name = forms.CharField(required=False)
	tax_source_desc = forms.CharField(required=False)
	class Meta:
		model = Fragility_Model
		fields = ['name', 'description','limit_states', 'taxonomy_source', 'xml']
		widgets = {
			'limit_states': forms.TextInput(attrs={'placeholder': 'Ex: slight, moderate, extensive, complete...'}),
		}

class CovertToVulnarabilityForm(forms.ModelForm):
	class Meta:
		model = Vulnerability_Model
		fields = ['name', 'description', 'consequence_model']	
		

@login_required
def index_fragility(request):
	models = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	form = FragilityForm()
	form.fields["taxonomy_source"].queryset = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
	page = request.GET.get('page')

	return render(request, 'eng_models/index_fragility.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_fragility(request, model_id):
	model = get_object_or_404(Fragility_Model ,pk=model_id, fragility_model_contributor__contributor=request.user)
	tax_list = Taxonomy_Fragility_Model.objects.filter(model_id=model_id)
	convert_form = CovertToVulnarabilityForm()
	convert_form.fields["consequence_model"].queryset = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user).filter(limit_states__len=len(model.limit_states))
	return render(request, 'eng_models/detail_fragility.html', {'model': model, 'taxonomies': tax_list, 'form': convert_form})

@login_required
def add_fragility_model(request):
	if request.method == 'POST':
		form = FragilityForm(request.POST, request.FILES)
		form.fields["taxonomy_source"].queryset = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
		if form.is_valid():
			model = form.save(commit=False)
			if 'add_tax_source' in request.POST:
				new_tax_source = Building_Taxonomy_Source(name=request.POST['tax_source_name'],
															description=request.POST['tax_source_desc'],
															date_created=timezone.now())
				new_tax_source.save()
				Building_Taxonomy_Source_Contributor.objects.create(contributor=request.user, source=new_tax_source, date_joined=new_tax_source.date_created, author=True)
				model.taxonomy_source = new_tax_source
			model.date_created = timezone.now()
			if request.FILES:
				try:
					fragility_parser.start(model)
					model.save()
				except Exception as e:
					#model.delete()
					return render(request, 'eng_models/index_fragility.html', {'form': form, 'parse_error': e})
			else:
				model.save()
			Fragility_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			return redirect('detail_fragility', model_id=model.id)
		else:
			models = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_fragility.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = FragilityForm()
		return render(request, 'eng_models/index_fragility.html', {'form': form})


@login_required
def convert_to_vulnerability(request, model_id):
	if request.method == 'POST':
		fragility_model = get_object_or_404(Fragility_Model ,pk=model_id, fragility_model_contributor__contributor=request.user)
		form = CovertToVulnarabilityForm(request.POST)
		form.fields["consequence_model"].queryset = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user).filter(limit_states__len=len(fragility_model.limit_states))
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.type = 'structural_vulnerability'
			model.asset_category = 'buildings'
			model.loss_category = 'economic_loss'
			model.fragility_model = fragility_model
			model.taxonomy_source = fragility_model.taxonomy_source

			taxonomies_fragility = Taxonomy_Fragility_Model.objects.filter(model=fragility_model)
			#model.imt = taxonomies_fragility[0].imt
			#model.sa_period = taxonomies_fragility[0].sa_period
			
			for tax in taxonomies_fragility:
				functions = Fragility_Function.objects.filter(tax_frag=tax)
				model.iml = functions[0].cdf[0]
				model.save()

				ordered_functions = []
				for state in fragility_model.limit_states:
					for f in functions:
						if state == f.limit_state:
							ordered_functions.append(f)

				i = 0
				values = []
				cf = []
				for intensity in model.iml:
					sum = 0
					j = 0
					for c in model.consequence_model.values:
						if j <len(model.consequence_model.values)-1:
							sum += c*(ordered_functions[j].cdf[1][i] - ordered_functions[j+1].cdf[1][i])
						else:
							sum += c*(ordered_functions[j].cdf[1][i])
						j += 1
					values.append(sum)
					cf.append(0)
					i += 1

				vulnerability_function = Vulnerability_Function(model=model, taxonomy=tax.taxonomy,
																probabilistic_distribution='LN',
																loss_ratio=values, coefficients_variation=cf,
																imt=tax.imt, sa_period = tax.sa_period)
				vulnerability_function.save()

			Vulnerability_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)

			return redirect('detail_vulnerability', model_id=model.id)
		else:
			tax_list = Taxonomy_Fragility_Model.objects.filter(model_id=model_id)
			return render(request, 'eng_models/detail_fragility.html', {'model': fragility_model, 'taxonomies': tax_list, 'form': form})
	else:
		form = CovertToVulnarabilityForm()
		model = get_object_or_404(Fragility_Model ,pk=model_id, fragility_model_contributor__contributor=request.user)
		tax_list = Taxonomy_Fragility_Model.objects.filter(model_id=model_id)
		return render(request, 'eng_models/detail_fragility.html', {'model': model, 'taxonomies': tax_list, 'form': form})



@login_required
def fragility_get_taxonomy(request, model_id, taxonomy_id):
	model = get_object_or_404(Fragility_Model ,pk=model_id, fragility_model_contributor__contributor=request.user)

	info = Taxonomy_Fragility_Model.objects.raw('select * \
											from eng_models_taxonomy_fragility_model \
											where eng_models_taxonomy_fragility_model.taxonomy_id = %s \
											and eng_models_taxonomy_fragility_model.model_id = %s', [taxonomy_id, model_id])
	info_data = serializers.serialize("json", info)

	functions = Fragility_Function.objects.raw('select * \
											from eng_models_fragility_function, eng_models_taxonomy_fragility_model\
											where eng_models_taxonomy_fragility_model.taxonomy_id = %s \
											and eng_models_taxonomy_fragility_model.model_id = %s \
											and eng_models_taxonomy_fragility_model.id = eng_models_fragility_function.tax_frag_id', [taxonomy_id, model_id])
	
	functions_data = serializers.serialize("json", functions)
	
	return HttpResponse(json.dumps({'limit_states': model.limit_states, 'info': json.loads(info_data), 'functions': json.loads(functions_data)}), content_type="application/json")


########################
##     CONSEQUENCE    ##
########################

class ConsequenceForm(forms.ModelForm):
	class Meta:
		model = Consequence_Model
		fields = ['name', 'description']

class ConsequenceDetailForm(forms.ModelForm):
	class Meta:
		model = Consequence_Model
		fields = ['limit_states', 'values']
		widgets = {
			'limit_states': forms.HiddenInput(),
			'values': forms.HiddenInput(),
		}


@login_required
def index_consequence(request):
	models = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user).order_by('-date_created')
	form = ConsequenceForm()
	page = request.GET.get('page')
	return render(request, 'eng_models/index_consequence.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_consequence(request, model_id):
	model = get_object_or_404(Consequence_Model ,pk=model_id, consequence_model_contributor__contributor=request.user)
	form = ConsequenceDetailForm()
	return render(request, 'eng_models/detail_consequence.html', {'model': model, 'form': form})


@login_required
def save_consequence_model(request, model_id):
	if request.method == 'POST':
		model = get_object_or_404(Consequence_Model ,pk=model_id, consequence_model_contributor__contributor=request.user)
		form = ConsequenceDetailForm(request.POST, instance=model)
		if form.is_valid():
			form.save()
			return redirect('detail_consequence', model_id=model.id)
		else:
			model = get_object_or_404(Consequence_Model ,pk=model_id, consequence_model_contributor__contributor=request.user)
			return render(request, 'eng_models/detail_consequence.html', {'model': model, 'form': form, 'save_error': True})
	else:
		form = ConsequenceDetailForm()
		return render(request, 'eng_models/detail_consequence.html', {'form': form})	



@login_required
def consequence_ajax(request, model_id):
	model = get_object_or_404(Consequence_Model ,pk=model_id, consequence_model_contributor__contributor=request.user)
	return HttpResponse(json.dumps({'limit_states': model.limit_states, 'values': model.values}), content_type="application/json")


@login_required
def add_consequence_model(request):
	if request.method == 'POST':
		form = ConsequenceForm(request.POST)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			Consequence_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			return redirect('detail_consequence', model_id=model.id)
		else:
			models = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_consequence.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = ConsequenceForm()
		return render(request, 'eng_models/index_consequence.html', {'form': form})





##########################
##     VULNERABILITY    ##
##########################

class VulnerabilityForm(forms.ModelForm):
	add_tax_source = forms.BooleanField(required=False)
	tax_source_name = forms.CharField(required=False)
	tax_source_desc = forms.CharField(required=False)
	class Meta:
		model = Vulnerability_Model
		fields = ['name', 'description', 'type', 'iml', 'xml', 'taxonomy_source']

class VulnerabilityFunctionForm(forms.ModelForm):
	class Meta:
		model = Vulnerability_Function
		fields = ['taxonomy', 'probabilistic_distribution', 'loss_ratio', 'coefficients_variation', 'imt', 'sa_period']				

@login_required
def index_vulnerability(request):
	models = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).order_by('-date_created')
	form = VulnerabilityForm()
	form.fields["taxonomy_source"].queryset = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
	page = request.GET.get('page')

	return render(request, 'eng_models/index_vulnerability.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_vulnerability(request, model_id):
	model = get_object_or_404(Vulnerability_Model ,pk=model_id, vulnerability_model_contributor__contributor=request.user)
	tax_list = Vulnerability_Function.objects.filter(model=model)
	form = VulnerabilityFunctionForm()
	form.fields['taxonomy'].queryset = Building_Taxonomy.objects.filter(source = model.taxonomy_source).exclude(id__in = [e.taxonomy.id for e in tax_list])
	return render(request, 'eng_models/detail_vulnerability.html', {'model': model, 'taxonomies': tax_list, 'form': form})

@login_required
def add_vulnerability_model(request):
	if request.method == 'POST':
		form = VulnerabilityForm(request.POST, request.FILES)
		form.fields["taxonomy_source"].queryset = Building_Taxonomy_Source.objects.filter(building_taxonomy_source_contributor__contributor=request.user).order_by('-date_created')
		if form.is_valid():
			model = form.save(commit=False)
			if 'add_tax_source' in request.POST:
				new_tax_source = Building_Taxonomy_Source(name=request.POST['tax_source_name'],
															description=request.POST['tax_source_desc'],
															date_created=timezone.now())
				new_tax_source.save()
				Building_Taxonomy_Source_Contributor.objects.create(contributor=request.user, source=new_tax_source, date_joined=new_tax_source.date_created, author=True)
				model.taxonomy_source = new_tax_source
			model.date_created = timezone.now()
			if request.FILES:
				try:
					vulnerability_parser.start(model)
					model.save()
				except Exception as e:
					print e
					return render(request, 'eng_models/index_vulnerability.html', {'form': form, 'parse_error': e})
			else:
				if model.type == 'structural_vulnerability' or model.type == 'nonstructural_vulnerability':
					model.asset_category = 'buildings'
					model.loss_category = 'economic_loss'
				elif model.type == 'contents_vulnerability' or model.type == 'business_interruption_vulnerability':
					model.asset_category = 'contents'
					model.loss_category = 'economic_loss'
				elif model.type == 'occupants_vulnerability':
					model.asset_category = 'population'
					model.loss_category = 'fatalities'
				model.save()
			Vulnerability_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			return redirect('detail_vulnerability', model_id=model.id)
		else:
			models = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_vulnerability.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = VulnerabilityForm()
		return render(request, 'eng_models/index_vulnerability.html', {'form': form})



@login_required
def add_vulnerability_function(request, model_id):
	if request.method == 'POST':
		model = get_object_or_404(Vulnerability_Model ,pk=model_id, vulnerability_model_contributor__contributor=request.user)
		tax_list = Vulnerability_Function.objects.filter(model=model)
		form = VulnerabilityFunctionForm(request.POST)
		form.fields['taxonomy'].queryset = Building_Taxonomy.objects.filter(source = model.taxonomy_source).exclude(id__in = [e.taxonomy.id for e in tax_list])
		if form.is_valid():
			function = form.save(commit=False)
			function.model = model
			function.save()
			return redirect('detail_vulnerability', model_id=model.id)
		else:
			return render(request, 'eng_models/detail_vulnerability.html', {'model': model, 'taxonomies': tax_list, 'form': form})
	else:
		form = VulnerabilityFunctionForm()
		return render(request, 'eng_models/detail_vulnerability.html', {'form': form})



@login_required
def vulnerability_get_taxonomy(request, model_id, taxonomy_id):
	model = get_object_or_404(Vulnerability_Model ,pk=model_id, vulnerability_model_contributor__contributor=request.user)
	function = Vulnerability_Function.objects.get(model=model, taxonomy_id=taxonomy_id)
	error = []
	for loss, std_dev in zip(function.loss_ratio, function.coefficients_variation):
		error.append([loss-std_dev, loss+std_dev])
	return HttpResponse(json.dumps({'iml': model.iml, 'function': function.loss_ratio, 'error': error}), content_type="application/json")


@login_required
def get_imt_from_vulnerability(request, model_id):
	model = get_object_or_404(Vulnerability_Model ,pk=model_id, vulnerability_model_contributor__contributor=request.user)
	tax_list = Vulnerability_Function.objects.filter(model=model)

	imt_l = {}
	for tax in tax_list:
		imt = tax.imt
		if imt == 'SA':
			sa_period = tax.sa_period
			imt = 'SA('+str(sa_period)+')'
		imt_l[imt] = model.iml

	return HttpResponse(json.dumps(imt_l), content_type="application/json")


####################################
##     LOGIC TREE SOURCE MODELS   ##
####################################

class LogicTreeSMForm(forms.ModelForm):
	class Meta:
		model = Logic_Tree_SM
		fields = ['name', 'description', 'xml']


@login_required
def index_logic_tree_sm(request):
	models = Logic_Tree_SM.objects.filter(user=request.user).order_by('-date_created')
	form = LogicTreeSMForm()
	page = request.GET.get('page')

	return render(request, 'eng_models/index_logic_tree_sm.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_logic_tree_sm(request, model_id):
	model = get_object_or_404(Logic_Tree_SM ,pk=model_id, user=request.user)
	return render(request, 'eng_models/detail_logic_tree_sm.html', {'model': model})

@login_required
def add_logic_tree_sm(request):
	if request.method == 'POST':
		form = LogicTreeSMForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.user = request.user
			model.save()

			if request.FILES:
				try:
					sm_logic_tree_parser.start(model)
				except Exception as e:
					model.delete()
					return render(request, 'eng_models/index_logic_tree_sm.html', {'form': form, 'parse_error': e})
			return redirect('detail_logic_tree_sm', model_id=model.id)
		else:
			models = Logic_Tree_SM.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_logic_tree_sm.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = LogicTreeSMForm()
		return render(request, 'eng_models/index_logic_tree_sm.html', {'form': form})



###########################
##     LOGIC TREE GMPE   ##
###########################

class LogicTreeGMPEForm(forms.ModelForm):
	class Meta:
		model = Logic_Tree_GMPE
		fields = ['name', 'description', 'xml']


@login_required
def index_logic_tree_gmpe(request):
	models = Logic_Tree_GMPE.objects.filter(user=request.user).order_by('-date_created')
	form = LogicTreeGMPEForm()
	page = request.GET.get('page')

	return render(request, 'eng_models/index_logic_tree_gmpe.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_logic_tree_gmpe(request, model_id):
	model = get_object_or_404(Logic_Tree_GMPE ,pk=model_id, user=request.user)
	return render(request, 'eng_models/detail_logic_tree_gmpe.html', {'model': model})

@login_required
def add_logic_tree_gmpe(request):
	if request.method == 'POST':
		form = LogicTreeGMPEForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.user = request.user
			model.save()

			if request.FILES:
				try:
					gmpe_logic_tree_parser.start(model)
				except Exception as e:
					model.delete()
					return render(request, 'eng_models/index_logic_tree_gmpe.html', {'form': form, 'parse_error': e})
			return redirect('detail_logic_tree_gmpe', model_id=model.id)
		else:
			models = Logic_Tree_GMPE.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_logic_tree_gmpe.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = LogicTreeGMPEForm()
		return render(request, 'eng_models/index_logic_tree_gmpe.html', {'form': form})


@login_required
def logic_tree_gmpe_ajax(request, model_id):
	model = get_object_or_404(Logic_Tree_GMPE ,pk=model_id, user=request.user)

	if request.method == 'GET':

		regions = [{'name': region[0], 'gmpes': [possible_gmpe for possible_gmpe in get_possible_gmpes(region[0]) ]} for region in TECTONIC_CHOICES]

		levels = Logic_Tree_GMPE_Level.objects.filter(logic_tree=model).order_by('level')
		levels = json.loads(serializers.serialize("json", levels))

		for level in levels:

			branches = Logic_Tree_GMPE_Branch.objects.filter(level_id = level['pk'])
			branches = json.loads(serializers.serialize("json", branches))

			level['gmpes'] = branches

		return HttpResponse(json.dumps({'levels': levels, 'regions': regions}), content_type="application/json")

	if request.method == 'POST':

		data = json.loads(request.body)

		i=0
		new_level_ids = []
		for level in data:
			try:
				new_level = Logic_Tree_GMPE_Level.objects.get(logic_tree=model, level = i, tectonic_region=level['fields']['tectonic_region'])
			except MultipleObjectsReturned:
				Logic_Tree_GMPE_Level.objects.filter(logic_tree=model, level = i, tectonic_region=level['fields']['tectonic_region']).delete()
				new_level = Logic_Tree_GMPE_Level(logic_tree=model, tectonic_region=level['fields']['tectonic_region'], level = i)
				new_level.save()
			except ObjectDoesNotExist:
				new_level = Logic_Tree_GMPE_Level(logic_tree=model, tectonic_region=level['fields']['tectonic_region'], level = i)
				new_level.save()

			new_level_ids.append(new_level.id)

			for branch in level['gmpes']:
				try:
					new_branch = Logic_Tree_GMPE_Branch.objects.get(level=new_level, gmpe=branch['fields']['gmpe'])
					new_branch.weight = branch['fields']['weight']
				except MultipleObjectsReturned:
					Logic_Tree_GMPE_Branch.objects.filter(level=new_level, gmpe=branch['fields']['gmpe']).delete()
					new_branch = Logic_Tree_GMPE_Branch(level=new_level, gmpe=branch['fields']['gmpe'], weight=branch['fields']['weight'])
				except ObjectDoesNotExist:
					new_branch = Logic_Tree_GMPE_Branch(level=new_level, gmpe=branch['fields']['gmpe'], weight=branch['fields']['weight'])
			
				new_branch.save()
			i+=1

		levels_to_delete = Logic_Tree_GMPE_Level.objects.filter(logic_tree=model).exclude(id__in=new_level_ids)
		levels_to_delete.delete()


		return HttpResponse(json.dumps({'data':data, 'msg': 'Data saved'}), content_type="application/json")







#@login_required
#def download_logic_tree(request, model_id):
#	model = get_object_or_404(Logic_Tree ,pk=model_id, user=request.user)
#	response = HttpResponse(content_type='application/force-download')
#	response['Content-Disposition'] = 'attachment; filename=%s' % model.name+'.xml'
#	response['X-Sendfile'] = model.xml
	# It's usually a good idea to set the 'Content-Length' header too.
	# You can also set any other required headers: Cache-Control, etc.
#	return response


#def update_logic_tree(dict, parent_branch, branches):
#	for e in dict:
#		if e['pk'] == parent_branch:
#			e['children'] = branches
#			break
#		else:
#			update_logic_tree(e['children'], parent_branch, branches)

#@login_required
#def logic_tree_ajax(request, model_id):
#	tree = get_object_or_404(Logic_Tree ,pk=model_id, user=request.user)

#	json_tree = [{"name": "Logic tree root",
#				    "parent": "null",
#				    "pk": 0,
#				    "children": []}]

#	levels = Logic_Tree_Level.objects.filter(logic_tree = tree)
#	for level in levels:
#		branch_sets = Logic_Tree_Branch_Set.objects.filter(level=level)
#		for branch_set in branch_sets:
#			branches = Logic_Tree_Branch.objects.filter(branch_set=branch_set)
#			branches = json.loads(serializers.serialize("json", branches))

#			for branch in branches:
#				branch['type'] = branch_set.uncertainty_type
#				if branch['type']== 'gmpeModel':
#					branch['name'] = 'GMPE: '+branch['fields']['gmpe']+' weight:'+str(branch['fields']['weight'])
#				if branch['type']== 'sourceModel':
#					branch['name'] = 'Source Model: '+str(branch['fields']['source_model'])+' weight:'+str(branch['fields']['weight'])
#				if branch['type']== 'maxMagGRRelative':
#					branch['name'] = 'Max Mag Rel: '+str(branch['fields']['max_mag_inc'])+' weight:'+str(branch['fields']['weight'])
#				if branch['type']== 'bGRRelative':
#					branch['name'] = 'b Rel: '+str(branch['fields']['b_inc'])+' weight:'+str(branch['fields']['weight'])
#				if branch['type']== 'abGRAbsolute':
#					a = branch['fields']['a_b'].split(', ')[0].split('[')[1]
#					b = branch['fields']['a_b'].split(', ')[1].split(']')[0]
#					branch['name'] = 'a rel: '+a+' b rel: '+b+' weight:'+str(branch['fields']['weight'])
#				if branch['type']== 'maxMagGRAbsolute':
#					branch['name'] = 'Max Mag Abs: '+str(branch['fields']['max_mag'])+' weight:'+str(branch['fields']['weight'])
#				branch['children']=[]
#
#			if level.level == 1:
#				parent_branch = 0
#			else:
#				parent_branch = branch_set.origin.id

#			update_logic_tree(json_tree, parent_branch, branches)

#	source_models = Source_Model.objects.raw('select eng_models_source_model.id \
#					from eng_models_source_model, \
#					eng_models_logic_tree, eng_models_logic_tree_source_models \
#					where eng_models_source_model.id = eng_models_logic_tree_source_models.source_model_id \
#					and eng_models_logic_tree_source_models.logic_tree_id = eng_models_logic_tree.id \
#					and eng_models_logic_tree.id = %s', [tree.id])
	
#	sm=[]
#	for e in source_models:
#		data = get_sources(e.id)
#		sm.append(data)

#	return HttpResponse(json.dumps({'tree':json_tree, 'sources':sm}), content_type="application/json")








