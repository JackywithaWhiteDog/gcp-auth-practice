#!bin/bash

curl -X POST "https://bigquery.googleapis.com/bigquery/v2/projects/$(gcloud config get-value project)/queries" \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d @$(dirname $0)/body.json
