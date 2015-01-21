from django.shortcuts import render, get_object_or_404, redirect
from eng_models.models import Exposure_Model, Site_Model, Fault_Model
from jobs.models import Scenario_Hazard
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.db import connection
import json
from leaflet.forms.widgets import LeafletWidget

# Create your views here.

############################
##     SCENARIO HAZARD    ##
############################


class ScenarioHazardForm(forms.ModelForm):
	class Meta:
		model = Scenario_Hazard
		exclude = ['user', 'date_created', 'error', 'ready']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
           			'region': forms.HiddenInput(),
            		'location': forms.HiddenInput(),
            		'rupture_geom': forms.HiddenInput(),
            		'fault': forms.HiddenInput(),
					}
		

def index_scenario_hazard(request):
	jobs = Scenario_Hazard.objects.all()
	form = ScenarioHazardForm()
	return render(request, 'jobs/index_scenario_hazard.html', {'jobs': jobs, 'form': form})

def add_sceanrio_hazard(request):
	if request.method == 'POST':
		form = ScenarioHazardForm(request.POST, request.FILES)
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.save()
			if request.FILES:
				pass
				#create parser
			return redirect('index_scenario_hazard')
	else:
		form = ScenarioHazardForm()
		return render(request, 'jobs/index_scenario_hazard.html', {'form': form})




