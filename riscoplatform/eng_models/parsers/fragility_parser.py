from xml.dom.minidom import parse
from eng_models.models import Fragility_Function, Building_Taxonomy, Taxonomy_Fragility_Model
from django.utils import timezone


def start(object):

	model = parse(object.xml)

	limit_states = model.getElementsByTagName('limitStates')[0].firstChild.nodeValue
	limit_states = limit_states.split('\n')
	limit_states = [ e.strip() for e in limit_states if e and e.strip()]

	object.limit_states = limit_states
	object.save()

	functions = model.getElementsByTagName('ffs')
	for ffs in functions:

		type = ffs.getAttribute('type')
		taxonomy = ffs.getElementsByTagName('taxonomy')[0].firstChild.nodeValue
		iml = ffs.getElementsByTagName('IML')[0]
		imt = iml.getAttribute('IMT')
		if imt.startswith("SA"):
			sa_period = imt.split('(')[1].split(')')[0]
			imt = 'SA'
		else:
			sa_period = None
		unit = iml.getAttribute('imlUnit')
		min_iml = iml.getAttribute('minIML')
		max_iml = iml.getAttribute('maxIML')


		try:
			taxonomy = Building_Taxonomy.objects.get(name=taxonomy, source=object.taxonomy_source)
		except:
			taxonomy = Building_Taxonomy(name=taxonomy, source=object.taxonomy_source)
			taxonomy.save()

		tax_frag = Taxonomy_Fragility_Model(model = object,
											taxonomy = taxonomy,
											dist_type = type,
											imt = imt,
											sa_period = sa_period,
											min_iml = min_iml,
											max_iml = max_iml,
											unit = unit)
		tax_frag.save()

		ffcs = ffs.getElementsByTagName('ffc')

		for ffc in ffcs:
			limit_state = ffc.getAttribute('ls')
			params = ffc.getElementsByTagName('params')[0]

			mean = params.getAttribute('mean')
			stddev = params.getAttribute('stddev')

			new_frag_function = Fragility_Function()
			new_frag_function.tax_frag = tax_frag
			new_frag_function.limit_state = limit_state
			new_frag_function.mean = mean
			new_frag_function.stddev = stddev

			new_frag_function.save()









