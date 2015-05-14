from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from eng_models.models import *
from jobs.models import *
from world.models import *
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.contrib.gis.measure import Distance, D
from django.db.models import Sum

from django.core import serializers
from django.contrib.auth.models import User
import redis
from rq import Queue
import json
import colors
import requests

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


def queue_job(job, type):
	conn = redis.Redis('priseOQ.fe.up.pt', 6379)
	q = Queue('risco', connection=conn)
	job_queue = q.enqueue('controller.start', job.id, type, DATABASE, timeout=3600)
	job.status = 'STARTED'
	job.save()


def get_imt_from_vul(model, job):
	if model.imt == 'PGA':
		if not job.pga:
			job.pga = True
	    
    	if model.imt == 'SA':
    		if model.sa_period not in job.sa_periods:
    			job.sa_periods = job.sa_periods + model.sa_period



############################
##     SCENARIO HAZARD    ##
############################


class ScenarioHazardForm(forms.ModelForm):
	fragility_model = forms.ModelChoiceField(queryset=Fragility_Model.objects.all().order_by('-date_created'), required=False)
	structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)
	
	def clean(self):
		form_data = self.cleaned_data

		if 'region' in form_data and 'rupture_model' in form_data: 
			region = form_data['region']
			rupture_model = form_data['rupture_model']

			cursor = connection.cursor()
			if rupture_model.rupture_type == 'POINT':
				cursor.execute('SELECT ST_DWithin(ST_GeomFromText(%s, 4326)::geography, ST_GeomFromText(%s, 4326)::geography, %s)', [region.wkt, rupture_model.location.wkt, float(form_data['max_distance'])*1000])
			else:
				cursor.execute('SELECT ST_DWithin(ST_GeomFromText(%s, 4326)::geography, ST_GeomFromText(%s, 4326)::geography, %s)', [region.wkt, rupture_model.rupture_geom.wkt, float(form_data['max_distance'])*1000])

			check = cursor.fetchone()[0]

			if not check:
				self._errors["max_distance"] = "The distance between the region selected and the rupture is greater than the specified."
				del form_data['max_distance']

		return form_data


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

	form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	return render(request, 'jobs/index_scenario_hazard.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_hazard(request):
	if request.method == 'POST':
		form = ScenarioHazardForm(request.POST)
		form.fields["site_model"].queryset = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
		form.fields["rupture_model"].queryset = Rupture_Model.objects.filter(user=request.user)
		
		form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
		form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user

			if form.cleaned_data["fragility_model"] != None:
				fragility_taxonomies = Taxonomy_Fragility_Model.objects.filter(model = form.cleaned_data['fragility_model'])
				periods = []
				for tax in fragility_taxonomies:
					if tax.imt == 'PGA':
						if not job.pga:
							job.pga = True
					if tax.imt == 'SA':
						if tax.sa_period not in periods:
							periods.append(tax.sa_period)
				job.sa_periods = periods

			if form.cleaned_data["structural_vulberability"] != None:
				get_imt_from_vul(form.cleaned_data["structural_vulberability"], job)
			if form.cleaned_data["non_structural_vulberability"] != None:
				get_imt_from_vul(form.cleaned_data["non_structural_vulberability"], job)
			if form.cleaned_data["contents_vulberability"] != None:
				get_imt_from_vul(form.cleaned_data["contents_vulberability"], job)
			if form.cleaned_data["business_int_vulberability"] != None:
				get_imt_from_vul(form.cleaned_data["business_int_vulberability"], job)
			if form.cleaned_data["occupants_vulberability"] != None:
				get_imt_from_vul(form.cleaned_data["occupants_vulberability"], job)

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
		queue_job(job, 'scenario_hazard')
		return redirect('results_scenario_hazard', job.id)
	except:
		return render(request, 'jobs/results_scenario_hazard.html', {'job': job, 'connection_error': True})
		

@login_required
def results_scenario_hazard_ajax(request, job_id):
	job = Scenario_Hazard.objects.get(pk=job_id, user=request.user)

	cursor = connection.cursor()
	d = []
    
	if job.pga:

		cursor.execute("SELECT ST_AsGeoJSON(cell), gmvs_mean, world_fishnet.id \
						FROM world_fishnet, jobs_scenario_hazard_results_by_cell \
						WHERE jobs_scenario_hazard_results_by_cell.job_id = %s \
						AND jobs_scenario_hazard_results_by_cell.cell_id = world_fishnet.id \
						AND jobs_scenario_hazard_results_by_cell.imt = 'PGA'", [job_id])
	
		cells = cursor.fetchall()
		features = list(dict(type='Feature', id=cell[2], properties=dict(color=colors.hazard_picker(cell[1]), a="{0:.4f}".format(cell[1])),
					geometry=json.loads(cell[0])) for cell in cells)

		d.append({'type': 'FeatureCollection', 'features': features, 'name': 'PGA'})

	for e in job.sa_periods:

		cursor.execute("SELECT ST_AsGeoJSON(cell), gmvs_mean, world_fishnet.id \
						FROM world_fishnet, jobs_scenario_hazard_results_by_cell \
						WHERE jobs_scenario_hazard_results_by_cell.job_id = %s \
						AND jobs_scenario_hazard_results_by_cell.cell_id = world_fishnet.id \
						AND jobs_scenario_hazard_results_by_cell.sa_period = %s", [job_id, e])
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


def get_geojson(features_list):
	features = list(dict(type='Feature',
						id=cell[0],
						properties=dict(id=cell[0]),
									geometry=json.loads(cell[1])) for cell in features_list)

	return {'type': 'FeatureCollection', 'features': features}


@login_required
def results_scenario_hazard_ajax_test(request, job_id):
	job = Scenario_Hazard.objects.get(pk=job_id, user=request.user)

	cursor = connection.cursor()
	d = []

	if job.pga:

		cursor.execute("SELECT world_fishnet.id, ST_AsGeoJSON(cell), gmvs_mean \
						FROM world_fishnet, jobs_scenario_hazard_results_by_cell \
						WHERE jobs_scenario_hazard_results_by_cell.job_id = %s \
						AND jobs_scenario_hazard_results_by_cell.cell_id = world_fishnet.id \
						AND jobs_scenario_hazard_results_by_cell.imt = 'PGA'", [job_id])
		cells = cursor.fetchall()

		data = list( {'id': cell[0], 'value': float("{0:.4f}".format(cell[2])) } for cell in cells)
		d.append({'name': 'PGA', 'values': data})

		geo_json = get_geojson(cells)

	for e in job.sa_periods:

		cursor.execute("SELECT world_fishnet.id, ST_AsGeoJSON(cell), gmvs_mean \
						FROM world_fishnet, jobs_scenario_hazard_results_by_cell \
						WHERE jobs_scenario_hazard_results_by_cell.job_id = %s \
						AND jobs_scenario_hazard_results_by_cell.cell_id = world_fishnet.id \
						AND jobs_scenario_hazard_results_by_cell.sa_period = %s", [job_id, e])
		cells = cursor.fetchall()

		data = list( {'id': cell[0], 'value': float("{0:.4f}".format(cell[2])) } for cell in cells)
		d.append({'name': 'Sa('+str(e)+')', 'values': data})

		if not geo_json:
			geo_json = get_geojson(cells) 

	return HttpResponse(json.dumps({ 'hazard': d, 'geojson': geo_json }), content_type="application/json")




############################
##     SCENARIO DAMAGE    ##
############################


def check_imts(hazard, struct):
	for e in struct:
		if e not in hazard:
			return False
	return True




class ScenarioDamageForm(forms.ModelForm):

	def clean(self):
	    form_data = self.cleaned_data

	    if 'fragility_model' in form_data and 'hazard_job' in form_data and 'exposure_model' in form_data and 'region'in form_data and 'max_hazard_dist' in form_data: 
		    fragility_taxonomies = Taxonomy_Fragility_Model.objects.filter(model = form_data['fragility_model'])
		    frag_imts = []
		    
		    for tax in fragility_taxonomies:
		    	if tax.imt == 'SA':
		    		imt = 'SA('+str(tax.sa_period)+')'
		    		if imt not in frag_imts:
		    			frag_imts.append(imt)
		    	else:
		    		if tax.imt not in frag_imts:
		    			frag_imts.append(tax.imt)

		    hazard = form_data['hazard_job']
		    haz_imts = []

		    if hazard.pga:
		    	haz_imts.append('PGA')
		    for period in hazard.sa_periods:
		    	haz_imts.append('SA('+str(period)+')')

		    if check_imts(haz_imts, frag_imts) == False:
		        self.add_error(None, '<p>Missing hazard IMTs.</p><p> Fragility Model IMTs: </p> <ul><li>'+'</li><li>'.join(frag_imts)+' </li></ul> <p> Available Hazard IMTs: </p> <ul><li>'+'</li><li>'.join(haz_imts)+'</li></ul>')

		    region = form_data['region']
		    exposure_model = form_data['exposure_model']

		    cursor = connection.cursor()
		    #cursor.execute('SELECT ST_DWithin(region::geography, ST_GeomFromText(%s, 4326)::geography, %s) FROM jobs_scenario_hazard WHERE id = %s', [region.wkt, float(form_data['max_hazard_dist'])*1000, hazard.id])
		    cursor.execute('SELECT ST_DWithin(jobs_scenario_hazard.region::geography, point.location::geography, %s) \
		    				FROM jobs_scenario_hazard, (SELECT DISTINCT location \
		    								FROM eng_models_asset \
		    								WHERE model_id = %s\
		    								AND ST_Within(location, ST_GeomFromText(%s, 4326))) AS point \
		    				WHERE jobs_scenario_hazard.id = %s \
		    				ORDER BY ST_Distance(point.location::geography, jobs_scenario_hazard.region::geography) DESC\
		    				LIMIT 1', [float(form_data['max_hazard_dist'])*1000, exposure_model.id, region.wkt, hazard.id])
		    
		    try:
		    	check = cursor.fetchone()[0]
		    except:
		    	self.add_error(None, 'There is no assets on the region you selected')
		    	check = False

		    if not check:
		    	self._errors["max_hazard_dist"] = "The distance between the hazard and the risk is greater than the specified."
		    	del form_data['max_hazard_dist']

	    return form_data

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
	form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
	form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	return render(request, 'jobs/index_scenario_damage.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_damage(request):
	if request.method == 'POST':
		form = ScenarioDamageForm(request.POST)
		form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
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
		queue_job(job, 'scenario_damage')
		return redirect('results_scenario_damage', job.id)
	except:
		return render(request, 'jobs/results_scenario_damage.html', {'job': job, 'connection_error': True})

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



##########################
##     SCENARIO RISK    ##
##########################


class ScenarioRiskForm(forms.ModelForm):
	structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)
	
	def clean(self):
		form_data = self.cleaned_data
		if 'occupants_vulberability' in form_data and form_data['insured_losses']:
			self.add_error(None, 'You cannot calculate insured losses with an occupants vulberability model')
		return form_data

	class Meta:
		model = Scenario_Risk
		exclude = ['user', 'date_created', 'vulnerability_models', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
           			'region': forms.HiddenInput(),
					}

@login_required	
def index_scenario_risk(request):
	jobs = Scenario_Risk.objects.filter(user=request.user).order_by('-date_created')
	form = ScenarioRiskForm()
	form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
	form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	return render(request, 'jobs/index_scenario_risk.html', {'jobs': jobs, 'form': form})

@login_required
def add_scenario_risk(request):
	if request.method == 'POST':
		form = ScenarioRiskForm(request.POST)
		form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
		form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
		form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			if form.cleaned_data["structural_vulberability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["structural_vulberability"])
			if form.cleaned_data["non_structural_vulberability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["non_structural_vulberability"])
			if form.cleaned_data["contents_vulberability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["contents_vulberability"])
			if form.cleaned_data["business_int_vulberability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["business_int_vulberability"])
			if form.cleaned_data["occupants_vulberability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["occupants_vulberability"])

			return redirect('results_scenario_risk', job.id)
		else:
			jobs = Scenario_Risk.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/index_scenario_risk.html', {'jobs': jobs, 'form': form})
	else:
		form = ScenarioRiskForm()
		return render(request, 'jobs/index_scenario_risk.html', {'form': form})

@login_required
def results_scenario_risk(request, job_id):
	job = get_object_or_404(Scenario_Risk ,pk=job_id)
	#taxonomies = Building_Taxonomy.objects.filter(source=job.exposure_model.taxonomy_source)
	return render(request, 'jobs/results_scenario_risk.html', {'job': job})


def get_geojson_countries(features_list):
	features = list(dict(type='Feature',
						id=cell[0],
						properties=dict(id=cell[0],
										name=cell[2]),
						geometry=json.loads(cell[1])) for cell in features_list)

	return {'type': 'FeatureCollection', 'features': features}


@login_required
def results_scenario_risk_ajax(request, job_id):
	job = get_object_or_404(Scenario_Risk ,pk=job_id, user=request.user)
	vulnerability_types = Scenario_Risk_Vulnerability_Model.objects.filter(job = job)

	cursor = connection.cursor()
	d = []

	for vulnerability in vulnerability_types:
		
		if request.GET.get('country') != 'undefined':
			country_id = request.GET.get('country')

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_adm_1 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [vulnerability.id, taxonomy_id ,country_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_adm_1 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [vulnerability.id, country_id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results, world_adm_1 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [vulnerability.id, country_id])
				info_per_taxonomy = cursor.fetchall()
		
		else:
			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_country, world_adm_1 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = world_country.id \
								GROUP BY world_country.id', [vulnerability.id, taxonomy_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_country, world_adm_1 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = world_country.id \
								GROUP BY world_country.id', [vulnerability.id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								GROUP BY eng_models_building_taxonomy.id', [vulnerability.id])
				info_per_taxonomy = cursor.fetchall()

		total = sum(e[3] for e in info_per_region)
		if job.insured_losses:
			total_insured = sum(e[4] for e in info_per_region)
		else:
			total_insured = None

		scale = len(str(total).split('.')[0])-1
		total_scale = round(total, -scale)

		if 'geo_json' not in locals():
			geo_json = get_geojson_countries(info_per_region)

		data_per_region = list( {'id': region[0], 'place': region[2], 'value': region[3], 'insured_value': region[4] } for region in info_per_region)
	
		if info_per_taxonomy:
			data_per_taxonomy = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': taxonomy[2], 'insured_value': taxonomy[3]} for taxonomy in info_per_taxonomy)
		else:
			data_per_taxonomy = None

		d.append({'name': vulnerability.vulnerability_model.type,
				'values': data_per_region,
				'values_per_taxonomy': data_per_taxonomy,
				'total': total,
				'total_insured': total_insured,
				'total_scale': total_scale,
				'currency': job.exposure_model.currency})
	
	job_json = serializers.serialize("json", [job])
	job_json = json.loads(job_json)

	exp_json = serializers.serialize("json", [job.exposure_model])
	exp_json = json.loads(exp_json)

	return HttpResponse(json.dumps({'job': job_json,
									'exposure_model': exp_json,
									'losses': d,
									'geojson': geo_json }), content_type="application/json")



@login_required
def start_scenario_risk(request, job_id):
	job = get_object_or_404(Scenario_Risk ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'scenario_risk')
		return redirect('results_scenario_risk', job.id)
	except:
		return render(request, 'jobs/results_scenario_risk.html', {'job': job, 'connection_error': True})




########################
##     PSHA HAZARD    ##
########################


class PSHAHazardForm(forms.ModelForm):
	structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)

	gmpe_logic_tree = forms.ModelChoiceField(queryset = Logic_Tree.objects.filter(type='gmpe'), required=False)
	source_logic_tree = forms.ModelChoiceField(queryset = Logic_Tree.objects.filter(type='source'), required=False)

	class Meta:
		model = Classical_PSHA_Hazard
		exclude = ['user', 'date_created', 'vulnerability_models', 'logic_trees', 'imt_l', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'sa_periods': forms.TextInput(attrs={'placeholder': 'Ex: 0.20, 0.5, 0.9, 1.3 ...'}),
           			'region': forms.HiddenInput(),
					}

@login_required	
def index_psha_hazard(request):
	jobs = Classical_PSHA_Hazard.objects.filter(user=request.user).order_by('-date_created')
	form = PSHAHazardForm()
	form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	form.fields["gmpe_logic_tree"].queryset = Logic_Tree.objects.filter(user=request.user).filter(type='gmpe').order_by('-date_created')
	form.fields["source_logic_tree"].queryset = Logic_Tree.objects.filter(user=request.user).filter(type='source').order_by('-date_created')
	return render(request, 'jobs/index_psha_hazard.html', {'jobs': jobs, 'form': form})

@login_required
def add_psha_hazard(request):
	if request.method == 'POST':
		form = PSHAHazardForm(request.POST)
		form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
		
		form.fields["gmpe_logic_tree"].queryset = Logic_Tree.objects.filter(user=request.user).filter(type='gmpe').order_by('-date_created')
		form.fields["source_logic_tree"].queryset = Logic_Tree.objects.filter(user=request.user).filter(type='source').order_by('-date_created')

		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			#if form.cleaned_data["structural_vulberability"] != None:
			#	job.vulnerability_models.add(form.cleaned_data["structural_vulberability"])
			#if form.cleaned_data["non_structural_vulberability"] != None:
			#	job.vulnerability_models.add(form.cleaned_data["non_structural_vulberability"])
			#if form.cleaned_data["contents_vulberability"] != None:
			#	job.vulnerability_models.add(form.cleaned_data["contents_vulberability"])
			#if form.cleaned_data["occupants_vulberability"] != None:
			#	job.vulnerability_models.add(form.cleaned_data["occupants_vulberability"])

			if form.cleaned_data["gmpe_logic_tree"] != None:
				job.logic_trees.add(form.cleaned_data["gmpe_logic_tree"])
			if form.cleaned_data["source_logic_tree"] != None:
				job.logic_trees.add(form.cleaned_data["source_logic_tree"])

			return redirect('results_psha_hazard', job.id)
		else:
			jobs = Classical_PSHA_Hazard.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/index_psha_hazard.html', {'jobs': jobs, 'form': form})
	else:
		form = PSHAHazardForm()
		return render(request, 'jobs/index_psha_hazard.html', {'form': form})

@login_required
def results_psha_hazard(request, job_id):
	job = get_object_or_404(Classical_PSHA_Hazard ,pk=job_id, user=request.user)
	return render(request, 'jobs/results_psha_hazard.html', {'job': job})

@login_required
def start_psha_hazard(request, job_id):
	job = get_object_or_404(Classical_PSHA_Hazard ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'psha_hazard')
		return redirect('results_psha_hazard', job.id)
	except:
		return render(request, 'jobs/results_psha_hazard.html', {'job': job, 'connection_error': True})






########################
##     PSHA RISK    ##
########################


class PSHARiskForm(forms.ModelForm):
	structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulberability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)

	class Meta:
		model = Classical_PSHA_Risk
		exclude = ['user', 'date_created', 'vulnerability_models', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
           			'region': forms.HiddenInput(),
					}

@login_required	
def index_psha_risk(request):
	jobs = Classical_PSHA_Risk.objects.filter(user=request.user).order_by('-date_created')
	form = PSHARiskForm()

	form.fields['hazard'].queryset = Classical_PSHA_Hazard.objects.filter(user=request.user, status='FINISHED').order_by('-date_created')

	form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	return render(request, 'jobs/index_psha_risk.html', {'jobs': jobs, 'form': form})

@login_required
def add_psha_risk(request):
	if request.method == 'POST':
		form = PSHARiskForm(request.POST)
		form.fields['hazard'].queryset = Classical_PSHA_Hazard.objects.filter(user=request.user, status='FINISHED').order_by('-date_created')
		form.fields["structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulberability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')

		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			if form.cleaned_data["structural_vulberability"] != None:
				job.vulnerability_models.add(form.cleaned_data["structural_vulberability"])
			if form.cleaned_data["non_structural_vulberability"] != None:
				job.vulnerability_models.add(form.cleaned_data["non_structural_vulberability"])
			if form.cleaned_data["contents_vulberability"] != None:
				job.vulnerability_models.add(form.cleaned_data["contents_vulberability"])
			if form.cleaned_data["business_int_vulberability"] != None:
				job.vulnerability_models.add(form.cleaned_data["business_int_vulberability"])
			if form.cleaned_data["occupants_vulberability"] != None:
				job.vulnerability_models.add(form.cleaned_data["occupants_vulberability"])

			return redirect('results_psha_risk', job.id)
		else:
			jobs = Classical_PSHA_Risk.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/index_psha_risk.html', {'jobs': jobs, 'form': form})
	else:
		form = PSHARiskForm()
		return render(request, 'jobs/index_psha_risk.html', {'form': form})

@login_required
def results_psha_risk(request, job_id):
	job = get_object_or_404(Classical_PSHA_Risk ,pk=job_id, user=request.user)
	return render(request, 'jobs/results_psha_risk.html', {'job': job})


@login_required
def start_psha_risk(request, job_id):
	job = get_object_or_404(Classical_PSHA_Risk ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'psha_risk')
		return redirect('results_psha_risk', job.id)
	except:
		return render(request, 'jobs/results_psha_risk.html', {'job': job, 'connection_error': True})




