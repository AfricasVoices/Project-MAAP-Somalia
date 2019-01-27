# Project UNICEF MAAP
Data pipeline for Monitoring and Accountability to Affected Populations (MAAP) Somalia.


This pipeline fetches all project data from a Rapid Pro instance, and processes it to produce CSV files suitable for downstream analysis.

## Pre-requisites
Before the pipeline can be run, the following tools must be installed:
- Docker
- Bash

Development requires the following additional tools:
- Python 3.6+
- pipenv
- git
## Usage
Running the pipeline requires (0) creating a phone number <-> UUID table to support de-identification of respondents, (1) fetching the PDM survey and demographics from Rapid Pro, (2) fetching the contact data from Rapid Pro (3) merging the post distribution monitoring data and the demographics, (4) merging the outside data(SCOPE) to the rapidpro data, (5) creating files for ICR, (6) creating CODA files (7) merging the coded CODA data with the rest of the data, and (8) creating the analysis files.

To simplify the configuration and execution of these stages, this project includes a `scripts` directory, which contains shell scripts for driving each of the stages. More detailed descriptions of the functions of each of those stages, and instructions for using the run scripts, are provided below.

### 0. Phone Number <-> UUID Table
First, create an empty phone number <-> UUID table by running the following command in the `scripts` directory:
```
$ ./00_create_uuid_table.sh <data-root> 
```

where - `data-root` is an absolute path to the directory in which all pipeline data should be stored. The UUID table will be saved to a file in the directory <data-root>/00 UUIDs.

### 1. Fetch PDM survey and demographics
Next, fetch PDM and demographics required by the pipeline from Rapid Pro by running the following command in the `scripts` directory:
```
$ ./01_fetch_messages.sh <user> <rapid-pro-root> <rapid-pro-server> 
<rapid-pro-token> <data-root> <test-contacts-path>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `rapid-pro-root` is an absolute path to the directory to store a local clone of [RapidProTools](https://github.com/AfricasVoices/RapidProTools) in. The RapidProTools project hosts the re-usable RapidPro data fetchers. The exact version required by this project is checked out automatically.
- `rapid-pro-server` is the root address of the RapidPro server to retrieve data from e.g. [app.rapidpro.io](https://app.rapidpro.io).
- `rapid-pro-token` is the access token for this instance of RapidPro. The access token may be found by logging into RapidPro's web interface, then navigating to your organisation page (via the button in the top-right), then copying the hexadecimal string given after "Your API Token is ..."
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. Raw data will be saved to TracedData JSON files in <data-root>/01 Raw Messages

### 2.Fetch Contact Data
This fetches saved contact data from Rapid Pro by running the following command in the `scripts` directory:
```
./02_fetch_contacts.sh <user> <rapid-pro-root> <rapid-pro-server> <rapid-pro-token> <data-root> <test-contacts-path>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `rapid-pro-root` is an absolute path to the directory to store a local clone of [RapidProTools](https://github.com/AfricasVoices/RapidProTools) in. The RapidProTools project hosts the re-usable RapidPro data fetchers. The exact version required by this project is checked out automatically.
 - `rapid-pro-server` is the root address of the RapidPro server to retrieve data from e.g. [app.rapidpro.io]( https://app.rapidpro.io).
- `rapid-pro-token` is the access token for this instance of RapidPro. The access token may be found by logging into RapidPro's web interface, then navigating to your organisation page (via the button in the top-right), then copying the hexadecimal string given after "Your API Token is ..."
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. Raw data will be saved to TracedData JSON files in `<data-root>/01 Raw Messages`
- `test-contacts-path` is the absolute path list of contacts that were used to test the pipeline.

### 3. Merge PDM and Demographics
Merges the pdm and demographics into a single TracedData JSON file by running the following command in the `scripts` directory:
```
./03_merge_pdm_demogs.sh <user> <data-root>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. The resulting data will be saved to a TracedData JSON file in <data-root>/03 PDM Demogs Merged/

### 4. Merge SCOPE data
Uses the *TracedData JSON file from (3)* merges SCOPE data into it by running the following command in the `scripts` directory: 
```
./04_merge_scope.sh <user> <data-root> <scope-path>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. The resulting data will be saved to a TracedData JSON file in `<data-root>/04 SCOPE with Messages/`
- scope-path is path to the SCOPE data csv

### 5. Create ICR files
Uses the *TracedData JSON file from (4)* to create files for inter-coder reliability in by running the following command in the `scripts` directory: 
```
./05_create_icr_files.sh <user> <data-root>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. The resulting data will be saved to a TracedData JSON file in `<data-root>/05 ICR/`

### 6 Create CODA files
Creates uncoded CODA files to be coded by running the following command in the `scripts` directory:
```
./06_create_coda_files.sh <user> <data-root>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. The TracedData JSON file will be saved in `<data-root>/06 CODA with Messages/`, the CODA file will be saved in `<data-root>/06 Uncoded CODA files/`

### 7 Merge CODA file
Uses *the the TracedData JSON from (6)* merges coded CODA files into it by running the following command in the `scripts` directory:
```
./07_merge_coda_files.sh <user> <data-root>
```

Where:
- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. The TracedData JSON file will be saved in` <data-root>/06 CODA with Messages/`, the CODA file will be saved in `<data-root>/06 Uncoded CODA files/`

Note that the coded coda files need to be saved in `<data-root>/coded_coda_files/` with the following names:
- gender_coded.json
- age_coded.json
- clan_coded.json
- needs_met_coded.json
- cash_modality_coded.json
- community_priorities_coded.json
- inclusion_coded.json

### 8 Create analysis file
Creates messages/individuals CSVs for final analysis, by running the following command in the `scripts` directory:
```
./08_create_analysis_files.sh <user> <data-root>
```
Where:

- `user` is the identifier of the person running the script, for use in the TracedData Metadata e.g. `user@africasvoices.org`
- `data-root` is an absolute path to the directory in which all pipeline data should be stored. The resulting data will be saved in `<data-root>/08 Analysis Files/`


