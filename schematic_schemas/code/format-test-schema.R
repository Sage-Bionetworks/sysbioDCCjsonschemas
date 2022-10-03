library(here)
library(tidyverse)
library(glue)
library(googlesheets4)
library(googledrive)
library(synapser)

# read in large csv file that Anthony made
big_model <- read_csv(here("schematic_schemas", "amp.ad.data.model.csv"))

all_templates <- big_model %>% 
  filter(Parent == "DataType") %>% 
  select(Attribute)

# pull out just a few templates to focus on
subset_templates <- all_templates %>% 
  filter(str_detect(Attribute, "assay_rnaSeq|assay_MRI|individual_animal|biospecimen_metadata")) %>% 
  pull()

# get all "dependsOn" values for this subset as a vector
data_properties <- big_model %>% 
  filter(Attribute %in% subset_templates) %>% 
  pull(DependsOn) %>% 
  glue_collapse(sep = ", ") %>% 
  str_split(", ") %>% 
  unlist() %>% 
  unique()

# filter data model for the 4 templates and their dependsOn attributes
test_schema <- big_model %>% 
  filter(Attribute %in% subset_templates | Attribute %in% data_properties)

# write csv
write_csv(test_schema, here("schematic_schemas", "model-ad-schematic-test-schema-v1.csv"), na = "")

# write googlesheet
gs4_create("model-ad-schematic-test-schema-v1", sheets = test_schema)


