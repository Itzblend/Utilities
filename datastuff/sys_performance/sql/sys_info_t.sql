CREATE TABLE IF NOT EXISTS system_data_t.system_info_t (
    cpu_percent NUMERIC,
    cpu_freq NUMERIC,
    disk_total NUMERIC,
    disk_used NUMERIC,
    disk_free NUMERIC,
    disk_percent NUMERIC,
    timestamp TIMESTAMP DEFAULT (current_timestamp AT TIME ZONE 'GMT-3')
);

CREATE INDEX timestamp_idx ON system_data_t.system_info_t (timestamp);

CREATE INDEX cpu_percent_idx ON system_data_t.system_info_t (cpu_percent);
CREATE INDEX disk_percent_idx ON system_data_t.system_info_t (disk_percent);
CREATE INDEX ram_percent_idx ON system_data_t.system_info_t (ram_percent);
