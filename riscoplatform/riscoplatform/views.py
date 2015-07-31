from django.shortcuts import render, redirect
from world.models import *
from eng_models.models import *
from jobs.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
import json
from riscoplatform.local_settings import *
import requests
from operator import attrgetter
from django.contrib.auth import authenticate, login


def register(request):
	if request.method == 'POST':
		form = forms.UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(username=request.POST['username'],
									password=request.POST['password'])
			login(request, new_user)
			return redirect('welcome')
	else:
		form = forms.UserCreationForm()
	return render(request, "registration/register.html", {
		'form': form,
	})

@login_required
def welcome(request):
	return render(request, 'welcome.html')



def home(request):

	publications = []

	source_models = Source_Model.objects.filter(source_model_contributor__contributor=request.user)
	for model in source_models:
		publications.append(model)

	site_models = Site_Model.objects.filter(site_model_contributor__contributor=request.user)
	for model in site_models:
		publications.append(model)
	
	rupture_models = Rupture_Model.objects.filter(user=request.user)
	for model in rupture_models:
		publications.append(model)

	exposure_models = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user)
	for model in exposure_models:
		publications.append(model)

	fragility_models = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user)
	for model in fragility_models:
		publications.append(model)

	consequence_models = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user)
	for model in consequence_models:
		publications.append(model)

	vulnerability_models = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user)
	for model in vulnerability_models:
		publications.append(model)

	logic_tree_sm = Logic_Tree_SM.objects.filter(user=request.user)
	for model in logic_tree_sm:
		publications.append(model)

	logic_tree_gmpe = Logic_Tree_GMPE.objects.filter(user=request.user)
	for model in logic_tree_sm:
		publications.append(model)



	scenario_hazard = Scenario_Hazard.objects.filter(user=request.user)
	for job in scenario_hazard:
		publications.append(job)

	scenario_damage = Scenario_Damage.objects.filter(user=request.user)
	for job in scenario_damage:
		publications.append(job)

	scenario_risk = Scenario_Risk.objects.filter(user=request.user)
	for job in scenario_risk:
		publications.append(job)

	classical_psha_hazard = Classical_PSHA_Hazard.objects.filter(user=request.user)
	for job in classical_psha_hazard:
		publications.append(job)

	classical_psha_hazard = Classical_PSHA_Hazard.objects.filter(user=request.user)
	for job in classical_psha_hazard:
		publications.append(job)

	classical_psha_risk = Classical_PSHA_Risk.objects.filter(user=request.user)
	for job in classical_psha_risk:
		publications.append(job)

	event_based_hazard = Event_Based_Hazard.objects.filter(user=request.user)
	for job in event_based_hazard:
		publications.append(job)

	event_based_risk = Event_Based_Risk.objects.filter(user=request.user)
	for job in event_based_risk:
		publications.append(job)
	

	return render(request, 'home.html', {'publications': sorted(publications,  key=attrgetter('date_created'), reverse=True) })

#class UserUpdate(forms.UserChangeForm):
#	class Meta:
#		model = User
#		fields = ['username', 'first_name', 'last_name', 'email']
#	form = UserUpdate()

@login_required
def account(request):
	source_models = Source_Model.objects.filter(source_model_contributor__contributor=request.user).order_by('-date_created')
	site_models = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
	rupture_models = Rupture_Model.objects.filter(user=request.user).order_by('-date_created')
	exposure_models = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	fragility_models = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	consequence_models = Consequence_Model.objects.filter(consequence_model_contributor__contributor=request.user).order_by('-date_created')
	vulnerability_models = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).order_by('-date_created')
	logic_trees = Logic_Tree.objects.filter(user=request.user).order_by('-date_created')

	return render(request, 'account.html', {'source_models': source_models, 
											'site_models': site_models,
											'rupture_models': rupture_models, 
											'exposure_models': exposure_models,
											'fragility_models': fragility_models,
											'consequence_models': consequence_models,
											'vulnerability_models': vulnerability_models,
											'logic_trees': logic_trees})
	#models = Eng_Models.objects.filter(source_model__source_model_contributor__contributor=request.user)
	#return render(request, 'account.html', {'models': models})


@login_required
def account_settings(request):
	pass


def world_geojson(request, z, x, y):
	geometries = requests.get(TILESTACHE_HOST+'world/'+str(z)+'/'+str(x)+'/'+str(y)+'.json')
	geom_dict = json.loads(geometries.text)
	return HttpResponse(json.dumps(geom_dict), content_type="application/json")

def countries(request):
	cursor = connection.cursor()
	cursor.execute('select id, name from world_country order by name')
	return HttpResponse(json.dumps(cursor.fetchall()), content_type="application/json")

def level1(request):
	country = request.GET.get('country')
	cursor = connection.cursor()
	cursor.execute('select id, name from world_adm_1 where country_id = %s order by name', [country])
	return HttpResponse(json.dumps(cursor.fetchall()), content_type="application/json")

def level2(request):
	level1 = request.GET.get('level1')
	cursor = connection.cursor()
	cursor.execute('select distinct id_2, name_2 from world_world where id_1 = %s order by name_2', [level1])
	return HttpResponse(json.dumps(cursor.fetchall()), content_type="application/json")

def level3(request):
	level2 = request.GET.get('level2')
	cursor = connection.cursor()
	cursor.execute('select distinct id_3, name_3 from world_world where id_2 = %s order by name_3', [level2])
	return HttpResponse(json.dumps(cursor.fetchall()), content_type="application/json")