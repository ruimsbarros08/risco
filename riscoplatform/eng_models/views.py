from django.shortcuts import render, get_object_or_404, redirect
from eng_models.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parsers import exposure_parser, fragility_parser, source_parser, site_model_parser, logic_tree_parser
from django.core import serializers
from django.db import connection
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



#####################
##     EXPOSURE    ##
#####################

class ExposureForm(forms.ModelForm):
	add_tax_source = forms.BooleanField(required=False)
	tax_source_name = forms.CharField(required=False)
	tax_source_desc = forms.CharField(required=False)
	class Meta:
		model = Exposure_Model
		fields = ['name', 'description', 'taxonomy_source', 'xml']

def index_exposure(request):
	models = Exposure_Model.objects.all()
	form = ExposureForm()
	return render(request, 'eng_models/index_exposure.html', {'models': models, 'form': form})

def detail_exposure(request, model_id):
	model = get_object_or_404(Exposure_Model ,pk=model_id)
	try:
		asset_list = Asset.objects.filter(model_id=model_id)
	except:
		asset_list = []
	page = request.GET.get('page')
	return render(request, 'eng_models/detail_exposure.html', {'model': model, 'assets': pagination(asset_list, 10, page)})

def add_exposure_model(request):
	if request.method == 'POST':
		form = ExposureForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			if 'add_tax_source' in request.POST:
				new_tax_source = Building_Taxonomy_Source(name=request.POST['tax_source_name'],
															description=request.POST['tax_source_desc'],
															date_created=timezone.now())
				new_tax_source.save()
				model.taxonomy_source = new_tax_source
			exposure_parser.start(model)
			return redirect('detail_exposure', model_id=model.id)
		else:
			print form.errors
	else:
		form = ExposureForm()
		return render(request, 'eng_models/index_exposure.html', {'form': form})

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


def index_site(request):
	models = Site_Model.objects.all()
	form = SiteForm()
	return render(request, 'eng_models/index_site.html', {'models': models, 'form': form})

def detail_site(request, model_id):
	model = get_object_or_404(Site_Model ,pk=model_id)
	try:
		site_list = Site.objects.filter(model_id=model_id)
	except:
		site_list = []
	#page = request.GET.get('page')
	return render(request, 'eng_models/detail_site.html', {'model': model, 'sites': site_list})

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


def add_site_model(request):
	if request.method == 'POST':
		form = SiteForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			if request.FILES:
				site_model_parser.start(model)
			return redirect('detail_site', model_id=model.id)
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
		

def index_source(request):
	models = Source_Model.objects.all()
	form = SourceModelForm()
	return render(request, 'eng_models/index_source.html', {'models': models, 'form': form})

def detail_source(request, model_id):
	model = get_object_or_404(Source_Model ,pk=model_id)
	try:
		sources = Source.objects.filter(model_id=model_id)
	except:
		sources = []
	page = request.GET.get('page')
	form = SourceForm()
	return render(request, 'eng_models/detail_source.html', {'model': model, 'form': form, 'sources': pagination(sources, 10, page)})


def add_source(request, model_id):
	if request.method == 'POST':
		form = SourceForm(request.POST)
		if form.is_valid():
			source = form.save(commit=False)
			source.model_id = model_id
			source.save()
			if request.FILES:
				pass
				#create  parser
			return redirect('detail_source', model_id=model_id)
		else:
			model = get_object_or_404(Source_Model ,pk=model_id)
			return render(request, 'eng_models/detail_source.html', {'model': model ,'form': form})
	else:
		form = SourceForm()
		return render(request, 'eng_models/detail_source.html', {'form': form})


def add_source_model(request):
	if request.method == 'POST':
		form = SourceModelForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			if request.FILES:
				source_parser.start(model)
			return redirect('detail_source', model_id=model.id)
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

def sources_ajax(request, model_id):
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

		
def index_rupture_model(request):
	models = Rupture_Model.objects.all()
	form = RuptureForm()
	return render(request, 'eng_models/index_rupture_model.html', {'models': models, 'form': form})

