

# @login_required
# def results_psha_risk_maps_ajax(request, job_id):
# 	job = get_object_or_404(Classical_PSHA_Risk ,pk=job_id, user=request.user)
# 	vulnerability_types = Classical_PSHA_Risk_Vulnerability.objects.filter(job = job)

# 	cursor = connection.cursor()
# 	d = []

# 	economic_loss_types = []

# 	for vulnerability in vulnerability_types:

# 		info_per_region = []
# 		info_per_taxonomy = []

# 		if request.GET.get('adm_1') != 'undefined':
# 			adm_1_id = request.GET.get('adm_1')

# 			if request.GET.get('taxonomy') != 'undefined':
# 				taxonomy_id = request.GET.get('taxonomy')

# 				for poe in job.poes:

# 					for quantile in job.quantile_loss_curves:

# 						cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.taxonomy_id = %s \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = %s\
# 										GROUP BY world_adm_2.id', [vulnerability.id, quantile, poe, taxonomy_id ,adm_1_id])

# 						regions = cursor.fetchall()
# 						data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 						info_per_region.append({'quantile': quantile, 'poe': poe, 'values': data})


# 					cursor.execute("SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.taxonomy_id = %s \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = %s\
# 									GROUP BY world_adm_2.id", [vulnerability.id, poe, taxonomy_id ,adm_1_id])

# 					regions = cursor.fetchall()
# 					data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 					info_per_region.append({'quantile': None, 'poe': poe, 'values': data})

# 			else:

# 				for poe in job.poes:

# 					for quantile in job.quantile_loss_curves:

# 						cursor.execute('SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = %s \
# 										GROUP BY world_adm_2.id', [vulnerability.id, quantile, poe, adm_1_id])
# 						regions = cursor.fetchall()
# 						data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 						info_per_region.append({'quantile': quantile, 'poe': poe, 'values': data})

# 						cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
# 										FROM eng_models_building_taxonomy ,eng_models_asset, \
# 										jobs_classical_psha_risk_loss_maps, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = %s \
# 										GROUP BY eng_models_building_taxonomy.id', [vulnerability.id, quantile, poe, adm_1_id])
# 						taxonomies = cursor.fetchall()
# 						data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
# 						info_per_taxonomy.append({'quantile': quantile, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT world_adm_2.id, ST_AsGeoJSON(world_adm_2.geom) , world_adm_2.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = %s \
# 									GROUP BY world_adm_2.id", [vulnerability.id, poe, adm_1_id])
# 					regions = cursor.fetchall()
# 					data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 					info_per_region.append({'quantile': None, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
# 									FROM eng_models_building_taxonomy ,eng_models_asset, \
# 									jobs_classical_psha_risk_loss_maps, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = %s \
# 									GROUP BY eng_models_building_taxonomy.id", [vulnerability.id, poe, adm_1_id])
# 					taxonomies = cursor.fetchall()
# 					data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
# 					info_per_taxonomy.append({'quantile': None, 'poe': poe, 'values': data})


# 		elif request.GET.get('country') != 'undefined':
# 			country_id = request.GET.get('country')

# 			if request.GET.get('taxonomy') != 'undefined':
# 				taxonomy_id = request.GET.get('taxonomy')

# 				for poe in job.poes:

# 					for quantile in job.quantile_loss_curves:

# 						cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
# 										FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.taxonomy_id = %s \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = world_adm_1.id \
# 										AND world_adm_1.country_id = %s \
# 										GROUP BY world_adm_1.id', [vulnerability.id, quantile, poe, taxonomy_id ,country_id])
# 						regions = cursor.fetchall()
# 						data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 						info_per_region.append({'quantile': quantile, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev)  \
# 									FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.taxonomy_id = %s \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = world_adm_1.id \
# 									AND world_adm_1.country_id = %s \
# 									GROUP BY world_adm_1.id", [vulnerability.id, poe, taxonomy_id ,country_id])
# 					regions = cursor.fetchall()
# 					data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 					info_per_region.append({'quantile': None, 'poe': poe, 'values': data})
# 			else:

# 				for poe in job.poes:

# 					for quantile in job.quantile_loss_curves:

# 						cursor.execute('SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = world_adm_1.id \
# 										AND world_adm_1.country_id = %s \
# 										GROUP BY world_adm_1.id', [vulnerability.id, quantile, poe, country_id])
# 						regions = cursor.fetchall()
# 						data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 						info_per_region.append({'quantile': quantile, 'poe': poe, 'values': data})

