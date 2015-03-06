from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from eng_models.models import Exposure_Model, Site_Model
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
	jobs = Scenario_Hazard.objects.all()
	form = ScenarioHazardForm()
	return render(request, 'jobs/index_scenario_hazard.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_hazard(request):
	if request.method == 'POST':
		form = ScenarioHazardForm(request.POST)
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			me = User.objects.get(id=1)
			job.user = me
			job.save()

			#queing to priseOQ
			conn = redis.Redis('priseOQ.fe.up.pt', 6379)
			q = Queue('risco', connection=conn)
			job = q.enqueue('start.start', job.id, 'scenario_hazard', DATABASE, timeout=3600)

			return redirect('index_scenario_hazard')
		else:
			print form.is_valid()
			print form.errors
	else:
		form = ScenarioHazardForm()
		return render(request, 'jobs/index_scenario_hazard.html', {'form': form})

@login_required
def results_scenario_hazard(request, job_id):
	job = get_object_or_404(Scenario_Hazard ,pk=job_id)
	return render(request, 'jobs/results_scenario_hazard.html', {'job': job})

@login_required
def results_scenario_hazard_ajax(request, job_id):
	job = Scenario_Hazard.objects.get(pk=job_id)

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

	return HttpResponse(json.dumps(d), content_type="application/json")




############################
##     SCENARIO DAMAGE    ##
############################


class ScenarioDamageForm(forms.ModelForm):
	class Meta:
		model = Scenario_Damage
		exclude = ['user', 'date_created', 'start', 'error', 'ready', 'oq_id']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
           			'region': forms.HiddenInput(),
					}

@login_required	
def index_scenario_damage(request):
	jobs = Scenario_Damage.objects.all()
	form = ScenarioDamageForm()
	return render(request, 'jobs/index_scenario_damage.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_damage(request):
	if request.method == 'POST':
		form = ScenarioDamageForm(request.POST, request.FILES)
		#print form
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			me = User.objects.get(id=1)
			job.user = me
			job.save()
			if request.FILES:
				pass
				#create parser

			#queing to priseOQ
			conn = redis.Redis('priseOQ.fe.up.pt', 6379)
			q = Queue('risco', connection=conn)
			job = q.enqueue('start.start', job.id, 'scenario_damage', DATABASE, timeout=3600)

			return redirect('index_scenario_damage')
		else:
			print form.is_valid()
			print form.errors
	else:
		form = ScenarioDamageForm()
		return render(request, 'jobs/index_scenario_damage.html', {'form': form})

@login_required
def results_scenario_damage(request, job_id):
	job = get_object_or_404(Scenario_Damage ,pk=job_id)
	return render(request, 'jobs/results_scenario_damage.html', {'job': job})

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



