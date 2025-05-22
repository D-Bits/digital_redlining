
CREATE SCHEMA IF NOT EXISTS fcc;

CREATE TABLE IF NOT EXISTS fcc.geo
(
    id BIGSERIAL,
    geography_id VARCHAR(5) NOT NULL,
    geography_type VARCHAR NOT NULL,
    geography_desc VARCHAR NOT NULL,
    total_area VARCHAR,
    PRIMARY KEY(ID, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc.mobile
(
    id BIGSERIAL,
    geography_id VARCHAR(5) NOT NULL,
    total_units INT,
    biz_res VARCHAR(1),
    technology VARCHAR(),
    speed_02_02 DECIMAL,
    speed_10_1 DECIMAL,
);