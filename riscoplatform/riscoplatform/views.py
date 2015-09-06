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
from django.db.models import Q
from django.contrib.auth.forms import UserChangeForm
from django import forms


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
	if request.user.is_authenticated():

		publications = []

		source_models = Source_Model.objects.filter(private=False)
		for model in source_models:
			publications.append(model)

		site_models = Site_Model.objects.filter(private=False)
		for model in site_models:
			publications.append(model)
		
		rupture_models = Rupture_Model.objects.filter(private=False)
		for model in rupture_models:
			publications.append(model)

		exposure_models = Exposure_Model.objects.filter(private=False)
		for model in exposure_models:
			publications.append(model)

		fragility_models = Fragility_Model.objects.filter(private=False)
		for model in fragility_models:
			publications.append(model)

		consequence_models = Consequence_Model.objects.filter(private=False)
		for model in consequence_models:
			publications.append(model)

		vulnerability_models = Vulnerability_Model.objects.filter(private=False)
		for model in vulnerability_models:
			publications.append(model)

		logic_tree_sm = Logic_Tree_SM.objects.filter(private=False)
		for model in logic_tree_sm:
			publications.append(model)

		logic_tree_gmpe = Logic_Tree_GMPE.objects.filter(private=False)
		for model in logic_tree_sm:
			publications.append(model)



		scenario_hazard = Scenario_Hazard.objects.filter(private=False)
		for job in scenario_hazard:
			publications.append(job)

		scenario_damage = Scenario_Damage.objects.filter(private=False)
		for job in scenario_damage:
			publications.append(job)

		scenario_risk = Scenario_Risk.objects.filter(private=False)
		for job in scenario_risk:
			publications.append(job)

		classical_psha_hazard = Classical_PSHA_Hazard.objects.filter(private=False)
		for job in classical_psha_hazard:
			publications.append(job)

		classical_psha_hazard = Classical_PSHA_Hazard.objects.filter(private=False).exclude(id__in=[job.id for job in Event_Based_Hazard.objects.all()])
		for job in classical_psha_hazard:
			publications.append(job)

		classical_psha_risk = Classical_PSHA_Risk.objects.filter(private=False).exclude(id__in=[job.id for job in Event_Based_Risk.objects.all()])
		for job in classical_psha_risk:
			publications.append(job)

		event_based_hazard = Event_Based_Hazard.objects.filter(private=False)
		for job in event_based_hazard:
			publications.append(job)

		event_based_risk = Event_Based_Risk.objects.filter(private=False)
		for job in event_based_risk:
			publications.append(job)
	
		return render(request, 'home.html', {'publications': sorted(publications,  key=attrgetter('date_created'), reverse=True) })


	else:
		return render(request, 'index.html')

#class UserUpdate(forms.UserChangeForm):
#	class Meta:
#		model = User
#		fields = ['username', 'first_name', 'last_name', 'email']
#	form = UserUpdate()

@login_required
def account(request):
	source_models 			= Source_Model.objects.filter(Q(source_model_contributor__contributor=request.user) | Q(author=request.user)).order_by('-date_created')
	site_models 			= Site_Model.objects.filter(Q(site_model_contributor__contributor=request.user) | Q(author=request.user)).order_by('-date_created')
	rupture_models 			= Rupture_Model.objects.filter(user=request.user).order_by('-date_created')
	exposure_models 		= Exposure_Model.objects.filter(Q(exposure_model_contributor__contributor=request.user) | Q(author=request.user)).order_by('-date_created')
	fragility_models 		= Fragility_Model.objects.filter(Q(fragility_model_contributor__contributor=request.user) | Q(author=request.user)).order_by('-date_created')
	consequence_models 		= Consequence_Model.objects.filter(Q(consequence_model_contributor__contributor=request.user) | Q(author=request.user)).order_by('-date_created')
	vulnerability_models 	= Vulnerability_Model.objects.filter(Q(vulnerability_model_contributor__contributor=request.user) | Q(author=request.user)).order_by('-date_created')
	logic_trees_sm 			= Logic_Tree_SM.objects.filter(user=request.user).order_by('-date_created')
	logic_trees_gmpe 		= Logic_Tree_GMPE.objects.filter(user=request.user).order_by('-date_created')

	scenario_hazard 		= Scenario_Hazard.objects.filter(user=request.user).order_by('-date_created')
	scenario_damage 		= Scenario_Damage.objects.filter(user=request.user).order_by('-date_created')
	scenario_risk 			= Scenario_Risk.objects.filter(user=request.user).order_by('-date_created')

	classical_hazard 		= Classical_PSHA_Hazard.objects.filter(user=request.user).order_by('-date_created').exclude(id__in=[job.id for job in Event_Based_Hazard.objects.filter(user=request.user)])
	classical_risk 			= Classical_PSHA_Risk.objects.filter(user=request.user).order_by('-date_created').exclude(id__in=[job.id for job in Event_Based_Risk.objects.filter(user=request.user)])

	event_based_hazard 		= Event_Based_Hazard.objects.filter(user=request.user).order_by('-date_created')
	event_based_risk 		= Event_Based_Risk.objects.filter(user=request.user).order_by('-date_created')

	return render(request, 'account.html', {'source_models': source_models, 
											'site_models': site_models,
											'rupture_models': rupture_models, 
											'exposure_models': exposure_models,
											'fragility_models': fragility_models,
											'consequence_models': consequence_models,
											'vulnerability_models': vulnerability_models,
											'logic_trees_sm': logic_trees_sm,
											'logic_trees_gmpe': logic_trees_gmpe,
											'scenario_hazard': scenario_hazard,
											'scenario_damage': scenario_damage,
											'scenario_risk': scenario_risk,
											'classical_hazard': classical_hazard,
											'classical_risk': classical_risk,
											'event_based_hazard': event_based_hazard,
											'event_based_risk': event_based_risk,
											})

