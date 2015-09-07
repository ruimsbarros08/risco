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
	job_queue = q.enqueue('controller.start', job.id, type, DATABASE, timeout=3600*12)
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
	structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)
	
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
	page = request.GET.get('page')
	jobs = Scenario_Hazard.objects.filter(private=False).order_by('-date_created')
	form = ScenarioHazardForm()
	form.fields["site_model"].queryset = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["rupture_model"].queryset = Rupture_Model.objects.filter(user=request.user)

	form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	return render(request, 'jobs/index_scenario_hazard.html', {'jobs': pagination(jobs, 10, page), 'form': form})

@login_required
def add_scenario_hazard(request):
	if request.method == 'POST':
		form = ScenarioHazardForm(request.POST)
		form.fields["site_model"].queryset = Site_Model.objects.filter(site_model_contributor__contributor=request.user).order_by('-date_created')
		form.fields["rupture_model"].queryset = Rupture_Model.objects.filter(user=request.user)
		
		form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
		form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
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

			if form.cleaned_data["structural_vulnerability"] != None:
				get_imt_from_vul(form.cleaned_data["structural_vulnerability"], job)
			if form.cleaned_data["non_structural_vulnerability"] != None:
				get_imt_from_vul(form.cleaned_data["non_structural_vulnerability"], job)
			if form.cleaned_data["contents_vulnerability"] != None:
				get_imt_from_vul(form.cleaned_data["contents_vulnerability"], job)
			if form.cleaned_data["business_int_vulnerability"] != None:
				get_imt_from_vul(form.cleaned_data["business_int_vulnerability"], job)
			if form.cleaned_data["occupants_vulnerability"] != None:
				get_imt_from_vul(form.cleaned_data["occupants_vulnerability"], job)

			job.save()
			return redirect('results_scenario_hazard', job.id)
		else:
			# jobs = Scenario_Hazard.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_scenario_hazard.html', {'form': form})
	else:
		form = ScenarioHazardForm()
		return render(request, 'jobs/new_scenario_hazard.html', {'form': form})

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


def get_geojson(features_list):
	features = list(dict(type='Feature',
						id=cell[0],
						properties=dict(id=cell[0]),
									geometry=json.loads(cell[1])) for cell in features_list)

	return {'type': 'FeatureCollection', 'features': features}


@login_required
def results_scenario_hazard_ajax(request, job_id):
	job = Scenario_Hazard.objects.get(pk=job_id)
	
	job_json = serializers.serialize("json", [job])
	job_json = json.loads(job_json)
	
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

		if 'geo_json' not in locals():
			geo_json = get_geojson(cells)

	
	source = Rupture_Model.objects.get(pk=job.rupture_model.id)
	source_json = serializers.serialize("json", [source])
	source_json = json.loads(source_json)

	epicenter = {'type': 'FeatureCollection', 'features': [dict(type='Feature', id=source.id, properties=dict(), geometry = json.loads(source.location.json) )] } 

	if job.rupture_model.rupture_type == 'POINT':
		rupture = None
	else:		
		rupture = {'type': 'FeatureCollection', 'features': [dict(type='Feature', id=source.id, properties=dict( name = source.name ),
					geometry = json.loads(source.rupture_geom.json) )] } 
	
	return HttpResponse(json.dumps({ 'hazard': d,
									'geojson': geo_json,
									'job': job_json,
									'rupture': {'epicenter': epicenter,
												'rupture': rupture,
												'info': source_json}
									}), content_type="application/json")





############################
##     SCENARIO DAMAGE    ##
############################


def get_geojson_countries(features_list):
	features = list(dict(type='Feature',
						id=cell[0],
						properties=dict(id=cell[0],
										name=cell[2]),
						geometry=json.loads(cell[1])) for cell in features_list)

	return {'type': 'FeatureCollection', 'features': features}



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
	page = request.GET.get('page')
	jobs = Scenario_Damage.objects.filter(private=False).order_by('-date_created')
	form = ScenarioDamageForm()
	form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
	form.fields["fragility_model"].queryset = Fragility_Model.objects.filter(fragility_model_contributor__contributor=request.user).order_by('-date_created')
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	return render(request, 'jobs/index_scenario_damage.html', {'jobs': pagination(jobs, 10, page), 'form': form})

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
			# jobs = Scenario_Damage.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_scenario_damage.html', {'form': form})
	else:
		form = ScenarioDamageForm()
		return render(request, 'jobs/new_scenario_damage.html', {'form': form})

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
def results_scenario_damage_ajax(request, job_id):
	job = get_object_or_404(Scenario_Damage ,pk=job_id, user=request.user)

	cursor = connection.cursor()
	cursor.execute("SELECT limit_state, sum(mean), sum(stddev) \
					FROM jobs_scenario_damage_results \
					WHERE job_id = %s \
					GROUP BY limit_state", [job_id])

	data_per_state = list( {'name': state[0], 'value': state[1], 'stddev': state[2]} for state in cursor.fetchall())

	d = []
	d.append({'name': 'overall',
			'values': data_per_state})


	for state in job.fragility_model.limit_states:

		if request.GET.get('country') != 'undefined':
			country_id = request.GET.get('country')

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
								sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev) \
								FROM eng_models_asset, jobs_scenario_damage_results, world_adm_1 \
								WHERE jobs_scenario_damage_results.job_id = %s \
								AND jobs_scenario_damage_results.limit_state = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_damage_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [job.id, state, taxonomy_id ,country_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
								sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev)  \
								FROM eng_models_asset, jobs_scenario_damage_results, world_adm_1 \
								WHERE jobs_scenario_damage_results.job_id = %s \
								AND jobs_scenario_damage_results.limit_state = %s \
								AND eng_models_asset.id = jobs_scenario_damage_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [job.id, state, country_id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_damage_results, world_adm_1 \
								WHERE jobs_scenario_damage_results.job_id = %s \
								AND jobs_scenario_damage_results.limit_state = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_damage_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [job.id, state, country_id])
				info_per_taxonomy = cursor.fetchall()
		
		else:
			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
								sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev) \
								FROM eng_models_asset, jobs_scenario_damage_results, world_country, world_adm_1 \
								WHERE jobs_scenario_damage_results.job_id = %s \
								AND jobs_scenario_damage_results.limit_state = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_damage_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = world_country.id \
								GROUP BY world_country.id', [job.id, state, taxonomy_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
								sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev) \
								FROM eng_models_asset, jobs_scenario_damage_results, world_country, world_adm_1 \
								WHERE jobs_scenario_damage_results.job_id = %s \
								AND jobs_scenario_damage_results.limit_state = %s \
								AND eng_models_asset.id = jobs_scenario_damage_results.asset_id \
								AND eng_models_asset.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = world_country.id \
								GROUP BY world_country.id', [job.id, state])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_scenario_damage_results.mean), sum(jobs_scenario_damage_results.stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_damage_results \
								WHERE jobs_scenario_damage_results.job_id = %s \
								AND jobs_scenario_damage_results.limit_state = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_damage_results.asset_id \
								GROUP BY eng_models_building_taxonomy.id', [job.id, state])
				info_per_taxonomy = cursor.fetchall()

		total = sum(e[3] for e in info_per_region)
		stddev = sum(e[4] for e in info_per_region)

		scale = len(str(total).split('.')[0])-1
		total_scale = round(total, -scale)

		if 'geo_json' not in locals():
			geo_json = get_geojson_countries(info_per_region)

		data_per_region = list( {'id': region[0], 'name': region[2], 'value': region[3], 'stddev': region[4] } for region in info_per_region)
	
		if info_per_taxonomy:
			data_per_taxonomy = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': taxonomy[2], 'stddev': taxonomy[3] } for taxonomy in info_per_taxonomy)
		else:
			data_per_taxonomy = None


		d.append({'name': state,
				'values': data_per_region,
				'values_per_taxonomy': data_per_taxonomy,
				'total': total,
				'stddev': stddev,
				'total_scale': total_scale})

	job_json = serializers.serialize("json", [job])
	job_json = json.loads(job_json)

	return HttpResponse(json.dumps({'job': job_json,
									'losses': d,
									'geojson': geo_json }), content_type="application/json")