def add_rupture_model(request):
	if request.method == 'POST':
		form = RuptureForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			me = User.objects.get(id=1)
			model.user = me
			model.save()
			if request.FILES:
				pass
				#create parser

			return redirect('index_rupture_model')
		else:
			print form.is_valid()
			print form.errors
	else:
		form = RuptureForm()
		return render(request, 'eng_models/index_rupture_model.html', {'form': form})


def ruptures_ajax(request):
	point_sources = Rupture_Model.objects.filter(rupture_type='POINT')
	point_features = [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
				geometry = json.loads(source.location.json) ) for source in point_sources]


	fault_sources = Rupture_Model.objects.filter(rupture_type='FAULT')
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
		fields = ['name', 'description', 'taxonomy_source', 'xml']


def index_fragility(request):
	models = Fragility_Model.objects.all()
	form = FragilityForm()
	return render(request, 'eng_models/index_fragility.html', {'models': models, 'form': form})

def detail_fragility(request, model_id):
	model = get_object_or_404(Fragility_Model ,pk=model_id)
	try:
		tax_list = Taxonomy_Fragility_Model.objects.filter(model_id=model_id)
	except:
		tax_list = []
	return render(request, 'eng_models/detail_fragility.html', {'model': model, 'taxonomies': tax_list})

def add_fragility_model(request):
	if request.method == 'POST':
		form = FragilityForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			if 'add_tax_source' in request.POST:
				new_tax_source = Building_Taxonomy_Source(name=request.POST['tax_source_name'],
															description=request.POST['tax_source_desc'],
															date_created=timezone.now())
				new_tax_source.save()
				model.taxonomy_source = new_tax_source
			model.date_created = timezone.now()
			fragility_parser.start(model)
			return redirect('detail_fragility', model_id=model.id)
	else:
		form = FragilityForm()
		return render(request, 'eng_models/index_fragility.html', {'form': form})


def fragility_get_taxonomy(request, model_id, taxonomy_id):

	functions = Fragility_Function.objects.raw('select * \
											from eng_models_fragility_function, eng_models_taxonomy_fragility_model \
											where eng_models_taxonomy_fragility_model.taxonomy_id = %s \
											and eng_models_taxonomy_fragility_model.model_id = %s \
											and eng_models_taxonomy_fragility_model.id = eng_models_fragility_function.tax_frag_id', [taxonomy_id, model_id])
	data = serializers.serialize("json", functions)
	return HttpResponse(data, content_type="application/json")




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


def index_logic_tree(request):
	models = Logic_Tree.objects.all().order_by('-date_created')
	form = LogicTreeForm()
	return render(request, 'eng_models/index_logic_tree.html', {'models': models, 'form': form})

def detail_logic_tree(request, model_id):
	model = get_object_or_404(Logic_Tree ,pk=model_id)
	return render(request, 'eng_models/detail_logic_tree.html', {'model': model})

def add_logic_tree(request):
	if request.method == 'POST':
		form = LogicTreeForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			me = User.objects.get(id=1)
			model.user = me
			model.save()
			if 'source_models' in request.POST:
				for e in request.POST['source_models']:
					model.source_models.add(e)
					model.save()
			logic_tree_parser.start(model)
			return redirect('detail_logic_tree', model_id=model.id)

	else:
		form = LogicTreeForm()
		return render(request, 'eng_models/index_logic_tree.html', {'form': form})

def download_logic_tree(request, model_id):
	model = get_object_or_404(Logic_Tree ,pk=model_id)
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

def logic_tree_ajax(request, model_id):
	json_tree = [{"name": "Logic tree root",
				    "parent": "null",
				    "pk": 0,
				    "children": []}]

	levels = Logic_Tree_Level.objects.filter(logic_tree_id = model_id)
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
					and eng_models_logic_tree.id = %s', [model_id])
	
	sm=[]
	for e in source_models:
		data = get_sources(e.id)
		sm.append(data)

	return HttpResponse(json.dumps({'tree':json_tree, 'sources':sm}), content_type="application/json")








