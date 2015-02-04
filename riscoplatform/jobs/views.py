from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

from eng_models.models import Exposure_Model, Site_Model, Fault_Model
from jobs.models import Scenario_Hazard, Scenario_Hazard_Results, Scenario_Damage
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



