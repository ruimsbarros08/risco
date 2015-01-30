from xml.dom.minidom import parse
#from eng_models.models import Fragility_Function, Building_Taxonomy
from django.utils import timezone


def start(path):

	#model = parse(object.xml)
	model = parse(path)

	functions = model.getElementsByTagName('ffs')
	for ffs in functions:

		type = ffs.getAttribute('type')
		taxonomy = ffs.getElementsByTagName('taxonomy')[0].firstChild.nodeValue
		iml = ffs.getElementsByTagName('IML')[0]
		sa_period = iml.getAttribute('IMT').split('(')[1].split(')')[0]
		unit = iml.getAttribute('imlUnit')
		min_iml = iml.getAttribute('minIML')
		max_iml = iml.getAttribute('maxIML')
		print '--------'
		print type, taxonomy, sa_period, unit, min_iml, max_iml
		print '--------'


		ffcs = ffs.getElementsByTagName('ffc')

		for ffc in ffcs:
			limit_state = ffc.getAttribute('ls')
			params = ffc.getElementsByTagName('params')[0]

			mean = params.getAttribute('mean')
			stddev = params.getAttribute('stddev')

			print '--------'
			print limit_state, mean, stddev

start('test_fragility.xml')



