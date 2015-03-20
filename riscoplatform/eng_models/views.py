from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from eng_models.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parsers import exposure_parser, fragility_parser, source_parser, site_model_parser, logic_tree_parser
from django.core import serializers
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.db import connection
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

class ExposureForm(forms.ModelForm):
	add_tax_source = forms.BooleanField(required=False)
	tax_source_name = forms.CharField(required=False)
	tax_source_desc = forms.CharField(required=False)
	class Meta:
		model = Exposure_Model
		fields = ['name', 'description', 'taxonomy_source', 'area_type', 'area_unit', 'aggregation', 'currency', 'deductible', 'insurance_limit', 'xml']

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
	page = request.GET.get('page')
	return render(request, 'eng_models/index_exposure.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_exposure(request, model_id):
	model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
	form = AssetForm()
	form.fields["taxonomy"].queryset = Building_Taxonomy.objects.filter(source=model.taxonomy_source)
	return render(request, 'eng_models/detail_exposure.html', {'model': model, 'form': form})


@login_required
def ajax_assets(request, model_id):
	model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
	try:
		page = int(request.GET.get('page'))
	except:
		page = 1
	asset_list = Asset.objects.filter(model=model)[page:page+49]
	json_list = serializers.serialize("json", asset_list)
	return HttpResponse(json_list, content_type="application/json")


@login_required
def ajax_heat_assets(request, model_id):
	model = get_object_or_404(Exposure_Model ,pk=model_id, exposure_model_contributor__contributor=request.user)
	
	cursor = connection.cursor()
	cursor.execute('select st_y(location), st_x(location), id from eng_models_asset where model_id = %s', [model.id])
	return HttpResponse(json.dumps(cursor.fetchall()), content_type="application/json")


@login_required
def add_exposure_model(request):
	if request.method == 'POST':
		form = ExposureForm(request.POST, request.FILES)
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
			if request.FILES:
				try:
					exposure_parser.start(model)
				except:
					model.delete()
					return render(request, 'eng_models/index_exposure.html', {'form': form, 'parse_error': True})
			Exposure_Model_Contributor.objects.create(contributor=request.user, model=model, date_joined=model.date_created, author=True)
			return redirect('detail_exposure', model_id=model.id)
		else:
			models = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_exposure.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = ExposureForm()
		return render(request, 'eng_models/index_exposure.html', {'form': form})


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


@login_required
def exposure_geojson_tiles(request, model_id, z, x, y):
	geometries = requests.get(TILESTACHE_HOST+'world/'+str(z)+'/'+str(x)+'/'+str(y)+'.json')
	geom_dict = json.loads(geometries.text)

	cursor = connection.cursor()

	for g in geom_dict["features"]:

		cursor.execute("select count(*) \
			from eng_models_exposure_model, eng_models_asset, world_world \
			where eng_models_exposure_model.id = %s \
			and eng_models_exposure_model.id = eng_models_asset.model_id \
			and st_intersects(eng_models_asset.location, world_world.geom) \
			and world_world.id = %s ", [model_id, g['id']])

		try:
			g['properties']['n_assets'] = cursor.fetchone()[0]
			#color = colors.damage_picker(m, int(z))
			#g['properties']['color'] = '#FF0000'
		except:
			pass

	#geom_dict["features"] = [feature for feature in geom_dict["features"] if feature['properties']['limit_states'] != []]
	return HttpResponse(json.dumps(geom_dict), content_type="application/json")


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

    cells = cursor.fetchall()
    features = [dict(type='Feature', id=cell[4], properties=dict(color='#FF0000', vs30="{0:.4f}".format(cell[1]),
																z1pt0="{0:.4f}".format(cell[2]),
																z2pt5="{0:.4f}".format(cell[3])),
				geometry=json.loads(cell[0])) for cell in cells]
    return HttpResponse(json.dumps({'type': 'FeatureCollection', 'features': features}), content_type="application/json")

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
				except:
					model.delete()
					return render(request, 'eng_models/index_site.html', {'form': form, 'parse_error': True})
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

class SourceForm(forms.ModelForm):
	class Meta:
		model = Source
		fields = ['name', 'tectonic_region', 'mag_scale_rel', 'rupt_aspect_ratio', 'mag_freq_dist_type', 'a', 'b', 'min_mag', 'max_mag', 'bin_width', 'occur_rates', 'source_type', 'upper_depth', 'lower_depth', 'nodal_plane_dist', 'hypo_depth_dist', 'dip', 'rake', 'point', 'area', 'fault']
		widgets = {
            		'point': forms.HiddenInput(),
            		'area': forms.HiddenInput(),
            		'fault': forms.HiddenInput(),
            		#'nodal_plane_dist': forms.HiddenInput(),
            		#'hypo_depth_dist': forms.HiddenInput(),
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
	page = request.GET.get('page')
	form = SourceForm()
	return render(request, 'eng_models/detail_source.html', {'model': model, 'form': form, 'sources': pagination(sources, 10, page)})

@login_required
def add_source(request, model_id):
	if request.method == 'POST':
		form = SourceForm(request.POST)
		if form.is_valid():
			source = form.save(commit=False)
			source.model_id = model_id
			source.save()
			return redirect('detail_source', model_id=model_id)
		else:
			model = get_object_or_404(Source_Model ,pk=model_id)
			return render(request, 'eng_models/detail_source.html', {'model': model ,'form': form})
	else:
		form = SourceForm()
		return render(request, 'eng_models/detail_source.html', {'form': form})

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
				except:
					model.delete()
					return render(request, 'eng_models/index_source.html', {'form': form, 'parse_error': True})
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
	point_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
				geometry = json.loads(source.point.json) ) for source in point_sources]

	area_sources = Source.objects.filter(model_id=model_id, source_type='AREA')
	area_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
				geometry = json.loads(source.area.json) ) for source in area_sources]

	fault_sources = Source.objects.filter(model_id=model_id, source_type='SIMPLE_FAULT')
	fault_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
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
		fields = ['name', 'description', 'consequnce_model']	
		

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
def fragility_get_taxonomy(request, model_id, taxonomy_id):

	info = Taxonomy_Fragility_Model.objects.raw('select * \
											from eng_models_taxonomy_fragility_model \
											where eng_models_taxonomy_fragility_model.taxonomy_id = %s \
											and eng_models_taxonomy_fragility_model.model_id = %s', [taxonomy_id, model_id])
	info_data = serializers.serialize("json", info)

	functions = Fragility_Function.objects.raw('select * \
											from eng_models_fragility_function, eng_models_taxonomy_fragility_model \
											where eng_models_taxonomy_fragility_model.taxonomy_id = %s \
											and eng_models_taxonomy_fragility_model.model_id = %s \
											and eng_models_taxonomy_fragility_model.id = eng_models_fragility_function.tax_frag_id', [taxonomy_id, model_id])
	functions_data = serializers.serialize("json", functions)
	
	return HttpResponse(json.dumps({'info': json.loads(info_data), 'functions': json.loads(functions_data)}), content_type="application/json")