# 						cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_building_taxonomy ,eng_models_asset, \
# 										jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = world_adm_1.id \
# 										AND world_adm_1.country_id = %s \
# 										GROUP BY eng_models_building_taxonomy.id', [vulnerability.id, quantile, poe, country_id])
# 						taxonomies = cursor.fetchall()
# 						data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
# 						info_per_taxonomy.append({'quantile': quantile, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT world_adm_1.id, ST_AsGeoJSON(world_adm_1.geom) , world_adm_1.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = world_adm_1.id \
# 									AND world_adm_1.country_id = %s \
# 									GROUP BY world_adm_1.id", [vulnerability.id, poe, country_id])
# 					regions = cursor.fetchall()
# 					data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 					info_per_region.append({'quantile': None, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_building_taxonomy ,eng_models_asset, \
# 									jobs_classical_psha_risk_loss_maps, world_adm_1, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = world_adm_1.id \
# 									AND world_adm_1.country_id = %s \
# 									GROUP BY eng_models_building_taxonomy.id", [vulnerability.id, poe, country_id])
# 					taxonomies = cursor.fetchall()
# 					data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
# 					info_per_taxonomy.append({'quantile': None, 'poe': poe, 'values': data})
		

# 		else:
# 			if request.GET.get('taxonomy') != 'undefined':
# 				taxonomy_id = request.GET.get('taxonomy')
# 				for poe in job.poes:

# 					for quantile in job.quantile_loss_curves:
# 						cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.taxonomy_id = %s \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = world_adm_1.id \
# 										AND world_country.id = world_adm_1.country_id \
# 										GROUP BY world_country.id', [vulnerability.id, quantile, poe, taxonomy_id])
# 						regions = cursor.fetchall()
# 						data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 						info_per_region.append({'quantile': quantile, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.taxonomy_id = %s \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = world_adm_1.id \
# 									AND world_country.id = world_adm_1.country_id \
# 									GROUP BY world_country.id", [vulnerability.id, poe, taxonomy_id])
# 					regions = cursor.fetchall()
# 					data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 					info_per_region.append({'quantile': None, 'poe': poe, 'values': data})

# 			else:
# 				for poe in job.poes:

# 					for quantile in job.quantile_loss_curves:
# 						cursor.execute('SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										AND eng_models_asset.adm_2_id = world_adm_2.id \
# 										AND world_adm_2.adm_1_id = world_adm_1.id \
# 										AND world_country.id = world_adm_1.country_id \
# 										GROUP BY world_country.id', [vulnerability.id, quantile, poe])
# 						regions = cursor.fetchall()
# 						data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 						info_per_region.append({'quantile': quantile, 'poe': poe, 'values': data})

# 						cursor.execute('SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
# 										sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 										FROM eng_models_building_taxonomy ,eng_models_asset, \
# 										jobs_classical_psha_risk_loss_maps \
# 										WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 										AND jobs_classical_psha_risk_loss_maps.quantile = %s \
# 										AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 										AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
# 										AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 										GROUP BY eng_models_building_taxonomy.id', [vulnerability.id, quantile, poe])
# 						taxonomies = cursor.fetchall()
# 						data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
# 						info_per_taxonomy.append({'quantile': quantile, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT world_country.id, ST_AsGeoJSON(world_country.geom_simp) , world_country.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_asset, jobs_classical_psha_risk_loss_maps, world_country, world_adm_1, world_adm_2 \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									AND eng_models_asset.adm_2_id = world_adm_2.id \
# 									AND world_adm_2.adm_1_id = world_adm_1.id \
# 									AND world_country.id = world_adm_1.country_id \
# 									GROUP BY world_country.id", [vulnerability.id, poe])
# 					regions = cursor.fetchall()
# 					data = list( {'id': region[0], 'name': region[2], 'value': float("{0:.4f}".format(region[3])), 'stddev': region[4] } for region in regions)
# 					info_per_region.append({'quantile': None, 'poe': poe, 'values': data})

