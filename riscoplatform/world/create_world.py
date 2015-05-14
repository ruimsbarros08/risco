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


def simplify_countries():
    cursor.execute('UPDATE world_country \
                    SET geom_simp = world_country_simp.geom \
                    FROM world_country_simp \
                    WHERE world_country.name = world_country_simp.name; \
                    \
                    UPDATE world_country \
                    SET geom_simp = world_country_simp.geom \
                    FROM world_country_simp \
                    WHERE world_country.geom_simp is NULL \
                    AND ST_Intersects(world_country_simp.geom, ST_PointOnSurface(world_country.geom)); \
                    \
                    UPDATE world_country \
                    SET geom_simp = geom \
                    WHERE geom_simp is NULL;')
    connection.commit()




#############
### ADM 1 ###
#############



level1_mapping = {
    'id_1' : 'ID_1',
    'name' : 'NAME_1',
    'geom' : 'MULTIPOLYGON',
}

level1_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'datasources/gadm/gadmV2_Level1.shp'))

def run_level1(verbose=True):
    lm = LayerMapping(Adm_1, level1_shp, level1_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


def match_country_adm1():
    cursor.execute('UPDATE world_adm_1 \
        SET country_id = \
        (SELECT world_country.id \
            FROM world_country \
            WHERE ST_Within(world_adm_1.geom, world_country.geom))')

    connection.commit()


def match_missing_adm1():
    cursor.execute('UPDATE world_adm_1 \
        SET country_id = \
        (SELECT world_country.id \
            FROM world_country \
            WHERE ST_Contains(world_country.geom, ST_PointOnSurface(world_adm_1.geom))) \
        WHERE world_adm_1.country_id IS NULL')
    connection.commit()





