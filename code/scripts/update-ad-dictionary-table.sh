#!/bin/bash

# run login script with scheduled job secrets
python3 code/python/synapse_login.py

# run script to update AD dccvalidator dictionary table
python3 code/python/create_Syn_table_from_Syn_schemas.py \
    --config_file config/schemas.yml --consortium AD overwrite_table --table_synapse_id syn21459391