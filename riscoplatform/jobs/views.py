from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

from eng_models.models import Exposure_Model, Site_Model, Fault_Model
from jobs.models import Scenario_Hazard, Scenario_Hazard_Results
#from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

#from django.core import serializers
#from django.db import connection
#import json
#from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth.models import User
import redis
from rq import Queue
import json


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
            		#'location': forms.HiddenInput(),
            		#'rupture_geom': forms.HiddenInput(),
            		'fault': forms.HiddenInput(),
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
			job = q.enqueue('scenario_hazard.start', job.id, timeout=3600)

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
	    features = list(dict(type='Feature', id=cell[2], properties=dict(color='#FF0000', pga="{0:.4f}".format(cell[1])),
					geometry=json.loads(cell[0])) for cell in cells)
	    d.append({'type': 'FeatureCollection', 'features': features})

	if job.sa1_period != None:
		cursor.execute("select ST_AsGeoJSON(cell), avg(gmvs), world_fishnet.id  \
						from world_fishnet, jobs_scenario_hazard_results \
						where jobs_scenario_hazard_results.job_id = %s \
						and jobs_scenario_hazard_results.cell_id = world_fishnet.id \
						and jobs_scenario_hazard_results.sa_period = %s \
						group by world_fishnet.id", [job_id, job.sa1_period])
		cells = cursor.fetchall()
		features = list(dict(type='Feature', id=cell[2], properties=dict(color='#FF0000', sa="{0:.4f}".format(cell[1]), period=job.sa1_period),
					geometry=json.loads(cell[0])) for cell in cells)
		d.append({'type': 'FeatureCollection', 'features': features})

		if job.sa2_period != None:
			cursor.execute("select ST_AsGeoJSON(cell), avg(gmvs), world_fishnet.id  \
							from world_fishnet, jobs_scenario_hazard_results \
							where jobs_scenario_hazard_results.job_id = %s \
							and jobs_scenario_hazard_results.cell_id = world_fishnet.id \
							and jobs_scenario_hazard_results.sa_period = %s \
							group by world_fishnet.id", [job_id, job.sa2_period])
			cells = cursor.fetchall()
			features = list(dict(type='Feature', id=cell[2], properties=dict(color='#FF0000', sa="{0:.4f}".format(cell[1]), period=job.sa2_period),
						geometry=json.loads(cell[0])) for cell in cells)
			d.append({'type': 'FeatureCollection', 'features': features})

			if job.sa3_period != None:
				cursor.execute("select ST_AsGeoJSON(cell), avg(gmvs), world_fishnet.id  \
								from world_fishnet, jobs_scenario_hazard_results \
								where jobs_scenario_hazard_results.job_id = %s \
								and jobs_scenario_hazard_results.cell_id = world_fishnet.id \
								and jobs_scenario_hazard_results.sa_period = %s \
								group by world_fishnet.id", [job_id, job.sa3_period])
				cells = cursor.fetchall()
				features = list(dict(type='Feature', id=cell[2], properties=dict(color='#FF0000', sa="{0:.4f}".format(cell[1]), period=job.sa3_period),
							geometry=json.loads(cell[0])) for cell in cells)
				d.append({'type': 'FeatureCollection', 'features': features})

	return HttpResponse(json.dumps(d), content_type="application/json")




