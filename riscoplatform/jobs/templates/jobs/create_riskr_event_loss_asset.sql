--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = riskr, pg_catalog;

SET default_tablespace = riskr_ts;

SET default_with_oids = false;

--
-- Name: event_loss_asset; Type: TABLE; Schema: riskr; Owner: oq_admin; Tablespace: riskr_ts
--

CREATE TABLE event_loss_asset (
    id integer NOT NULL,
    event_loss_id integer NOT NULL,
    rupture_id integer NOT NULL,
    asset_id integer NOT NULL,
    loss double precision NOT NULL
);


ALTER TABLE riskr.event_loss_asset OWNER TO oq_admin;

--
-- Name: TABLE event_loss_asset; Type: COMMENT; Schema: riskr; Owner: oq_admin
--

COMMENT ON TABLE event_loss_asset IS 'Loss per loss_type per event per asset';


--
-- Name: COLUMN event_loss_asset.event_loss_id; Type: COMMENT; Schema: riskr; Owner: oq_admin
--

COMMENT ON COLUMN event_loss_asset.event_loss_id IS 'event_loss (id)';


--
-- Name: COLUMN event_loss_asset.rupture_id; Type: COMMENT; Schema: riskr; Owner: oq_admin
--

COMMENT ON COLUMN event_loss_asset.rupture_id IS 'ses_rupture (id)';


--
-- Name: COLUMN event_loss_asset.asset_id; Type: COMMENT; Schema: riskr; Owner: oq_admin
--

COMMENT ON COLUMN event_loss_asset.asset_id IS 'exposure_data (id)';


--
-- Name: COLUMN event_loss_asset.loss; Type: COMMENT; Schema: riskr; Owner: oq_admin
--

COMMENT ON COLUMN event_loss_asset.loss IS 'Loss value';


--
-- Name: event_loss_asset_id_seq; Type: SEQUENCE; Schema: riskr; Owner: oq_admin
--

CREATE SEQUENCE event_loss_asset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE riskr.event_loss_asset_id_seq OWNER TO oq_admin;

--
-- Name: event_loss_asset_id_seq; Type: SEQUENCE OWNED BY; Schema: riskr; Owner: oq_admin
--

ALTER SEQUENCE event_loss_asset_id_seq OWNED BY event_loss_asset.id;


--
-- Name: id; Type: DEFAULT; Schema: riskr; Owner: oq_admin
--

ALTER TABLE ONLY event_loss_asset ALTER COLUMN id SET DEFAULT nextval('event_loss_asset_id_seq'::regclass);


SET default_tablespace = '';

--
-- Name: event_loss_asset_pkey; Type: CONSTRAINT; Schema: riskr; Owner: oq_admin; Tablespace: 
--

ALTER TABLE ONLY event_loss_asset
    ADD CONSTRAINT event_loss_asset_pkey PRIMARY KEY (id);


--
-- Name: event_loss_asset_asset_id_fkey; Type: FK CONSTRAINT; Schema: riskr; Owner: oq_admin
--

ALTER TABLE ONLY event_loss_asset
    ADD CONSTRAINT event_loss_asset_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES riski.exposure_data(id);


--
-- Name: event_loss_asset_event_loss_id_fkey; Type: FK CONSTRAINT; Schema: riskr; Owner: oq_admin
--

ALTER TABLE ONLY event_loss_asset
    ADD CONSTRAINT event_loss_asset_event_loss_id_fkey FOREIGN KEY (event_loss_id) REFERENCES event_loss(id);


--
-- Name: event_loss_asset_rupture_id_fkey; Type: FK CONSTRAINT; Schema: riskr; Owner: oq_admin
--

ALTER TABLE ONLY event_loss_asset
    ADD CONSTRAINT event_loss_asset_rupture_id_fkey FOREIGN KEY (rupture_id) REFERENCES hzrdr.ses_rupture(id);


--
-- Name: event_loss_asset; Type: ACL; Schema: riskr; Owner: oq_admin
--

REVOKE ALL ON TABLE event_loss_asset FROM PUBLIC;
REVOKE ALL ON TABLE event_loss_asset FROM oq_admin;
GRANT ALL ON TABLE event_loss_asset TO oq_admin;
GRANT SELECT,INSERT ON TABLE event_loss_asset TO oq_job_init;


--
-- Name: event_loss_asset_id_seq; Type: ACL; Schema: riskr; Owner: oq_admin
--

REVOKE ALL ON SEQUENCE event_loss_asset_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE event_loss_asset_id_seq FROM oq_admin;
GRANT ALL ON SEQUENCE event_loss_asset_id_seq TO oq_admin;
GRANT USAGE ON SEQUENCE event_loss_asset_id_seq TO oq_job_init;


--
-- PostgreSQL database dump complete
--
