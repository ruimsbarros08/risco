import os
from django.contrib.gis.utils import LayerMapping
from models import *
from django.db import connection

cursor = connection.cursor()


#################
### COUNTRIES ###
#################

world_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name' : 'NAME_0',
    'geom' : 'MULTIPOLYGON',
}

world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'datasources/gadm/gadmV2_Level0.shp'))

def run(verbose=True):
    lm = LayerMapping(Country, world_shp, world_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


#def simplify_countries(verbose=True):
#    cursor.execute('UPDATE world_country SET geom_simp = ST_Multi( ST_SimplifyPreserveTopology(geom, 0.5) )')
#    connection.commit()


world_mapping_natural_earth = {
    'iso' : 'iso_a3',
    'name' : 'name',
    'geom' : 'MULTIPOLYGON',
}

world_shp_natural_earth = os.path.abspath(os.path.join(os.path.dirname(__file__), 'datasources/ne_50m_admin_0_countries_lakes/ne_50m_admin_0_countries_lakes.shp'))

def run_natural_earth(verbose=True):
    lm = LayerMapping(Country_Simp, world_shp_natural_earth, world_mapping_natural_earth, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


#def simplify_countries():
#    cursor.execute('UPDATE world_country \
#                    SET geom_simp = world_country_simp.geom \
#                    FROM world_country_simp \
#                    WHERE world_country.name = world_country_simp.name; \
#                    \
#                    UPDATE world_country \
#                    SET geom_simp = world_country_simp.geom \
#                    FROM world_country_simp \
#                    WHERE world_country.geom_simp is NULL \
#                    AND ST_Intersects(world_country_simp.geom, ST_PointOnSurface(world_country.geom)); \
#                    \
#                    UPDATE world_country \
#                    SET geom_simp = geom \
#                    WHERE geom_simp is NULL;')
#    connection.commit()




#############
### ADM 1 ###
#############



level1_mapping = {
    'name' : 'ADMIN_NAME',
    'type' : 'TYPE_ENG',
    'country_name' : 'CNTRY_NAME',
    'country_iso' : 'GMI_CNTRY',
    'geom' : 'MULTIPOLYGON',
}

level1_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'datasources/admin98/admin98.shp'))

def run_level1(verbose=True):
    lm = LayerMapping(Adm_1, level1_shp, level1_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


def match_country_adm1():
    cursor.execute('UPDATE world_adm_1 \
                    SET country_id = world_country.id \
                    FROM world_country \
                    WHERE world_country.iso = world_adm_1.country_iso \
                    AND world_adm_1.new = true ')
    connection.commit()


def match_missing_adm1():
    cursor.execute('UPDATE world_adm_1 \
                    SET country_id = \
                    (SELECT world_country.id \
                        FROM world_country \
                        WHERE ST_Contains(world_country.geom, ST_PointOnSurface(world_adm_1.geom))) \
                    WHERE world_adm_1.country_id IS NULL')
    connection.commit()



#############
### ADM 2 ###
#############


level2_mapping = {
    'name' : 'NAME_2',
    'adm_1_name' : 'NAME_1',
    'country_iso' : 'ISO',
    'geom' : 'MULTIPOLYGON',
}

level2_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'datasources/gadm_level2/gadm_v1_lev2_shp/gadm_v1_lev2.shp'))

def run_level2(verbose=True):
    lm = LayerMapping(Adm_2, level2_shp, level2_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


def match_missing_adm2_1():
    cursor.execute('UPDATE world_adm_2 \
                    SET adm_1_id = world_adm_1.id \
                    FROM world_adm_1 \
                    WHERE world_adm_2.country_iso = world_adm_1.country_iso \
                    AND world_adm_1.new = true \
                    AND world_adm_2.adm_1_name = world_adm_1.name')
    connection.commit()


def match_missing_adm2_2():
    cursor.execute('UPDATE world_adm_2 \
                    SET adm_1_id = world_adm_1.id \
                    FROM world_adm_1 \
                    WHERE world_adm_2.adm_1_id IS NULL \
                    AND ST_Contains(world_adm_1.geom, ST_PointOnSurface(world_adm_2.geom))')
                    #AND world_adm_2.country_iso = world_adm_1.country_iso \
    connection.commit()


def add_missing_adm2():
    cursor.execute('INSERT INTO world_adm_2 (name, geom, repeated, country_iso) \
                    SELECT name_1, geom, true, iso  \
                    FROM world_world \
                    WHERE iso NOT IN (SELECT country_iso FROM world_adm_2)')
    connection.commit()





