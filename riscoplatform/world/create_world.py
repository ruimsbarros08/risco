import os
from django.contrib.gis.utils import LayerMapping
from models import *
from django.db import connection

cursor = connection.cursor()


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


def match_missing():
    cursor.execute('UPDATE world_adm_1 \
        SET country_id = \
        (SELECT world_country.id \
            FROM world_country \
            WHERE ST_Contains(world_country.geom, ST_PointOnSurface(world_adm_1.geom))) \
        WHERE world_adm_1.country_id IS NULL')
    connection.commit()


#def match_missing():
#    cursor.execute('UPDATE world_adm_1 \
#                    SET country_id = \
#                    (SELECT world_country.id \
#                    FROM world_country \
#                    WHERE ST_Intersects(world_adm_1.geom, world_country.geom) \
#                    AND world_country.id != 407 \
#                    ORDER BY ST_Area(ST_Intersection(world_adm_1.geom, world_country.geom)) DESC \
#                    LIMIT 1) \
#                    WHERE country_id is null')
#    connection.commit()



