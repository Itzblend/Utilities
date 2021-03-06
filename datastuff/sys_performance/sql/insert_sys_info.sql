
INSERT INTO system_data_t.system_info_t (
    cpu_percent,
    cpu_freq,
    disk_total_gb,
    disk_used_gb,
    disk_free_gb,
    disk_percent,
    ram_used_gb,
    ram_free_gb,
    ram_percent,
    bytes_sent,
    bytes_recv,
    packets_sent,
    packets_rec
)
SELECT 
    (data ->> 'cpu_percent')::NUMERIC AS cpu_percent,
    (data ->> 'cpu_freq')::NUMERIC AS cpu_freq,
    TRUNC((data ->> 'disk_total')::NUMERIC / 1000000000, 2) AS disk_total_gb,
    TRUNC((data ->> 'disk_used')::NUMERIC / 1000000000, 2) AS disk_used_gb,
    TRUNC((data ->> 'disk_free')::NUMERIC / 1000000000, 2) AS disk_free_gb,
    (data ->> 'disk_percent')::NUMERIC AS disk_percent,
    TRUNC((data ->> 'ram_used')::NUMERIC / 1000000000, 2) AS ram_used_gb,
    TRUNC((data ->> 'ram_free')::NUMERIC / 1000000000, 2) AS ram_free_gb,
    (data ->> 'ram_percent')::NUMERIC AS disk_free_gb,
    TRUNC((data ->> 'bytes_sent')::NUMERIC / 1000000000, 2) AS bytes_sent,
    TRUNC((data ->> 'bytes_recv')::NUMERIC / 1000000000, 2) AS bytes_recv,
    (data ->> 'packets_sent')::NUMERIC AS packets_sent,
    (data ->> 'packets_recv')::NUMERIC AS packets_rec

FROM
    staging
ON CONFLICT DO NOTHING
