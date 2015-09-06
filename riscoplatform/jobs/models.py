from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from world.models import World, Fishnet
from djorm_pgarray.fields import FloatArrayField, TextArrayField
from eng_models.models import *
from eng_models.constants import *
from django_pgjson.fields import JsonField

# Create your models here.
MODEL = 'VARIABLE_CONDITIONS'
DEFAULT = 'DEFAULT_CONDITIONS'
SITES_CHOICES = (
	(MODEL, 'Site model'),
	(DEFAULT, 'Default conditions'),
	)

MEASURED = 'measured'
INFERRED = 'inferred'
VS30_CHOICES = (
	(MEASURED, 'measured'),
	(INFERRED, 'inferred'),
)

CREATED = 'CREATED'
STARTED = 'STARTED'
ERROR = 'ERROR'
FINISHED = 'FINISHED'
STATUS_CHOICES = (
	(CREATED, 'Created'),
	(STARTED, 'Started'),
	(ERROR, 'Error'),
	(FINISHED, 'Finished'),
)


# class Job(models.Model):
#     user                        = models.ForeignKey(User)
#     date_created                = models.DateTimeField('date created')
#     name                        = models.CharField(max_length=200)
#     description                 = models.CharField(max_length=200, null=True)


# class Hazard(models.Model):
#     #Region
#     region                      = models.PolygonField(srid=4326)
#     grid_spacing                = models.FloatField(default=1)

#     #Sites
#     sites_type                  = models.CharField(max_length=50, choices=SITES_CHOICES, default=DEFAULT)
#     site_model                  = models.ForeignKey(Site_Model, null=True, blank=True)
#     vs30                        = models.FloatField(null=True, blank=True)
#     vs30type                    = models.CharField(max_length=10, choices=VS30_CHOICES, default=MEASURED, null=True, blank=True)
#     z1pt0                       = models.FloatField(null=True, blank=True)
#     z2pt5                       = models.FloatField(null=True, blank=True)

#     rupture_mesh_spacing        = models.IntegerField(default=5)
#     random_seed                 = models.IntegerField(default=3)
#     truncation_level            = models.FloatField(default=3)
#     max_distance                = models.FloatField(default=200)



class Scenario_Hazard(models.Model):
	private                     = models.BooleanField(default=False)
	user 						= models.ForeignKey(User)
	date_created 				= models.DateTimeField('date created')
	name 						= models.CharField(max_length=200)
	description 				= models.CharField(max_length=200, null=True)

	#Region
	region  					= models.PolygonField(srid=4326)
	grid_spacing				= models.FloatField(default=1)

	#Sites
	sites_type                  = models.CharField(max_length=50, choices=SITES_CHOICES, default=DEFAULT)
	site_model                  = models.ForeignKey(Site_Model, null=True, blank=True)
	vs30                        = models.FloatField(null=True, blank=True)
	vs30type                    = models.CharField(max_length=10, choices=VS30_CHOICES, default=MEASURED, null=True, blank=True)
	z1pt0                       = models.FloatField(null=True, blank=True)
	z2pt5                       = models.FloatField(null=True, blank=True)

	random_seed                 = models.IntegerField(default=3)
	rupture_mesh_spacing		= models.IntegerField(default=5)

	#Rupture
	rupture_model               = models.ForeignKey(Rupture_Model)

	pga 						= models.BooleanField(default=True)
	sa_periods                  = FloatArrayField(null=True)
	truncation_level			= models.FloatField(default=3)
	max_distance				= models.FloatField(default=200)
	gmpe						= models.CharField(max_length=50, choices=GMPE_CHOICES)
	correlation_model			= models.BooleanField(default=True)
	vs30_clustering 			= models.BooleanField(default=False)
	n_gmf 						= models.IntegerField(default=50)

	ini_file                    = models.FileField(upload_to='uploads/scenario/hazard/', null=True, blank=True)

	status                      = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED)
	oq_id                       = models.IntegerField(null=True)


	def __unicode__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'jobs_scenario_hazard'


class Scenario_Hazard_Results(models.Model):

	job                         = models.ForeignKey(Scenario_Hazard)
	location                    = models.PointField(srid=4326)
	imt                         = models.CharField(max_length=3)
	sa_period                   = models.FloatField(null=True)
	sa_damping                  = models.IntegerField(null=True)
	gmvs                        = models.FloatField()
	cell                        = models.ForeignKey(Fishnet, null=True)

	def __unicode__(self):
		return self.job.name+' results'