##########################
##     SCENARIO RISK    ##
##########################


class ScenarioRiskForm(forms.ModelForm):
	structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)
	
	def clean(self):
		form_data = self.cleaned_data
		if 'occupants_vulnerability' in form_data and form_data['insured_losses']:
			self.add_error(None, 'You cannot calculate insured losses with an occupants vulnerability model')
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
	page = request.GET.get('page')
	jobs = Scenario_Risk.objects.filter(private=False).order_by('-date_created')
	form = ScenarioRiskForm()
	form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
	form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	return render(request, 'jobs/index_scenario_risk.html', {'jobs': pagination(jobs, 10, page), 'form': form})

@login_required
def add_scenario_risk(request):
	if request.method == 'POST':
		form = ScenarioRiskForm(request.POST)
		form.fields["hazard_job"].queryset = Scenario_Hazard.objects.filter(user=request.user, status='FINISHED')
		form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
		form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			if form.cleaned_data["structural_vulnerability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["structural_vulnerability"])
			if form.cleaned_data["non_structural_vulnerability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["non_structural_vulnerability"])
			if form.cleaned_data["contents_vulnerability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["contents_vulnerability"])
			if form.cleaned_data["business_int_vulnerability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["business_int_vulnerability"])
			if form.cleaned_data["occupants_vulnerability"] != None:
				Scenario_Risk_Vulnerability_Model.objects.create(job=job, vulnerability_model=form.cleaned_data["occupants_vulnerability"])

			return redirect('results_scenario_risk', job.id)
		else:
			# jobs = Scenario_Risk.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_scenario_risk.html', {'form': form})
	else:
		form = ScenarioRiskForm()
		return render(request, 'jobs/new_scenario_risk.html', {'form': form})

@login_required
def results_scenario_risk(request, job_id):
	job = get_object_or_404(Scenario_Risk ,pk=job_id)
	vulnerability_types = Scenario_Risk_Vulnerability_Model.objects.filter(job = job)
	economic_loss_types = []
	total = False
	for vulnerability in vulnerability_types:
		if vulnerability.vulnerability_model.type != 'occupants_vulnerability':
			economic_loss_types.append(vulnerability.vulnerability_model.type)
		if len(economic_loss_types) > 1:
			total = True
			break
		
	return render(request, 'jobs/results_scenario_risk.html', {'job': job, 'total': total})


@login_required
def results_scenario_risk_ajax(request, job_id):
	job = get_object_or_404(Scenario_Risk ,pk=job_id, user=request.user)
	vulnerability_types = Scenario_Risk_Vulnerability_Model.objects.filter(job = job)

	cursor = connection.cursor()
	d = []

	economic_loss_types = []

	for vulnerability in vulnerability_types:

		if request.GET.get('adm_1') != 'undefined':
			adm_1_id = request.GET.get('adm_1')

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s\
								GROUP BY world_adm_2.id', [vulnerability.id, taxonomy_id ,adm_1_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY world_adm_2.id', [vulnerability.id, adm_1_id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [vulnerability.id, adm_1_id])
				info_per_taxonomy = cursor.fetchall()

		elif request.GET.get('country') != 'undefined':
			country_id = request.GET.get('country')

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [vulnerability.id, taxonomy_id ,country_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [vulnerability.id, country_id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [vulnerability.id, country_id])
				info_per_taxonomy = cursor.fetchall()
		
		else:
			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id', [vulnerability.id, taxonomy_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id', [vulnerability.id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results \
								WHERE jobs_scenario_risk_results.job_vul_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								GROUP BY eng_models_building_taxonomy.id', [vulnerability.id])
				info_per_taxonomy = cursor.fetchall()

		total = sum(e[3] for e in info_per_region)
		stddev = sum(e[5] for e in info_per_region)
		if job.insured_losses:
			total_insured = sum(e[4] for e in info_per_region)
			stddev_insured = sum(e[6] for e in info_per_region)
			total_not_insured = total - total_insured
			stddev_not_insured = stddev - stddev_insured
		else:
			total_insured = None
			stddev_insured = None
			total_not_insured = None
			stddev_not_insured = None

		scale = len(str(total).split('.')[0])-1
		total_scale = round(total, -scale)

		if 'geo_json' not in locals():
			geo_json = get_geojson_countries(info_per_region)

		data_per_region = list( {'id': region[0], 'name': region[2], 'value': region[3], 'insured_value': region[4], 'stddev': region[5], 'insured_stddev': region[6] } for region in info_per_region)
	
		if info_per_taxonomy:
			data_per_taxonomy = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': taxonomy[2], 'insured_value': taxonomy[3], 'stddev': taxonomy[4], 'insured_stddev': taxonomy[5]} for taxonomy in info_per_taxonomy)
		else:
			data_per_taxonomy = None

		if vulnerability.vulnerability_model.type != 'occupants_vulnerability':
			economic_loss_types.append(vulnerability.vulnerability_model.type)

		d.append({'name': vulnerability.vulnerability_model.type,
				'values': data_per_region,
				'values_per_taxonomy': data_per_taxonomy,
				'total': total,
				'stddev': stddev,
				'total_insured': total_insured,
				'stddev_insured': stddev_insured,
				'total_not_insured': total_not_insured,
				'stddev_not_insured': stddev_not_insured,
				'total_scale': total_scale})

	if len(economic_loss_types) > 1:

		if request.GET.get('adm_1') != 'undefined':
			adm_1_id = request.GET.get('adm_1')

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY world_adm_2.id', [job.id, taxonomy_id ,adm_1_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY world_adm_2.id', [job.id, adm_1_id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [job.id, adm_1_id])
				info_per_taxonomy = cursor.fetchall()

		elif request.GET.get('country') != 'undefined':
			country_id = request.GET.get('country')

			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [job.id, taxonomy_id ,country_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [job.id, country_id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [job.id, country_id])
				info_per_taxonomy = cursor.fetchall()
		
		else:
			if request.GET.get('taxonomy') != 'undefined':
				taxonomy_id = request.GET.get('taxonomy')
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id', [job.id, taxonomy_id])
				info_per_region = cursor.fetchall()
				info_per_taxonomy = None
			else:
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_asset, jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id', [job.id])
				info_per_region = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name ,sum(jobs_scenario_risk_results.mean), sum(jobs_scenario_risk_results.insured_mean), \
								sum(jobs_scenario_risk_results.stddev) ,sum(jobs_scenario_risk_results.insured_stddev) \
								FROM eng_models_building_taxonomy ,eng_models_asset, \
								jobs_scenario_risk_results, jobs_scenario_risk_vulnerability_model \
								WHERE jobs_scenario_risk_results.job_vul_id = jobs_scenario_risk_vulnerability_model.id \
								AND jobs_scenario_risk_vulnerability_model.job_id = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_scenario_risk_results.asset_id \
								GROUP BY eng_models_building_taxonomy.id', [job.id])
				info_per_taxonomy = cursor.fetchall()

		total = sum(e[3] for e in info_per_region)
		stddev = sum(e[5] for e in info_per_region)
		if job.insured_losses:
			total_insured = sum(e[4] for e in info_per_region)
			stddev_insured = sum(e[6] for e in info_per_region)
			total_not_insured = total - total_insured
			stddev_not_insured = stddev - stddev_insured
		else:
			total_insured = None
			stddev_insured = None
			total_not_insured = None
			stddev_not_insured = None

		scale = len(str(total).split('.')[0])-1
		total_scale = round(total, -scale)

		data_per_region = list( {'id': region[0], 'name': region[2], 'value': region[3], 'insured_value': region[4], 'stddev': region[5], 'insured_stddev': region[6] } for region in info_per_region)
	
		if info_per_taxonomy:
			data_per_taxonomy = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': taxonomy[2], 'insured_value': taxonomy[3], 'stddev': taxonomy[4], 'insured_stddev': taxonomy[5]} for taxonomy in info_per_taxonomy)
		else:
			data_per_taxonomy = None

		d.append({'name': 'total',
				'values': data_per_region,
				'values_per_taxonomy': data_per_taxonomy,
				'total': total,
				'stddev': stddev,
				'total_insured': total_insured,
				'stddev_insured': stddev_insured,
				'total_not_insured': total_not_insured,
				'stddev_not_insured': stddev_not_insured,
				'total_scale': total_scale})
	
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

def clean_hazard(form, form_data):

	if 'gmpe_logic_tree' in form_data and 'sm_logic_tree' in form_data:

		levels = Logic_Tree_GMPE_Level.objects.filter(logic_tree = form_data['gmpe_logic_tree'])

		for level in levels:
			region = level.tectonic_region

			check = False
			for source_model in form_data['sm_logic_tree'].source_models.all():
				sources = Source.objects.filter(model=source_model)

				for source in sources:
					if source.tectonic_region == region:
						check = True

			if check == False:
				form.add_error(None, 'Every tectonic region specified in the GMPE logic tree must have at least one source from the same type in the Source Models of the Source Model Logic Tree')
				break

	if form_data['locations_type'] == 'EXPOSURE':
		if 'exposure_model' not in form_data:
			self._errors["exposure_model"] = "You should set an Exposure Model"


	elif form_data['locations_type'] == 'GRID': 
		if 'grid_spacing' not in form_data:
			self._errors["grid_spacing"] = "You should set a grid spacing"
		if 'region' not in form_data:
			self._errors["region"] = "You should draw a region"


	else:
		if 'locations' not in form_data:
			self._errors["region"] = "You should draw the location where the hazard will be computed"

	return form_data


psha_form_categories = {'general': ['name', 'description', 'description', 'investigation_time', 'truncation_level', 'max_distance', 'random_seed', 'imt_l'],
						'locations': ['locations_type','exposure_model', 'region', 'grid_spacing', 'locations'],
						'rupture': ['rupture_mesh_spacing', 'width_of_mfd_bin', 'area_source_discretization'],
						'sites': ['sites_type', 'site_model', 'vs30', 'vs30type', 'z1pt0', 'z2pt5'],
						'logic_trees': ['n_lt_samples', 'gmpe_logic_tree', 'sm_logic_tree'],
						'imts': ['structural_vulnerability', 'non_structural_vulnerability', 'contents_vulnerability',
								'business_int_vulnerability', 'occupants_vulnerability'],
						'outputs': ['quantile_hazard_curves', 'poes']}


class PSHAHazardForm(forms.ModelForm):
	structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)

	def clean(self):
		form_data = clean_hazard(self, self.cleaned_data)
		return form_data

	class Meta:
		model = Classical_PSHA_Hazard
		exclude = ['user', 'date_created', 'vulnerability_models', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'quantile_hazard_curves': forms.TextInput(attrs={'placeholder': 'Ex: 0.05, 0.5, 0.95'}),
					'poes': forms.TextInput(attrs={'placeholder': 'Ex: 0.2, 0.5, 0.9 ...'}),
					'region': forms.HiddenInput(),
					'locations': forms.HiddenInput(),
					'imt_l': forms.HiddenInput(),
					}

@login_required	
def index_psha_hazard(request):
	page = request.GET.get('page')
	jobs = Classical_PSHA_Hazard.objects.filter(private=False).order_by('-date_created').exclude(id__in=[job.id for job in Event_Based_Hazard.objects.all()])
	form = PSHAHazardForm()

	form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')
	
	return render(request, 'jobs/index_psha_hazard.html', {'jobs': pagination(jobs, 10, page), 'form': form, 'categories': psha_form_categories})


@login_required
def add_psha_hazard(request):
	if request.method == 'POST':
		form = PSHAHazardForm(request.POST)

		form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')

		form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')

		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			return redirect('results_psha_hazard', job.id)
		else:
			# jobs = Classical_PSHA_Hazard.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_psha_hazard.html', { 'form': form, 'categories': psha_form_categories})
	else:
		form = PSHAHazardForm()
		return render(request, 'jobs/new_psha_hazard.html', {'form': form, 'categories': psha_form_categories })

@login_required
def results_psha_hazard(request, job_id):
	job = get_object_or_404(Classical_PSHA_Hazard ,pk=job_id, user=request.user)
	imts = job.imt_l.keys()
	return render(request, 'jobs/results_psha_hazard.html', {'job': job, 'imts': imts})

@login_required
def start_psha_hazard(request, job_id):
	job = get_object_or_404(Classical_PSHA_Hazard ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'psha_hazard')
		return redirect('results_psha_hazard', job.id)
	except:
		return render(request, 'jobs/results_psha_hazard.html', {'job': job, 'connection_error': True})



@login_required
def results_psha_hazard_maps_ajax(request, job_id):
	job = Classical_PSHA_Hazard.objects.get(pk=job_id, user=request.user)
	
	job_json = serializers.serialize("json", [job])
	job_json = json.loads(job_json)
	
	cursor = connection.cursor()
	d = []

	if job.status == 'FINISHED':

		for imt in job.imt_l.keys():

			for poe in job.poes:

				for quantile in job.quantile_hazard_curves:

					if 'SA' in imt:
						sa_period = imt.split('(')[1].split(')')[0]
						cursor.execute("SELECT world_fishnet.id, ST_AsGeoJSON(world_fishnet.cell), AVG(jobs_classical_psha_hazard_maps.iml) \
										FROM world_fishnet, jobs_classical_psha_hazard_maps, jobs_classical_psha_hazard_curves \
										WHERE jobs_classical_psha_hazard_curves.job_id = %s \
										AND jobs_classical_psha_hazard_curves.sa_period = %s \
										AND jobs_classical_psha_hazard_curves.quantile = %s \
										AND jobs_classical_psha_hazard_curves.cell_id = world_fishnet.id \
										AND jobs_classical_psha_hazard_curves.id = jobs_classical_psha_hazard_maps.location_id \
										AND jobs_classical_psha_hazard_maps.poe = %s \
										GROUP BY world_fishnet.id", [job_id, sa_period, quantile, poe])

					else:
						cursor.execute("SELECT world_fishnet.id, ST_AsGeoJSON(world_fishnet.cell), AVG(jobs_classical_psha_hazard_maps.iml)  \
										FROM world_fishnet, jobs_classical_psha_hazard_maps, jobs_classical_psha_hazard_curves \
										WHERE jobs_classical_psha_hazard_curves.job_id = %s \
										AND jobs_classical_psha_hazard_curves.imt = %s \
										AND jobs_classical_psha_hazard_curves.quantile = %s \
										AND jobs_classical_psha_hazard_curves.cell_id = world_fishnet.id \
										AND jobs_classical_psha_hazard_curves.id = jobs_classical_psha_hazard_maps.location_id \
										AND jobs_classical_psha_hazard_maps.poe = %s \
										GROUP BY world_fishnet.id", [job_id, imt, quantile, poe])

					cells = cursor.fetchall()
					data = list( {'id': cell[0], 'value': float("{0:.4f}".format(cell[2])) } for cell in cells)
					d.append({'imt': imt, 'quantile': quantile, 'poe': poe, 'values': data})


				if 'SA' in imt:
					sa_period = imt.split('(')[1].split(')')[0]
					cursor.execute("SELECT world_fishnet.id, ST_AsGeoJSON(world_fishnet.cell), AVG(jobs_classical_psha_hazard_maps.iml) \
									FROM world_fishnet, jobs_classical_psha_hazard_maps, jobs_classical_psha_hazard_curves \
									WHERE jobs_classical_psha_hazard_curves.job_id = %s \
									AND jobs_classical_psha_hazard_curves.sa_period = %s \
									AND jobs_classical_psha_hazard_curves.statistics = 'mean' \
									AND jobs_classical_psha_hazard_curves.cell_id = world_fishnet.id \
									AND jobs_classical_psha_hazard_curves.id = jobs_classical_psha_hazard_maps.location_id \
									AND jobs_classical_psha_hazard_maps.poe = %s \
									GROUP BY world_fishnet.id", [job_id, sa_period, poe])

				else:
					cursor.execute("SELECT world_fishnet.id, ST_AsGeoJSON(world_fishnet.cell), AVG(jobs_classical_psha_hazard_maps.iml)  \
									FROM world_fishnet, jobs_classical_psha_hazard_maps, jobs_classical_psha_hazard_curves \
									WHERE jobs_classical_psha_hazard_curves.job_id = %s \
									AND jobs_classical_psha_hazard_curves.imt = %s \
									AND jobs_classical_psha_hazard_curves.statistics = 'mean' \
									AND jobs_classical_psha_hazard_curves.cell_id = world_fishnet.id \
									AND jobs_classical_psha_hazard_curves.id = jobs_classical_psha_hazard_maps.location_id \
									AND jobs_classical_psha_hazard_maps.poe = %s \
									GROUP BY world_fishnet.id", [job_id, imt, poe])

				cells = cursor.fetchall()
				data = list( {'id': cell[0], 'value': float("{0:.4f}".format(cell[2])) } for cell in cells)
				d.append({'imt': imt, 'quantile': None, 'poe': poe, 'values': data})

				if 'geo_json' not in locals():
					geo_json = get_geojson(cells)

		return HttpResponse(json.dumps({'hazard': d,
										'geojson': geo_json,
										'job': job_json }), content_type="application/json")

	else:
		return HttpResponse(json.dumps({'job': job_json }), content_type="application/json")



@login_required
def results_psha_hazard_curves_ajax(request, job_id):
	job = Classical_PSHA_Hazard.objects.get(pk=job_id, user=request.user)
	
	job_json = serializers.serialize("json", [job])
	job_json = json.loads(job_json)
	
	cell_id = request.GET.get('cell')

	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT ST_X(location), ST_Y(location), location \
					FROM jobs_classical_psha_hazard_curves \
					WHERE cell_id = %s and job_id = %s", [cell_id, job_id])
	points = [{ 'lon': pt[0], 'lat': pt[1], 'location': pt[2] } for pt in cursor.fetchall() ]

	if job.status == 'FINISHED':

		for point in points:

			curves = Classical_PSHA_Hazard_Curves.objects.filter(location=point['location'], job_id=job_id)
			curves_json = serializers.serialize("json", curves)
			curves_json = json.loads(curves_json)
			point['curves'] = curves_json

		return HttpResponse(json.dumps({'points': points,
										'job': job_json }), content_type="application/json")

	else:
		return HttpResponse(json.dumps({'job': job_json }), content_type="application/json")



########################
##     PSHA RISK    ##
########################


psha_risk_form_categories = {'general': ['name', 'description', 'random_seed', 'exposure_model', 'hazard',
								'asset_hazard_distance', 'region', 'lrem_steps_per_interval', 'asset_correlation'],
						'vulnerability': ['structural_vulnerability', 'non_structural_vulnerability', 'contents_vulnerability',
										'business_int_vulnerability', 'occupants_vulnerability'],
						'output': ['quantile_loss_curves', 'poes']}

class PSHARiskForm(forms.ModelForm):
	structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)

	class Meta:
		model = Classical_PSHA_Risk
		exclude = ['user', 'date_created', 'vulnerability_models', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'region': forms.HiddenInput(),
					}

@login_required	
def index_psha_risk(request):
	page = request.GET.get('page')
	jobs = Classical_PSHA_Risk.objects.filter(private=False).order_by('-date_created').exclude(id__in=[job.id for job in Event_Based_Risk.objects.all()])
	form = PSHARiskForm()

	form.fields['hazard'].queryset = Classical_PSHA_Hazard.objects.filter(user=request.user, status='FINISHED').order_by('-date_created')

	form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	return render(request, 'jobs/index_psha_risk.html', {'jobs': pagination( jobs, 10, page), 'form': form})

@login_required
def add_psha_risk(request):
	if request.method == 'POST':
		form = PSHARiskForm(request.POST)
		form.fields['hazard'].queryset = Classical_PSHA_Hazard.objects.filter(user=request.user, status='FINISHED').order_by('-date_created')
		form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')

		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			if form.cleaned_data["structural_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["structural_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["structural_vulnerability"])
			if form.cleaned_data["non_structural_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["non_structural_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["non_structural_vulnerability"])
			if form.cleaned_data["contents_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["contents_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["contents_vulnerability"])
			if form.cleaned_data["business_int_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["business_int_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["business_int_vulnerability"])
			if form.cleaned_data["occupants_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["occupants_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["occupants_vulnerability"])

			return redirect('results_psha_risk', job.id)
		else:
			# jobs = Classical_PSHA_Risk.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_psha_risk.html', {'form': form, 'categories': psha_risk_form_categories})
	else:
		form = PSHARiskForm()
		return render(request, 'jobs/new_psha_risk.html', {'form': form, 'categories': psha_risk_form_categories})

@login_required
def results_psha_risk(request, job_id):
	job = get_object_or_404(Classical_PSHA_Risk ,pk=job_id, user=request.user)
	vulnerability_types = Classical_PSHA_Risk_Vulnerability.objects.filter(job = job)

	economic_loss_types = []
	total = False
	for vulnerability in vulnerability_types:
		if vulnerability.vulnerability_model.type != 'occupants_vulnerability':
			economic_loss_types.append(vulnerability.vulnerability_model.type)
		if len(economic_loss_types) > 1:
			total = True
			break
	return render(request, 'jobs/results_psha_risk.html', {'job': job, 'total': total})


@login_required
def start_psha_risk(request, job_id):
	job = get_object_or_404(Classical_PSHA_Risk ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'psha_risk')
		return redirect('results_psha_risk', job.id)
	except:
		return render(request, 'jobs/results_psha_risk.html', {'job': job, 'connection_error': True})





@login_required
def results_psha_risk_maps_ajax(request, job_id):
	job = get_object_or_404(Classical_PSHA_Risk ,pk=job_id, user=request.user)
	vulnerability_types = Classical_PSHA_Risk_Vulnerability.objects.filter(job = job)
	vulnerabilities = list(vulnerability.vulnerability_model.type for vulnerability in vulnerability_types)

	try:
		if request.GET.get('vulnerability') == 'undefined':
			vulnerability 	= vulnerability_types[0].vulnerability_model.type
			if job.status == 'FINISHED':
				it_loss_values_agg 			= vulnerability_types[0].it_loss_values_agg
				at_loss_rates_agg 			= vulnerability_types[0].at_loss_rates_agg
				periods_agg 				= vulnerability_types[0].periods_agg
				default_periods_agg 		= vulnerability_types[0].default_periods_agg
				it_loss_values_table_agg 	= vulnerability_types[0].it_loss_values_table_agg
				aal_agg 					= vulnerability_types[0].aal_agg
				tce_agg 					= vulnerability_types[0].tce_agg
				it_loss_values_occ 			= vulnerability_types[0].it_loss_values_occ
				at_loss_rates_occ 			= vulnerability_types[0].at_loss_rates_occ
				periods_occ 				= vulnerability_types[0].periods_occ
				default_periods_occ 		= vulnerability_types[0].default_periods_occ
				it_loss_values_table_occ 	= vulnerability_types[0].it_loss_values_table_occ
				aal_occ 					= vulnerability_types[0].aal_occ
				tce_occ 					= vulnerability_types[0].tce_occ


			else:
				it_loss_values_agg 			= None
				at_loss_rates_agg 			= None
				periods_agg 				= None
				default_periods_agg 		= None
				it_loss_values_table_agg 	= None
				aal_agg 					= None
				tce_agg 					= None
				it_loss_values_occ 			= None
				at_loss_rates_occ 			= None
				periods_occ 				= None
				default_periods_occ 		= None
				it_loss_values_table_occ 	= None
				aal_occ 					= None
				tce_occ 					= None
		
		else:
			vulnerability 	= request.GET.get('vulnerability')
			vm 				= Classical_PSHA_Risk_Vulnerability.objects.get(job = job,
															vulnerability_model__type = vulnerability)
			if job.status == 'FINISHED':
				it_loss_values_agg 			= vm.it_loss_values_agg
				at_loss_rates_agg 			= vm.at_loss_rates_agg
				periods_agg 				= vm.periods_agg
				default_periods_agg 		= vm.default_periods_agg
				it_loss_values_table_agg 	= vm.it_loss_values_table_agg
				aal_agg 					= vm.aal_agg
				tce_agg 					= vm.tce_agg
				it_loss_values_occ 			= vm.it_loss_values_occ
				at_loss_rates_occ 			= vm.at_loss_rates_occ
				periods_occ 				= vm.periods_occ
				default_periods_occ 		= vm.default_periods_occ
				it_loss_values_table_occ 	= vm.it_loss_values_table_occ
				aal_occ 					= vm.aal_occ
				tce_occ 					= vm.tce_occ

			else:
				it_loss_values_agg 			= None
				at_loss_rates_agg 			= None
				periods_agg 				= None
				default_periods_agg 		= None
				it_loss_values_table_agg 	= None
				aal_agg 					= None
				tce_agg 					= None
				it_loss_values_occ 			= None
				at_loss_rates_occ 			= None
				periods_occ 				= None
				default_periods_occ 		= None
				it_loss_values_table_occ 	= None
				aal_occ 					= None
				tce_occ 					= None

	except:
		vulnerability 	= vulnerability_types[0].vulnerability_model.type
		if job.status == 'FINISHED':
				it_loss_values_agg 			= vulnerability_types[0].it_loss_values_agg
				at_loss_rates_agg 			= vulnerability_types[0].at_loss_rates_agg
				periods_agg 				= vulnerability_types[0].periods_agg
				default_periods_agg 		= vulnerability_types[0].default_periods_agg
				it_loss_values_table_agg 	= vulnerability_types[0].it_loss_values_table_agg
				aal_agg 					= vulnerability_types[0].aal_agg
				tce_agg 					= vulnerability_types[0].tce_agg
				it_loss_values_occ 			= vulnerability_types[0].it_loss_values_occ
				at_loss_rates_occ 			= vulnerability_types[0].at_loss_rates_occ
				periods_occ 				= vulnerability_types[0].periods_occ
				default_periods_occ 		= vulnerability_types[0].default_periods_occ
				it_loss_values_table_occ 	= vulnerability_types[0].it_loss_values_table_occ
				aal_occ 					= vulnerability_types[0].aal_occ
				tce_occ 					= vulnerability_types[0].tce_occ
		else:
				it_loss_values_agg 			= None
				at_loss_rates_agg 			= None
				periods_agg 				= None
				default_periods_agg 		= None
				it_loss_values_table_agg 	= None
				aal_agg 					= None
				tce_agg 					= None
				it_loss_values_occ 			= None
				at_loss_rates_occ 			= None
				periods_occ 				= None
				default_periods_occ 		= None
				it_loss_values_table_occ 	= None
				aal_occ 					= None
				tce_occ 					= None

	pml = {
				'it_loss_values_agg' 		: it_loss_values_agg,
				'at_loss_rates_agg' 		: at_loss_rates_agg,
				'periods_agg' 				: periods_agg,
				'default_periods_agg' 		: default_periods_agg,
				'it_loss_values_table_agg' 	: it_loss_values_table_agg,
				'aal_agg' 					: aal_agg,
				'tce_agg' 					: tce_agg,
				'it_loss_values_occ' 		: it_loss_values_occ,
				'at_loss_rates_occ' 		: at_loss_rates_occ,
				'periods_occ' 				: periods_occ,
				'default_periods_occ' 		: default_periods_occ,
				'it_loss_values_table_occ' 	: it_loss_values_table_occ,
				'aal_occ' 					: aal_occ,
				'tce_occ' 					: tce_occ
			}

	level = int(request.GET.get('level'))
	
	try:
		region = int(request.GET.get('region'))
	except:
		region = None

	taxonomy = request.GET.get('taxonomy')

	try:
		poe = float(request.GET.get('poe'))
	except:
		poe = job.poes[0]

	statistics = request.GET.get('statistics')
	insured = request.GET.get('insured')

	if insured == 'false':
		insured = False
	else:
		insured = True


	cursor = connection.cursor()

	if level == 3:

		if request.GET.get('taxonomy') != 'undefined':
			taxonomy_id = request.GET.get('taxonomy')

			try:
				statistics = float(statistics)
				cursor.execute('SELECT eng_models_asset.id, eng_models_asset.name, \
								jobs_classical_psha_risk_loss_maps.mean, jobs_classical_psha_risk_loss_maps.stddev, \
								ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability,eng_models_asset, jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = %s', [job.id, vulnerability, statistics, poe, insured, taxonomy_id ,region])

			except:
				cursor.execute("SELECT eng_models_asset.id , eng_models_asset.name , ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location), \
								jobs_classical_psha_risk_loss_maps.mean, jobs_classical_psha_risk_loss_maps.stddev \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = %s", [job.id, vulnerability, poe, insured, taxonomy_id ,region])

			regions = cursor.fetchall()


		else:

			try:
				statistics = float(statistics)
				cursor.execute('SELECT eng_models_asset.id , eng_models_asset.name, \
								jobs_classical_psha_risk_loss_maps.mean, jobs_classical_psha_risk_loss_maps.stddev, \
								ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = %s ', [job.id, vulnerability, quantile, poe, insured, region])
				regions = cursor.fetchall()


				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [job.id, vulnerability, quantile, poe, insured, region])
				taxonomies = cursor.fetchall()

			except:
				cursor.execute("SELECT eng_models_asset.id , eng_models_asset.name, \
								jobs_classical_psha_risk_loss_maps.mean, jobs_classical_psha_risk_loss_maps.stddev, \
								ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id =  %s ", [job.id, vulnerability, poe, insured, region])
				regions = cursor.fetchall()


				cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = %s \
								GROUP BY eng_models_building_taxonomy.id", [job.id, vulnerability, poe, insured, region])
				taxonomies = cursor.fetchall()


	elif level == 2:

		if request.GET.get('taxonomy') != 'undefined':
			taxonomy_id = request.GET.get('taxonomy')

			try:
				statistics = float(statistics)
				cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability,eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s\
								GROUP BY world_adm_2.id', [job.id, vulnerability, statistics, poe, insured, taxonomy_id ,region])

			except:
				cursor.execute("SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s\
								GROUP BY world_adm_2.id", [job.id, vulnerability, poe, insured, taxonomy_id ,region])

			regions = cursor.fetchall()


		else:

			try:
				statistics = float(statistics)
				cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY world_adm_2.id', [job.id, vulnerability, quantile, poe, insured, region])
				regions = cursor.fetchall()


				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [job.id, vulnerability, quantile, poe, insured, region])
				taxonomies = cursor.fetchall()

			except:
				cursor.execute("SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY world_adm_2.id", [job.id, vulnerability, poe, insured, region])
				regions = cursor.fetchall()


				cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = %s \
								GROUP BY eng_models_building_taxonomy.id", [job.id, vulnerability, poe, insured, region])
				taxonomies = cursor.fetchall()



	elif level == 1:

		if request.GET.get('taxonomy') != 'undefined':
			taxonomy_id = request.GET.get('taxonomy')

			try:
				statistics = float(statistics)

				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [job.id, vulnerability, quantile, poe, insured, taxonomy_id ,region])

			except:
				cursor.execute("SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id", [job.id, vulnerability, poe, insured, taxonomy_id ,region])
			regions = cursor.fetchall()

		else:
			try:
				statistics = float(statistics)

				cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id', [job.id, vulnerability, quantile, poe, insured, region])
				regions = cursor.fetchall()


				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY eng_models_building_taxonomy.id', [job.id, vulnerability, quantile, poe, insured, region])
				taxonomies = cursor.fetchall()

			except:
				cursor.execute("SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY world_adm_1.id", [job.id, vulnerability, poe, insured, region])
				regions = cursor.fetchall()


				cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_adm_1.country_id = %s \
								GROUP BY eng_models_building_taxonomy.id", [job.id, vulnerability, poe, insured, region])
				taxonomies = cursor.fetchall()



	else: #WORLD
		if request.GET.get('taxonomy') != 'undefined': 
			taxonomy_id = int(request.GET.get('taxonomy'))

			try:
				statistics = float(statistics)
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id', [job.id, vulnerability, statistics, poe, insured, taxonomy_id])

			except:
				cursor.execute("SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id", [job.id, vulnerability, poe, insured, taxonomy_id])
			regions = cursor.fetchall()
		else:
			try:
				statistics = float(statistics)
				cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id', [job.id, vulnerability, quantile, poe, insured])
				regions = cursor.fetchall()

				cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.quantile = %s \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								GROUP BY eng_models_building_taxonomy.id', [job.id, vulnerability, quantile, poe, insured])
				taxonomies = cursor.fetchall()
			
			except:
				cursor.execute("SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								AND eng_models_asset.adm_2_id = world_adm_2.id \
								AND world_adm_2.adm_1_id = world_adm_1.id \
								AND world_country.id = world_adm_1.country_id \
								GROUP BY world_country.id", [job.id, vulnerability, poe, insured])
				regions = cursor.fetchall()
				
				cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
								sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
								FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_building_taxonomy ,eng_models_asset, \
								jobs_classical_psha_risk_loss_maps \
								WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
								AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
								AND eng_models_vulnerability_model.type = %s \
								AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
								AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
								AND jobs_classical_psha_risk_loss_maps.poe = %s \
								AND jobs_classical_psha_risk_loss_maps.insured = %s \
								AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
								AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
								GROUP BY eng_models_building_taxonomy.id", [job.id, vulnerability, poe, insured])
				taxonomies = cursor.fetchall()

	if level == 3:
		regions_data = list( {'id': region[0], 'name': region[1], 'value': float("{0:.4f}".format(region[2])), 'stddev': region[3], 'lon': region[4], 'lat': region[5] } for region in regions)
		geo_json = None
	else:
		regions_data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
		geo_json = get_geojson_countries(regions)
	

	try:
		taxonomies_data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
	except:
		taxonomies_data = []

	job_json = serializers.serialize("json", [job])
	job_json = json.loads(job_json)

	exp_json = serializers.serialize("json", [job.exposure_model])
	exp_json = json.loads(exp_json)

	return HttpResponse(json.dumps({'job': job_json,
									'exposure_model': exp_json,
									'losses_per_region': regions_data,
									'losses_per_taxonomy': taxonomies_data,
									'vulnerability': vulnerability,
									'vulnerabilities': vulnerabilities,
									'poe': poe,
									'statistics': statistics,
									'geojson': geo_json,
									'pml': pml }), content_type="application/json")




@login_required
def results_psha_risk_locations_ajax(request, job_id):
	job = Classical_PSHA_Risk.objects.get(pk=job_id, user=request.user)

	adm_2_id = request.GET.get('country')

	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location), world_adm_2.name \
					FROM jobs_classical_psha_risk_vulnerability, jobs_classical_psha_risk_loss_maps, eng_models_asset, world_adm_2 \
					WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
					AND jobs_classical_psha_risk_loss_maps.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
					AND jobs_classical_psha_risk_loss_maps.asset_id = eng_models_asset.id \
					AND eng_models_asset.adm_2_id = world_adm_2.id \
					AND world_adm_2.id = %s ", [job.id, adm_2_id])
	points = [{ 'lon': pt[0],
				'lat': pt[1],
				'adm_2': pt[2]} for pt in cursor.fetchall() ]

	if job.status == 'FINISHED':
		return HttpResponse(json.dumps({'locations': points}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'locations': None }), content_type="application/json")


