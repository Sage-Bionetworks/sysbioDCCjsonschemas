import synapseclient
import json

syn = synapseclient.login()
js = syn.service("json_schema")

# Create, manage, and delete a JSON Schema organization
my_org = js.JsonSchemaOrganization("awilliams.test")

with open('amp-ad-metadata-schemas/amp.ad.data.ManifestMetadataTemplate.schema.json') as f:
    raw_body = json.load(f)

schema_name = 'ManifestMetadataTemplate'

new_version1 = my_org.create_json_schema(raw_body, schema_name, "0.1.1")
