# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.

from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from world.models import World, Fishnet
from django.core.files import File
from django.template.loader import render_to_string
from djorm_pgarray.fields import FloatArrayField
from scipy.stats import lognorm
import numpy as np


class Building_Taxonomy_Source(models.Model):
    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200, null=True)
    contributors                = models.ManyToManyField(User, through='Building_Taxonomy_Source_Contributor')

    class Meta:
        managed = True
        db_table = 'eng_models_building_taxonomy_source'

    def __unicode__(self):
        return self.name


class Building_Taxonomy_Source_Contributor(models.Model):
    contributor                 = models.ForeignKey(User)
    source                      = models.ForeignKey(Building_Taxonomy_Source)
    author                      = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField('date joined')

    class Meta:
        managed = True
        db_table = 'eng_models_building_taxonomy_source_contributor'
        

class Building_Taxonomy(models.Model):
    source                      = models.ForeignKey(Building_Taxonomy_Source)
    name                        = models.CharField(max_length=20)
    description                 = models.CharField(max_length=200, null=True)
    material                    = models.CharField(max_length=10, null=True)
    nstoreys                    = models.CharField(max_length=10, null=True)

    class Meta:
        managed = True
        db_table = 'eng_models_building_taxonomy'

    def __unicode__(self):
        return self.name        


