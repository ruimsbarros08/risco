from django.shortcuts import render, get_object_or_404, redirect
from eng_models.models import Exposure_Model, Asset, Site_Model, Site, Rupture_Model, Fragility_Model, Fragility_Function, Building_Taxonomy_Source, Building_Taxonomy, Taxonomy_Fragility_Model, Source_Model, Source
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parsers import exposure_parser, fragility_parser
from django.core import serializers
from django.db import connection
import json


def pagination(list, n, page):
	paginator = Paginator(list, n)
	try:
		new_list = paginator.page(page)
	except PageNotAnInteger:
		new_list = paginator.page(1)
	except EmptyPage:
		new_list = paginator.page(paginator.num_pages)
	return new_list



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
	page = request.GET.get('page')
	return render(request, 'eng_models/detail_site.html', {'model': model, 'sites': pagination(site_list, 10, page)})

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
			#model = Site_Model(xml=request.FILES['xml'])
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			if request.FILES:
				pass
				#site_model_parser.start_parse(model)
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
				pass
				#create source parser
			return redirect('detail_source', model_id=model.id)
	else:
		form = SourceModelForm()
		return render(request, 'eng_models/index_source.html', {'form': form})


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






