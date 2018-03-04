-- Indexes on tables.

/* On stock */

/* On keystat */

DROP INDEX IF EXISTS keystat_stock_stat_idx;
CREATE INDEX keystat_stock_stat_idx
    ON keystat(stock, stat);

DROP INDEX IF EXISTS keystat_stat_idx;
CREATE INDEX keystat_stat_idx
    ON keystat(stat);

DROP INDEX IF EXISTS keystat_val_idx;
CREATE INDEX keystat_val_idx
    ON keystat(val);

/* On growthrate */

DROP INDEX IF EXISTS growthrate_stock_stat_idx;
CREATE INDEX growthrate_stock_stat_idx
    ON keystat(stock, stat);

DROP INDEX IF EXISTS growthrate_stat_idx;
CREATE INDEX growthrate_stat_idx
    ON keystat(stat);

DROP INDEX IF EXISTS keystat_val_idx;
CREATE INDEX growthrate_val_idx
    ON keystat(val);

/* On annual */

DROP INDEX IF EXISTS annual_stock_stat_idx;
CREATE INDEX annual_stock_stat_idx
    ON annual(stock, stat);

DROP INDEX IF EXISTS annual_stat_idx;
CREATE INDEX annual_stat_idx
    ON annual(stat);

DROP INDEX IF EXISTS annual_date_idx;
CREATE INDEX annual_date_idx
    ON annual(date);

DROP INDEX IF EXISTS annual_val_idx;
CREATE INDEX annual_val_idx
    ON annual(val);

/* On quarterly */

DROP INDEX IF EXISTS quarterly_stock_stat_idx;
CREATE INDEX quarterly_stock_stat_idx
    ON quarterly(stock, stat);

DROP INDEX IF EXISTS quarterly_stat_idx;
CREATE INDEX quarterly_stat_idx
    ON quarterly(stat);

DROP INDEX IF EXISTS quarterly_date_idx;
CREATE INDEX quarterly_date_idx
    ON quarterly(date);

DROP INDEX IF EXISTS quarterly_val_idx;
CREATE INDEX quarterly_val_idx
    ON quarterly(val);
