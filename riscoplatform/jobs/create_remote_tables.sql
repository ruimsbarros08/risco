

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

DROP FOREIGN TABLE IF EXISTS foreign_lt_realization;
DROP FOREIGN TABLE IF EXISTS foreign_lt_source_model;
DROP FOREIGN TABLE IF EXISTS foreign_hazard_curve;
DROP FOREIGN TABLE IF EXISTS foreign_hazard_curve_data;
DROP FOREIGN TABLE IF EXISTS foreign_hazard_map;

--SCENARIO DAMAGE

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

--SCENARIO HAZARD

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

--SCENARIO RISK

CREATE FOREIGN TABLE foreign_loss_map (
	id integer,
	output_id integer,
	loss_type character varying,
	insured boolean
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

--PSHA HAZARD

CREATE FOREIGN TABLE foreign_lt_realization (
	id integer,
	lt_model_id integer,
	weight double precision,
	gsim_lt_path character varying[]
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'lt_realization');


CREATE FOREIGN TABLE foreign_lt_source_model (
	id integer,
	hazard_calculation_id integer,
	weight double precision,
	sm_lt_path character varying[]
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'lt_source_model');


CREATE FOREIGN TABLE foreign_hazard_curve (
	id integer,
 	output_id integer,
 	lt_realization_id integer,
 	investigation_time double precision,
	imt character varying,
	imls double precision[],
	statistics character varying,
	quantile double precision,
	sa_period double precision,
	sa_damping double precision 
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'hazard_curve');


CREATE FOREIGN TABLE foreign_hazard_curve_data (
 	id integer,
 	hazard_curve_id integer,
 	poes double precision[],
 	weight numeric,
 	location geometry(Point,4326)
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'hazard_curve_data');


CREATE FOREIGN TABLE foreign_hazard_map (
	id integer,
	output_id integer,
	lt_realization_id integer,
	investigation_time double precision,
	imt character varying,
	statistics character varying,
	quantile double precision, 
	sa_period double precision,
	sa_damping double precision,
	poe double precision,
	lons double precision[],
	lats double precision[],
	imls double precision[]
)
SERVER priseoq OPTIONS (schema_name 'hzrdr', table_name 'hazard_map');