@login_required
def results_psha_risk_curves_ajax(request, job_id):
	job = Classical_PSHA_Risk.objects.get(pk=job_id, user=request.user)

	vulnerability = request.GET.get('vulnerability')
	asset = request.GET.get('asset')

	statistics = request.GET.get('statistics')
	insured = request.GET.get('insured')

	if insured == 'false':
		insured = False
	else:
		insured = True

	cursor = connection.cursor()

	try:
		statistics = float(statistics)
		cursor.execute('SELECT eng_models_asset.id, eng_models_asset.name, \
						jobs_classical_psha_risk_loss_curves.loss_ratios, jobs_classical_psha_risk_loss_curves.poes, \
						jobs_classical_psha_risk_loss_curves.average_loss_ratio, jobs_classical_psha_risk_loss_curves.stddev_loss_ratio, \
						jobs_classical_psha_risk_loss_curves.asset_value \
						FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_curves \
						WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
						AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
						AND eng_models_vulnerability_model.type = %s \
						AND jobs_classical_psha_risk_loss_curves.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
						AND jobs_classical_psha_risk_loss_curves.quantile = %s \
						AND jobs_classical_psha_risk_loss_curves.insured = %s \
						AND eng_models_asset.id = %s \
						AND eng_models_asset.id = jobs_classical_psha_risk_loss_curves.asset_id ', [job.id, vulnerability, statistics, insured, asset])

	except:
		cursor.execute("SELECT eng_models_asset.id , eng_models_asset.name, \
						jobs_classical_psha_risk_loss_curves.loss_ratios, jobs_classical_psha_risk_loss_curves.poes, \
						jobs_classical_psha_risk_loss_curves.average_loss_ratio, jobs_classical_psha_risk_loss_curves.stddev_loss_ratio, \
						jobs_classical_psha_risk_loss_curves.asset_value \
						FROM eng_models_vulnerability_model, jobs_classical_psha_risk_vulnerability, eng_models_asset, jobs_classical_psha_risk_loss_curves \
						WHERE jobs_classical_psha_risk_vulnerability.job_id = %s \
						AND jobs_classical_psha_risk_vulnerability.vulnerability_model_id = eng_models_vulnerability_model.id \
						AND eng_models_vulnerability_model.type = %s \
						AND jobs_classical_psha_risk_loss_curves.vulnerability_model_id = jobs_classical_psha_risk_vulnerability.id \
						AND jobs_classical_psha_risk_loss_curves.statistics = 'mean' \
						AND jobs_classical_psha_risk_loss_curves.insured = %s \
						AND eng_models_asset.id = %s \
						AND eng_models_asset.id = jobs_classical_psha_risk_loss_curves.asset_id ", [job.id, vulnerability, insured, asset])
	
	asset = cursor.fetchone()
	asset = {'id': asset[0],
			'name': asset[1],
			'loss_ratios': asset[2],
			'poes': asset[3],
			'average_loss_ratio': asset[4],
			'stddev_loss_ratio': asset[5],
			'asset_value': asset[6]
			}

	return HttpResponse(json.dumps(asset), content_type="application/json")


###############################
##     EVENT BASED HAZARD    ##
###############################


event_based_form_categories = {'general': ['name', 'description', 'investigation_time', 'truncation_level', 'max_distance', 'random_seed', 'imt_l'],
						'locations': ['locations_type', 'exposure_model', 'region', 'grid_spacing', 'locations'],
						'rupture': ['rupture_mesh_spacing', 'width_of_mfd_bin', 'area_source_discretization'],
						'sites': ['sites_type', 'site_model', 'vs30', 'vs30type', 'z1pt0', 'z2pt5'],
						'logic_trees': ['n_lt_samples', 'gmpe_logic_tree', 'sm_logic_tree', 'ses_per_logic_tree_path'],
						'imts': ['structural_vulnerability', 'non_structural_vulnerability', 'contents_vulnerability',
								'business_int_vulnerability', 'occupants_vulnerability'],
						'outputs': ['quantile_hazard_curves', 'poes']}


class EventBased_HazardForm(forms.ModelForm):
	structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)


	def clean(self):
		form_data = clean_hazard(self, self.cleaned_data)
		return form_data

	class Meta:
		model = Event_Based_Hazard
		exclude = ['user', 'date_created', 'status', 'oq_id', 'ini_file']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'quantile_hazard_curves': forms.TextInput(attrs={'placeholder': 'Ex: 0.05, 0.5, 0.95'}),
					'poes': forms.TextInput(attrs={'placeholder': 'Ex: 0.2, 0.5, 0.9 ...'}),
					'region': forms.HiddenInput(),
					'locations': forms.HiddenInput(),
					'imt_l': forms.HiddenInput(),
					}

