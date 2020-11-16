CREATE TABLE IF NOT EXISTS system_data_t.system_info_t (
    cpu_percent NUMERIC,
    cpu_freq NUMERIC,
    disk_total_gb NUMERIC,
    disk_used_gb NUMERIC,
    disk_free_gb NUMERIC,
    disk_percent NUMERIC,
    ram_used_gb NUMERIC,
    ram_free_gb NUMERIC,
    ram_percent NUMERIC,
    bytes_sent NUMERIC,
    bytes_recv NUMERIC,
    packets_sent NUMERIC,
    packets_rec NUMERIC,
    timestamp TIMESTAMP DEFAULT (current_timestamp AT TIME ZONE 'GMT-3')
);

CREATE INDEX timestamp_idx ON system_data_t.system_info_t (timestamp);

CREATE INDEX cpu_percent_idx ON system_data_t.system_info_t (cpu_percent);
CREATE INDEX disk_percent_idx ON system_data_t.system_info_t (disk_percent);
CREATE INDEX ram_percent_idx ON system_data_t.system_info_t (ram_percent);
