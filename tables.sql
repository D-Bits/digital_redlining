
CREATE SCHEMA IF NOT EXISTS fcc_fixed;

CREATE TABLE IF NOT EXISTS fcc_fixed.fact_geo
(
    id BIGSERIAL,
    geography_id VARCHAR NOT NULL,
    geography_type VARCHAR NOT NULL,
    geography_desc VARCHAR NOT NULL,
    total_area VARCHAR,
    FOREIGN KEY (id, geography_id) REFERENCES fcc_fixed.dim_speed(id, geography_id),
    FOREIGN KEY (id, geography_id) REFERENCES fcc_fixed.dim_technology(id, geography_id), 
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc_fixed.dim_speed
(
    id BIGSERIAL,
    geography_id VARCHAR NOT NULL,
    speed_02_02 DECIMAL,
    speed_10_1 DECIMAL,
    speed_25_3 DECIMAL,
    speed_100_20 DECIMAL,
    speed_250_25 DECIMAL,
    speed_1000_100 DECIMAL,
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc_fixed.dim_technology
(
    id BIGSERIAL,
    geography_id VARCHAR NOT NULL,
    area_data_type VARCHAR,
    biz_res VARCHAR(1),
    technology VARCHAR,
    total_units INT,
    PRIMARY KEY(id, geography_id)
);


CREATE SCHEMA IF NOT EXISTS fcc_mobile;

CREATE TABLE IF NOT EXISTS fcc_mobile.fact_geo
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    geography_type VARCHAR NOT NULL,
    geography_desc VARCHAR NOT NULL,
    total_area DECIMAL,
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc_mobile.dim_speed
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    speed_5_1 DECIMAL,
    speed_10_1 DECIMAL,
    speed_25_3 DECIMAL,
    speed_100_10 DECIMAL,
    speed_250_25 DECIMAL,
    speed_1000_100 DECIMAL,
    PRIMARY KEY(id, geography_id)
); 

CREATE TABLE IF NOT EXISTS fcc_mobile.dim_3g
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    mobilebb_3g_area_st_pct DECIMAL,
    mobilebb_3g_area_iv_pct DECIMAL,
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc_mobile.dim_4g
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    mobilebb_4g_area_st_pct DECIMAL,
    mobilebb_4g_area_iv_pct DECIMAL,
    PRIMARY KEY(id, geography_id)
);

CREATE TABLE IF NOT EXISTS fcc_mobile.dim_5g
(
    id BIGSERIAL,
    geography_id INT NOT NULL,
    mobilebb_5g_spd1_area_st_pct DECIMAL,
    mobilebb_5g_spd1_area_iv_pct DECIMAL,
    mobilebb_5g_spd2_area_st_pct DECIMAL,
    mobilebb_5g_spd2_area_iv_pct DECIMAL,
    PRIMARY KEY(id, geography_id)
);