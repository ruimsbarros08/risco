
from xml.dom.minidom import parse
from eng_models.models import *


def start(object):

	model = parse(object.xml)

	levels = model.getElementsByTagName('logicTreeBranchingLevel')
	level_order = 1
	level_0 = Logic_Tree_Level(logic_tree = object, level = 0)

	for level_tag in levels:
		xml_id = level_tag.getAttribute('branchingLevelID')
		level = Logic_Tree_Level(logic_tree = object, level = level_order, xml_id=xml_id)
		level.save()

		branch_sets = level_tag.getElementsByTagName('logicTreeBranchSet')
		for branch_set_tag in branch_sets:
			xml_id = level_tag.getAttribute('branchSetID')
			uncertainty_type = branch_set_tag.getAttribute('uncertaintyType')

			#ORIGIN
			if level_order == 1:
				branch_set = Logic_Tree_Branch_Set(level=level_0)
				origin = Logic_Tree_Branch(branch_set=branch_set, weight=1.0)
				origin_branches=[origin]

			elif branch_set_tag.getAttribute('applyToBranches'):
				origin_branches_list = branch_set_tag.getAttribute('applyToBranches').split()
				origin_branches = []
				for e in origin_branches_list:
					o = Logic_Tree_Branch.objects.raw('select * \
						from eng_models_logic_tree, eng_models_logic_tree_level, \
						eng_models_logic_tree_branch_set, eng_models_logic_tree_branch \
						where eng_models_logic_tree.id = %s \
						and eng_models_logic_tree.id = eng_models_logic_tree_level.logic_tree_id \
						and eng_models_logic_tree_level.id = eng_models_logic_tree_branch_set.level_id \
						and eng_models_logic_tree_branch_set.id = eng_models_logic_tree_branch.branch_set_id \
						and eng_models_logic_tree_branch.xml_id = %s ', [object.id, e])[0]
					origin_branches.append(o)

			else:
				origin_branches = Logic_Tree_Branch.objects.raw('select * \
					from eng_models_logic_tree, eng_models_logic_tree_level, \
					eng_models_logic_tree_branch_set, eng_models_logic_tree_branch \
					where eng_models_logic_tree.id = %s \
					and eng_models_logic_tree.id = eng_models_logic_tree_level.logic_tree_id \
					and eng_models_logic_tree_level.id = eng_models_logic_tree_branch_set.level_id \
					and eng_models_logic_tree_branch_set.id = eng_models_logic_tree_branch.branch_set_id \
					and eng_models_logic_tree_level.level = %s', [object.id, level_order-1])

			#SOURCES
			if branch_set_tag.getAttribute('applyToSources'):
				sources_list = branch_set_tag.getAttribute('applyToSources').split()
				sources = []
				for e in sources_list:
					o = Source.objects.get(pk=int(e))
					sources.append(o)

			elif branch_set_tag.getAttribute('applyToSourceType'):
				sources_type = branch_set_tag.getAttribute('applyToSourceType')
				if sources_type =='area':
					sources_type = 'AREA'
				elif sources_type =='point':
					sources_type = 'POINT'
				elif sources_type =='simpleFault':
					sources_type = 'SIMPLE_FAULT'
				elif sources_type =='complexFault':
					sources_type = 'COMPLEX_FAULT'
				sources = Source.objects.raw('select eng_models_source.id \
					from eng_models_source, eng_models_source_model, \
					eng_models_logic_tree, eng_models_logic_tree_source_models \
					where eng_models_source.model_id = eng_models_source_model.id \
					and eng_models_source.source_type = %s \
					and eng_models_source_model.id = eng_models_logic_tree_source_models.source_model_id \
					and eng_models_logic_tree_source_models.logic_tree_id = eng_models_logic_tree.id \
					and eng_models_logic_tree.id = %s', [sources_type, object.id])

			elif branch_set_tag.getAttribute('applyToTectonicRegionType'):
				region_type = branch_set_tag.getAttribute('applyToTectonicRegionType')
				sources = Source.objects.raw('select eng_models_source.id \
					from eng_models_source, eng_models_source_model, \
					eng_models_logic_tree, eng_models_logic_tree_source_models \
					where eng_models_source.model_id = eng_models_source_model.id \
					and eng_models_source.tectonic_region = %s \
					and eng_models_source_model.id = eng_models_logic_tree_source_models.source_model_id \
					and eng_models_logic_tree_source_models.logic_tree_id = eng_models_logic_tree.id \
					and eng_models_logic_tree.id = %s', [region_type, object.id])
			else:
				sources=[]

			for e in origin_branches:

				branch_set = Logic_Tree_Branch_Set(level=level, uncertainty_type=uncertainty_type, xml_id=xml_id, origin=e)
				branch_set.save()
				for src in sources:
					branch_set.sources.add(src.id)

				branches = branch_set_tag.getElementsByTagName('logicTreeBranch')
				for branch_tag in branches:
					xml_id = level_tag.getAttribute('branchID')
					uncertaintyModel = branch_tag.getElementsByTagName('uncertaintyModel')[0].firstChild.nodeValue
					uncertaintyWeight = branch_tag.getElementsByTagName('uncertaintyWeight')[0].firstChild.nodeValue

					if branch_set.uncertainty_type == 'gmpeModel':
						branch = Logic_Tree_Branch(branch_set=branch_set, weight=uncertaintyWeight, gmpe=uncertaintyModel, xml_id=xml_id)
					
					if branch_set.uncertainty_type == 'sourceModel':
						source_model = Source_Model.objects.get(pk=uncertaintyModel)
						object.source_models.add(source_model)
						branch = Logic_Tree_Branch(branch_set=branch_set, weight=uncertaintyWeight, source_model_id=int(uncertaintyModel), xml_id=xml_id)

					if branch_set.uncertainty_type == 'maxMagGRRelative':
						branch = Logic_Tree_Branch(branch_set=branch_set, weight=uncertaintyWeight, max_mag_inc=uncertaintyModel, xml_id=xml_id)
					
					if branch_set.uncertainty_type == 'bGRRelative':
						branch = Logic_Tree_Branch(branch_set=branch_set, weight=uncertaintyWeight, b_inc=uncertaintyModel, xml_id=xml_id)
					
					if branch_set.uncertainty_type == 'abGRAbsolute':
						a = float(uncertaintyModel.split(' ')[0])
						b = float(uncertaintyModel.split(' ')[1])
						uncertaintyModel = [a, b]
						branch = Logic_Tree_Branch(branch_set=branch_set, weight=uncertaintyWeight, a_b=uncertaintyModel, xml_id=xml_id)

					if branch_set.uncertainty_type == 'maxMagGRAbsolute':
						branch = Logic_Tree_Branch(branch_set=branch_set, weight=uncertaintyWeight, max_mag=uncertaintyModel, xml_id=xml_id)

					branch.save()

		level_order += 1



