#########################################################
## Description: Add a new study to the PEC dccvalidator
##              Studies table 
## Input: study_to_add - study_name to add, str
##        folder_synid - folder of the new study
## Output: updated version of dccvalidator Studies table
#########################################################
#clear environment
rm(list=ls())

#load packages 
library(readr)
library(glue)
library(tibble)
library(synapser)
library(dplyr)

#login to synapse
synLogin()

# fill in the study name
study_to_add <- ""
# fill in the study folder
folder_synid <- ""
# specify backend study table
table_synid <- "syn20968992"

# function to delete table rows and save the edited content - note that in the backend of the Synapse table,
# rows are being appended not deleted. ROW_ID will increment every time this script
# is executed.
update_table <- function(synId, replacement_df) {
  current <- synTableQuery(glue::glue("SELECT * FROM {synId}"))
  synDelete(current) # delete current rows
  new <- Table(synId, replacement_df)
  synStore(new)
}

# get table
table <- read_csv(synTableQuery(glue("Select * from {table_synid}"))$filepath)
table <- as.data.table(table)
# add new row with new entry
table <- tibble::add_row(table, Study = folder_synid, StudyName = study_to_add)
# keep a record of the original table in case modify the table accidently
table_ori <- copy(table)
# order table alphabetically
table <- table[order(table$StudyName),]
#deal with RowID error
table$ROW_ID <- NA
table$ROW_VERSION <- NA

#update table 
update_table(table_synid, table)