########################
##     CONSEQUENCE    ##
########################

class ConsequenceForm(forms.ModelForm):
	class Meta:
		model = Consequence_Model
		fields = ['name', 'description']


@login_required
def index_consequence(request):
	models = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user).order_by('-date_created')
	form = ConsequenceForm()
	page = request.GET.get('page')
	return render(request, 'eng_models/index_consequence.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_consequence(request, model_id):
	model = get_object_or_404(Consequence_Model ,pk=model_id, consequence_model_contributor__contributor=request.user)
	return render(request, 'eng_models/detail_consequence.html', {'model': model})

@login_required
def consequence_ajax(request, model_id):
	#model = get_object_or_404(Consequence_Model ,pk=model_id, consequence_model_contributor__contributor=request.user)
	model = Consequence_Model.objects.filter(pk=model_id, consequence_model_contributor__contributor=request.user)
	data = serializers.serialize("json", model)
	data = json.loads(data)
	data = data[0]['fields']
	return HttpResponse(json.dumps(data), content_type="application/json")


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


#######################
##     LOGIC TREE    ##
#######################

class LogicTreeForm(forms.ModelForm):
	class Meta:
		model = Logic_Tree
		exclude = ['user', 'date_created']
		widgets = {
			'source_models': forms.CheckboxSelectMultiple()
		}

@login_required
def index_logic_tree(request):
	models = Logic_Tree.objects.filter(user=request.user).order_by('-date_created')
	form = LogicTreeForm()
	form.fields["source_models"].queryset = Source_Model.objects.filter(source_model_contributor__contributor=request.user)
	page = request.GET.get('page')

	return render(request, 'eng_models/index_logic_tree.html', {'models': pagination(models, 10, page), 'form': form})

@login_required
def detail_logic_tree(request, model_id):
	model = get_object_or_404(Logic_Tree ,pk=model_id, user=request.user)
	return render(request, 'eng_models/detail_logic_tree.html', {'model': model})

@login_required
def add_logic_tree(request):
	if request.method == 'POST':
		form = LogicTreeForm(request.POST, request.FILES)
		form.fields["source_models"].queryset = Source_Model.objects.filter(source_model_contributor__contributor=request.user)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.user = request.user
			model.save()
			if 'source_models' in request.POST:
				for e in request.POST['source_models']:
					model.source_models.add(e)
					model.save()
			if request.FILES:
				try:
					logic_tree_parser.start(model)
				except:
					model.delete()
					return render(request, 'eng_models/index_logic_tree.html', {'form': form, 'parse_error': True})
			return redirect('detail_logic_tree', model_id=model.id)
		else:
			models = Logic_Tree.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'eng_models/index_logic_tree.html', {'models': pagination(models, 10, 1), 'form': form})
	else:
		form = LogicTreeForm()
		form.fields["source_models"].queryset = Source_Model.objects.filter(source_model_contributor__contributor=request.user)
		return render(request, 'eng_models/index_logic_tree.html', {'form': form})

