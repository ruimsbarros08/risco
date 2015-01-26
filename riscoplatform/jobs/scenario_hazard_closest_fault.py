import math
from django.db import connection
from django.template import Context, loader
from django.core.files import File


cur = connection.cursor()


def find_closest_fault(lon,lat):
    # The fault model is the result of the NRML parsering process

	cur.execute("SELECT fdist.*, ST_X(ST_PointN(ST_linemerge(fdist.geom), \
				generate_series(1,ST_NPoints(ST_linemerge(fdist.geom))))) as Lats, \
				ST_Y(ST_PointN(ST_linemerge(fdist.geom), \
				generate_series(1,ST_NPoints(ST_linemerge(fdist.geom))))) as Longs \
				from (select eng_models_fault.*, ST_distance(eng_models_fault.geom, ST_geographyfromtext \
				('SRID=4326;Point(%s %s)')) as mindist from eng_models_fault order by mindist limit 1) as fdist \
				limit 2;" % (str(lon), str(lat)))
			
	data = cur.fetchall()
	
	segment = [[data[0][-2],data[0][-1]],[data[1][-2],data[1][-1]]]

	dip = data[0][6]
	rake = data[0][7]
	upperSeismoDepth = data[0][3]
	lowerSeismoDepth = data[0][4]
	# print data[0][2], segment, dip, rake, upperSeismoDepth, lowerSeismoDepth
	
	return segment, dip, rake, upperSeismoDepth, lowerSeismoDepth
    

def estimate_rupture_geometry(rake,dip,segment,upperSeismoDepth,lowerSeismoDepth,lon,lat,mag,depth):

    cur.execute("SELECT ST_distance(ST_geographyfromtext('SRID=4326;POINT(%s %s)'), \
				ST_geographyfromtext('SRID=4326;POINT(%s %s)'));" \
				% (str(segment[0][0]), str(segment[0][1]), str(segment[1][0]), str(segment[1][1])))
			
    data = cur.fetchall()
    segmentLentgh = data[0][0]/1000

    # segmentLentgh = (((float(segment[0][1])*math.cos(float(segment[0][0])*math.pi/180) - \
            # float(segment[1][1])*math.cos(float(segment[1][0])*math.pi/180))*111)**2 + \
            # ((float(segment[0][0])-float(segment[1][0]))*111)**2)**0.5
			 

    strike = estimate_strike(segment,segmentLentgh)
    
    if (-45 <= rake <= 45) or (rake >= 135) or (rake <= -135):
        # strike slip
        area =  10.0 ** (-3.42 + 0.90 * mag)
        length = 10.0 ** (-3.55 + 0.74 * mag)
    elif rake > 0:
        # thrust/reverse
        area =  10.0 ** (-3.99 + 0.98 * mag)
        length = 10.0 ** (-2.86 + 0.63 * mag)
    else:
        # normal
        area =   10.0 ** (-2.87 + 0.82 * mag)
        length = 10.0 ** (-2.01 + 0.50 * mag)


    if length > segmentLentgh:
        length = segmentLentgh
		
    width = area/length
	
    lowerDepth = depth+width*math.sin(float(dip)*math.pi/180)/2

    # lowerDepth = depth+width*math.sin(float(dip)*math.pi/180)/2
    if lowerDepth > lowerSeismoDepth:
        lowerDepth = lowerSeismoDepth
	
    upperDepth = max([lowerDepth-width*math.sin(float(dip)*math.pi/180),upperSeismoDepth])
    # upperDepth = max([depth-width*math.sin(float(dip)*math.pi/180)/2,0])
	
    if float(dip)==90:
        offset = 0
    else:
        # offset = upperDepth*math.tan(float(dip)*math.pi/180)		
        offset = depth/math.tan(float(dip)*math.pi/180)
    
    # faultTrace = estimate_fault_trace(offset,strike,length,lon,lat)
    ni = (segmentLentgh - length)/(2*segmentLentgh)	# percentagem inicial do segmento
    nf = 1 - ni	# percentagem final do segmento

	
    cur.execute("select ST_X(ST_Line_Interpolate_Point(ST_GeomFromText('LINESTRING(%s %s, %s %s)',4326), %s));" \
	% (str(segment[0][0]),str(segment[0][1]), str(segment[1][0]),str(segment[1][1]),str(ni)))
    x1 = cur.fetchall()
	
    cur.execute("select ST_Y(ST_Line_Interpolate_Point(ST_GeomFromText('LINESTRING(%s %s, %s %s)',4326), %s));" \
	% (str(segment[0][0]),str(segment[0][1]), str(segment[1][0]),str(segment[1][1]),str(ni)))
    y1 = cur.fetchall()	
	
    cur.execute("select ST_X(ST_Line_Interpolate_Point(ST_GeomFromText('LINESTRING(%s %s, %s %s)',4326), %s));" \
	% (str(segment[0][0]),str(segment[0][1]), str(segment[1][0]),str(segment[1][1]),str(nf)))
    x2 = cur.fetchall()
	
    cur.execute("select ST_Y(ST_Line_Interpolate_Point(ST_GeomFromText('LINESTRING(%s %s, %s %s)',4326), %s));" \
	% (str(segment[0][0]),str(segment[0][1]), str(segment[1][0]),str(segment[1][1]),str(nf)))
    y2 = cur.fetchall()
    
    faultTrace = [[x1[0][0],y1[0][0]],[x2[0][0],y2[0][0]]]
	
    print faultTrace
    print segment
    return upperDepth, lowerDepth, strike, faultTrace

 
def estimate_fault_trace(offset,strike,length,lon,lat):
    
    angle = strike*math.pi/180
    A = [lon - length/2*math.sin(angle)/111 - offset*math.cos(angle)/111, lat - length/2*math.cos(angle)/111/math.cos(lat*math.pi/180) + offset*math.sin(angle)/111]
    B = [lon + length/2*math.sin(angle)/111 - offset*math.cos(angle)/111, lat + length/2*math.cos(angle)/111/math.cos(lat*math.pi/180) + offset*math.sin(angle)/111]
    
    return [A,B]

    
def estimate_strike(segment,length):
        
    strike = math.acos((float(segment[1][1])-float(segment[0][1]))/length)*180/math.pi
    if segment[0][0]>segment[1][0]:
        strike = 360-strike
    elif segment[0][0]<segment[1][0] and segment[0][1]==segment[1][1]:
        strike = 90
    elif segment[0][0]==segment[1][0] and segment[0][1]>segment[1][1]:
        strike = 180
    elif segment[0][0]>segment[1][0] and segment[0][1]==segment[1][1]:
        strike = 270
    
    return strike

def write_fault_rupture_nrml(faultTrace,rake,dip,lowerDepth,upperDepth,lon,lat,mag,depth):
	pass

	
def write_point_rupture_nrml(rake,dip,strike,lon,lat,mag,depth):
    pass