class Exposure_Model(models.Model):

    SQUARED_METERS = 'squared meters'
    HECTARE = 'hectare'
    UNIT_CHOICES = (
        (SQUARED_METERS, 'Squared meters'),
        (HECTARE, 'Hectare')
    )

    AGGREGATED = 'aggregated'
    PER_UNIT = 'per_unit'
    PER_AREA = 'per_area'
    AGG_CHOICES = (
        (AGGREGATED, 'Aggregated'),
        (PER_UNIT, 'Per unit'),
        (PER_AREA, 'Per area'),
    )

    EURO = 'EUR'
    DOLLAR = 'DOL'
    CURRENCY_CHOICES = (
        (EURO, 'Euro'),
        (DOLLAR, 'Dollar'),
    )

    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'
    INSURANCE_SETTINGS = (
        (ABSOLUTE, 'absolute'),
        (RELATIVE, 'relative')
    )


    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200)
    contributors                = models.ManyToManyField(User, through='Exposure_Model_Contributor')
    taxonomy_source             = models.ForeignKey(Building_Taxonomy_Source, blank=True, null=True)
    area_type                   = models.CharField(max_length=20, choices=AGG_CHOICES, null=True)
    area_unit                   = models.CharField(max_length=20, choices=UNIT_CHOICES, null=True)
    struct_cost_type            = models.CharField(max_length=20, choices=AGG_CHOICES, null=True)
    struct_cost_currency        = models.CharField(max_length=5, choices=CURRENCY_CHOICES, null=True)
    non_struct_cost_type        = models.CharField(max_length=20, choices=AGG_CHOICES, null=True)
    non_struct_cost_currency    = models.CharField(max_length=5, choices=CURRENCY_CHOICES, null=True)
    contents_cost_type          = models.CharField(max_length=20, choices=AGG_CHOICES, null=True)
    contents_cost_currency      = models.CharField(max_length=5, choices=CURRENCY_CHOICES, null=True)
    business_int_cost_type      = models.CharField(max_length=20, choices=AGG_CHOICES, null=True)
    business_int_cost_currency  = models.CharField(max_length=5, choices=CURRENCY_CHOICES, null=True)
    deductible                  = models.CharField(max_length=20, choices=INSURANCE_SETTINGS, null=True)
    insurance_limit             = models.CharField(max_length=20, choices=INSURANCE_SETTINGS, null=True)
    xml                         = models.FileField(upload_to='uploads/exposure/', null=True, blank=True)
    oq_id                       = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super(Exposure_Model, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'eng_models_exposure_model'


    def __unicode__(self):
        return self.name


class Exposure_Model_Contributor(models.Model):
    contributor                 = models.ForeignKey(User)
    model                       = models.ForeignKey(Exposure_Model)
    author                      = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField('date joined')

    class Meta:
        managed = True
        db_table = 'eng_models_exposure_model_contributor'




class Asset(models.Model):
    model                       = models.ForeignKey(Exposure_Model)
    taxonomy                    = models.ForeignKey(Building_Taxonomy)
    parish                      = models.ForeignKey(World, null=True)
    location                    = models.PointField(null=True, srid=4326)
    name                        = models.CharField(max_length=10)
    n_buildings                 = models.IntegerField()
    area                        = models.FloatField()
    struct_cost                 = models.FloatField(null=True)
    struct_deductible           = models.FloatField(null=True)
    struct_insurance_limit      = models.FloatField(null=True)
    retrofitting_cost           = models.FloatField(null=True)
    non_struct_cost             = models.FloatField(null=True)
    non_struct_deductible       = models.FloatField(null=True)
    non_struct_insurance_limit  = models.FloatField(null=True)
    contents_cost               = models.FloatField(null=True)
    contents_deductible         = models.FloatField(null=True)
    contents_insurance_limit    = models.FloatField(null=True)
    business_int_cost           = models.FloatField(null=True)
    business_int_deductible     = models.FloatField(null=True)
    business_int_insurance_limit= models.FloatField(null=True)
    oc_day                      = models.FloatField(null=True)
    oc_night                    = models.FloatField(null=True)
    oc_transit                  = models.FloatField(null=True)

    class Meta:
        managed = True
        db_table = 'eng_models_asset'

    def __unicode__(self):
        return self.name


class Site_Model(models.Model):
    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200)
    contributors                = models.ManyToManyField(User, through='Site_Model_Contributor')
    xml                         = models.FileField(upload_to='uploads/site/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Site_Model, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'eng_models_site_model'

    def __unicode__(self):
        return self.name

class Site_Model_Contributor(models.Model):
    contributor                 = models.ForeignKey(User)
    model                       = models.ForeignKey(Site_Model)
    author                      = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField('date joined')

    class Meta:
        managed = True
        db_table = 'eng_models_site_model_contributor'


class Site(models.Model):
    MEASURED = 'measured'
    INFERRED = 'inferred'
    CHOICES = (
        (MEASURED, 'measured'),
        (INFERRED, 'inferred'),
    )

    model                       = models.ForeignKey(Site_Model)
    location                    = models.PointField(srid=4326)
    vs30                        = models.FloatField()
    vs30type                    = models.CharField(max_length=10, choices=CHOICES, default=MEASURED)
    z1pt0                       = models.FloatField()
    z2pt5                       = models.FloatField()
    lat                         = models.FloatField(null=True)
    lon                         = models.FloatField(null=True)
    cell                        = models.ForeignKey(Fishnet, null=True)

    class Meta:
        managed = True
        db_table = 'eng_models_site'


    def save(self, *args, **kwargs):
        self.lat = self.location.y
        self.lon = self.location.x   
        super(Site, self).save(*args, **kwargs)


class Source_Model(models.Model):
    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200)
    contributors                = models.ManyToManyField(User, through='Source_Model_Contributor')
    xml                         = models.FileField(upload_to='uploads/source/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Source_Model, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Source_Model_Contributor(models.Model):
    contributor                 = models.ForeignKey(User)
    model                       = models.ForeignKey(Source_Model)
    author                      = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField('date joined')


class Source(models.Model):
    ACTIVE = 'Active Shallow Crust'
    STABLE = 'Stable Shallow Crust'
    SUBDUCTION = 'Subduction Interface'
    ACTIVE_INTERSLAB = 'Active Interslab'
    VOLCANIC = 'Volcanic'
    TECTONIC_CHOICES = (
        (ACTIVE, 'Active Shallow Crust'),
        (STABLE, 'Stable Shallow Crust'),
        (SUBDUCTION, 'Subduction Interface'),
        (ACTIVE_INTERSLAB, 'Active Interslab'),
        (VOLCANIC, 'Volcanic'),
        )

    WC1994 = 'WC1994'
    TA2012 = 'TA2012'
    MAG_SCALE_REL = (
        (WC1994, 'Wells and Coopersmith 1994'),
        (WC1994, 'Thomas et al. 2012 (PEER)'),
        )

    TRUNC = 'TRUNC'
    INC = 'INC'
    MAG_FREQ_DIST_CHOICES = (
        (TRUNC, 'Truncated Guttenberg Richer'),
        (INC, 'Incremental MFD'),
        )

    POINT = 'POINT'
    AREA = 'AREA'
    SIMPLE_FAULT = 'SIMPLE_FAULT'
    #COMPLEX_FAULT = 'COMPLEX_FAULT'
    SOURCE_TYPES_CHOICES = (
        (POINT, 'Point'),
        (AREA, 'Area'),
        (SIMPLE_FAULT, 'Simple Fault'),
    #    (COMPLEX_FAULT, 'Complex Fault'),
        )

    model                       = models.ForeignKey(Source_Model)
    name                        = models.CharField(max_length=200)
    
    tectonic_region             = models.CharField(max_length=50, choices=TECTONIC_CHOICES, default=ACTIVE)
    mag_scale_rel               = models.CharField(max_length=50, choices=MAG_SCALE_REL, default=WC1994)
    rupt_aspect_ratio           = models.FloatField(default=2.0)

    mag_freq_dist_type          = models.CharField(max_length=10, choices=MAG_FREQ_DIST_CHOICES, default=TRUNC)
    #trunc
    a                           = models.FloatField(null=True, default=-3.5)
    b                           = models.FloatField(null=True, default=-1.0)
    min_mag                     = models.FloatField(null=True)
    max_mag                     = models.FloatField(null=True)
    #inc
    bin_width                   = models.FloatField(null=True)
    occur_rates                 = FloatArrayField(null=True)

    source_type                 = models.CharField(max_length=20, choices=SOURCE_TYPES_CHOICES, default=POINT)
    #point
    point                       = models.PointField(srid=4326, null=True)
    upper_depth                 = models.FloatField(null=True, default=0)
    lower_depth                 = models.FloatField(null=True, default=10)
    nodal_plane_dist            = FloatArrayField(null=True, dimension=4)
    hypo_depth_dist             = FloatArrayField(null=True, dimension=2)
    #area
    area                        = models.PolygonField(srid=4326, null=True)
    #fault
    fault                       = models.LineStringField(srid=4326, null=True)
    dip                         = models.IntegerField()
    rake                        = models.IntegerField()

    def __unicode__(self):
        return self.name

    #class Meta:
    #    managed = True
    #    db_table = 'eng_models_fault'


class Rupture_Model(models.Model):
    #CLOSEST = 'CLOSEST_FAULT'
    CUSTOM = 'CUSTOM_RUPTURE'
    UPLOAD = 'UPLOAD_XML'
    INPUT_CHOICES = (
#        (CLOSEST, 'closest fault'),
        (CUSTOM, 'custom rupture'),
        (UPLOAD, 'upload xml'),
    )

    POINT = 'POINT'
    FAULT = 'FAULT'
    RUPTURE_TYPES = (
        (POINT, 'Point'),
        (FAULT, 'Fault'),
        )

    user                        = models.ForeignKey(User)
    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200, null=True)

    input_type                  = models.CharField(max_length=50, choices=INPUT_CHOICES, default=CUSTOM)
    rupture_type                = models.CharField(max_length=50, choices=RUPTURE_TYPES, default=FAULT)
    magnitude                   = models.FloatField(null=True, blank=True)
    depth                       = models.FloatField(null=True, blank=True)
    rake                        = models.FloatField(null=True, blank=True)
    upper_depth                 = models.FloatField(null=True, blank=True)
    lower_depth                 = models.FloatField(null=True, blank=True)
    dip                         = models.FloatField(null=True, blank=True)
    
    location                    = models.PointField(srid=4326)
    rupture_geom                = models.LineStringField(srid=4326, null=True, blank=True)
    
    #Closest
    #fault_model                 = models.ForeignKey(Fault_Model, null=True, blank=True)
    #fault                       = models.ForeignKey(Fault, null=True, blank=True)
    #upload
    
    xml                         = models.FileField(upload_to='uploads/rupture/', null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.rupture_type == 'POINT':
            string = str(render_to_string('eng_models/rupture_point_source.xml', {'rupture': self}))
        else:
            string = str(render_to_string('eng_models/rupture_fault_source.xml', {'rupture': self}))
        #f = open('/tmp/rupture.xml', 'rw')
        #djangofile = File(f)
        #djangofile.write(string)
        #self.xml = djangofile

        super(Rupture_Model, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.name


class Fragility_Model(models.Model):

    CONTINUOUS = 'continuous'
    DISCRETE = 'discrete'
    FORMAT_CHOICES =(
        (CONTINUOUS, 'Continuous'),
        (DISCRETE, 'Discrete'),
        )

    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200)
    contributors                = models.ManyToManyField(User, through='Fragility_Model_Contributor')
    taxonomy_source             = models.ForeignKey(Building_Taxonomy_Source)
    format                      = models.CharField(max_length=10, choices=FORMAT_CHOICES, default=CONTINUOUS)

    xml                         = models.FileField(upload_to='uploads/fragility/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Fragility_Model, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Fragility_Model_Contributor(models.Model):
    contributor                 = models.ForeignKey(User)
    model                       = models.ForeignKey(Fragility_Model)
    author                      = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField('date joined')


class Taxonomy_Fragility_Model(models.Model):
    PGA = 'PGA'
    PGV = 'PGV'
    MMI = 'MMI'
    SA = 'SA'
    IMT_CHOICES = (
        (PGA, 'PGA'),
        (PGV, 'PGV'),
        (MMI, 'MMI'),
        (SA, 'Sa'),
        )
    
    LOGNORMAL = 'lognormal'
    DIST_TYPES = (
        (LOGNORMAL, 'Lognormal'),
        )

    model                       = models.ForeignKey(Fragility_Model)
    taxonomy                    = models.ForeignKey(Building_Taxonomy)
    dist_type                   = models.CharField(max_length=20, choices=DIST_TYPES, default=LOGNORMAL)
    imt                         = models.CharField(max_length=3, choices=IMT_CHOICES, default=PGA)
    sa_period                   = models.FloatField(null=True)
    unit                        = models.CharField(max_length=3)
    min_iml                     = models.FloatField(null=True)
    max_iml                     = models.FloatField(null=True)
    no_dmg_limit                = models.FloatField(null=True)

        
class Fragility_Function(models.Model):

    NO_DAMAGE = 'no_damage'
    SLIGHT = 'slight'
    MODERATE = 'moderate'
    EXTENSIVE = 'extensive'
    COMPLETE = 'complete'
    LIMIT_STATES = (
        (NO_DAMAGE, 'no_damage'),
        (SLIGHT, 'Slight'),
        (MODERATE, 'Moderate'),
        (EXTENSIVE, 'Extensive'),
        (COMPLETE, 'Complete'),
        )

    tax_frag                    = models.ForeignKey(Taxonomy_Fragility_Model, null=True)
    limit_state                 = models.CharField(max_length=20, choices=LIMIT_STATES)
    #limit_state                 = models.ForeignKey(Limit_State)
    mean                        = models.FloatField(null=True)
    stddev                      = models.FloatField(null=True)
    pdf                         = FloatArrayField(dimension=2)
    cdf                         = FloatArrayField(dimension=2)

    def save(self, *args, **kwargs):
        dist = lognorm(float(self.stddev), loc = float(self.mean))
        #x = np.linspace(0, 2.5, 0.25)
        x = np.array([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5])
        pdf = dist.pdf(x)
        cdf = dist.cdf(x)
        self.pdf = [x.tolist(), pdf.tolist()]
        self.cdf = [x.tolist(), cdf.tolist()]

        super(Fragility_Function, self).save(*args, **kwargs)