@login_required
def profile(request, user_id):
	user = User.objects.get(pk=user_id)

	if user == request.user:
		return redirect('account')

	source_models 			= Source_Model.objects.filter(private=False).filter(Q(source_model_contributor__contributor=user) | Q(author=user)).order_by('-date_created')
	site_models 			= Site_Model.objects.filter(private=False).filter(Q(site_model_contributor__contributor=user) | Q(author=user)).order_by('-date_created')
	rupture_models 			= Rupture_Model.objects.filter(user=user).order_by('-date_created')
	exposure_models 		= Exposure_Model.objects.filter(private=False).filter(Q(exposure_model_contributor__contributor=user) | Q(author=user)).order_by('-date_created')
	fragility_models 		= Fragility_Model.objects.filter(private=False).filter(Q(fragility_model_contributor__contributor=user) | Q(author=user)).order_by('-date_created')
	consequence_models 		= Consequence_Model.objects.filter(private=False).filter(Q(consequence_model_contributor__contributor=user) | Q(author=user)).order_by('-date_created')
	vulnerability_models 	= Vulnerability_Model.objects.filter(private=False).filter(Q(vulnerability_model_contributor__contributor=user) | Q(author=user)).order_by('-date_created')
	logic_trees_sm 			= Logic_Tree_SM.objects.filter(private=False).filter(user=user).order_by('-date_created')
	logic_trees_gmpe 		= Logic_Tree_GMPE.objects.filter(private=False).filter(user=user).order_by('-date_created')

	scenario_hazard 		= Scenario_Hazard.objects.filter(private=False).filter(user=user).order_by('-date_created')
	scenario_damage 		= Scenario_Damage.objects.filter(private=False).filter(user=user).order_by('-date_created')
	scenario_risk 			= Scenario_Risk.objects.filter(private=False).filter(user=user).order_by('-date_created')

	classical_hazard 		= Classical_PSHA_Hazard.objects.filter(private=False).filter(user=user).order_by('-date_created').exclude(id__in=[job.id for job in Event_Based_Hazard.objects.filter(user=user)])
	classical_risk 			= Classical_PSHA_Risk.objects.filter(private=False).filter(user=user).order_by('-date_created').exclude(id__in=[job.id for job in Event_Based_Risk.objects.filter(user=user)])

	event_based_hazard 		= Event_Based_Hazard.objects.filter(private=False).filter(user=user).order_by('-date_created')
	event_based_risk 		= Event_Based_Risk.objects.filter(private=False).filter(user=user).order_by('-date_created')

	return render(request, 'profile.html', {'profile': user,
											'source_models': source_models, 
											'site_models': site_models,
											'rupture_models': rupture_models, 
											'exposure_models': exposure_models,
											'fragility_models': fragility_models,
											'consequence_models': consequence_models,
											'vulnerability_models': vulnerability_models,
											'logic_trees_sm': logic_trees_sm,
											'logic_trees_gmpe': logic_trees_gmpe,
											'scenario_hazard': scenario_hazard,
											'scenario_damage': scenario_damage,
											'scenario_risk': scenario_risk,
											'classical_hazard': classical_hazard,
											'classical_risk': classical_risk,
											'event_based_hazard': event_based_hazard,
											'event_based_risk': event_based_risk,
											})

class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name' ]
        exclude = ['password',]
    def clean_password(self):
        return ""


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance  and self.instance.pk:
            self.fields['username'] = self.instance.username
            self.fields['email'] = self.instance.email
            self.fields['first_name'] = self.instance.first_name
            self.fields['last_name'] = self.instance.last_name

@login_required
def account_settings(request):
	if request.method == 'GET':
		form = UserProfileForm()
		return render(request, 'account_settings.html', {'form': form})

	elif request.method == 'POST':
		form = UserProfileForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect('account')
		else:
			return render(request, 'account_settings.html', {'form': form})
		




