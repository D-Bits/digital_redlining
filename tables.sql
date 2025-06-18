
CREATE SCHEMA IF NOT EXISTS fcc;

CREATE TABLE IF NOT EXISTS fcc.geo
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    geography_type VARCHAR NOT NULL,
    geography_desc VARCHAR NOT NULL,
    total_area VARCHAR,
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc.fixed
(
    id BIGSERIAL,
    area_data_type VARCHAR,
    geography_type VARCHAR NOT NULL,
    geography_desc VARCHAR NOT NULL,
    geography_id INT NOT NULL,
    geography_desc_full VARCHAR,
    total_units INT,
    biz_res VARCHAR(1),
    technology VARCHAR,
    speed_02_02 DECIMAL,
    speed_10_1 DECIMAL,
    speed_25_3 DECIMAL,
    speed_100_20 DECIMAL,
    speed_250_25 DECIMAL,
    speed_1000_100 DECIMAL,
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc.mobile
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    geography_type VARCHAR NOT NULL,
    geography_desc VARCHAR NOT NULL,
    total_area DECIMAL,
    mobilebb_3g_area_st_pct DECIMAL,
    mobilebb_3g_area_iv_pct DECIMAL,
    mobilebb_4g_area_st_pct DECIMAL,
    mobilebb_4g_area_iv_pct DECIMAL,
    mobilebb_5g_spd1_area_st_pct DECIMAL,
    mobilebb_5g_spd1_area_iv_pct DECIMAL,
    mobilebb_5g_spd2_area_st_pct DECIMAL,
    mobilebb_5g_spd2_area_iv_pct DECIMAL,
    PRIMARY KEY(id, geography_id)
);
