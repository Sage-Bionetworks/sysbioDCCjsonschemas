# sysbioDCCjsonschemas
This repository holds the JSON schemas for the Systems Biology (SysBio) DCC.

## Schemas

### Organization

#### Metadata Templates

The metadata templates are located in the schema_metadata_templates folder and are organized by consortium.

- **shared:** Any new templates or additions to existing should be reviewed with the SysBio DCC to see if they meet everyone's needs. If all consortia in the SysBio DCC agree to the template, then it should be in the shared folder.
- **AD:** The AD folder contains all the templates specific to the AD consortium.
- **PsychENCODE:** The PsychENCODE folder contains all the templates specific to the PsychENCODE consortium.

#### Annotation Schema

Annotation schema can be found in the schema_annotations folder and are organized by consortium.

- **AD:** The AD annotation schema is not currently set on any projects and will be updated to a new format.

### Format

For readability, both the metadata template and annotation schema are stored as yaml files. Since yaml structure is highly dependent on indentation and does not have concepts such as if-else logic, these schema require special care.

The schemas also rely on the use of anchors and aliases to simplify version dependency for terms. This is handled by a Synapse table with columns: key, alias, version, schema, module. Before registering schema, the table will be turned into a set of anchors for you to reference via their alias. For example, the keys for analysis and assay would be turned into the following yaml snippet.

```yaml
anchors:
    analysis_analysisType: &analysis_analysisType
        $ref: sage.annotations-analysis.analysisType-0.0.9
    experimentalData_assay: &experimentalData_assay
        $ref: sage.annotations-experimentalData.assay-0.0.15
```

The '&module_key' serves as an anchor for referencing the key in the schema via an alias (*module_key). Note that the naming convention for synapseAnnotations schema is 'module.key', but for the purposes of combining yaml and json, the naming convention for anchors and aliases should be 'module_key'.

```yaml
main-schema:
    $schema: http://json-schema.org/draft-07/schema#
    $id: my.organization-example.schema-0.0.1
    description: Simple example schema
    properties:
        analysisType: *analysis_analysisType
        assay: *experimentalData_assay
    required:
        - analysisType
        - assay
```

Note: The alias table allows for reusing schema with different names. For example, both 'primaryDiagnosis' and 'otherDiagnosis' would use the same 'sage.annotations-experimentalData.diagnosis' schema. The table only needs a single entry for alias 'experimentalData_diagnosis'. The new names for the term would be given in the schema itself. For example:

``` yaml
primaryDiagnosis: *experimentalData_diagnosis
otherDiagnosis: *experimentalData_diagnosis
```

Every schema, for metadata templates or annotations, should have a section called main-schema (see first example). It's possible to break up the schema into many sections and use anchors/aliases to reduce duplication or simplify your schema. The main-schema should be the last schema in the file. However, all parts must combine correctly via 'main-schema' for registration. For example, the AD annotation schema breaks out the logic for species/model systems and multispecimens, giving each of these sections an anchor so they can be referred to in 'main-schema'.

### Updating an Existing Schema

#### Adding a new key

1. Add key to schema table
2. Add key to yaml schema where needed (use *alias to reference the term as a property)
3. Increment version in yaml schema
4. Merge if checks pass; automation should register the schema in Synapse and update the dictionary table(s)

#### Adding a new value to a key

1. Update term in synapseAnnotations
2. Wait until next day for automation PR; merge if checks pass; automation should register the schema in Synapse and update the dictionary table(s)

### Adding a New Schema

1. Add any keys missing from alias.yml
2. Create new template with version 0.0.1 and section name called 'main-schema'
3. Add template to yaml config
4. Merge if checks pass; automation should register the schema in Synapse, update the dictionary table(s), and generate metadata templates

## Code

There are python scripts in the code/python folder for generating metadata templates and annotation tables based on the metadata template schemas registered in Synapse.

**NOTE:** The scripts in this repository assume the latest versions of all JSON schema are registered. If you have added or changed a schema, ensure the schema has been registered before running the scripts.

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

#### Generate Metadata Template

create_template_from_Syn_schema.py will generate either a .csv or .xlsx metadata template based on a registered metadata schema. Note that this script will not upload the file to Synapse automatically.

Parameters:

- `<registered schema id>`: id of the registered metadata schema, including organization (e.g. sysbio.metadataTemplates_assay.STARRSeq).
- `<output file path>`: Full path to the where the template file should be output.
- `csv`  OR `excel`: Choose output as .csv (csv) or .xlsx (excel). A csv file will only include a header with the metadata keys. An excel file will include three sheets: one with a header of metadata keys, one with a dictionary of key descriptions, and one with a dictionary of allowed values plus their descriptions.

### Docker

This repo contains a Dockerfile that can be used to build a docker image locally. Alternatively, the docker image is on Docker Hub under [aryllen/sysbioDCCjsonschemas](https://hub.docker.com/repository/docker/aryllen/sysbiodccjsonschemas).

##### Build Image Locally

If you'd like to build the docker image locally, clone this repo and open a terminal in the sysbioDCCjsonschemas folder. Then build image and run interactively.

```bash
git clone https://github.com/Sage-Bionetworks/sysbioDCCjsonschemas.git
cd sysbioDCCjsonschemas
docker build --no-cache -t sysbiodccjsonschemas .
docker run --rm -it sysbiodccjsonschemas
```

##### Pull Existing Image

If you'd like to use an existing image, then pull the docker image from Docker Hub. Below assumes pulling the latest version of the image. To use a different version, replace `latest` with the [desired tag](https://hub.docker.com/repository/docker/aryllen/sysbiodccjsonschemas/tags?page=1&ordering=last_updated). The container can be run interactively once the image is pulled.

```
docker pull aryllen/sysbiodccjsonschemas:latest
docker run --rm -it aryllen/sysbiodccjsonschemas:latest
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

##### Annotation Table

The annotation table can be updated with a single command. Example:

```bash
python3 code/python/create_Syn_table_from_Syn_schemas.py \
  --config_file config/schemas.yml \
  --consortium PsychENCODE \
  new_table \
  --parent_synapse_id syn21786765 \
  --synapse_table_name pec_annots
```

##### Generate Metadata Template

Since the metadata template script does not upload the template to Synapse, there is an extra step.

1. Generate the metadata template(s). Example:

   ```bash
   python3 create_template_from_Syn_schema.py \
     sysbio.metadataTemplates-assay.STARRSeq \
     template_assay_STARRSeq.xlsx excel
   ```

2. Store the metadata template in Synapse. Example:

   ```bash
   synapse store --parentid syn20729790 template_assay_STARRSeq.xlsx
   ```
