#!/bin/bash
# First fetch information about iwoca Ltd (company no. 07798925).
curl -s -X GET -u yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt: https://api.companieshouse.gov.uk/company/07798925 | json_pp
# Fetch a list of all iwoca Ltd's officers (link can also be found under links.officers of the previous response).
curl -s -X GET -u yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt: https://api.companieshouse.gov.uk/company/07798925/officers | json_pp
# Fetch all James the CTO's appointments (available under items[].links.officer.appointments).
curl -s -X GET -u yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt: https://api.companieshouse.gov.uk/officers/Y-7-tBrvzDw7tplKHhkcX4x8N-M/appointments | json_pp
# Turns out James has been appointed at 3 companies.
