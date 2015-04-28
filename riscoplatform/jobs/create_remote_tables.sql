

--CREATE SERVER priseoq FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'priseOQ.fe.up.pt', dbname 'openquake2', port '5432');

--DROP USER MAPPING IF EXISTS FOR postgres SERVER priseoq;
--CREATE USER MAPPING FOR postgres SERVER priseoq OPTIONS (user 'postgres', password 'prisefeup');


DROP FOREIGN TABLE IF EXISTS foreign_dmg_dist_per_asset;
DROP FOREIGN TABLE IF EXISTS foreign_exposure_data;
DROP FOREIGN TABLE IF EXISTS foreign_dmg_state;
DROP FOREIGN TABLE IF EXISTS foreign_exposure_model;

DROP FOREIGN TABLE IF EXISTS foreign_gmf;
DROP FOREIGN TABLE IF EXISTS foreign_gmf_data;
DROP FOREIGN TABLE IF EXISTS foreign_hazard_site;

DROP FOREIGN TABLE IF EXISTS foreign_loss_map;
DROP FOREIGN TABLE IF EXISTS foreign_loss_map_data;



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
	exposure_model_id integer,
	asset_ref character varying
)
SERVER priseoq OPTIONS (schema_name 'riski', table_name 'exposure_data');

CREATE FOREIGN TABLE foreign_dmg_state (
	id integer,
	risk_calculation_id integer,
	dmg_state character varying
)
SERVER priseoq OPTIONS (schema_name 'riskr', table_name 'dmg_state');

CREATE FOREIGN TABLE foreign_exposure_model (
	id integer,
	job_id integer
)
SERVER priseoq OPTIONS (schema_name 'riski', table_name 'exposure_model');



CREATE FOREIGN TABLE foreign_gmf_data (
	id integer,
	gmf_id integer,
	imt character varying,
	sa_period double precision,
	sa_damping double precision,
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



CREATE FOREIGN TABLE foreign_loss_map (
	id integer,
	output_id integer,
	loss_type character varying
)
SERVER priseoq OPTIONS (schema_name 'riskr', table_name 'loss_map');

CREATE FOREIGN TABLE foreign_loss_map_data (
	id integer,
	loss_map_id integer,
	asset_ref character varying,
	value double precision,
	std_dev double precision
)
SERVER priseoq OPTIONS (schema_name 'riskr', table_name 'loss_map_data');

