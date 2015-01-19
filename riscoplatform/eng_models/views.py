from django.shortcuts import render, get_object_or_404, redirect
from eng_models.models import Exposure_Model, Asset, Site_Model, Site, Fault_Model, Fault
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import exposure_model_parser
#import site_model_parser
from django.core import serializers
from django.db import connection
import json
from leaflet.forms.widgets import LeafletWidget


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
	class Meta:
		model = Exposure_Model
		fields = ['name', 'description', 'xml']

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
			model.date_created = timezone.now()
			model.save()
			if request.FILES:
				pass
				#exposure_model_parser.start_parse(model)
			return redirect('detail_exposure', model_id=model.id)
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
##     HAZARD    ##
###################


class FaultModelForm(forms.ModelForm):
	class Meta:
		model = Fault_Model
		fields = ['name', 'description', 'xml']

class FaultForm(forms.ModelForm):
	class Meta:
		model = Fault
		fields = ['name', 'mindepth', 'maxdepth', 'strike', 'dip', 'rake', 'sr', 'maxmag', 'geom']
		widgets = {'geom': LeafletWidget()}
		

def index_hazard(request):
	fault_models = Fault_Model.objects.all()
	form = FaultModelForm()
	return render(request, 'eng_models/index_hazard.html', {'fault_models': fault_models, 'form': form})

def detail_faults(request, model_id):
	model = get_object_or_404(Fault_Model ,pk=model_id)
	try:
		fault_list = Fault.objects.filter(model_id=model_id)
	except:
		fault_list = []
	page = request.GET.get('page')
	form = FaultForm()
	return render(request, 'eng_models/detail_faults.html', {'model': model, 'form': form, 'faults': pagination(fault_list, 10, page)})


def add_fault(request):
	if request.method == 'POST':
		form = FaultForm(request.POST, request.FILES)
		if form.is_valid():
			fault = form.save(commit=False)
			fault.save()
			if request.FILES:
				pass
				#create  parser
			return redirect('detail_faults', model_id=model.id)
	else:
		form = FaultForm()
		return render(request, 'eng_models/detail_faults.html', {'form': form})

def add_fault_model(request):
	if request.method == 'POST':
		form = FaultModelForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save(commit=False)
			model.date_created = timezone.now()
			model.save()
			if request.FILES:
				pass
				#create fault source parser
			return redirect('detail_faults', model_id=model.id)
	else:
		form = FaultModelForm()
		return render(request, 'eng_models/index_hazard.html', {'form': form})




