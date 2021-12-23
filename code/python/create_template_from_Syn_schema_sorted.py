#!/usr/bin/env python3

"""
Program: create_template_from_Syn_schema_sorted.py

Purpose: Use a JSON schema registered in Synapse to generate either csv file
         templates or an Excel workbook containing template worksheets.  The
         following will be generated as either separate files (csv) or
         worksheets within the workbook (Excel):
         - a blank template to use for data entry
         - a dictionary defining the columns in the template
         - a listing of allowable values for columns that use a controlled
           vocabulary list

Input parameters: Full name of the registered schema, including
                      organization
                  Full pathname to the output template file
                  Desired output - either csv or excel
                  Full pathname for the template json file in 
                  schema_metadata_templates folder
Outputs: csv template files or Excel workbook

Execution: create_template_from_Syn_schema.py <JSON schema name>
             <output file> <csv/excel> <template_json>
"""

import argparse
import os
import pandas as pd
import synapseclient
import schemaTools
import json 
from collections import OrderedDict

def template_csv(template_file_name, template_df, dictionary_df, values_df):
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
        template_file_name: Name of the template file to output. The dictionary
                            and values files will append "_dictionary" and
                            "_values", respectively, after the file name and
                            before the ".csv" extension.
        template_df - An empty pandas dataframe with the column names being
                      the desired template columns
        dictionary_df - A pandas dataframe containing the definition
                        information for each column in the template
        values_df - A pandas dataframe of the values lists used by columns
                    in the template
    """
    base_file_name, base_file_ext = os.path.splitext(template_file_name)
    dictionary_file_name = (base_file_name + "_dictionary" +
                            base_file_ext)
    values_file_name = (base_file_name + "_values" + base_file_ext)

    # Create a template file.
    with open(template_file_name, "w") as template_file:
        template_df.to_csv(template_file, index=False)

    # Create a dictionary file
    with open(dictionary_file_name, "w") as dictionary_file:
        dictionary_df.to_csv(dictionary_file, index=False)

    # Create a values file
    with open(values_file_name, "w") as values_file:
        values_df.to_csv(values_file, index=False)


def template_excel(workbook_name, template_df, dictionary_df, values_df):
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
        workbook_name: Name of the workbook to output
        template_df - An empty pandas dataframe with the column names being
                      the desired template columns
        dictionary_df - A pandas dataframe containing the definition
                        information for each column in the template
        values_df - A pandas dataframe of the values lists used by columns
                    in the template
    """
    workbook_writer = pd.ExcelWriter(workbook_name, engine="xlsxwriter")

    # Create a template worksheet.
    template_df.to_excel(workbook_writer, index=False, sheet_name="Template")

    # Create a dictionary worksheet
    dictionary_df.to_excel(workbook_writer, index=False, sheet_name="Dictionary")

    # Create a values worksheet
    values_df.to_excel(workbook_writer, index=False, sheet_name="Values")

    workbook_writer.save()


def main():

    syn = synapseclient.Synapse()
    syn.login(silent=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("json_schema_name", type=str,
                        help="Full name for the registered JSON schema")
    parser.add_argument("output_file", type=str,
                        help="Full pathname for the output file")
    parser.add_argument("type_of_output", type=str,
                        help="Type of output (csv or excel)")
    parser.add_argument("template_json", type=str,
                        help="Full pathname for the template json file in schema_metadata_templates folder")
    args = parser.parse_args()

    json_schema = syn.restGET(f"/schema/type/registered/{args.json_schema_name}")
    definitions_df, values_df = schemaTools.get_Syn_definitions_values(json_schema, syn)
    #re-order the columns as template json file
    with open(args.template_json, 'r') as f:
        template = json.load(f, object_pairs_hook=OrderedDict)
        order_series = pd.Series(template['properties'].keys())
    definitions_df = definitions_df[["key", "description"]]
    definitions_df = definitions_df.set_index('key')
    definitions_df = definitions_df.loc[order_series].reset_index()
    template_df = pd.DataFrame(columns=definitions_df["key"].tolist())

    if args.type_of_output == "csv":
        template_csv(args.output_file, template_df, definitions_df, values_df)
    elif args.type_of_output == "excel":
        template_excel(args.output_file, template_df, definitions_df, values_df)


if __name__ == "__main__":
    main()