# 					cursor.execute("SELECT eng_models_building_taxonomy.id ,eng_models_building_taxonomy.name, \
# 									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
# 									FROM eng_models_building_taxonomy ,eng_models_asset, \
# 									jobs_classical_psha_risk_loss_maps \
# 									WHERE jobs_classical_psha_risk_loss_maps.vulnerability_model_id = %s \
# 									AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
# 									AND jobs_classical_psha_risk_loss_maps.poe = %s \
# 									AND eng_models_asset.taxonomy_id = eng_models_building_taxonomy.id \
# 									AND eng_models_asset.id = jobs_classical_psha_risk_loss_maps.asset_id \
# 									GROUP BY eng_models_building_taxonomy.id", [vulnerability.id, poe])
# 					taxonomies = cursor.fetchall()
# 					data = list( {'id': taxonomy[0], 'name': taxonomy[1], 'value': float("{0:.4f}".format(taxonomy[2])), 'stddev': taxonomy[3] } for taxonomy in taxonomies)
# 					info_per_taxonomy.append({'quantile': None, 'poe': poe, 'values': data})
		

# 		if 'geo_json' not in locals():
# 			geo_json = get_geojson_countries(regions)


# 		if vulnerability.vulnerability_model.type != 'occupants_vulnerability':
# 			economic_loss_types.append(vulnerability.vulnerability_model.type)

# 		max_list = []
# 		for map in info_per_region:
# 			max_total = max( list( f['value'] for f in map['values'] ) )
# 			max_list.append(max_total)

# 		max_ = max(max_list)

# 		d.append({'name': vulnerability.vulnerability_model.type,
# 				'values_per_region': info_per_region,
# 				'values_per_taxonomy': info_per_taxonomy,
# 				'max': max_})	


# 	if len(economic_loss_types) > 1:
# 		pass
	
# 	job_json = serializers.serialize("json", [job])
# 	job_json = json.loads(job_json)

# 	exp_json = serializers.serialize("json", [job.exposure_model])
# 	exp_json = json.loads(exp_json)

# 	return HttpResponse(json.dumps({'job': job_json,
# 									'exposure_model': exp_json,
# 									'losses': d,
# 									'geojson': geo_json }), content_type="application/json")



#@login_required
#def results_psha_risk_locations_ajax(request, job_id):
#	job = Classical_PSHA_Risk.objects.get(pk=job_id, user=request.user)
#	vulnerability_types = Classical_PSHA_Risk_Vulnerability.objects.filter(job = job)
#
#	adm_2_id = request.GET.get('country')
#
#	d = []
#
#	cursor = connection.cursor()
#	
#	for vulnerability in vulnerability_types:
#
#		if request.GET.get('taxonomy') != 'undefined':
#			taxonomy_id = request.GET.get('taxonomy')
#
#			for poe in job.poes:
#
#				for quantile in job.quantile_loss_curves:
#
#					cursor.execute("SELECT ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location), world_adm_2.name, \
#									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
#									FROM jobs_classical_psha_risk_vulnerability, jobs_classical_psha_risk_loss_maps, eng_models_asset, world_adm_2 \
#									WHERE jobs_classical_psha_risk_vulnerability.id = %s\
#									AND jobs_classical_psha_risk_loss_maps.quantile = %s \
#									AND jobs_classical_psha_risk_loss_maps.poe = %s \
#									AND jobs_classical_psha_risk_loss_maps.asset_id = eng_models_asset.id \
#									AND eng_models_asset.adm_2_id = world_adm_2.id \
#									AND world_adm_2.id = %s \
#									GROUP BY eng_models_asset.location", [vulnerability.id, adm_2_id])
#
#				cursor.execute("SELECT ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location), world_adm_2.name, \
#					sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
#					FROM jobs_classical_psha_risk_vulnerability, jobs_classical_psha_risk_loss_maps, eng_models_asset, world_adm_2 \
#					WHERE jobs_classical_psha_risk_vulnerability.id = %s\
#					AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
#					AND jobs_classical_psha_risk_loss_maps.poe = %s \
#					AND jobs_classical_psha_risk_loss_maps.asset_id = eng_models_asset.id \
#					AND eng_models_asset.adm_2_id = world_adm_2.id \
#					AND world_adm_2.id = %s \
#					GROUP BY eng_models_asset.location", [vulnerability.id, adm_2_id])


