#!/bin/bash

python3
## Login to synapse
import os
import synapseclient as synapse
syn = synapse.Synapse()
# if using auth token:
# syn.login(authToken = os.environ['SYNAPSE_PAT'], rememberMe = True)
# if using .synapseConfig:
synlogin(rememberMe = True)
exit()
## run script to update AD dccvalidator dictionary table
python3 code/python/create_Syn_table_from_Syn_schemas.py \
    --config_file config/schemas.yml --consortium AD overwrite_table --table_synapse_id syn21459391