from django.shortcuts import render
from world.models import *
from eng_models.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required

import json


def home(request):
	return render(request, 'home.html')

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
	logic_trees = Logic_Tree.objects.filter(user=request.user).order_by('-date_created')

	return render(request, 'account.html', {'source_models': source_models, 
											'site_models': site_models,
											'rupture_models': rupture_models, 
											'exposure_models': exposure_models,
											'fragility_models': fragility_models,
											'logic_trees': logic_trees})
	#models = Eng_Models.objects.filter(source_model__source_model_contributor__contributor=request.user)
	#return render(request, 'account.html', {'models': models})


@login_required
def account_settings(request):
	pass



def countries(request):
	cursor = connection.cursor()
	cursor.execute('select distinct id_0, name_0 from world_world order by name_0')
	return HttpResponse(json.dumps(cursor.fetchall()), content_type="application/json")

def level1(request):
	country = request.GET.get('country')
	cursor = connection.cursor()
	cursor.execute('select distinct id_1, name_1 from world_world where id_0 = %s order by name_1', [country])
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