# Utilities

### Get JSON value paths
`jq -r 'path(..) | map(tostring) | join("/")'`
