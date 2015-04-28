INSERT INTO world_country (id_0, name, iso, geom)
SELECT id_0, name_0, iso, ST_Multi(ST_Union(f.geom)) as singlegeom
FROM world_world As f
GROUP BY id_0, name_0, iso;