@login_required	
def index_event_based_hazard(request):
	page = request.GET.get('page')
	jobs = Event_Based_Hazard.objects.filter(private=False).order_by('-date_created')
	form = EventBased_HazardForm()
	form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')


	return render(request, 'jobs/index_event_based_hazard.html', {'jobs': pagination( jobs, 10, page), 'form': form, 'categories': event_based_form_categories})


@login_required
def add_event_based_hazard(request):
	if request.method == 'POST':
		form = EventBased_HazardForm(request.POST)

		form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')

		form.fields["exposure_model"].queryset = Exposure_Model.objects.filter(exposure_model_contributor__contributor=request.user).order_by('-date_created')


		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			return redirect('results_event_based_hazard', job.id)
		else:
			# jobs = Event_Based_Hazard.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_event_based_hazard.html', {'form': form, 'categories': event_based_form_categories})
	else:
		form = EventBased_HazardForm()
		return render(request, 'jobs/new_event_based_hazard.html', {'form': form, 'categories': event_based_form_categories })

@login_required
def results_event_based_hazard(request, job_id):
	job = get_object_or_404(Event_Based_Hazard ,pk=job_id, user=request.user)
	#imts = job.imt_l.keys()
	return render(request, 'jobs/results_event_based_hazard.html', {'job': job})

