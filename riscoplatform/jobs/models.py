from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from world.models import World
from eng_models.models import Site_Model, Fault_Model, Fault

# Create your models here.

def file2string(file):
    with open(file, 'r') as f:
        content = f.read()
        return content

class Scenario_Hazard(models.Model):

    ABRAHAMSON_AND_SILVA_2008 		= 'ABRAHAMSON_AND_SILVA_2008'
    AKKAR_AND_BOMMER_2010 			= 'AKKAR_AND_BOMMER_2010'
    AKKAR_AND_CAGNAN_2010 			= 'AKKAR_AND_CAGNAN_2010'
    BOORE_AND_ATKINSON_2008 		= 'BOORE_AND_ATKINSON_2008'
    CAUZZI_AND_FACCIOLI_2008 		= 'CAUZZI_AND_FACCIOLI_2008'
    CHIOU_AND_YOUNGS_2008 			= 'CHIOU_AND_YOUNGS_2008'
    FACCIOLI_ET_AL_2010 			= 'FACCIOLI_ET_AL_2010'
    SADIGH_ET_AL_1997 				= 'SADIGH_ET_AL_1997'
    ZHAO_ET_AL_2006_ASC 			= 'ZHAO_ET_AL_2006_ASC'
    ATKINSON_AND_BOORE_2003_INTER 	= 'ATKINSON_AND_BOORE_2003_INTER'
    ATKINSON_AND_BOORE_2003_IN_SLAB = 'ATKINSON_AND_BOORE_2003_IN_SLAB'
    LIN_AND_LEE_2008_INTER 			= 'LIN_AND_LEE_2008_INTER'
    LIN_AND_LEE_2008_IN_SLAB 		= 'LIN_AND_LEE_2008_IN_SLAB'
    YOUNGS_ET_AL_1997_INTER 		= 'YOUNGS_ET_AL_1997_INTER'
    YOUNGS_ET_AL_1997_IN_SLAB 		= 'YOUNGS_ET_AL_1997_IN_SLAB'
    ZHAO_ET_AL_2006_INTER 			= 'ZHAO_ET_AL_2006_INTER'
    ZHAO_ET_AL_2006_IN_SLAB 		= 'ZHAO_ET_AL_2006_IN_SLAB'
    ATKINSON_AND_BOORE_2006 		= 'ATKINSON_AND_BOORE_2006'
    CAMPBELL_2003 					= 'CAMPBELL_2003'
    TORO_ET_AL_2002 				= 'TORO_ET_AL_2002'

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

    CLOSEST = 'CLOSEST_FAULT'
    CUSTOM = 'CUSTOM_RUPTURE'
    UPLOAD = 'UPLOAD_XML'
    RUPTURE_CHOICES = (
        (CLOSEST, 'closest fault'),
        (CUSTOM, 'custom rupture'),
        (UPLOAD, 'upload xml'),
    )

    user 						= models.ForeignKey(User)
    date_created 				= models.DateTimeField('date created')
    name 						= models.CharField(max_length=200)
    description 				= models.CharField(max_length=200, null=True)

    #Region
    region  					= models.PolygonField(srid=4326, null=True)
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

    #rupture
    rupture_type                = models.CharField(max_length=50, choices=RUPTURE_CHOICES, default=CLOSEST)
    #Closest
    magnitude 					= models.FloatField(null=True, blank=True)
    location 					= models.PointField(srid=4326, null=True, blank=True)
    depth 						= models.FloatField(null=True, blank=True)
    fault_model                 = models.ForeignKey(Fault_Model, null=True, blank=True)
    fault                       = models.ForeignKey(Fault, null=True, blank=True)
    #Custom
    rake                        = models.FloatField(null=True, blank=True)
    upper_depth                 = models.FloatField(null=True, blank=True)
    lower_depth                 = models.FloatField(null=True, blank=True)
    dip                         = models.FloatField(null=True, blank=True)
    rupture_geom                = models.LineStringField(srid=4326, null=True, blank=True)
    #upload
    rupture_xml                 = models.FileField(upload_to='uploads/rupture/', null=True, blank=True)
    rupture_xml_string          = models.TextField(null=True)

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
    ini_file_string             = models.TextField(null=True)

    error                       = models.BooleanField(default=False)
    ready                       = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.rupture_xml_string = file2string(rupture_xml)
        self.ini_file_string = file2string(ini_file)
        super(Scenario_Hazard, self).save(*args, **kwargs)

    def __unicode__(self):
    	return self.name

    class Meta:
        managed = True
        db_table = 'jobs_scenario_hazard'