class Scenario_Hazard_Results_By_Cell(models.Model):

	job                         = models.ForeignKey(Scenario_Hazard)
	cell                        = models.ForeignKey(Fishnet)    
	imt                         = models.CharField(max_length=3)
	sa_period                   = models.FloatField(null=True)
	gmvs_mean                   = models.FloatField()

	def __unicode__(self):
		return self.job.name+' results'


class Scenario_Damage(models.Model):
	private                     = models.BooleanField(default=False)
	user                        = models.ForeignKey(User)
	date_created                = models.DateTimeField('date created')
	name                        = models.CharField(max_length=200)
	description                 = models.CharField(max_length=200, null=True)
	hazard_job                  = models.ForeignKey(Scenario_Hazard)
	fragility_model             = models.ForeignKey(Fragility_Model)
	exposure_model              = models.ForeignKey(Exposure_Model)
	region                      = models.PolygonField(srid=4326)
	max_hazard_dist             = models.FloatField()

	status                      = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED)
	oq_id                       = models.IntegerField(null=True)

	ini_file                    = models.FileField(upload_to='uploads/scenario/damage/', null=True, blank=True)

	def __unicode__(self):
		return self.name


class Scenario_Damage_Results(models.Model):
	job                         = models.ForeignKey(Scenario_Damage)
	asset                       = models.ForeignKey(Asset)
	limit_state                 = models.CharField(max_length=20)
	mean                        = models.FloatField()
	stddev                      = models.FloatField()

	def __unicode__(self):
		return self.job.name+' results'



class Scenario_Risk(models.Model):

	DAY = 'day'
	NIGHT = 'night'
	TRANSIT = 'transit'
	TIME_CHOICES = (
		(DAY, 'Day'),
		(NIGHT, 'Night'),
		(TRANSIT, 'Transit'),
		)

	private                     = models.BooleanField(default=False)
	user                        = models.ForeignKey(User)
	date_created                = models.DateTimeField('date created')
	name                        = models.CharField(max_length=200)
	description                 = models.CharField(max_length=200, null=True)
	hazard_job                  = models.ForeignKey(Scenario_Hazard)
	exposure_model              = models.ForeignKey(Exposure_Model)
	region                      = models.PolygonField(srid=4326)
	max_hazard_dist             = models.FloatField()
	
	master_seed                 = models.IntegerField()
	vul_correlation_coefficient = models.FloatField()
	insured_losses              = models.BooleanField(default=True)

	vulnerability_models        = models.ManyToManyField(Vulnerability_Model, through='Scenario_Risk_Vulnerability_Model')

	time_of_the_day             = models.CharField(max_length=10, choices=TIME_CHOICES)

	status                      = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED)
	oq_id                       = models.IntegerField(null=True)

	ini_file                    = models.FileField(upload_to='uploads/scenario/damage/', null=True, blank=True)

	def __unicode__(self):
		return self.name

class Scenario_Risk_Vulnerability_Model(models.Model):
	job                         = models.ForeignKey(Scenario_Risk)
	vulnerability_model         = models.ForeignKey(Vulnerability_Model)


class Scenario_Risk_Results(models.Model):
	job_vul                     = models.ForeignKey(Scenario_Risk_Vulnerability_Model)
	asset                       = models.ForeignKey(Asset)
	mean                        = models.FloatField()
	stddev                      = models.FloatField()
	insured_mean                = models.FloatField(null=True)
	insured_stddev              = models.FloatField(null=True)   

EXPOSURE = 'EXPOSURE'
GRID = 'GRID'
LOCATIONS = 'LOCATIONS'
LOCATIONS_CHOICES = (
	(EXPOSURE, 'Exposure model'),
	(GRID, 'Grid'),
	(LOCATIONS, 'Locations'),
	)


