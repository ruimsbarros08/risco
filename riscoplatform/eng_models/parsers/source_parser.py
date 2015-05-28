from xml.dom.minidom import parse
from eng_models.models import Source_Model, Source
from django.utils import timezone
from django.contrib.gis.geos import Point, GEOSGeometry


def start(object):

	model = parse(object.xml)
	#model = parse(path)
	
	##############
	#POINT SOURCE#
	##############

	point_sources = model.getElementsByTagName('pointSource')
	if point_sources != []:
		for source_tag in point_sources:

			name = source_tag.getAttribute('name')
			tectonic_region = source_tag.getAttribute('tectonicRegion')

			point_text = source_tag.getElementsByTagName('pointGeometry')[0].getElementsByTagName('gml:Point')[0].getElementsByTagName('gml:pos')[0].firstChild.nodeValue
			lon = float(point_text.split(' ')[0])
			lat = float(point_text.split(' ')[1])
			point = Point(lon, lat)

			upper_depth = source_tag.getElementsByTagName('pointGeometry')[0].getElementsByTagName('upperSeismoDepth')[0].firstChild.nodeValue
			lower_depth = source_tag.getElementsByTagName('pointGeometry')[0].getElementsByTagName('lowerSeismoDepth')[0].firstChild.nodeValue

			mag_scale_rel = source_tag.getElementsByTagName('magScaleRel')[0].firstChild.nodeValue
			rupt_aspect_ratio = source_tag.getElementsByTagName('ruptAspectRatio')[0].firstChild.nodeValue

			if source_tag.getElementsByTagName('truncGutenbergRichterMFD') != []:

				mag_freq_dist_type = 'TRUNC'
				a = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('aValue')
				b = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('bValue')
				min_mag = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('minMag')
				max_mag = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('maxMag')

				bin_width = None
				occur_rates = None

			if source_tag.getElementsByTagName('incrementalMFD') != []:
				
				mag_freq_dist_type = 'INC'
				a = None
				b = None
				min_mag = source_tag.getElementsByTagName('incrementalMFD')[0].getAttribute('minMag')
				max_mag = None

				bin_width = source_tag.getElementsByTagName('incrementalMFD')[0].getAttribute('binWidth')
				occur_rates = source_tag.getElementsByTagName('incrementalMFD')[0].getElementsByTagName('occurRates')[0].firstChild.nodeValue
				occur_rates = occur_rates.split(' ')

			nodal_plane_dist = []
			for nodal_plane in source_tag.getElementsByTagName('nodalPlane'):
				nodal_plane_dist.append([float(nodal_plane.getAttribute('probability')),
										float(nodal_plane.getAttribute('strike')),
										float(nodal_plane.getAttribute('dip')),
										float(nodal_plane.getAttribute('rake'))])

			hypo_depth_dist = []
			for hypo_depth in source_tag.getElementsByTagName('hypoDepth'):
				hypo_depth_dist.append([float(hypo_depth.getAttribute('probability')),
										float(hypo_depth.getAttribute('depth'))])

			source = Source(source_type = 'POINT',
							model = object,
							name = name,
							tectonic_region = tectonic_region,
							point = point,
							upper_depth = upper_depth,
							lower_depth = lower_depth,
							mag_scale_rel = mag_scale_rel,
							rupt_aspect_ratio = rupt_aspect_ratio,
							mag_freq_dist_type = mag_freq_dist_type,
							a = a,
							b = b,
							min_mag = min_mag,
							max_mag = max_mag,
							bin_width = bin_width,
							occur_rates = occur_rates,
							nodal_plane_dist = nodal_plane_dist,
							hypo_depth_dist = hypo_depth_dist)
			source.save()


	#############
	#AREA SOURCE#
	#############

	area_sources = model.getElementsByTagName('areaSource')
	if area_sources != []:
		for source_tag in area_sources:

			name = source_tag.getAttribute('name')
			tectonic_region = source_tag.getAttribute('tectonicRegion')

			area_text = source_tag.getElementsByTagName('areaGeometry')[0].getElementsByTagName('gml:Polygon')[0].getElementsByTagName('gml:exterior')[0].getElementsByTagName('gml:LinearRing')[0].getElementsByTagName('gml:posList')[0].firstChild.nodeValue
			points_list = area_text.split('\n')
			del points_list[0]
			del points_list[-1]

			points_list.append(points_list[0])

			wkt = 'POLYGON((' + ', '.join(points_list) + '))'
			area = GEOSGeometry(wkt)

			upper_depth = source_tag.getElementsByTagName('upperSeismoDepth')[0].firstChild.nodeValue
			lower_depth = source_tag.getElementsByTagName('lowerSeismoDepth')[0].firstChild.nodeValue

			mag_scale_rel = source_tag.getElementsByTagName('magScaleRel')[0].firstChild.nodeValue
			rupt_aspect_ratio = source_tag.getElementsByTagName('ruptAspectRatio')[0].firstChild.nodeValue

			if source_tag.getElementsByTagName('truncGutenbergRichterMFD') != []:

				mag_freq_dist_type = 'TRUNC'
				a = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('aValue')
				b = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('bValue')
				min_mag = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('minMag')
				max_mag = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('maxMag')

				bin_width = None
				occur_rates = None

			if source_tag.getElementsByTagName('incrementalMFD') != []:
				
				mag_freq_dist_type = 'INC'
				a = None
				b = None
				min_mag = source_tag.getElementsByTagName('incrementalMFD')[0].getAttribute('minMag')
				max_mag = None

				bin_width = source_tag.getElementsByTagName('incrementalMFD')[0].getAttribute('binWidth')
				occur_rates = source_tag.getElementsByTagName('incrementalMFD')[0].getElementsByTagName('occurRates')[0].firstChild.nodeValue
				occur_rates = occur_rates.split(' ')

			nodal_plane_dist = []
			for nodal_plane in source_tag.getElementsByTagName('nodalPlane'):
				nodal_plane_dist.append([float(nodal_plane.getAttribute('probability')),
										float(nodal_plane.getAttribute('strike')),
										float(nodal_plane.getAttribute('dip')),
										float(nodal_plane.getAttribute('rake'))])

			hypo_depth_dist = []
			for hypo_depth in source_tag.getElementsByTagName('hypoDepth'):
				hypo_depth_dist.append([float(hypo_depth.getAttribute('probability')),
										float(hypo_depth.getAttribute('depth'))])

			source = Source(source_type = 'AREA',
							model = object,
							name = name,
							tectonic_region = tectonic_region,
							area = area,
							upper_depth = upper_depth,
							lower_depth = lower_depth,
							mag_scale_rel = mag_scale_rel,
							rupt_aspect_ratio = rupt_aspect_ratio,
							mag_freq_dist_type = mag_freq_dist_type,
							a = a,
							b = b,
							min_mag = min_mag,
							max_mag = max_mag,
							bin_width = bin_width,
							occur_rates = occur_rates,
							nodal_plane_dist = nodal_plane_dist,
							hypo_depth_dist = hypo_depth_dist)
			source.save()


	##############
	#FAULT SOURCE#
	##############

	fault_sources = model.getElementsByTagName('simpleFaultSource')
	if fault_sources != []:
		for source_tag in fault_sources:

			name = source_tag.getAttribute('name')
			tectonic_region = source_tag.getAttribute('tectonicRegion')

			fault_text = source_tag.getElementsByTagName('simpleFaultGeometry')[0].getElementsByTagName('gml:LineString')[0].getElementsByTagName('gml:posList')[0].firstChild.nodeValue
			points_list = fault_text.split('\n')
			del points_list[0]
			del points_list[-1]
			wkt = 'LINESTRING(' + ', '.join(points_list) + ')'
			fault = GEOSGeometry(wkt)

			upper_depth = source_tag.getElementsByTagName('upperSeismoDepth')[0].firstChild.nodeValue
			lower_depth = source_tag.getElementsByTagName('lowerSeismoDepth')[0].firstChild.nodeValue

			dip = source_tag.getElementsByTagName('dip')[0].firstChild.nodeValue
			rake = source_tag.getElementsByTagName('rake')[0].firstChild.nodeValue

			mag_scale_rel = source_tag.getElementsByTagName('magScaleRel')[0].firstChild.nodeValue
			rupt_aspect_ratio = source_tag.getElementsByTagName('ruptAspectRatio')[0].firstChild.nodeValue

			if source_tag.getElementsByTagName('truncGutenbergRichterMFD') != []:

				mag_freq_dist_type = 'TRUNC'
				a = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('aValue')
				b = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('bValue')
				min_mag = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('minMag')
				max_mag = source_tag.getElementsByTagName('truncGutenbergRichterMFD')[0].getAttribute('maxMag')

				bin_width = None
				occur_rates = None

			if source_tag.getElementsByTagName('incrementalMFD') != []:
				
				mag_freq_dist_type = 'INC'
				a = None
				b = None
				min_mag = source_tag.getElementsByTagName('incrementalMFD')[0].getAttribute('minMag')
				max_mag = None

				bin_width = source_tag.getElementsByTagName('incrementalMFD')[0].getAttribute('binWidth')
				occur_rates = source_tag.getElementsByTagName('incrementalMFD')[0].getElementsByTagName('occurRates')[0].firstChild.nodeValue
				occur_rates = occur_rates.split(' ')

			#nodal_plane_dist = [[], [], [], []]
			#for nodal_plane in source_tag.getElementsByTagName('nodalPlaneDist'):
			#	nodal_plane_dist[0].append(nodal_plane.getAttribute('probability'))
			#	nodal_plane_dist[1].append(nodal_plane.getAttribute('strike'))
			#	nodal_plane_dist[2].append(nodal_plane.getAttribute('dip'))
			#	nodal_plane_dist[3].append(nodal_plane.getAttribute('rake'))

			#hypo_depth_dist = [[], []]
			#for hypo_depth in source_tag.getElementsByTagName('hypoDepthDist'):
			#	hypo_depth_dist[0].append(hypo_depth.getAttribute('probability'))
			#	hypo_depth_dist[1].append(hypo_depth.getAttribute('depth'))

			source = Source(source_type = 'SIMPLE_FAULT',
							model = object,
							name = name,
							tectonic_region = tectonic_region,
							fault = fault,
							upper_depth = upper_depth,
							lower_depth = lower_depth,
							dip = float(dip),
							rake = float(rake),
							mag_scale_rel = mag_scale_rel,
							rupt_aspect_ratio = rupt_aspect_ratio,
							mag_freq_dist_type = mag_freq_dist_type,
							a = a,
							b = b,
							min_mag = min_mag,
							max_mag = max_mag,
							bin_width = bin_width,
							occur_rates = occur_rates,
							#nodal_plane_dist = nodal_plane_dist,
							#hypo_depth_dist = hypo_depth_dist
							)
			source.save()


