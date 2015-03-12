from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from eng_models.models import *
from jobs.models import Scenario_Hazard, Scenario_Hazard_Results, Scenario_Damage, Scenario_Damage_Results
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

#from django.core import serializers
from django.contrib.auth.models import User
import redis
from rq import Queue
import json
import colors
import requests
import socket

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

#JOBS HOME

def home(request):
	return render(request, 'jobs/home.html')


############################
##     SCENARIO HAZARD    ##
############################


class ScenarioHazardForm(forms.ModelForm):
	class Meta:
		model = Scenario_Hazard
		exclude = ['user', 'date_created', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'sa_periods': forms.TextInput(attrs={'placeholder': 'Ex: 0.20, 0.5, 0.9, 1.3 ...'}),
           			'region': forms.HiddenInput(),
					}

@login_required	
def index_scenario_hazard(request):
	jobs = Scenario_Hazard.objects.filter(user=request.user).order_by('-date_created')
	form = ScenarioHazardForm()
	form.fields["site_model"].queryset = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["rupture_model"].queryset = Rupture_Model.objects.filter(user=request.user)
	return render(request, 'jobs/index_scenario_hazard.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_hazard(request):
	if request.method == 'POST':
		form = ScenarioHazardForm(request.POST)
		form.fields["site_model"].queryset = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
		form.fields["rupture_model"].queryset = Rupture_Model.objects.filter(user=request.user)
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()
			return redirect('results_scenario_hazard', job.id)
		else:
			jobs = Scenario_Hazard.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/index_scenario_hazard.html', {'jobs': jobs, 'form': form})
	else:
		form = ScenarioHazardForm()
		return render(request, 'jobs/index_scenario_hazard.html', {'form': form})

@login_required
def results_scenario_hazard(request, job_id):
	job = get_object_or_404(Scenario_Hazard ,pk=job_id, user=request.user)
	return render(request, 'jobs/results_scenario_hazard.html', {'job': job})

@login_required
def start_scenario_hazard(request, job_id):
	job = get_object_or_404(Scenario_Hazard ,pk=job_id, user=request.user)
	try:
		#queing to priseOQ
		#conn = redis.Redis('priseOQ.fe.up.pt', 6379)
		#q = Queue('risco', connection=conn)
		#job_queue = q.enqueue('start.start', job.id, 'scenario_hazard', DATABASE, timeout=3600)
		job.status = 'STARTED'
		job.save()
		return redirect('results_scenario_hazard', job.id)
	except:
		return redirect('results_scenario_hazard', job.id)
		

@login_required
def results_scenario_hazard_ajax(request, job_id):
	job = Scenario_Hazard.objects.get(pk=job_id, user=request.user)

	cursor = connection.cursor()
	d = []
    
	if job.pga:
	    cursor.execute("select ST_AsGeoJSON(cell), avg(gmvs), world_fishnet.id  \
						from world_fishnet, jobs_scenario_hazard_results \
						where jobs_scenario_hazard_results.job_id = %s \
						and jobs_scenario_hazard_results.cell_id = world_fishnet.id \
						and jobs_scenario_hazard_results.imt = 'PGA' \
						group by world_fishnet.id", [job_id])
	    cells = cursor.fetchall()
	    features = list(dict(type='Feature', id=cell[2], properties=dict(color=colors.hazard_picker(cell[1]), a="{0:.4f}".format(cell[1])),
					geometry=json.loads(cell[0])) for cell in cells)
	    d.append({'type': 'FeatureCollection', 'features': features, 'name': 'PGA'})

	for e in job.sa_periods:
		cursor.execute("select ST_AsGeoJSON(cell), avg(gmvs), world_fishnet.id  \
						from world_fishnet, jobs_scenario_hazard_results \
						where jobs_scenario_hazard_results.job_id = %s \
						and jobs_scenario_hazard_results.cell_id = world_fishnet.id \
						and jobs_scenario_hazard_results.sa_period = %s \
						group by world_fishnet.id", [job_id, e])
		cells = cursor.fetchall()
		features = list(dict(type='Feature', id=cell[2], properties=dict(color=colors.hazard_picker(cell[1]), a="{0:.4f}".format(cell[1])),
					geometry=json.loads(cell[0])) for cell in cells)
		d.append({'type': 'FeatureCollection', 'features': features, 'name': 'Sa('+str(e)+')'})

	source = Rupture_Model.objects.get(pk=job.rupture_model.id)
	if job.rupture_model.rupture_type == 'POINT':
		rupture = dict(type='Feature', id=source.id, properties=dict( name = source.name ),
					geometry = json.loads(source.location.json) )
	else:
		rupture = dict(type='Feature', id=source.id, properties=dict( name = source.name ),
					geometry = json.loads(source.rupture_geom.json) )
	data = {'type': 'FeatureCollection', 'features': [rupture] }

	return HttpResponse(json.dumps({'hazard':d, 'rupture': data}), content_type="application/json")




############################
##     SCENARIO DAMAGE    ##
############################


class ScenarioDamageForm(forms.ModelForm):
	class Meta:
		model = Scenario_Damage
		exclude = ['user', 'date_created', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
           			'region': forms.HiddenInput(),
					}

@login_required	
def index_scenario_damage(request):
	jobs = Scenario_Damage.objects.filter(user=request.user).order_by('-date_created')
	form = ScenarioDamageForm()
	form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user)
	form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	return render(request, 'jobs/index_scenario_damage.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_damage(request):
	if request.method == 'POST':
		form = ScenarioDamageForm(request.POST)
		form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user)
		form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
		form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()
			return redirect('results_scenario_damage', job.id)
		else:
			jobs = Scenario_Damage.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/index_scenario_damage.html', {'jobs': jobs, 'form': form})
	else:
		form = ScenarioDamageForm()
		return render(request, 'jobs/index_scenario_damage.html', {'form': form})