class Classical_PSHA_Hazard(models.Model):
	private                     = models.BooleanField(default=False)
	user                        = models.ForeignKey(User)
	date_created                = models.DateTimeField('date created')
	name                        = models.CharField(max_length=200)
	description                 = models.CharField(max_length=200, null=True)

	random_seed                 = models.IntegerField(default=3)
	
	#region
	locations_type				= models.CharField(max_length=20, choices=LOCATIONS_CHOICES, default=EXPOSURE)
	exposure_model              = models.ForeignKey(Exposure_Model, null=True, blank=True)
	locations                   = models.MultiPointField(srid=4326, null=True, blank=True)
	region                      = models.PolygonField(srid=4326, null=True, blank=True)
	grid_spacing                = models.FloatField(default=1, null=True, blank=True)

	n_lt_samples                = models.IntegerField()
	
	#km
	rupture_mesh_spacing        = models.FloatField()
	width_of_mfd_bin            = models.FloatField()
	area_source_discretization  = models.FloatField()

	#site
	sites_type                  = models.CharField(max_length=50, choices=SITES_CHOICES, default=DEFAULT)
	site_model                  = models.ForeignKey(Site_Model, null=True, blank=True)
	vs30                        = models.FloatField(null=True, blank=True)
	vs30type                    = models.CharField(max_length=10, choices=VS30_CHOICES, default=MEASURED, null=True, blank=True)
	z1pt0                       = models.FloatField(null=True, blank=True)
	z2pt5                       = models.FloatField(null=True, blank=True)

	sm_logic_tree               = models.ForeignKey(Logic_Tree_SM)
	gmpe_logic_tree             = models.ForeignKey(Logic_Tree_GMPE)
	
	investigation_time          = models.IntegerField()

	imt_l                       = JsonField()
	truncation_level            = models.FloatField()
	max_distance                = models.FloatField(default=200)

	quantile_hazard_curves      = FloatArrayField(null=True, blank=True)
	poes                        = FloatArrayField(null=True)

	ini_file                    = models.FileField(upload_to='uploads/psha/hazard/', null=True, blank=True)

	status                      = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED)
	oq_id                       = models.IntegerField(null=True)


	def __unicode__(self):
		return self.name


class Classical_PSHA_Hazard_Curves(models.Model):

	job                         = models.ForeignKey(Classical_PSHA_Hazard)
	location                    = models.PointField(srid=4326)
	cell                        = models.ForeignKey(Fishnet, null=True)
	imt                         = models.CharField(max_length=3)
	sa_period                   = models.FloatField(null=True)
	sa_damping                  = models.IntegerField(null=True)
	weight                      = models.FloatField(null=True)
	statistics                  = models.CharField(max_length=20, null=True)
	quantile                    = models.FloatField(null=True)
	sm_lt_path                  = TextArrayField(null=True)
	gsim_lt_path                = TextArrayField(null=True)
	imls                        = FloatArrayField()
	poes                        = FloatArrayField()
	 

	def __unicode__(self):
		return self.job.name+' curve'


class Classical_PSHA_Hazard_Maps(models.Model):

	location                    = models.ForeignKey(Classical_PSHA_Hazard_Curves)
	poe                         = models.FloatField()
	iml                         = models.FloatField()
	 

	def __unicode__(self):
		return self.job.name+' map'



class Classical_PSHA_Risk(models.Model):
	private                     = models.BooleanField(default=False)
	user                        = models.ForeignKey(User)
	date_created                = models.DateTimeField('date created')
	name                        = models.CharField(max_length=200)
	description                 = models.CharField(max_length=200, null=True)

	random_seed                 = models.IntegerField(default=3)

	exposure_model              = models.ForeignKey(Exposure_Model)

	hazard                      = models.ForeignKey(Classical_PSHA_Hazard, null=True, blank=True)
	asset_hazard_distance       = models.FloatField()
	lrem_steps_per_interval     = models.IntegerField(null=True, blank=True)
	asset_correlation           = models.FloatField()
	insured_losses              = models.BooleanField(default=False)            

	vulnerability_models        = models.ManyToManyField(Vulnerability_Model, through='Classical_PSHA_Risk_Vulnerability')

	region                      = models.PolygonField(srid=4326)

	quantile_loss_curves        = FloatArrayField(null=True)
	poes                        = FloatArrayField(null=True)
	
	ini_file                    = models.FileField(upload_to='uploads/psha/risk/', null=True, blank=True)

	status                      = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED)
	oq_id                       = models.IntegerField(null=True)


	def __unicode__(self):
		return self.name


