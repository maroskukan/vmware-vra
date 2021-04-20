#!/usr/bin/env bash

# The following loop will generate a list of available API endpoints
# Global endpoint (US)
base_url="api.mgmt.cloud.vmware.com"
printf '%s ' ${base_url} && curl -s -o /dev/null -w '%{time_starttransfer}\n' https://${base_url}

# Search for remaining countries and measure them
for country in $(curl -s https://restcountries.eu/rest/v2/all\?fields\=alpha2Code | jq -r '.[]["alpha2Code"]'); do 
record=${country,,}.${base_url} && \
query=$(dig $record +short) && \
[[ ! -z $query ]] && printf '%s ' $record && curl -s -o /dev/null -w '%{time_starttransfer}\n' https://${country}.${base_url}
done