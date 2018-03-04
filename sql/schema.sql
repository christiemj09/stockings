-- Schema definition for the stocks database.

DROP TABLE IF EXISTS stock CASCADE;
CREATE TABLE stock (

    -- Top-level stocks key (e.g. STOCK)
    id TEXT PRIMARY KEY,

    -- Attributes from stocks['STOCK']
    name TEXT,
    industry TEXT,
    sector TEXT
);

DROP TABLE IF EXISTS keystat CASCADE;
CREATE TABLE keystat (

    -- Top-level stocks key (e.g. STOCK)
    stock TEXT REFERENCES stock(id),

    -- Key-value pairs from stocks['STOCK']['keystats']
    stat TEXT,
    val NUMERIC,

    -- Key stats liable to change per download
    downloaded TIMESTAMP
);

DROP TABLE IF EXISTS growthrate CASCADE;
CREATE TABLE growthrate (

    -- Top-level stocks key (e.g. STOCK)
    stock TEXT REFERENCES stock(id),

    -- Key-value pairs from stocks['STOCK']['growthrates']
    stat TEXT,
    val NUMERIC,

    -- Growth rates liable to change per download
    downloaded TIMESTAMP
);

DROP TABLE IF EXISTS annual CASCADE;
CREATE TABLE annual (

    -- Top-level stocks key (e.g. STOCK)
    stock TEXT REFERENCES stock(id),

    -- Data from stocks['STOCK']['annual']
    stat TEXT,
    date DATE,
    val NUMERIC
);

DROP TABLE IF EXISTS quarterly CASCADE;
CREATE TABLE quarterly (

    -- Top-level stocks key (e.g. STOCK)
    stock TEXT REFERENCES stock(id),

    -- Data from stocks['STOCK']['annual']
    stat TEXT,
    date DATE,
    val NUMERIC
);
