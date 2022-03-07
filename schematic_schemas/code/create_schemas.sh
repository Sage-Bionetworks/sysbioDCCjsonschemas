#!/bin/bash

schematic schema convert --base_schema ./minimal.model.jsonld ./individual-human-data-model.csv
schematic manifest --config config.yml get -s -oa -p individual-human-data-model.jsonld -t IndividualHuman -dt IndividualHuman

schematic schema convert --base_schema ./minimal.model.jsonld ./amp.ad.data.model.csv
schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t IndividualHumanMetadataTemplate -dt IndividualHumanMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t ManifestMetadataTemplate -dt ManifestMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t BiospecimenMetadataTemplate -dt BiospecimenMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t Assay16SrRNAseqMetadataTemplate -dt Assay16SrRNAseqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayATACSeqMetadataTemplate -dt AssayATACSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayBisulfiteSeqMetadataTemplate -dt AssayBisulfiteSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayChIPSeqMetadataTemplate -dt AssayChIPSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayHICMetadataTemplate -dt AssayHICMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayMetabolomicsMetadataTemplate -dt AssayMetabolomicsMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayMethylationArrayMetadataTemplate -dt AssayMethylationArrayMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayMRIMetadataTemplate -dt AssayMRIMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayNanostringMetadataTemplate -dt AssayNanostringMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayPETMetadataTemplate -dt AssayPETMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayRnaArrayMetadataTemplate -dt AssayRnaArrayMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayRnaSeqMetadataTemplate -dt AssayRnaSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayScrnaSeqMetadataTemplate -dt AssayScrnaSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssaySnpArrayMetadataTemplate -dt AssaySnpArrayMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssaySTARRSeqMetadataTemplate -dt AssaySTARRSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayTMTquantitationMetadataTemplate -dt AssayTMTquantitationMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayWholeExomeSeqMetadataTemplate -dt AssayWholeExomeSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t AssayWholeGenomeSeqMetadataTemplate -dt AssayWholeGenomeSeqMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t BiospecimenDrosophilaMetadataTemplate -dt BiospecimenDrosophilaMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t BiospecimenInvitroMetadataTemplate -dt BiospecimenInvitroMetadataTemplate

schematic manifest --config config.yml get -s -oa -p ./amp.ad.data.model.jsonld -t IndividualAnimalMetadataTemplate -dt IndividualAnimalMetadataTemplate
