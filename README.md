# Utilities

### Get JSON value paths
`jq -r 'path(..) | map(tostring) | join("/")'`

### Get disk usage of cassandra tables (in megabytes)
`docker exec cassandra1 nodetool cfstats -- stackoverflow_t | grep "Memtable data size" | grep -o '[0-9]\+' | xargs -I{} expr {} / 1000000`
