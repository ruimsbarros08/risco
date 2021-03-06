from django.db import models
from django.contrib.gis.db import models

# Create your models here.


class Fishnet(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    cell = models.PolygonField()
    spacing = models.IntegerField()
    objects = models.GeoManager()

    class Meta:
        managed = True
        db_table = 'world_fishnet'


class Country(models.Model):
    name = models.CharField(max_length=75)
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=3)
    geom = models.MultiPolygonField()
    geom_simp = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Country_Simp(models.Model):
    name = models.CharField(max_length=75)
    iso = models.CharField(max_length=3)
    geom = models.MultiPolygonField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Adm_1(models.Model):
    country = models.ForeignKey(Country, null=True)
    name = models.CharField(max_length=75)
    id_1 = models.IntegerField(null=True)
    type = models.CharField(max_length=50, null=True)
    geom = models.MultiPolygonField()
    geom_simp = models.MultiPolygonField(null=True)
    new = models.NullBooleanField(default=True, null=True)
    country_name = models.CharField(max_length=75, null=True)
    country_iso = models.CharField(max_length=3, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Adm_2(models.Model):
    adm_1 = models.ForeignKey(Adm_1, null=True) 
    adm_1_name = models.CharField(max_length=75, null=True) 
    country_iso = models.CharField(max_length=3, null=True) 
    name = models.CharField(max_length=75)
    id_2 = models.IntegerField(null=True)
    type = models.CharField(max_length=50, null=True)
    geom = models.MultiPolygonField()
    geom_simp = models.MultiPolygonField(null=True)
    repeated = models.NullBooleanField(default=False, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class World(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    objectid = models.IntegerField()
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=3)
    name_0 = models.CharField(max_length=75)
    id_1 = models.IntegerField()
    name_1 = models.CharField(max_length=75)
    varname_1 = models.CharField(max_length=150)
    nl_name_1 = models.CharField(max_length=50)
    hasc_1 = models.CharField(max_length=15)
    cc_1 = models.CharField(max_length=15)
    type_1 = models.CharField(max_length=50)
    engtype_1 = models.CharField(max_length=50)
    validfr_1 = models.CharField(max_length=25)
    validto_1 = models.CharField(max_length=25)
    remarks_1 = models.CharField(max_length=125)
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=75)
    varname_2 = models.CharField(max_length=150)
    nl_name_2 = models.CharField(max_length=75)
    hasc_2 = models.CharField(max_length=15)
    cc_2 = models.CharField(max_length=15)
    type_2 = models.CharField(max_length=50)
    engtype_2 = models.CharField(max_length=50)
    validfr_2 = models.CharField(max_length=25)
    validto_2 = models.CharField(max_length=25)
    remarks_2 = models.CharField(max_length=100)
    id_3 = models.IntegerField()
    name_3 = models.CharField(max_length=75)
    varname_3 = models.CharField(max_length=100)
    nl_name_3 = models.CharField(max_length=75)
    hasc_3 = models.CharField(max_length=25)
    type_3 = models.CharField(max_length=50)
    engtype_3 = models.CharField(max_length=50)
    validfr_3 = models.CharField(max_length=25)
    validto_3 = models.CharField(max_length=25)
    remarks_3 = models.CharField(max_length=50)
    id_4 = models.IntegerField()
    name_4 = models.CharField(max_length=100)
    varname_4 = models.CharField(max_length=100)
    type4 = models.CharField(max_length=25)
    engtype4 = models.CharField(max_length=25)
    type_4 = models.CharField(max_length=35)
    engtype_4 = models.CharField(max_length=35)
    validfr_4 = models.CharField(max_length=25)
    validto_4 = models.CharField(max_length=25)
    remarks_4 = models.CharField(max_length=50)
    id_5 = models.IntegerField()
    name_5 = models.CharField(max_length=75)
    type_5 = models.CharField(max_length=25)
    engtype_5 = models.CharField(max_length=25)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField()
    objects = models.GeoManager()

    class Meta:
        managed = True
        db_table = 'world_world'