@login_required
def start_event_based_hazard(request, job_id):
	job = get_object_or_404(Event_Based_Hazard ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'event_based_hazard')
		return redirect('results_event_based_hazard', job.id)
	except:
		return render(request, 'jobs/results_event_based_hazard.html', {'job': job, 'connection_error': True})



#############################
##     EVENT BASED RISK    ##
#############################


event_based_risk_form_categories = {'general': ['name', 'description', 'random_seed', 'exposure_model', 'hazard',
												'asset_hazard_distance', 'region', 'lrem_steps_per_interval', 'asset_correlation', 'loss_curve_resolution'],
									'vulnerability': ['structural_vulnerability', 'non_structural_vulnerability', 'contents_vulnerability',
													'business_int_vulnerability', 'occupants_vulnerability'],
									'output': ['quantile_loss_curves', 'poes']}


class EventBased_RiskForm(forms.ModelForm):
	hazard_event_based = forms.ModelChoiceField(queryset = Event_Based_Hazard.objects.filter(status='FINISHED'), required=False)
	structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='structural_vulnerability'), required=False)
	non_structural_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='nonstructural_vulnerability'), required=False)
	contents_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='contents_vulnerability'), required=False)
	business_int_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='business_interruption_vulnerability'), required=False)
	occupants_vulnerability = forms.ModelChoiceField(queryset = Vulnerability_Model.objects.filter(type='occupants_vulnerability'), required=False)

	
	# def clean(self):
	# 	form_data = self.cleaned_data
	# 	if 'occupants_vulnerability' in form_data and form_data['insured_losses']:
	# 		self.add_error(None, 'You cannot calculate insured losses with an occupants vulnerability model')

	# 	if 'hazard_event_based' in form_data and 'exposure_model' in form_data and 'region'in form_data: 

	# 		cursor = connection.cursor()
	# 		#cursor.execute('SELECT ST_DWithin(region::geography, ST_GeomFromText(%s, 4326)::geography, %s) FROM jobs_scenario_hazard WHERE id = %s', [region.wkt, float(form_data['max_hazard_dist'])*1000, hazard.id])
	# 		cursor.execute('SELECT ST_DWithin(jobs_classical_psha_hazard.region::geography, point.location::geography, %s) \
	# 						FROM jobs_classical_psha_hazard, (SELECT DISTINCT location \
	# 															FROM eng_models_asset \
	# 															WHERE model_id = %s\
	# 															AND ST_Within(location, ST_GeomFromText(%s, 4326))) AS point \
	# 						WHERE jobs_classical_psha_hazard.id = %s \
	# 						ORDER BY ST_Distance(point.location::geography, jobs_classical_psha_hazard.region::geography) DESC\
	# 						LIMIT 1', [float(form_data['hazard_event_based'].max_distance)*1000, form_data['exposure_model'].id, form_data['region'].wkt, form_data['hazard_event_based'].id])
			
	# 		try:
	# 			check = cursor.fetchone()[0]
	# 		except:
	# 			self.add_error(None, 'There is no assets on the region you selected')
	# 			check = False

	# 		if not check:
	# 			self._errors["max_hazard_dist"] = "The distance between the hazard and the risk is greater than the specified."
	# 			del form_data['max_hazard_dist']

	# 	return form_data



	class Meta:
		model = Event_Based_Risk
		exclude = ['user', 'date_created', 'vulnerability_models', 'status', 'oq_id', 'ini_file', 'hazard']
		widgets = {
					'description': forms.Textarea(attrs={'rows':5}),
					'region': forms.HiddenInput(),
					}

