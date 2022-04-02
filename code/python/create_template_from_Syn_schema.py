#!/usr/bin/env python3

"""
Program: create_template_from_Syn_schema.py

Purpose: Use a JSON schema registered in Synapse to generate either csv file
         templates or an Excel workbook containing template worksheets.  The
         following will be generated as either separate files (csv) or
         worksheets within the workbook (Excel):
         - a blank template to use for data entry
         - a dictionary defining the columns in the template
         - a listing of allowable values for columns that use a controlled
           vocabulary list

Input parameters: registered_schema_id - Full name of the registered schema, i.e. schema id
                  config_file - schemas.yml that includes all registered schemas, e.g. /home/ec2-user/sysbioDCCjsonschemas/config/schemas.yml 
                  template_json - Optional. Specify it when you want the output template columns to match the order of the terms as they appear in a json file. 
                                  Full pathname for the template json file in the schema_metadata_templates folder. 
Outputs: a csv template files or Excel workbook in the Consortium specific metadata folder

Execution: create_template_from_Syn_schema.py <registered_schema_id> <config_file> <template_json>
"""
import argparse
import os
import pandas as pd
import synapseclient
from synapseclient.entity import File
import schemaTools
import yaml
import json 
from collections import OrderedDict

def prGreen(skk:str) -> str:
    print("\033[92m {}\033[00m" .format(skk))

def template_csv(template_file_name, template_file_ext, template_df, dictionary_df, values_df, syn, parent):
    """
    Function: template_csv

    Purpose: Write csv files as follows:
             - <file name>_template.csv: template file with column names to be
                   used for entering data
             - <file name>_dictionary.csv: file with the definitions of the
                   columns in the "_template" file
             - <file name>_Values: file with any controlled vocabulary lists
                   used for columns in the "_template" file

    Arguments:
        template_file_name - Name of the template file to output. The dictionary
                            and values files will append "_dictionary" and
                            "_values", respectively, after the file name and
                            before the ".csv" extension.
        template_file_ext - the file extension of the template file
        template_df - An empty pandas dataframe with the column names being
                      the desired template columns
        dictionary_df - A pandas dataframe containing the definition
                        information for each column in the template
        values_df - A pandas dataframe of the values lists used by columns
                    in the template
    """
    dictionary_file_name = (template_file_name + "_dictionary." +
                            template_file_ext)
    values_file_name = (template_file_name + "_values." + template_file_ext)
    template_file_name = (template_file_name + '.' + template_file_ext)
    for parent_id in parent: 
        # Create and store a template file.
        template_df.to_csv(template_file_name, index=False)
        prGreen(f'Saving template in {parent_id}')
        syn.store(File(template_file_name, parent=parent_id))
        # Create and store a dictionary file
        dictionary_df.to_csv(dictionary_file_name, index=False)
        prGreen(f'Saving dictionary in {parent_id}')
        syn.store(File(dictionary_file_name, parent=parent_id))
        # Create and store a values file
        values_df.to_csv(values_file_name, index=False)
        prGreen(f'Saving values in {parent_id}')
        syn.store(File(values_file_name, parent=parent_id))

def template_excel(template_file_name, template_df, dictionary_df, values_df,syn, parent):
    """
    Function: template_excel

    Purpose: Write an Excel workbook containing the following worksheets:
             - "Template": worksheet with column names to be used for
                           entering data
             - "Dictionary": worksheet with the definitions of the columns in
                             the "Template" worksheet
             - "Values": worksheet with any controlled vocabulary lists used
                         for columns in the "Template" worksheet

    Arguments:
        template_file_name: Name of the workbook to output
        template_df - An empty pandas dataframe with the column names being
                      the desired template columns
        dictionary_df - A pandas dataframe containing the definition
                        information for each column in the template
        values_df - A pandas dataframe of the values lists used by columns
                    in the template
    """
    workbook_writer = pd.ExcelWriter(template_file_name, engine="xlsxwriter")

    # Create a template worksheet.
    template_df.to_excel(workbook_writer, index=False, sheet_name="Template")

    # Create a dictionary worksheet
    dictionary_df.to_excel(workbook_writer, index=False, sheet_name="Dictionary")

    # Create a values worksheet
    values_df.to_excel(workbook_writer, index=False, sheet_name="Values")
    workbook_writer.save()
    for parent_id in parent: 
        prGreen(f'Save template in {parent_id}')
        syn.store(File(template_file_name, parent=parent_id))

def main():

    syn = synapseclient.Synapse()
    syn.login(silent=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("registered_schema_id", type=str,  
                        help="Registered JSON schema id")
    parser.add_argument("config_file", type=argparse.FileType("r"),
                               help="Full pathname for the YAML config file")
    parser.add_argument("template_json", type=str, nargs='?',
                        help="Optional. Full pathname for the template json file in schema_metadata_templates folder. ")
    args = parser.parse_args()

    json_schema = syn.restGET(f"/schema/type/registered/{args.registered_schema_id}")
    definitions_df, values_df = schemaTools.get_Syn_definitions_values(json_schema, syn)
    if args.template_json is not None:
        #re-order the columns as template json file
        with open(args.template_json, 'r') as f:
            template = json.load(f, object_pairs_hook=OrderedDict)
            order_series = pd.Series(template['properties'].keys())
        definitions_df = definitions_df[["key", "description"]]
        definitions_df = definitions_df.set_index('key')
        definitions_df = definitions_df.loc[order_series].reset_index()
        template_df = pd.DataFrame(columns=definitions_df["key"].tolist())
    else: 
        definitions_df = definitions_df[["key", "description"]]
        template_df = pd.DataFrame(columns=definitions_df["key"].tolist())
    #get the parent SynapseID and template file name for each template based on schemas.yml
    schema_dict = yaml.safe_load(args.config_file)
    schema_dict = schema_dict[args.registered_schema_id]
    parent = [value for key, value in schema_dict.items() if key != 'schema_name']
    template_file_name = schema_dict['schema_name']
    template_file_ext = template_file_name.rsplit('.',1)[1]
    if template_file_ext == "csv":
       template_file_name = template_file_name.rsplit('.',1)[0]
       template_csv(template_file_name, template_file_ext, template_df, definitions_df, values_df, syn, parent)
    elif template_file_ext == "xlsx":
        template_excel(template_file_name, template_df, definitions_df, values_df, syn, parent)

if __name__ == "__main__":
    main()
