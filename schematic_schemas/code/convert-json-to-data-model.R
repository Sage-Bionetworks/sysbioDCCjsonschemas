library(rjson)
library(tibble)
library(purrr)
library(tidyr)
library(dplyr)
library(readr)

assay_schema <- list.files("~/work/sysbioDCCjsonschemas/schema_metadata_templates/shared",
                         full.names = TRUE)

ad_schema <- list.files("~/work/sysbioDCCjsonschemas/schema_metadata_templates/AD",
                      full.names = TRUE)

syn_schema <- list.files("~/work/synapseAnnotations/terms",
                         full.names = TRUE, recursive = TRUE)

parse_ad_schema <- function(x, Parent = NA_character_) {
  
  json <- rjson::fromJSON(file = x)
  id <- ifelse("$id" %in% names(json), json$`$id`, NA_character_)
  description <- ifelse("description" %in% names(json), json$description, NA_character_)
  if ("properties" %in% names(json)) {
    # properties <- purrr::imap_dfc(json$properties, ~ .x$`$ref`) %>%
    #   tidyr::pivot_longer(everything(), names_to = "attribute", values_to = "source") %>%
    #   dplyr::mutate("Parent" = "DataProperty")
    # properties <- paste(imap_chr(json$properties, ~ .x$`$ref`), collapse = ", ")
    dependsOn <- paste(names(json$properties), collapse = ", ")
  } else dependsOn <- NA
  required <- ifelse("required" %in% names(json), paste(json$required, collapse = ", "), NA_character_)
  # attribute <- gsub("(^assay_|_metadata_template)", "", basename(tools::file_path_sans_ext(x)))
  attribute <- basename(tools::file_path_sans_ext(x))
  anyOf <- ifelse("anyOf" %in% names(json), paste(imap_chr(json$anyOf, ~.x$const), collapse = ", "), NA_character_)
  
  tibble::tibble(
    Attribute = attribute,
    Description = description,
    "Valid Values" = anyOf,
    DependsOn = dependsOn,
    Properties = NA_character_,
    Required = required,
    Parent = Parent,
    "DependsOn Component" = NA_character_,
    Source = id,
    "Validation Rules" = NA_character_
  )
  
}

dataTypes <- bind_rows(
  imap_dfr(ad_schema, ~ parse_ad_schema(.x, Parent = "DataType")),
  imap_dfr(assay_schema, ~parse_ad_schema(.x, Parent = "DataType"))
)

dataProperties <- imap_dfr(syn_schema, ~parse_ad_schema(.x, Parent = "DataProperty"))

data_model <- bind_rows(dataTypes, dataProperties)

required_vars <- unique(unlist(strsplit(stats::na.omit(unique(data_model$Required)), ", ")))

data_model <- data_model %>% mutate(
  Required = case_when(!Attribute %in% required_vars ~ FALSE, TRUE ~ TRUE),
  DependsOn = case_when(Parent == "DataType" ~ paste0("Component, ", DependsOn),
                        TRUE ~ DependsOn)
)

write_csv(data_model, "../amp.ad.data.model.csv", na = "")

