# sysbioDCCjsonschemas
This repository holds the JSON schemas for the Systems Biology (SysBio) DCC.

## Annotation Schema

Annotation schema can be found in the schema_annotations folder and are organized by consortium.

- **AD:** The AD annotation schema is not currently set on any projects and will be updated to a new format.

## Code

There are python scripts in the code/python folder for generating metadata templates and annotation tables based on the metadata template schemas registered in Synapse.

**NOTE:** The scripts in this repository assume the latest versions of all JSON schema are registered. If you have added or changed a schema, ensure the schema has been registered before running the scripts.

The annotation table can be created with a single command. Example:

```bash
python3 code/python/create_Syn_table_from_Syn_schemas.py \
  --config_file config/schemas.yml \
  --consortium PsychENCODE \
  new_table \
  --parent_synapse_id syn21786765 \
  --synapse_table_name pec_annots
```

The annotation table can be updated with a single command. Example:

```bash
python3 code/python/create_Syn_table_from_Syn_schemas.py \
  --config_file config/schemas.yml \
  --consortium PsychENCODE \
  overwrite_table \
  --table_synapse_id syn20981788 \
```

#### Annotations Table

create_Syn_table_from_Syn_schemas.py will generate a Synapse table of all terms found in a set of metadata templates. The set is determined by consortium using the config file (config/schemas.yml). There are options to create a new table or overwrite an existing table.

Parameters:

- `--config_file <YAML file>`: Path to the config file.
- `--consortium <consortium>`: The consortium to create the table for; will only gather terms in registered templates for that consortium.
- `new_table`  OR `overwrite_table`: Choose to create a new table or overwrite an existing table.
  - For `new_table`
    - `--parent_synapse_id <synID>`: synID for project that table should be created in.
    - `--synapse_table_name <table name>`: Name for the new table.
  - For`overwrite_table`
    - `--table_synapse_id <synID>`: synID of table to overwrite.

## Metadata Templates
The metadata templates are located in the schema_metadata_templates folder and are organized by consortium.

- **shared:** Any new templates or additions to existing should be reviewed with the SysBio DCC to see if they meet everyone's needs. If all consortia in the SysBio DCC agree to the template, then it should be in the shared folder.
- **AD:** The AD folder contains all the templates specific to the AD consortium.
- **PsychENCODE:** The PsychENCODE folder contains all the templates specific to the PsychENCODE consortium.
- **1kD:** The 1kD folder contains all the templates specific to the 1kD consortium.

#### Generate Metadata Template
Currently, there are two approaches to generate metadata templates. 

1. Generate the metadata template(s) using registered schames.

create_template_from_Syn_schema.py will generate either a .csv or .xlsx metadata template based on a registered metadata schema. 

Parameters:

- `<registered schema id>`: id of the registered metadata schema, including organization (e.g. sysbio.metadataTemplates_assay.STARRSeq).
- `<config file>`: Full path to the schemas.yml that includes all registered schemas, e.g. /home/ec2-user/sysbioDCCjsonschemas/config/schemas.yml 
- `<template json>`: Optional. Full path for the template json file in the schema_metadata_templates folder. Specify it when you want the output template columns to match the order of the terms as they appear in a json file. 

#### Code
   ```bash
   python3 create_template_from_Syn_schema.py \
     sysbio.metadataTemplates-pec.manifest \
     /home/ec2-user/sysbioDCCjsonschemas/config/schemas.yml \
     /home/ec2-user/sysbioDCCjsonschemas/schema_metadata_templates/PsychENCODE/manifest_metadata_template.json
   ```

2. Generate the metadata template(s) using schematic workflow.

Metadata templates created by [schematic](https://github.com/Sage-Bionetworks/schematic/) are stored in `schematic_schemas`. This directory contains the data model csv and its derived jsonld schema. The `json` and `xlsx` directories contain individual schemas and template sheets, respectively. The `code` directory contains the scripts for creating these files.

Here is a step-by-step instructions on how to generate interactive excel metadata using schematic. 
1. Update data.model.csv data model by hand. Example: [1kD.data.model.csv](https://www.synapse.org/#!Synapse:syn28777861).

2. Prerequisites: Make sure you have a [minimal.model.jsonld](https://github.com/imCORE-DCC/data_model/blob/production/minimal.model.jsonld) and a [credentials.json](https://www.synapse.org/#!Synapse:syn23643259) file in your repository. 

3. Convert data model to json schema (jsonld). Example:
schematic schema convert --base_schema ./minimal.model.jsonld ./1kD.data.model.csv

4. Create a google sheet template and json for each data type.
schematic manifest --config config.yml get -s -oa -p ./1kD.data.model.jsonld -t IndividualHumanMetadataTemplate1kD -dt IndividualHumanMetadataTemplate1kD

5. Manually download all the google sheets as excel. Using the google drive API would be clutch.

6. Upload all the excel templates to Synapse, AD, PEC and 1kD.

7. Register the json schemas to synapse by tinkering with register-schemas.py for each schema. (haven't test yet)

**NOTE:** Don't forget to commit and push the newly generated data model, model jsonld, json schema(s), excel template(s) to this repository.

### Docker

This repo contains a Dockerfile that can be used to build a docker image locally. Alternatively, the docker image is on Docker Hub under [sagebionetworks/sysbioDCCjsonschemas](https://hub.docker.com/repository/docker/sagebionetworks/sysbiodccjsonschemas).

##### Build Image Locally

If you'd like to build the docker image locally, clone this repo and open a terminal in the sysbioDCCjsonschemas folder. Then build image and run interactively.

```bash
git clone https://github.com/Sage-Bionetworks/sysbioDCCjsonschemas.git
cd sysbioDCCjsonschemas
docker build --no-cache -t sysbiodccjsonschemas .
docker run --rm -it sysbiodccjsonschemas
```

##### Pull Existing Image

If you'd like to use an existing image, then pull the docker image from Docker Hub. Below assumes pulling the latest version of the image. To use a different version, replace `latest` with the [desired tag](https://hub.docker.com/repository/docker/sagebionetworks/sysbiodccjsonschemas/tags?page=1&ordering=last_updated). The container can be run interactively once the image is pulled.

```
docker pull sagebionetworks/sysbiodccjsonschemas:latest
docker run --rm -it sagebionetworks/sysbiodccjsonschemas:latest
```
Because the docker image is not currently auto-deployed, it may be out of date with the repo. It is recommend to build the image locally or use `git pull` within the container to get the latest version if you are: 

- adding a new key to an existing template
- adding an entirely new template
- generating the annotation table when a new template has been added to the config

#### Usage

The docker container opens in bash at the top level of the sysbioDCCjsonschemas directory. The docker container will not have Synapse credentials. Due to this, follow these steps to log into Synapse. Note that this should be done every time you start a new container.

1. Generate a Synapse Personal Access Token (PAT) by logging into Synapse and going to your profile settings. The token should be created with all permissions checked.

2. Start a docker container using the docker image as specified above.

3. Start python3, log into Synapse, and exit python.

   ```bash
   python3
   ```

   ```python
   import synapseclient as synapse
   syn = synapse.Synapse()
   syn.login(authToken="your PAT", rememberMe=True)
   exit()
   ```

4. Run the scripts needed (see below), with the desired parameters, using python3.