class Classical_PSHA_Risk_Vulnerability(models.Model):
	job                         = models.ForeignKey(Classical_PSHA_Risk)
	vulnerability_model         = models.ForeignKey(Vulnerability_Model)
	
	it_loss_values_agg			= FloatArrayField(null=True)
	at_loss_rates_agg			= FloatArrayField(null=True)
	periods_agg 				= FloatArrayField(null=True)
	default_periods_agg			= FloatArrayField(null=True)
	it_loss_values_table_agg	= FloatArrayField(null=True)
	aal_agg 					= models.FloatField(null=True)
	tce_agg 					= FloatArrayField(null=True)

	it_loss_values_occ			= FloatArrayField(null=True)
	at_loss_rates_occ			= FloatArrayField(null=True)
	periods_occ					= FloatArrayField(null=True)
	default_periods_occ			= FloatArrayField(null=True)
	it_loss_values_table_occ	= FloatArrayField(null=True)
	aal_occ 					= models.FloatField(null=True)
	tce_occ 					= FloatArrayField(null=True)

class Classical_PSHA_Risk_Loss_Curves(models.Model):
	vulnerability_model         = models.ForeignKey(Classical_PSHA_Risk_Vulnerability)
	asset                       = models.ForeignKey(Asset)
	
	hazard_output_id            = models.IntegerField(null=True)
	statistics                  = models.CharField(max_length=20, null=True)
	quantile                    = models.FloatField(null=True)
	loss_ratios                 = FloatArrayField()
	poes                        = FloatArrayField()       
	average_loss_ratio          = models.FloatField()
	stddev_loss_ratio           = models.FloatField(null=True)
	asset_value                 = models.FloatField()
	insured                     = models.BooleanField(default=False)            



class Classical_PSHA_Risk_Loss_Maps(models.Model):
	vulnerability_model         = models.ForeignKey(Classical_PSHA_Risk_Vulnerability)
	asset                       = models.ForeignKey(Asset)

	hazard_output_id            = models.IntegerField(null=True)   
	statistics                  = models.CharField(max_length=20, null=True)
	quantile                    = models.FloatField(null=True) 
	poe                         = models.FloatField()
	mean                        = models.FloatField()
	stddev                      = models.FloatField(null=True)
	insured                     = models.BooleanField(default=False)            



class Event_Based_Hazard(Classical_PSHA_Hazard):
	ses_per_logic_tree_path     = models.IntegerField()

	def __unicode__(self):
		return self.name


class Event_Based_Hazard_SES_Rupture(models.Model):
	job 						= models.ForeignKey(Event_Based_Hazard)
	rake 						= models.FloatField()
	magnitude 					= models.FloatField()
	location 					= models.PointField(srid=4326)
	depth 						= models.FloatField()
	output_id 					= models.IntegerField()
	ses_id                      = models.IntegerField()
	rupture_id                  = models.IntegerField()
	# rupture_oq                  = models.IntegerField()
	weight 						= models.FloatField()



class Event_Based_Risk(Classical_PSHA_Risk):
	hazard_event_based          = models.ForeignKey(Event_Based_Hazard)
	loss_curve_resolution 		= models.IntegerField()



# class Event_Loss_Table(models.Model):
# 	rupture                     = models.ForeignKey(Event_Based_Hazard_SES_Rupture)
# 	job_vulnerability           = models.ForeignKey(Classical_PSHA_Risk_Vulnerability)
# 	asset                       = models.ForeignKey(Asset)
# 	loss                        = models.FloatField()


# class Ses_to_Risk(models.Model):
# 	ses_collection_id 			= models.IntegerField()
# 	ses_output_id		 		= models.IntegerField()
# 	gmf_id						= models.IntegerField()
# 	hzrdr_job_id 				= models.IntegerField()
# 	riskr_job_id 				= models.IntegerField()
# 	weight 						= models.FloatField()


# class Risk(models.Model):
# 	rupture_id 					= models.IntegerField()
# 	loss 						= models.FloatField()
# 	hazard_output_id 			= models.IntegerField()
# 	job_vulnerability           = models.ForeignKey(Classical_PSHA_Risk_Vulnerability)
#  	asset                       = models.ForeignKey(Asset)


# class Loss(models.Model):
# 	ses_id 						= models.IntegerField()
# 	loss_total 					= models.FloatField()
# 	hazard_output_id 			= models.IntegerField()
# 	job_vulnerability           = models.ForeignKey(Classical_PSHA_Risk_Vulnerability)
#  	asset                       = models.ForeignKey(Asset)
# 	weight 						= models.FloatField()





