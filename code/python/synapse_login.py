import json, os, synapseclient
secrets=json.loads(os.getenv("SCHEDULED_JOB_SECRETS"))
auth_token = secrets["PAT"]
syn=synapseclient.Synapse()
syn.login(authToken=auth_token)
