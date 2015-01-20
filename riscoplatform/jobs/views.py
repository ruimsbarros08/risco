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


#class FaultModelForm(forms.ModelForm):
#	class Meta:
#		model = Fault_Model
#		fields = ['name', 'description', 'xml']

class ScenarioHazardForm(forms.ModelForm):
	class Meta:
		model = Scenario_Hazard
		#fields = ['geom', 'name', 'mindepth', 'maxdepth', 'strike', 'dip', 'rake', 'sr', 'maxmag']
		#widgets = {
        #   		'name': forms.TextInput(attrs={'class': 'form-control'}),
        #    		'mindepth': forms.TextInput(attrs={'class': 'form-control'}),
        #    		'maxdepth': forms.TextInput(attrs={'class': 'form-control'}),
        #   			'strike': forms.TextInput(attrs={'class': 'form-control'}),
        #    		'dip': forms.TextInput(attrs={'class': 'form-control'}),
        #    		'rake': forms.TextInput(attrs={'class': 'form-control'}),
        #    		'sr': forms.TextInput(attrs={'class': 'form-control'}),
        #    		'maxmag': forms.TextInput(attrs={'class': 'form-control'}),
		#			'geom': LeafletWidget()
		#			}
		

def index_scenario_hazard(request):
	jobs = Scenario_Hazard.objects.all()
	form = ScenarioHazardForm()
	return render(request, 'eng_models/index_scenario_hazard.html', {'jobs': jobs, 'form': form})




