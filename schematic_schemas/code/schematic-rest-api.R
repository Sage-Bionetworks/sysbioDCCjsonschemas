# curl -X 'GET' \
# 'http://127.0.0.1:3001/v1/manifest/generate?schema_url=https%3A%2F%2Fraw.githubusercontent.com%2FSage-Bionetworks%2Fschematic%2Fdevelop%2Ftests%2Fdata%2Fexample.model.jsonld&title=Patient%20Metadata%20Manifest&data_type=Patient&oauth=true&use_annotations=false&dataset_id=123' \
# -H 'accept: application/json'

# https://github.com/Sage-Bionetworks/schematic/tree/develop/api

schema_url = "https://raw.githubusercontent.com/Sage-Bionetworks/schematic/develop/tests/data/example.model.jsonld"
title = "Patient Metadata Manifest"
data_type = "Patient"
oauth = "true"
use_annotations = "false"
dataset_id = "123"

library(httr)
url <- "http://127.0.0.1:3001/v1/manifest/generate"

resp <- GET(url,
            query = list(schema_url=schema_url,
                         title = title,
                         data_type = data_type,
                         oauth = oauth,
                         use_annotations = use_annotations,
                         dataset_id = dataset_id))

resp <- GET('http://127.0.0.1:3001/v1/manifest/generate?schema_url=https%3A%2F%2Fraw.githubusercontent.com%2FSage-Bionetworks%2Fschematic%2Fdevelop%2Ftests%2Fdata%2Fexample.model.jsonld&title=Patient%20Metadata%20Manifest&data_type=Patient&oauth=true&use_annotations=false&dataset_id=123')
