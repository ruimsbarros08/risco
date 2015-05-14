create table poly as (
    select id, id_0, (st_dump(geom)).* 
    from world_country
);

create table rings as (
    select st_exteriorRing((st_dumpRings(geom)).geom) as g 
    from poly
);

create table simplerings as (
    select st_simplifyPreserveTopology(st_linemerge(st_union(g)), 10000) as g 
    from rings
);