#		else:
#
#			for poe in job.poes:
#
#				for quantile in job.quantile_loss_curves:
#
#					cursor.execute("SELECT ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location), world_adm_2.name, \
#									sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
#									FROM jobs_classical_psha_risk_vulnerability, jobs_classical_psha_risk_loss_maps, eng_models_asset, world_adm_2 \
#									WHERE jobs_classical_psha_risk_vulnerability.id = %s\
#									AND jobs_classical_psha_risk_loss_maps.quantile = %s \
#									AND jobs_classical_psha_risk_loss_maps.poe = %s \
#									AND jobs_classical_psha_risk_loss_maps.asset_id = eng_models_asset.id \
#									AND eng_models_asset.adm_2_id = world_adm_2.id \
#									AND world_adm_2.id = %s \
#									GROUP BY eng_models_asset.location", [vulnerability.id, adm_2_id])
#
#				cursor.execute("SELECT ST_X(eng_models_asset.location), ST_Y(eng_models_asset.location), world_adm_2.name, \
#					sum(jobs_classical_psha_risk_loss_maps.mean), sum(jobs_classical_psha_risk_loss_maps.stddev) \
#					FROM jobs_classical_psha_risk_vulnerability, jobs_classical_psha_risk_loss_maps, eng_models_asset, world_adm_2 \
#					WHERE jobs_classical_psha_risk_vulnerability.id = %s\
#					AND jobs_classical_psha_risk_loss_maps.statistics = 'mean' \
#					AND jobs_classical_psha_risk_loss_maps.poe = %s \
#					AND jobs_classical_psha_risk_loss_maps.asset_id = eng_models_asset.id \
#					AND eng_models_asset.adm_2_id = world_adm_2.id \
#					AND world_adm_2.id = %s \
#					GROUP BY eng_models_asset.location", [vulnerability.id, adm_2_id])
#
#		points = [{ 'lon': pt[0],
#					'lat': pt[1],
#					'adm_2': pt[2]} for pt in cursor.fetchall() ]
#
#	if job.status == 'FINISHED':
#		return HttpResponse(json.dumps({'locations': points}), content_type="application/json")
#	else:
#		return HttpResponse(json.dumps({'locations': None }), content_type="application/json")
#



# @login_required
# def results_psha_risk_curves_ajax(request, job_id):
# 	job = Classical_PSHA_Risk.objects.get(pk=job_id, user=request.user)
# 	vulnerability_types = Classical_PSHA_Risk_Vulnerability.objects.filter(job = job)

# 	job_json = serializers.serialize("json", [job])
# 	job_json = json.loads(job_json)
	
# 	adm_2_id = request.GET.get('country')
# 	lat = request.GET.get('lat')
# 	lon = request.GET.get('lon')

# 	location = 'POINT('+lon+' '+lat+')'

# 	d = []

# 	for vulnerability in vulnerability_types:

# 		cursor = connection.cursor()
# 		cursor.execute("SELECT eng_models_asset.name, \
# 						jobs_classical_psha_risk_loss_curves.statistics, jobs_classical_psha_risk_loss_curves.quantile, \
# 						jobs_classical_psha_risk_loss_curves.loss_ratios, jobs_classical_psha_risk_loss_curves.poes, \
# 						jobs_classical_psha_risk_loss_curves.average_loss_ratio, jobs_classical_psha_risk_loss_curves.stddev_loss_ratio, \
# 						jobs_classical_psha_risk_loss_curves.asset_value, jobs_classical_psha_risk_loss_curves.insured \
# 						FROM jobs_classical_psha_risk_loss_curves, eng_models_asset \
# 						WHERE jobs_classical_psha_risk_loss_curves.vulnerability_model_id = %s \
# 						AND jobs_classical_psha_risk_loss_curves.asset_id = eng_models_asset.id \
# 						AND eng_models_asset.adm_2_id = %s", [vulnerability.id, adm_2_id])
# 		points = [{ 'lon': pt[0],
# 					'lat': pt[1],
# 					'asset_name': pt[2],
# 					'statistics': pt[3],
# 					'quantile': pt[4],
# 					'loss_ratios': pt[5],
# 					'poes': pt[6],
# 					'average_loss_ratio': pt[7],
# 					'stddev_loss_ratio': pt[8],
# 					'asset_value': pt[9],
# 					'insured': pt[10]} for pt in cursor.fetchall() ]

# 		d.append({'name': vulnerability.vulnerability_model.type,
# 				'values': points })	

# 	if job.status == 'FINISHED':

# 		return HttpResponse(json.dumps({'curves': d,
# 										'job': job_json }), content_type="application/json")
# 	else:
# 		return HttpResponse(json.dumps({'job': job_json }), content_type="application/json")

