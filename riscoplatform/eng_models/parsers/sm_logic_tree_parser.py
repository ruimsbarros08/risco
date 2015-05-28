
from xml.dom.minidom import parse
from eng_models.models import Logic_Tree_SM, Logic_Tree_SM_Level, Logic_Tree_SM_Branch_Set, Logic_Tree_SM_Branch, Source_Model, Source

class InvalidLogicTree(Exception):
    pass

def start(object):

	model = parse(object.xml)

	levels = model.getElementsByTagName('logicTreeBranchingLevel')
	level_order = 1
	#level_0 = Logic_Tree_SM_Level(logic_tree = object, level = 0)

	for level_tag in levels:
		xml_id = level_tag.getAttribute('branchingLevelID')
		level = Logic_Tree_SM_Level(logic_tree = object, level = level_order, xml_id=xml_id)
		level.save()

		branch_sets = level_tag.getElementsByTagName('logicTreeBranchSet')

		if level_order == 1 and len(branch_sets) > 1:
			raise InvalidLogicTree('The first level of a Source Model Logic Tree must have only one branch set')

		for branch_set_tag in branch_sets:
			xml_id = branch_set_tag.getAttribute('branchSetID')
			uncertainty_type = branch_set_tag.getAttribute('uncertaintyType')

			branch_set = Logic_Tree_SM_Branch_Set(level=level, uncertainty_type=uncertainty_type, xml_id=xml_id)
			branch_set.save()


			branches = branch_set_tag.getElementsByTagName('logicTreeBranch')


			if level_order == 1 and uncertainty_type != 'sourceModel':
				raise InvalidLogicTree('The branch set of the first level of a Source Model Logic Tree \
										must have an uncertainty type of "sourceModel"')

			if level_order != 1 and uncertainty_type == 'sourceModel':
				raise InvalidLogicTree('The uncertainty type of "sourceModel" can only be defined in the branch set \
										 of the first level of a Source Model Logic Tree')

			
			
			if level_order == 1:

				for branch_tag in branches:
					xml_id = level_tag.getAttribute('branchID')
					uncertaintyWeight = branch_tag.getElementsByTagName('uncertaintyWeight')[0].firstChild.nodeValue
					try:
						source_model_id = int(branch_tag.getElementsByTagName('uncertaintyModel')[0].firstChild.nodeValue)
						source_model = Source_Model.objects.get(pk=source_model_id)
					except Exception:
						raise InvalidLogicTree('You have specified an id of a Source Model that does not exist')
					object.source_models.add(source_model)
					branch = Logic_Tree_SM_Branch(branch_set=branch_set, weight=uncertaintyWeight, source_model_id=source_model_id, xml_id=xml_id)
					branch.save()

			else:
				sources = []

				if uncertainty_type == 'abGRAbsolute' or uncertainty_type == 'maxMagGRAbsolute':
					if branch_set_tag.getAttribute('applyToSources') == None:
						raise InvalidLogicTree('An absolute uncertainty type must have the "applyToSources" filter')
					else:
						sources_list = branch_set_tag.getAttribute('applyToSources').split()
						if len(sources_list) > 1:
							raise InvalidLogicTree('Only one source can br specified in the "applyToSources" filter for an absolute uncertainty type')
						else:
							branch_set.filter = 'sources'

							try:
								source_id = int(sources_list[0])
								source = Source.objects.get(pk=source_id)
								branch_set.sources.add(source)
							except Exception:
								raise InvalidLogicTree('The source id(s) you specified are not valid')


				else:

					if branch_set_tag.getAttribute('applyToSources'):
						if sources != []:
							raise InvalidLogicTree('Only one filter can be applied per branch set')
						
						sources_list = branch_set_tag.getAttribute('applyToSources').split()
						branch_set.filter = 'sources'
						for src in sources_list:
							try:
								s = Source.objects.get(pk=int(src))
								sources.append(s)
							except Exception:
								raise InvalidLogicTree('The source id(s) you specified are not valid')


					if branch_set_tag.getAttribute('applyToSourceType'):
						if sources != []:
							raise InvalidLogicTree('Only one filter can be applied per branch set')

						branch_set.filter = 'sources'
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
							eng_models_logic_tree_sm, eng_models_logic_tree_sm_source_models \
							where eng_models_source.model_id = eng_models_source_model.id \
							and eng_models_source.source_type = %s \
							and eng_models_source_model.id = eng_models_logic_tree_sm_source_models.source_model_id \
							and eng_models_logic_tree_sm_source_models.logic_tree_sm_id = eng_models_logic_tree_sm.id \
							and eng_models_logic_tree_sm.id = %s', [sources_type, object.id])
						
						if sources == []:
							raise InvalidLogicTree('The source id(s) you specified are not valid')

					if branch_set_tag.getAttribute('applyToTectonicRegionType'):
						if sources != []:
							raise InvalidLogicTree('Only one filter can be applied per branch set')

						branch_set.filter = 'sources'
						region_type = branch_set_tag.getAttribute('applyToTectonicRegionType')

						sources = Source.objects.raw('select eng_models_source.id \
							from eng_models_source, eng_models_source_model, \
							eng_models_logic_tree_sm, eng_models_logic_tree_sm_source_models \
							where eng_models_source.model_id = eng_models_source_model.id \
							and eng_models_source.tectonic_region = %s \
							and eng_models_source_model.id = eng_models_logic_tree_sm_source_models.source_model_id \
							and eng_models_logic_tree_sm_source_models.logic_tree_sm_id = eng_models_logic_tree_sm.id \
							and eng_models_logic_tree_sm.id = %s', [region_type, object.id])

						if sources == []:
							raise InvalidLogicTree('The source id(s) you specified are not valid')

					for source in sources:
						branch_set.sources.add(source)


					if branch_set_tag.getAttribute('applyToBranches'):
						if sources != []:
							raise InvalidLogicTree('Only one filter can be applied per branch set')

						branch_set.filter = 'branches'
						origin_branches_list = branch_set_tag.getAttribute('applyToBranches').split()
						for e in origin_branches_list:
							o = Logic_Tree_SM_Branch.objects.raw('select eng_models_logic_tree_sm_branch.id \
								from eng_models_logic_tree_sm, eng_models_logic_tree_sm_level, \
								eng_models_logic_tree_sm_branch_set, eng_models_logic_tree_sm_branch \
								where eng_models_logic_tree_sm.id = %s \
								and eng_models_logic_tree_sm.id = eng_models_logic_tree_sm_level.logic_tree_id \
								and eng_models_logic_tree_sm_level.id = eng_models_logic_tree_sm_branch_set.level_id \
								and eng_models_logic_tree_sm_branch_set.id = eng_models_logic_tree_sm_branch.branch_set_id \
								and eng_models_logic_tree_sm_branch.xml_id = %s ', [object.id, e])[0]

							if o == None:
								raise InvalidLogicTree('The branch you specified on the "applyToBranches" filter does not exist')

							branch_set.origins.add(o)


				for branch_tag in branches:
					xml_id = branch_tag.getAttribute('branchID')
					uncertaintyModel = branch_tag.getElementsByTagName('uncertaintyModel')[0].firstChild.nodeValue
					uncertaintyWeight = branch_tag.getElementsByTagName('uncertaintyWeight')[0].firstChild.nodeValue

					
					if uncertainty_type == 'maxMagGRRelative':
						branch = Logic_Tree_SM_Branch(branch_set=branch_set, weight=uncertaintyWeight, max_mag_inc=uncertaintyModel, xml_id=xml_id)
					
					if uncertainty_type == 'bGRRelative':
						branch = Logic_Tree_SM_Branch(branch_set=branch_set, weight=uncertaintyWeight, b_inc=uncertaintyModel, xml_id=xml_id)
					
					if uncertainty_type == 'abGRAbsolute':
						a = float(uncertaintyModel.split(' ')[0])
						b = float(uncertaintyModel.split(' ')[1])
						uncertaintyModel = [a, b]
						branch = Logic_Tree_SM_Branch(branch_set=branch_set, weight=uncertaintyWeight, a_b=uncertaintyModel, xml_id=xml_id)

					if uncertainty_type == 'maxMagGRAbsolute':
						branch = Logic_Tree_SM_Branch(branch_set=branch_set, weight=uncertaintyWeight, max_mag=uncertaintyModel, xml_id=xml_id)

					branch.save()

		level_order += 1



