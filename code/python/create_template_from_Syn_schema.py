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

Input parameters: Full name of the registered schema, including
                      organization
                  Full pathname to the output template file
                  Desired output - either csv or excel

Outputs: csv template files or Excel workbook

Execution: create_template_from_Syn_schema.py <JSON schema name>
             <output file> <csv/excel>
"""

import argparse
import os
import pandas as pd
import synapseclient

VALUES_LIST_KEYWORDS = ["anyOf", "enum"]

def get_alias_dictionary(json_schema):
    """
    Function: get_alias_dictionary

    Purpose: Given a dereferenced Synapse schema, return a dictionary of schema
             names and their associated properties. This is necessary because
             there are occasions where the property references a schema with
             a different name. For example, in the PEC snpArray template
             schema, the property is 260/280 but the schema it references is
             qc260280 because Synapse does not allow non-alphanumeric
             characters in the schema name and also requires that the schema
             name starts with a character.

    Input parameters: A dereferenced Synapse schema

    Returns: A dictionary with the schema name as the key and the schema
             property as the value.
    """
    alias_dict = {}
    schema_properties = json_schema["validationSchema"]["properties"]

    for key_val in schema_properties:
        key = schema_properties[key_val]["$ref"].split(".")[-1]
        alias_dict[key] = key_val

    return alias_dict


def get_Syn_definitions_values(json_schema, synlogin):
    """
    Function: get_Syn_definitions_values

    Purpose: Return pandas dataframes of schema properties needed to generate
             templates.

    Input parameters: File object pointing to the JSON schema file
                      Synapse object created in the main program to log into
                      Synapse.

    Returns: A dataframe of key types, definitions, required keys, and maximum
             sizes
                 definitions_df["key"] - string
                 definitions_df["type"] - string
                 definitions_df["description"] - string
                 definitions_df["required"] - Boolean
                 definitions_df["maximumSize"] - integer

             A dataframe of key values lists
                 values_df["key"] - string
                 values_df["value"] - string
                 values_df["valueDescription"] - string
                 values_df["source"] - string

    Note: This function is used with JSON schemas that are registered in
          Synapse
    """

    import pandas as pd

    definitions_columns = ["key", "type", "description", "required", "maximumSize"]
    definitions_df = pd.DataFrame(columns=definitions_columns)
    values_columns = ["key", "value", "valueDescription", "source"]
    values_df = pd.DataFrame(columns=values_columns)

    # Get a list of schema aliases in case the property name is different
    # from the schema name.
    alias_dict = get_alias_dictionary(json_schema)

    schema_defs = json_schema["validationSchema"]["definitions"]
    for full_schema_name in schema_defs:
        definitions_dict = {}

        # The pattern of the schema name is organization-module.key
        key = full_schema_name.split("-")[1].split(".")[1]
        definitions_dict["key"] = alias_dict[key]
        schema_values = schema_defs[full_schema_name]

        if schema_values:
            if "type" in schema_values:
                definitions_dict["type"] = schema_values["type"]

            if "description" in schema_values:
                definitions_dict["description"] = schema_values["description"]

            if "maximumSize" in schema_values:
                definitions_dict["maximumSize"] = schema_values["maximumSize"]

            if (("required" in json_schema["validationSchema"])
                and (key in json_schema["validationSchema"]["required"])):
                definitions_dict["required"] = True
            else:
                definitions_dict["required"] = False

            definitions_df = definitions_df.append(definitions_dict, ignore_index=True)

            # If the term is a redefinition of an existing term, resolve the
            # existing reference in order to get the values list. If the
            # existing object contains a values list (anyOf or enum), add it
            # to the redefined terms keys.
            if "properties" in schema_values:
                existing_schema = synlogin._waitForAsync("/schema/type/validation/async",
                                                         {"$id": schema_values["properties"][key]["$ref"]})

                if any([value_key in existing_schema["validationSchema"] for value_key in VALUES_LIST_KEYWORDS]):
                    vkey = list(set(VALUES_LIST_KEYWORDS).intersection(existing_schema["validationSchema"]))[0]
                    schema_values[vkey] = existing_schema["validationSchema"][vkey]

            values_dict = {}
            if "pattern" in schema_values:
                values_dict["key"] = alias_dict[key]
                values_dict["value"] = schema_values["pattern"]
                values_df = values_df.append(values_dict, ignore_index=True)

            elif any([value_key in schema_values for value_key in VALUES_LIST_KEYWORDS]):
                vkey = list(set(VALUES_LIST_KEYWORDS).intersection(schema_values))[0]
                for value_row in schema_values[vkey]:
                    values_dict["key"] = alias_dict[key]

                    if "const" in value_row:
                        values_dict["value"] = value_row["const"]

                    if "description" in value_row:
                        values_dict["valueDescription"] = value_row["description"]

                    if "source" in value_row:
                        values_dict["source"] = value_row["source"]

                    values_df = values_df.append(values_dict, ignore_index=True)
                    values_dict = {}

    return(definitions_df, values_df)


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

    args = parser.parse_args()

    json_schema = syn._waitForAsync("/schema/type/validation/async", {"$id": args.json_schema_name})
    definitions_df, values_df = get_Syn_definitions_values(json_schema, syn)
    definitions_df = definitions_df[["key", "description"]]
    template_df = pd.DataFrame(columns=definitions_df["key"].tolist())

    if args.type_of_output == "csv":
        template_csv(args.output_file, template_df, definitions_df, values_df)
    elif args.type_of_output == "excel":
        template_excel(args.output_file, template_df, definitions_df, values_df)


if __name__ == "__main__":
    main()
