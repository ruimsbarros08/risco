

def hazard_picker(val):

	if val < 0.05:
		return '#FFFF00'
	elif 0.05 <= val < 0.1:
		return '#FFAA00'
	elif 0.1 <= val < 0.15:
		return '#FF7F00'
	elif 0.15 <= val < 0.2:
		return '#FF5500'
	elif val >= 0.2:
		return '#FF0000'

def damage_picker(val, zoom):
	
	if zoom < 10:
		multiplier = 100
	elif 9 < zoom < 13:
		multiplier = 10
	else:
		multiplier = 1

	if val < (10 * multiplier):
		return '#FFFF00'
	elif (10 * multiplier) <= val < (20 * multiplier):
		return '#FFAA00'
	elif (20 * multiplier) <= val < (30 * multiplier):
		return '#FF7F00'
	elif (30 * multiplier) <= val < (40 * multiplier):
		return '#FF5500'
	elif val >= (40 * multiplier):
		return '#FF0000'


def probabilistic_picker(val, zoom):
	
	fac = 1000000

	if zoom < 10:
		multiplier = 100
	elif 9 < zoom < 13:
		multiplier = 10
	else:
		multiplier = 1

	if val < (10 * fac * multiplier):
		return '#FFFF00'
	elif (10 * fac * multiplier) <= val < (20 * fac * multiplier):
		return '#FFAA00'
	elif (20 * fac * multiplier) <= val < (30 * fac * multiplier):
		return '#FF7F00'
	elif (30 * fac * multiplier) <= val < (40 * fac * multiplier):
		return '#FF5500'
	elif val >= (40 * fac * multiplier):
		return '#FF0000'