@login_required
def results_scenario_damage(request, job_id):
	job = get_object_or_404(Scenario_Damage ,pk=job_id)
	return render(request, 'jobs/results_scenario_damage.html', {'job': job})

@login_required
def start_scenario_damage(request, job_id):
	job = get_object_or_404(Scenario_Damage ,pk=job_id, user=request.user)
	try:
		#queing to priseOQ
		#conn = redis.Redis('priseOQ.fe.up.pt', 6379)
		#q = Queue('risco', connection=conn)
		#job_queue = q.enqueue('start.start', job.id, 'scenario_damage', DATABASE, timeout=3600)
		job.status = 'STARTED'
		job.save()
		return redirect('results_scenario_damage', job.id)
	except:
		return redirect('results_scenario_damage', job.id)

@login_required
def geojson_tiles(request, job_id, z, x, y):
	geometries = requests.get(TILESTACHE_HOST+'world/'+str(z)+'/'+str(x)+'/'+str(y)+'.json')
	geom_dict = json.loads(geometries.text)

	cursor = connection.cursor()

	for g in geom_dict["features"]:

		cursor.execute("select limit_state, sum(mean), sum(stddev), name_3 \
						from world_world, jobs_scenario_damage_results, eng_models_asset \
						where jobs_scenario_damage_results.asset_id = eng_models_asset.id \
						and jobs_scenario_damage_results.job_id = %s \
						and st_intersects(eng_models_asset.location, world_world.geom) \
						and world_world.id = %s \
						group by jobs_scenario_damage_results.limit_state, world_world.name_3", [job_id, g['id']])
		data = [dict(limit_state = e[0],
					mean = e[1],
					stddev = e[2],
					name = e[3]) for e in cursor.fetchall()]


		if data != []:
			g['properties']['limit_states'] = data

			for e in data:
				if e['limit_state'] == 'complete':
					color = colors.damage_picker(e['mean'], int(z))

			g['properties']['color'] = color


	geom_dict["features"] = [feature for feature in geom_dict["features"] if 'limit_states' in feature['properties']]
	return HttpResponse(json.dumps(geom_dict), content_type="application/json")



