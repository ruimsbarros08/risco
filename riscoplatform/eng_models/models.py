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


def file2string(file):
    with open(file, 'r') as f:
        content = f.read()
        return content

class Exposure_Model(models.Model):

    SQUARED_METERS = 'squared_meters'
    HECTARE = 'hectare'
    UNIT_CHOICES = (
        (SQUARED_METERS, 'squared meters'),
        (HECTARE, 'hectare')
    )

    AGGREGATED = 'aggregated'
    PER_UNIT = 'per_unit'
    AGG_CHOICES = (
        (AGGREGATED, 'aggregated'),
        (PER_UNIT, 'per_unit'),
    )

    EURO = 'EUR'
    DOLLAR = 'DOL'
    CURRENCY_CHOICES = (
        (EURO, 'eur'),
        (DOLLAR, 'dol'),
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
    area_type                   = models.CharField(max_length=20, choices=AGG_CHOICES, default=AGGREGATED, null=True)
    area_unit                   = models.CharField(max_length=20, choices=UNIT_CHOICES, default=SQUARED_METERS, null=True)
    struct_cost_type            = models.CharField(max_length=20, choices=AGG_CHOICES, default=AGGREGATED, null=True)
    struct_cost_currency        = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=EURO, null=True)
    non_struct_cost_type        = models.CharField(max_length=20, choices=AGG_CHOICES, default=AGGREGATED, null=True)
    non_struct_cost_currency    = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=EURO, null=True)
    contents_cost_type          = models.CharField(max_length=20, choices=AGG_CHOICES, default=AGGREGATED, null=True)
    contents_cost_currency      = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=EURO, null=True)
    business_int_cost_type      = models.CharField(max_length=20, choices=AGG_CHOICES, default=AGGREGATED, null=True)
    business_int_cost_currency  = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=EURO, null=True)
    deductible                  = models.CharField(max_length=20, choices=INSURANCE_SETTINGS, default=ABSOLUTE, null=True)
    insurance_limit             = models.CharField(max_length=20, choices=INSURANCE_SETTINGS, default=ABSOLUTE, null=True)
    xml                         = models.FileField(upload_to='uploads/exposure/', null=True, blank=True)
    xml_string                  = models.TextField(null=True)

    def save(self, *args, **kwargs):
        self.xml_string = file2string(self.xml)
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
    name                        = models.CharField(max_length=10, unique=True)
    description                 = models.CharField(max_length=200, null=True)
    material                    = models.CharField(max_length=10, null=True)
    nstoreys                    = models.CharField(max_length=10, null=True)

    class Meta:
        managed = True
        db_table = 'eng_models_building_taxonomy'

    def __unicode__(self):
        return self.name        


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
    xml_string                  = models.TextField(null=True)

    def save(self, *args, **kwargs):
        self.xml_string = file2string(self.xml)
        super(Exposure_Model, self).save(*args, **kwargs)

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


class Fault_Model(models.Model):
    date_created                = models.DateTimeField('date created')
    name                        = models.CharField(max_length=200)
    description                 = models.CharField(max_length=200)
    contributors                = models.ManyToManyField(User, through='Fault_Model_Contributor')
    xml                         = models.FileField(upload_to='uploads/fault/', null=True, blank=True)
    xml_string                  = models.TextField(null=True)

    def save(self, *args, **kwargs):
        self.xml_string = file2string(self.xml)
        super(Exposure_Model, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'eng_models_fault_model'

class Fault_Model_Contributor(models.Model):
    contributor                 = models.ForeignKey(User)
    model                       = models.ForeignKey(Fault_Model)
    author                      = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField('date joined')

    class Meta:
        managed = True
        db_table = 'eng_models_fault_model_contributor'


class Fault(models.Model):
    model                       = models.ForeignKey(Site_Model)
    name                        = models.CharField(max_length=200)
    mindepth                    = models.FloatField()
    maxdepth                    = models.FloatField()
    strike                      = models.IntegerField()
    dip                         = models.IntegerField()
    rake                        = models.IntegerField()
    sr                          = models.FloatField()
    maxmag                      = models.FloatField()
    #geom                        = models.MultiLineStringField(srid=4326)
    geom                        = models.LineStringField(srid=4326, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'eng_models_fault'


