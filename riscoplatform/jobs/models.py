from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from world.models import World, Fishnet
from eng_models.models import Site_Model, Rupture_Model, Fragility_Model, Exposure_Model, Asset

# Create your models here.

class Scenario_Hazard(models.Model):

    ABRAHAMSON_AND_SILVA_2008 		= 'AbrahamsonSilva2008'
    AKKAR_AND_BOMMER_2010 			= 'AkkarBommer2010'
    AKKAR_AND_CAGNAN_2010 			= 'AkkarCagnan2010'
    BOORE_AND_ATKINSON_2008 		= 'BooreAtkinson2008'
    CAUZZI_AND_FACCIOLI_2008 		= 'CauzziFaccioli2008'
    CHIOU_AND_YOUNGS_2008 			= 'ChiouYoungs2008'
    FACCIOLI_ET_AL_2010 			= 'FaccioliEtAl2010'
    SADIGH_ET_AL_1997 				= 'SadighEtAl1997'
    ZHAO_ET_AL_2006_ASC 			= 'ZhaoEtAl2006Asc'
    ATKINSON_AND_BOORE_2003_INTER 	= 'AtkinsonBoore2003SInter'
    ATKINSON_AND_BOORE_2003_IN_SLAB = 'AtkinsonBoore2003SSlab'
    LIN_AND_LEE_2008_INTER 			= 'LinLee2008SInter'
    LIN_AND_LEE_2008_IN_SLAB 		= 'LinLee2008SSlab'
    YOUNGS_ET_AL_1997_INTER 		= 'YoungsEtAl1997SInter'
    YOUNGS_ET_AL_1997_IN_SLAB 		= 'YoungsEtAl1997SSlab'
    ZHAO_ET_AL_2006_INTER 			= 'ZhaoEtAl2006SInter'
    ZHAO_ET_AL_2006_IN_SLAB 		= 'ZhaoEtAl2006SSlab'
    ATKINSON_AND_BOORE_2006 		= 'AtkinsonBoore2006'
    CAMPBELL_2003 					= 'Campbell2003'
    TORO_ET_AL_2002 				= 'ToroEtAl2002'

    GMPE_CHOICES = (
    	(ABRAHAMSON_AND_SILVA_2008 			,'Abrahamson and Silva 2008'),
	    (AKKAR_AND_BOMMER_2010 				,'Akkar and Boomer 2010'),
	    (AKKAR_AND_CAGNAN_2010 				,'Akkar and Cagnan 2010'),
	    (BOORE_AND_ATKINSON_2008 			,'Boore and Atkinson 2008'),
	    (CAUZZI_AND_FACCIOLI_2008 			,'Cauzzi and Faccioli 2008'),
	    (CHIOU_AND_YOUNGS_2008 				,'Chiou and Youngs 2008'),
	    (FACCIOLI_ET_AL_2010 				,'Faccioli et al. 2010'),
	    (SADIGH_ET_AL_1997 					,'Sadigh et al. 1997'),
	    (ZHAO_ET_AL_2006_ASC 				,'Zhao et al. 2006 (ASC)'),
	    (ATKINSON_AND_BOORE_2003_INTER 		,'Atkinson and Boore 2003 (Inter)'),
	    (ATKINSON_AND_BOORE_2003_IN_SLAB 	,'Atkinson and Boore 2003 (In-slab)'),
	    (LIN_AND_LEE_2008_INTER 			,'Lin and Lee 2008 (Inter)'),
	    (LIN_AND_LEE_2008_IN_SLAB 			,'Lin and Lee 2008 (In-slab)'),
	    (YOUNGS_ET_AL_1997_INTER 			,'Youngs et al. 1997 (Inter)'),
	    (YOUNGS_ET_AL_1997_IN_SLAB 			,'Youngs et al. 1997 (In-slab)'),
	    (ZHAO_ET_AL_2006_INTER 				,'Zhao et al. 2006 (Inter)'),
	    (ZHAO_ET_AL_2006_IN_SLAB 			,'Zhao et al. 2006 (In-slab)'),
	    (ATKINSON_AND_BOORE_2006 			,'Atkinson and Boore 2006'),
	    (CAMPBELL_2003 						,'Campbell 2003'),
	    (TORO_ET_AL_2002 					,'Toro et al. 2002'),
    )

    MODEL = 'VARIABLE_CONDITIONS'
    DEFAULT = 'DEFAULT_CONDITIONS'
    SITES_CHOICES = (
        (MODEL, 'Site model'),
        (DEFAULT, 'Default conditions'),
        )

    MEASURED = 'MEASURED'
    INFERRED = 'INFERRED'
    VS30_CHOICES = (
        (MEASURED, 'measured'),
        (INFERRED, 'inferred'),
    )

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
    sa1_period					= models.FloatField(null=True, blank=True)
    sa2_period					= models.FloatField(null=True, blank=True)
    sa3_period					= models.FloatField(null=True, blank=True)
    truncation_level			= models.FloatField(default=3)
    max_distance				= models.FloatField(default=200)
    gmpe						= models.CharField(max_length=50, choices=GMPE_CHOICES)
    correlation_model			= models.BooleanField(default=True)
    vs30_clustering 			= models.BooleanField(default=False)
    n_gmf 						= models.IntegerField(default=50)

    ini_file                    = models.FileField(upload_to='uploads/scenario/hazard/', null=True, blank=True)

    start                       = models.BooleanField(default=False)
    error                       = models.BooleanField(default=False)
    ready                       = models.BooleanField(default=False)
    oq_id                       = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super(Scenario_Hazard, self).save(*args, **kwargs)

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


class Scenario_Damage(models.Model):
    user                        = models.ForeignKey(User)
    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200, null=True)
    hazard_job                  = models.ForeignKey(Scenario_Hazard)
    fragility_model             = models.ForeignKey(Fragility_Model)
    exposure_model              = models.ForeignKey(Exposure_Model)
    region                      = models.PolygonField(srid=4326)
    max_hazard_dist             = models.FloatField()

    start                       = models.BooleanField(default=False)
    error                       = models.BooleanField(default=False)
    ready                       = models.BooleanField(default=False)
    oq_id                       = models.IntegerField(null=True)

    ini_file                    = models.FileField(upload_to='uploads/scenario/damage/', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Scenario_Damage_Results(models.Model):
    job                         = models.ForeignKey(Scenario_Damage)
    asset                       = models.ForeignKey(Asset)
    #limit state
    mean                        = models.FloatField()
    stddev                      = models.FloatField()

    def __unicode__(self):
        return self.job.name+' results'

        



