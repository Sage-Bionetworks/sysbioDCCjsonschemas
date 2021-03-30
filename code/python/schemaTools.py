#!/usr/bin/env python3

"""
Program: schemaTools.py

Purpose: Common functions used by programs utilizing schemas in Synapse.

"""

VALUES_LIST_KEYWORDS = ["anyOf", "enum"]

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
          Synapse.
    """

    import pandas as pd

    definitions_columns = ["key", "type", "description", "required", "maximumSize"]
    definitions_df = pd.DataFrame(columns=definitions_columns)
    values_columns = ["key", "value", "valueDescription", "source"]
    values_df = pd.DataFrame(columns=values_columns)

    for key in json_schema["properties"]:

        if "$ref" in json_schema["properties"][key]:
            # Dereference the term schema.
            term_schema = synlogin._waitForAsync("/schema/type/validation/async",
                                                 {"$id": json_schema["properties"][key]["$ref"]})

            schema_defs = term_schema["validationSchema"]
            schema_module = json_schema["properties"][key]["$ref"].split("-")[1].split(".")[0]
        else:
            schema_defs = json_schema["properties"][key]
            schema_module = ""

        definitions_dict = {}
        definitions_dict["key"] = key
        definitions_dict["module"] = schema_module

        if "type" in schema_defs:
            definitions_dict["type"] = schema_defs["type"]

            # If the type is Boolean, create a true/false values list.
            if schema_defs["type"].upper() == "BOOLEAN":
                schema_defs["anyOf"] = []
                tf_dict = {}
                tf_dict["const"] = "false"
                schema_defs["anyOf"].append(tf_dict.copy())
                tf_dict["const"] = "False"
                schema_defs["anyOf"].append(tf_dict.copy())
                tf_dict["const"] = "FALSE"
                schema_defs["anyOf"].append(tf_dict.copy())
                tf_dict["const"] = "true"
                schema_defs["anyOf"].append(tf_dict.copy())
                tf_dict["const"] = "True"
                schema_defs["anyOf"].append(tf_dict.copy())
                tf_dict["const"] = "TRUE"
                schema_defs["anyOf"].append(tf_dict.copy())

        if "description" in schema_defs:
            definitions_dict["description"] = schema_defs["description"]

        if "maximumSize" in schema_defs:
            definitions_dict["maximumSize"] = schema_defs["maximumSize"]

        if (("required" in json_schema)
            and (key in json_schema["required"])):
            definitions_dict["required"] = True
        else:
            definitions_dict["required"] = False

        definitions_df = definitions_df.append(definitions_dict, ignore_index=True)

        # If the term is a redefinition of an existing term, resolve the
        # existing reference in order to get the values list. If the existing
        # object contains a values list (anyOf or enum), add it  to the
        # redefined terms keys.
        if "properties" in schema_defs:
            redef_schema = synlogin._waitForAsync("/schema/type/validation/async",
                                                  {"$id": schema_defs["properties"][key]["$ref"]})

            if any([value_key in redef_schema["validationSchema"] for value_key in VALUES_LIST_KEYWORDS]):
                vkey = list(set(VALUES_LIST_KEYWORDS).intersection(redef_schema["validationSchema"]))[0]
                schema_defs[vkey] = redef_schema["validationSchema"][vkey]

        values_dict = {}
        if "pattern" in schema_defs:
            values_dict["key"] = key
            values_dict["value"] = schema_defs["pattern"]
            values_df = values_df.append(values_dict, ignore_index=True)

        elif "const" in schema_defs:
            values_dict["key"] = key
            values_dict["value"] = schema_defs["const"]
            values_df = values_df.append(values_dict, ignore_index=True)

        elif any([value_key in schema_defs for value_key in VALUES_LIST_KEYWORDS]):
            vkey = list(set(VALUES_LIST_KEYWORDS).intersection(schema_defs))[0]
            for value_row in schema_defs[vkey]:
                values_dict["key"] = key

                if "const" in value_row:
                    values_dict["value"] = value_row["const"]

                if "description" in value_row:
                    values_dict["valueDescription"] = value_row["description"]

                if "source" in value_row:
                    values_dict["source"] = value_row["source"]

                values_df = values_df.append(values_dict, ignore_index=True)
                values_dict = {}

    return(definitions_df, values_df)