@login_required	
def index_event_based_risk(request):
	page = request.GET.get('page')
	jobs = Event_Based_Risk.objects.filter(private=False).order_by('-date_created')
	form = EventBased_RiskForm()

	form.fields['hazard_event_based'].queryset = Event_Based_Hazard.objects.filter(user=request.user, status='FINISHED').order_by('-date_created')

	form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
	form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
	form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
	form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
	form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')
	
	return render(request, 'jobs/index_event_based_risk.html', {'jobs': pagination( jobs, 10, page), 'form': form, 'categories': event_based_risk_form_categories})

@login_required
def add_event_based_risk(request):
	if request.method == 'POST':
		form = EventBased_RiskForm(request.POST)
		form.fields['hazard_event_based'].queryset = Event_Based_Hazard.objects.filter(user=request.user, status='FINISHED').order_by('-date_created')
		form.fields["structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='structural_vulnerability').order_by('-date_created')
		form.fields["non_structural_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='nonstructural_vulnerability').order_by('-date_created')
		form.fields["contents_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='contents_vulnerability').order_by('-date_created')
		form.fields["business_int_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='business_interruption_vulnerability').order_by('-date_created')
		form.fields["occupants_vulnerability"].queryset = Vulnerability_Model.objects.filter(vulnerability_model_contributor__contributor=request.user).filter(type='occupants_vulnerability').order_by('-date_created')

		if form.is_valid():
			job = form.save(commit=False)
			job.date_created = timezone.now()
			job.user = request.user
			job.save()

			if form.cleaned_data["structural_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["structural_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["structural_vulnerability"])
			if form.cleaned_data["non_structural_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["non_structural_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["non_structural_vulnerability"])
			if form.cleaned_data["contents_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["contents_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["contents_vulnerability"])
			if form.cleaned_data["business_int_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["business_int_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["business_int_vulnerability"])
			if form.cleaned_data["occupants_vulnerability"] != None:
				job_vul = Classical_PSHA_Risk_Vulnerability(job = job, vulnerability_model = form.cleaned_data["occupants_vulnerability"])
				job_vul.save()
				#job.vulnerability_models.add(form.cleaned_data["occupants_vulnerability"])

			return redirect('results_event_based_risk', job.id)
		else:
			# jobs = Event_Based_Risk.objects.filter(user=request.user).order_by('-date_created')
			return render(request, 'jobs/new_event_based_risk.html', {'form': form, 'categories': event_based_risk_form_categories})
	else:
		form = PSHARiskForm()
		return render(request, 'jobs/new_event_based_risk.html', {'form': form, 'categories': event_based_risk_form_categories})

@login_required
def results_event_based_risk(request, job_id):
	job = get_object_or_404(Event_Based_Risk ,pk=job_id, user=request.user)
	vulnerability_types = Classical_PSHA_Risk_Vulnerability.objects.filter(job = job)

	economic_loss_types = []
	total = False
	for vulnerability in vulnerability_types:
		if vulnerability.vulnerability_model.type != 'occupants_vulnerability':
			economic_loss_types.append(vulnerability.vulnerability_model.type)
		if len(economic_loss_types) > 1:
			total = True
			break
	return render(request, 'jobs/results_event_based_risk.html', {'job': job, 'total': total})


@login_required
def start_event_based_risk(request, job_id):
	job = get_object_or_404(Event_Based_Risk ,pk=job_id, user=request.user)
	try:
		queue_job(job, 'event_based_risk')
		return redirect('results_event_based_risk', job.id)
	except:
		return render(request, 'jobs/results_event_based_risk.html', {'job': job, 'connection_error': True})


