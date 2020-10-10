
INSERT INTO system_data_t.system_info_t (
    cpu_percent,
    cpu_freq,
    disk_total,
    disk_used,
    disk_free,
    disk_percent
)
SELECT 
    (data ->> 'cpu_percent')::NUMERIC AS cpu_percent,
    (data ->> 'cpu_freq')::NUMERIC AS cpu_freq,
    (data ->> 'disk_total')::NUMERIC AS disk_total,
    (data ->> 'disk_used')::NUMERIC AS disk_used,
    (data ->> 'disk_free')::NUMERIC AS disk_free,
    (data ->> 'disk_percent')::NUMERIC AS disk_percent
FROM
    staging
ON CONFLICT DO NOTHING