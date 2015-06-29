from xml.dom.minidom import parse
from eng_models.models import Asset, Building_Taxonomy
from world.models import *
from django.contrib.gis.geos import Point
from django.utils import timezone


class InvalidExposureModel(Exception):
    pass


def valid_aggregation_type(type, area_type):
	if type not in ['per_asset', 'per_area', 'per_unit', 'aggregated']:
		return False
	else:
		if type == 'per_area':
			if area_type == None:
				return False
			else:
				return True
		else:
			return True

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
		if area_type not in ['per_asset', 'per_unit', 'aggregated'] :
			raise InvalidExposureModel('The area aggregation settings must be one of the three possibilities: "per_asset", "per_unit" or "aggregated" ')
		
		area_unit = area[0].getAttribute('unit')
		if area_unit not in ['square meters', 'hectare']:
			raise InvalidExposureModel('The area units must be one of the two possibilities: "square meters" or "hectare" ')
		
	else:
		area_type = None
		area_unit = None


	structural_cost_type 			= None
	structural_cost_unit 			= None
	non_structural_cost_type 		= None
	non_structural_cost_unit 		= None
	business_interruption_cost_type = None
	business_interruption_cost_unit = None
	contents_cost_type 				= None
	contents_cost_unit 				= None

	try:
		deductible = conversions[0].getElementsByTagName('deductible')[0]
		if deductible.getAttribute('isAbsolute') == 'false':
			deductible_abs = 'relative'
		elif deductible.getAttribute('isAbsolute') == 'true':
			deductible_abs = 'absolute'
		else:
			raise InvalidExposureModel('The deductible "isAbsolute" setting must be one of the two possibilities: "true" or "false" ')

	except:
		deductible_abs = None

	try:
		insuranceLimit = conversions[0].getElementsByTagName('insuranceLimit')[0]
		if insuranceLimit.getAttribute('isAbsolute') == 'false':
			insuranceLimit_abs = 'relative'
		elif insuranceLimit.getAttribute('isAbsolute') == 'true':
			insuranceLimit_abs = 'absolute'
		else:
			raise InvalidExposureModel('The insurance limit "isAbsolute" setting must be one of the two possibilities: "true" or "false" ')

	except:
			insuranceLimit_abs = None


	costTypes = conversions[0].getElementsByTagName('costTypes')[0].getElementsByTagName('costType')
	if costTypes == []:
		raise InvalidExposureModel('At least one cost type must be defined. Ex: "structural, "nonstructural", "contents", "business_interruption"')
	
	c_types = {}
	for cost in costTypes:
		c_types[cost.getAttribute('name')] = False

		if cost.getAttribute('name') == 'structural':
			structural_cost_type = cost.getAttribute('type')
			if valid_aggregation_type(structural_cost_type, area_type) == False:
				raise InvalidExposureModel('The area aggregation settings must be one of the three possibilities: "per_asset", "per_unit", "per_area" or "aggregated". If "per_area" the area type and units must be defined')
			
			structural_cost_unit = cost.getAttribute('unit')
			if structural_cost_unit not in ['EUR', 'USD'] :
				raise InvalidExposureModel('The currency must be one of the two possibilities: "EUR" or "USD" ')
		

		if cost.getAttribute('name') == 'nonstructural':
			non_structural_cost_type = cost.getAttribute('type')
			if valid_aggregation_type(non_structural_cost_type, area_type) == False:
				raise InvalidExposureModel('The area aggregation settings must be one of the three possibilities: "per_asset", "per_unit", "per_area" or "aggregated". If "per_area" the area type and units must be defined')
			
			non_structural_cost_unit = cost.getAttribute('unit')
			if non_structural_cost_unit not in ['EUR', 'USD'] :
				raise InvalidExposureModel('The currency must be one of the two possibilities: "EUR" or "USD" ')
		
		if cost.getAttribute('name') == 'business_interruption':
			business_interruption_cost_type = cost.getAttribute('type')
			if valid_aggregation_type(business_interruption_cost_type, area_type) == False:
				raise InvalidExposureModel('The area aggregation settings must be one of the three possibilities: "per_asset", "per_unit", "per_area" or "aggregated". If "per_area" the area type and units must be defined')
			
			business_interruption_cost_unit = cost.getAttribute('unit')
			if business_interruption_cost_unit not in ['EUR', 'USD'] :
				raise InvalidExposureModel('The currency must be one of the two possibilities: "EUR" or "USD" ')
		
		if cost.getAttribute('name') == 'contents':
			contents_cost_type = cost.getAttribute('type')
			if valid_aggregation_type(contents_cost_type, area_type) == False:
				raise InvalidExposureModel('The area aggregation settings must be one of the three possibilities: "per_asset", "per_unit", "per_area" or "aggregated". If "per_area" the area type and units must be defined')
			
			contents_cost_unit = cost.getAttribute('unit')
			if contents_cost_unit not in ['EUR', 'USD'] :
				raise InvalidExposureModel('The currency must be one of the two possibilities: "EUR" or "USD" ')
		

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
			area = float(asset.getAttribute('area').strip())
		else:
			area = None
			if structural_cost_type == 'per_area' or non_structural_cost_type == 'per_area' or contents_cost_type == 'per_area' or business_interruption_cost_type == 'per_area':
				raise InvalidExposureModel('if a cost type is defined as "per_area", all assets must include the value of the area on the respective units')

		if asset.getAttribute('number'):
			number = float(asset.getAttribute('number').strip())
		else:
			number = None
			if structural_cost_type == 'per_area' or non_structural_cost_type == 'per_area' or contents_cost_type == 'per_area' or business_interruption_cost_type == 'per_area' \
				or structural_cost_type == 'per_unit' or non_structural_cost_type == 'per_unit' or contents_cost_type == 'per_unit' or business_interruption_cost_type == 'per_unit':
				raise InvalidExposureModel('if a cost type is defined as "per_unit" or "per_area", all assets must include the number of its units')

		if asset.getAttribute('taxonomy'):
			taxonomy = asset.getAttribute('taxonomy').strip()
			if taxonomy == '':
				raise InvalidExposureModel('You must include a valid taxonomy name for every asset')
		else:
			raise InvalidExposureModel('You must include a valid taxonomy name for every asset')


		location = asset.getElementsByTagName('location')[0]
		lon = location.getAttribute('lon')
		lat = location.getAttribute('lat')
		try:
			loc = Point(float(lon), float(lat))
		except:
			raise InvalidExposureModel('The location of all the assets must be correct')

		try:
			adm_2 = Adm_2.objects.get(geom__intersects=loc)
		except:
			adm_2 = None
		
		costs = asset.getElementsByTagName('costs')[0].getElementsByTagName('cost')
		for cost in costs:
			
			c_types[cost.getAttribute('type')] = True

			if cost.getAttribute('type') == 'structural':
				structural_value = float(cost.getAttribute('value'))
				if structural_value < 0:
					raise InvalidExposureModel('All the cost values must be greater than zero')

				if cost.getAttribute('retrofitted'):
					retrofitting_cost = float(cost.getAttribute('retrofitted'))
					if retrofitting_cost < 0:
						raise InvalidExposureModel('All the cost values must be greater than zero')

				if deductible_abs != None:
					struct_deductible = float(cost.getAttribute('deductible')) 
					if deductible_abs == 'absolute':
						if struct_deductible < 0:
							raise InvalidExposureModel('The deductible value must be greater than zero')

					else:#relative
						if struct_deductible < 0 or struct_deductible > 1:
							raise InvalidExposureModel('The deductible value must be on the range [0, 1]')

				if insuranceLimit_abs != None:
					struct_insurance_limit = float(cost.getAttribute('insuranceLimit')) 
					if insuranceLimit_abs == 'absolute':
						if struct_insurance_limit < 0:
							raise InvalidExposureModel('The insurance limit value must be greater than zero')

					else:#relative
						if struct_insurance_limit < 0 or struct_insurance_limit > 1:
							raise InvalidExposureModel('The insurance limit value must be on the range [0, 1]')



			if cost.getAttribute('type') == 'nonstructural':
				non_structural_value = cost.getAttribute('value')
				if non_structural_value < 0:
					raise InvalidExposureModel('All the cost values must be greater than zero')

				if deductible_abs != None:
					non_struct_deductible = float(cost.getAttribute('deductible')) 
					if deductible_abs == 'absolute':
						if non_struct_deductible < 0:
							raise InvalidExposureModel('The deductible value must be greater than zero')

					else:#relative
						if non_struct_deductible < 0 or non_struct_deductible > 1:
							raise InvalidExposureModel('The deductible value must be on the range [0, 1]')

				if insuranceLimit_abs != None:
					non_struct_insurance_limit = float(cost.getAttribute('insuranceLimit')) 
					if insuranceLimit_abs == 'absolute':
						if non_struct_insurance_limit < 0:
							raise InvalidExposureModel('The insurance limit value must be greater than zero')

					else:#relative
						if non_struct_insurance_limit < 0 or non_struct_insurance_limit > 1:
							raise InvalidExposureModel('The insurance limit value must be on the range [0, 1]')

			if cost.getAttribute('type') == 'contents':
				contents_value = cost.getAttribute('value')
				if contents_value < 0:
					raise InvalidExposureModel('All the cost values must be greater than zero')

				if deductible_abs != None:
					contents_deductible = float(cost.getAttribute('deductible')) 
					if deductible_abs == 'absolute':
						if contents_deductible < 0:
							raise InvalidExposureModel('The deductible value must be greater than zero')

					else:#relative
						if contents_deductible < 0 or contents_deductible > 1:
							raise InvalidExposureModel('The deductible value must be on the range [0, 1]')

				if insuranceLimit_abs != None:
					contents_insurance_limit = float(cost.getAttribute('insuranceLimit')) 
					if insuranceLimit_abs == 'absolute':
						if contents_insurance_limit < 0:
							raise InvalidExposureModel('The insurance limit value must be greater than zero')

					else:#relative
						if contents_insurance_limit < 0 or contents_insurance_limit > 1:
							raise InvalidExposureModel('The insurance limit value must be on the range [0, 1]')

			if cost.getAttribute('type') == 'business_interruption':
				business_interruption_value = cost.getAttribute('value')
				if business_interruption_value < 0:
					raise InvalidExposureModel('All the cost values must be greater than zero')

				if deductible_abs != None:
					business_int_deductible = float(cost.getAttribute('deductible')) 
					if deductible_abs == 'absolute':
						if business_int_deductible < 0:
							raise InvalidExposureModel('The deductible value must be greater than zero')

					else:#relative
						if business_int_deductible < 0 or business_int_deductible > 1:
							raise InvalidExposureModel('The deductible value must be on the range [0, 1]')

				if insuranceLimit_abs != None:
					business_int_insurance_limit = float(cost.getAttribute('insuranceLimit')) 
					if insuranceLimit_abs == 'absolute':
						if business_int_insurance_limit < 0:
							raise InvalidExposureModel('The insurance limit value must be greater than zero')

					else:#relative
						if business_int_insurance_limit < 0 or business_int_insurance_limit > 1:
							raise InvalidExposureModel('The insurance limit value must be on the range [0, 1]')

		for e in c_types.keys():
			if c_types[e] == False:
				raise InvalidExposureModel('All the cost types included in the conversions must appear on every asset')
			c_types[e] = False

		occupancies = asset.getElementsByTagName('occupancies')[0].getElementsByTagName('occupancy')
		for oc in occupancies:
			if oc.getAttribute('period').lower() == 'day':
				oc_day = float(oc.getAttribute('occupants'))
				if oc_day < 0:
					raise InvalidExposureModel('The occupancy must be greater than zero')

			if oc.getAttribute('period').lower() == 'night':
				oc_night = float(oc.getAttribute('occupants'))
				if oc_night < 0:
					raise InvalidExposureModel('The occupancy must be greater than zero')

			if oc.getAttribute('period').lower() == 'transit':
				oc_transit = float(oc.getAttribute('occupants'))
				if oc_transit < 0:
					raise InvalidExposureModel('The occupancy must be greater than zero')

		try:
			taxonomy = Building_Taxonomy.objects.get(name=taxonomy, source=object.taxonomy_source)
		except:
			taxonomy = Building_Taxonomy(name=taxonomy, source=object.taxonomy_source)
			taxonomy.save()

		new_asset = Asset(name = asset_name,
							taxonomy = taxonomy,
							adm_2 = adm_2,
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
							location = loc,
							model = object,
							oc_day = oc_day,
							oc_night = oc_night,
							oc_transit = oc_transit)
		new_asset.save()

