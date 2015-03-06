from xml.dom.minidom import parse
from eng_models.models import Site
from world.models import Fishnet
from django.contrib.gis.geos import Point


def start(object):

	model = parse(object.xml)
	#model = parse(path)

	sites = model.getElementsByTagName('site')

	for site in sites:
		lon = float(site.getAttribute('lon'))
		lat = float(site.getAttribute('lat'))
		location = Point(lon, lat)
		vs30 = site.getAttribute('vs30')
		vs30type = site.getAttribute('vs30Type')
		z1pt0 = site.getAttribute('z1pt0')
		z2pt5 = site.getAttribute('z2pt5')

		new_site = Site(model= object,
						location = location,
						vs30 = vs30,
						vs30type = vs30type,
						z1pt0 = z1pt0,
						z2pt5 = z2pt5,
						cell = Fishnet.objects.filter(cell__intersects=location)[0])

		new_site.save()