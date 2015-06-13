
from xml.dom.minidom import parse
from eng_models.models import Logic_Tree_GMPE, Logic_Tree_GMPE_Level, Logic_Tree_GMPE_Branch
from eng_models.constants import tectonic_region_is_valid, gmpe_is_valid, gmpe_tectonic_region_is_compatible

class InvalidLogicTree(Exception):
    pass

def start(object):

	model = parse(object.xml)

	levels = model.getElementsByTagName('logicTreeBranchingLevel')
	level_order = 1

	for level_tag in levels:
		xml_id = level_tag.getAttribute('branchingLevelID')

		branch_sets = level_tag.getElementsByTagName('logicTreeBranchSet')

		if len(branch_sets) > 1:
			raise InvalidLogicTree('The levels of the GMPE Logic Trees must have only one branch set')

		for branch_set_tag in branch_sets:
			
			if branch_set_tag.getAttribute('applyToTectonicRegionType') == None:
				raise InvalidLogicTree('It is mandatory to use the "applyToTectonicRegionType" filter in all the branch sets of GMPE Logic Tree')

			region_type = branch_set_tag.getAttribute('applyToTectonicRegionType')

			if tectonic_region_is_valid(region_type) == False:
				raise InvalidLogicTree('The tectonic region you have specified is not valid')

			level = Logic_Tree_GMPE_Level(logic_tree = object, level = level_order, xml_id=xml_id, tectonic_region=region_type)
			level.save()

			uncertainty_type = branch_set_tag.getAttribute('uncertaintyType')

			if uncertainty_type != 'gmpeModel':
				raise InvalidLogicTree('Only uncertainty type "gmpeModel" is allowed in GMPE Logic Trees')

			branches = branch_set_tag.getElementsByTagName('logicTreeBranch')

			weight_sum = 0
			
			for branch_tag in branches:
				xml_id = branch_tag.getAttribute('branchID')
				gmpe = branch_tag.getElementsByTagName('uncertaintyModel')[0].firstChild.nodeValue
				weight = float(branch_tag.getElementsByTagName('uncertaintyWeight')[0].firstChild.nodeValue)

				weight_sum += weight

				if weight_sum > 1.0:
					raise InvalidLogicTree('The sum of the weights in all the branches of a branch set must be equal to 1.0')

				if weight > 1.0 or weight < 0.0:
					raise InvalidLogicTree('The weight of a branch must be inside the range [0.0, 1.0]')

				if gmpe_is_valid(gmpe) == False:
					raise InvalidLogicTree('The GMPE you have specified is not valid')

				if gmpe_tectonic_region_is_compatible(gmpe, region_type) == False:
					raise InvalidLogicTree('The GMPE you have specified is not compatible with the tectonic region')

				branch = Logic_Tree_GMPE_Branch(level=level, weight=weight, gmpe=gmpe, xml_id=xml_id)
				branch.save()

			if weight_sum != 1.0:
				raise InvalidLogicTree('The sum of the weights in all the branches of a branch set must be equal to 1.0')


		level_order += 1