@login_required
def download_logic_tree(request, model_id):
	model = get_object_or_404(Logic_Tree ,pk=model_id, user=request.user)
	response = HttpResponse(content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename=%s' % model.name+'.xml'
	response['X-Sendfile'] = model.xml
	# It's usually a good idea to set the 'Content-Length' header too.
	# You can also set any other required headers: Cache-Control, etc.
	return response


def update_logic_tree(dict, parent_branch, branches):
	for e in dict:
		if e['pk'] == parent_branch:
			e['children'] = branches
			break
		else:
			update_logic_tree(e['children'], parent_branch, branches)

@login_required
def logic_tree_ajax(request, model_id):
	tree = get_object_or_404(Logic_Tree ,pk=model_id, user=request.user)

	json_tree = [{"name": "Logic tree root",
				    "parent": "null",
				    "pk": 0,
				    "children": []}]

	levels = Logic_Tree_Level.objects.filter(logic_tree = tree)
	for level in levels:
		branch_sets = Logic_Tree_Branch_Set.objects.filter(level=level)
		for branch_set in branch_sets:
			branches = Logic_Tree_Branch.objects.filter(branch_set=branch_set)
			branches = json.loads(serializers.serialize("json", branches))

			for branch in branches:
				branch['type'] = branch_set.uncertainty_type
				if branch['type']== 'gmpeModel':
					branch['name'] = 'GMPE: '+branch['fields']['gmpe']+' weight:'+str(branch['fields']['weight'])
				if branch['type']== 'sourceModel':
					branch['name'] = 'Source Model: '+str(branch['fields']['source_model'])+' weight:'+str(branch['fields']['weight'])
				if branch['type']== 'maxMagGRRelative':
					branch['name'] = 'Max Mag Rel: '+str(branch['fields']['max_mag_inc'])+' weight:'+str(branch['fields']['weight'])
				if branch['type']== 'bGRRelative':
					branch['name'] = 'b Rel: '+str(branch['fields']['b_inc'])+' weight:'+str(branch['fields']['weight'])
				if branch['type']== 'abGRAbsolute':
					a = branch['fields']['a_b'].split(', ')[0].split('[')[1]
					b = branch['fields']['a_b'].split(', ')[1].split(']')[0]
					branch['name'] = 'a rel: '+a+' b rel: '+b+' weight:'+str(branch['fields']['weight'])
				if branch['type']== 'maxMagGRAbsolute':
					branch['name'] = 'Max Mag Abs: '+str(branch['fields']['max_mag'])+' weight:'+str(branch['fields']['weight'])
				branch['children']=[]

			if level.level == 1:
				parent_branch = 0
			else:
				parent_branch = branch_set.origin.id

			update_logic_tree(json_tree, parent_branch, branches)

	source_models = Source_Model.objects.raw('select eng_models_source_model.id \
					from eng_models_source_model, \
					eng_models_logic_tree, eng_models_logic_tree_source_models \
					where eng_models_source_model.id = eng_models_logic_tree_source_models.source_model_id \
					and eng_models_logic_tree_source_models.logic_tree_id = eng_models_logic_tree.id \
					and eng_models_logic_tree.id = %s', [tree.id])
	
	sm=[]
	for e in source_models:
		data = get_sources(e.id)
		sm.append(data)

	return HttpResponse(json.dumps({'tree':json_tree, 'sources':sm}), content_type="application/json")








