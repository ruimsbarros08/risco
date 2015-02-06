from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

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


# Create your views here.

############################
##     SCENARIO HAZARD    ##
############################


class ScenarioHazardForm(forms.ModelForm):
	class Meta:
		model = Scenario_Hazard
		exclude = ['user', 'date_created', 'start', 'error', 'ready', 'oq_id']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
           			'region': forms.HiddenInput(),
					}

		
def index_scenario_hazard(request):
	jobs = Scenario_Hazard.objects.all()
	form = ScenarioHazardForm()
	return render(request, 'jobs/index_scenario_hazard.html', {'jobs': jobs, 'form': form})

def add_scenario_hazard(request):
	if request.method == 'POST':
		form = ScenarioHazardForm(request.POST, request.FILES)
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
			q = Queue(connection=conn)
			job = q.enqueue('start.start', job.id, 'scenario_hazard', timeout=3600)

			return redirect('index_scenario_hazard')
		else:
			print form.is_valid()
			print form.errors
	else:
		form = ScenarioHazardForm()
		return render(request, 'jobs/index_scenario_hazard.html', {'form': form})


def results_scenario_hazard(request, job_id):
	job = get_object_or_404(Scenario_Hazard ,pk=job_id)
	return render(request, 'jobs/results_scenario_hazard.html', {'job': job})

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

		
def index_scenario_damage(request):
	jobs = Scenario_Damage.objects.all()
	form = ScenarioDamageForm()
	return render(request, 'jobs/index_scenario_damage.html', {'jobs': jobs, 'form': form})

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
			q = Queue(connection=conn)
			job = q.enqueue('start.start', job.id, 'scenario_damage', timeout=3600)

			return redirect('index_scenario_damage')
		else:
			print form.is_valid()
			print form.errors
	else:
		form = ScenarioDamageForm()
		return render(request, 'jobs/index_scenario_damage.html', {'form': form})

def results_scenario_damage(request, job_id):
	job = get_object_or_404(Scenario_Damage ,pk=job_id)
	return render(request, 'jobs/results_scenario_damage.html', {'job': job})


def geojson_tiles(request, job_id, z, x, y):
	geometries = requests.get('http://localhost:8080/portugal/'+str(z)+'/'+str(x)+'/'+str(y)+'.json')
	geom_dict = json.loads(geometries.text)

	cursor = connection.cursor()

	for g in geom_dict["features"]:

		cursor.execute("select sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev), \
			jobs_scenario_damage_results.limit_state \
			from jobs_scenario_damage_results, eng_models_asset, world_world \
			where jobs_scenario_damage_results.id = %s \
			and jobs_scenario_damage_results.asset_id = eng_models_asset.id \
			and st_intersects(eng_models_asset.location, world_world.geom) \
			and world_world.id = %s \
			group by jobs_scenario_damage_results.limit_state;", [job_id, g['id']])
		data = [dict(mean = e[0],
					stddev = e[1],
					limit_state = e[2]) for e in cursor.fetchall()]

		if data != []:
			g['properties']['limit_states'] = data
			#color = colors.damage_picker(m, int(z))
			g['properties']['color'] = '#FF0000'
		else:
			pass

	#geom_dict["features"] = [feature for feature in geom_dict["features"] if feature['properties']['limit_states'] != []]
	return HttpResponse(json.dumps(geom_dict), content_type="application/json")




