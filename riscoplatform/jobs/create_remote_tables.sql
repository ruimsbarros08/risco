DROP FOREIGN TABLE IF EXISTS foreign_dmg_dist_per_asset;
DROP FOREIGN TABLE IF EXISTS foreign_exposure_data;

DROP FOREIGN TABLE IF EXISTS foreign_gmf;
DROP FOREIGN TABLE IF EXISTS foreign_gmf_data;
DROP FOREIGN TABLE IF EXISTS foreign_hazard_site;



CREATE FOREIGN TABLE foreign_dmg_dist_per_asset (
	id integer,
	dmg_state_id integer,
	exposure_data_id integer,
	mean double precision,
	stddev double precision
)
SERVER priseoq OPTIONS (schema_name 'riskr', table_name 'dmg_dist_per_asset');

CREATE FOREIGN TABLE foreign_exposure_data (
	id integer,
	asset_ref character varying
)
SERVER priseoq OPTIONS (schema_name 'riski', table_name 'exposure_data');




CREATE FOREIGN TABLE foreign_gmf_data (
	id integer,
	gmf_id integer,
	gmvs double precision[],
	site_id integer
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'gmf_data');

CREATE FOREIGN TABLE foreign_gmf (
	id integer,
	output_id integer
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'gmf');

CREATE FOREIGN TABLE foreign_hazard_site (
	id integer,
	location geography(Point,4326)
)
SERVER priseoq OPTIONS (schema_name 'hzrdi', table_name 'hazard_site');