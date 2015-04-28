from xml.dom.minidom import parse
from eng_models.models import Asset, Building_Taxonomy
from django.contrib.gis.geos import Point
from django.utils import timezone



def start(object):

	model = parse(object.xml)
	data = model.getElementsByTagName('exposureModel')[0]

	################
	#INFO###########
	################

	#model_name = data.getAttribute('id')
	#taxonomySource = data.getAttribute('taxonomySource')
	#description = model.getElementsByTagName('description')[0].firstChild.nodeValue.strip()
	conversions = model.getElementsByTagName('conversions')

	area = conversions[0].getElementsByTagName('area')

	################
	#CONVERSIONS####
	################

	if area != []:
		area_type = area[0].getAttribute('type')
		area_unit = area[0].getAttribute('unit')
	else:
		area_type = None
		area_unit = None

	deductible = conversions[0].getElementsByTagName('deductible')[0]

	deductible_abs 					= 'true'
	insuranceLimit_abs 				= 'true'
	structural_cost_type 			= None
	structural_cost_unit 			= None
	non_structural_cost_type 		= None
	non_structural_cost_unit 		= None
	business_interruption_cost_type = None
	business_interruption_cost_unit = None
	contents_cost_type 				= None
	contents_cost_unit 				= None


	if deductible != []:
		deductible_abs = deductible.getAttribute('isAbsolute')

	insuranceLimit = conversions[0].getElementsByTagName('insuranceLimit')[0]

	if insuranceLimit != []:
		insuranceLimit_abs = deductible.getAttribute('isAbsolute')

	costTypes = conversions[0].getElementsByTagName('costTypes')[0].getElementsByTagName('costType')
	for cost in costTypes:
		if cost.getAttribute('name') == 'structural':
			structural_cost_type = cost.getAttribute('type')
			structural_cost_unit = cost.getAttribute('unit')
		if cost.getAttribute('name') == 'nonstructural':
			non_structural_cost_type = cost.getAttribute('type')
			non_structural_cost_unit = cost.getAttribute('unit')
		if cost.getAttribute('name') == 'business_interruption':
			business_interruption_cost_type = cost.getAttribute('type')
			business_interruption_cost_unit = cost.getAttribute('unit')
		if cost.getAttribute('name') == 'contents':
			contents_cost_type = cost.getAttribute('type')
			contents_cost_unit = cost.getAttribute('unit')

	object.deductible = deductible_abs
	object.insurance_limit = insuranceLimit_abs
	object.area_type = area_type
	object.area_unit = area_unit
	object.struct_cost_type = structural_cost_type
	object.struct_cost_currency = structural_cost_unit
	object.non_struct_cost_type = non_structural_cost_type
	object.non_struct_cost_currency =  non_structural_cost_unit
	object.contents_cost_type = contents_cost_type
	object.contents_cost_currency = contents_cost_unit
	object.business_int_cost_type = business_interruption_cost_type
	object.business_int_cost_currency = business_interruption_cost_unit
	#object.date_created = timezone.now()
	object.save()


	################
	#ASSETS#########
	################


	assets = model.getElementsByTagName('assets')[0].getElementsByTagName('asset')
	for asset in assets:
		
		structural_value 							= None
		structural_deductible_percentage 			= None
		structural_insuranceLimit_value 			= None
		retrofitting_cost 							= None

		non_structural_value 						= None
		non_structural_deductible_percentage 		= None
		non_structural_insuranceLimit_value 		= None

		contents_value 								= None
		contents_deductible_percentage 				= None
		contents_insuranceLimit_value 				= None
		
		business_interruption_value 				= None
		business_interruption_deductible_percentage = None
		business_interruption_insuranceLimit_value 	= None

		oc_day 										= None
		oc_night 									= None
		oc_transit 									= None

		asset_name = asset.getAttribute('id').strip()

		if asset.getAttribute('area'):
			area = asset.getAttribute('area').strip()
		else:
			area = None

		if asset.getAttribute('number'):
			number = asset.getAttribute('number').strip()
		else:
			number = None

		taxonomy = asset.getAttribute('taxonomy').strip()

		location = asset.getElementsByTagName('location')[0]
		lon = location.getAttribute('lon')
		lat = location.getAttribute('lat')

		
		costs = asset.getElementsByTagName('costs')[0].getElementsByTagName('cost')
		for cost in costs:
			
			if cost.getAttribute('type') == 'structural':
				structural_value = cost.getAttribute('value')
				if cost.getAttribute('retrofitted'):
					retrofitting_cost = cost.getAttribute('retrofitted')
				if ('deductible_abs' in locals() and deductible_abs == 'false'):
					structural_deductible_percentage = cost.getAttribute('deductible')
				if ('insuranceLimit_abs' in locals() and insuranceLimit_abs == 'false'):
					structural_insuranceLimit_value = cost.getAttribute('insuranceLimit')

			if cost.getAttribute('type') == 'nonstructural':
				non_structural_value = cost.getAttribute('value')
				if ('deductible_abs' in locals() and deductible_abs == 'false'):
					non_structural_deductible_percentage = cost.getAttribute('deductible')
				if ('insuranceLimit_abs' in locals() and insuranceLimit_abs == 'false'):
					non_structural_insuranceLimit_value = cost.getAttribute('insuranceLimit')

			if cost.getAttribute('type') == 'contents':
				contents_value = cost.getAttribute('value')
				if ('deductible_abs' in locals() and deductible_abs == 'false'):
					contents_deductible_percentage = cost.getAttribute('deductible')
				if ('insuranceLimit_abs' in locals() and insuranceLimit_abs == 'false'):
					contents_insuranceLimit_value = cost.getAttribute('insuranceLimit')

			if cost.getAttribute('type') == 'business_interruption':
				business_interruption_value = cost.getAttribute('value')
				if ('deductible_abs' in locals() and deductible_abs == 'false'):
					business_interruption_deductible_percentage = cost.getAttribute('deductible')
				if ('insuranceLimit_abs' in locals() and insuranceLimit_abs == 'false'):
					business_interruption_insuranceLimit_value = cost.getAttribute('insuranceLimit')

		occupancies = asset.getElementsByTagName('occupancies')[0].getElementsByTagName('occupancy')
		for oc in occupancies:
			if oc.getAttribute('period').lower() == 'day':
				oc_day = oc.getAttribute('occupants')
			if oc.getAttribute('period').lower() == 'night':
				oc_night = oc.getAttribute('occupants')
			if oc.getAttribute('period').lower() == 'transit':
				oc_transit = oc.getAttribute('occupants')

		try:
			taxonomy = Building_Taxonomy.objects.get(name=taxonomy, source=object.taxonomy_source)
		except:
			taxonomy = Building_Taxonomy(name=taxonomy, source=object.taxonomy_source)
			taxonomy.save()

		new_asset = Asset(name = asset_name,
							taxonomy = taxonomy,
							parish = None,
							n_buildings = number,
							area = area,
							struct_cost = structural_value,
							struct_deductible = structural_deductible_percentage,
							struct_insurance_limit = structural_insuranceLimit_value,
							retrofitting_cost = retrofitting_cost,
							non_struct_cost = non_structural_value,
							non_struct_deductible = non_structural_deductible_percentage,
							non_struct_insurance_limit = non_structural_insuranceLimit_value,
							contents_cost = contents_value,
							contents_deductible = contents_deductible_percentage,
							contents_insurance_limit = contents_insuranceLimit_value,						
							business_int_cost = business_interruption_value,
							business_int_deductible = business_interruption_deductible_percentage,
							business_int_insurance_limit = business_interruption_insuranceLimit_value,
							location = Point(float(lon), float(lat)),
							model = object,
							oc_day = oc_day,
							oc_night = oc_night,
							oc_transit = oc_transit)
		new_asset.save()

