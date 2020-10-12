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
    timestamp TIMESTAMP DEFAULT (current_timestamp AT TIME ZONE 'GMT-3')
)
