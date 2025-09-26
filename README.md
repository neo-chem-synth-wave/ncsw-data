# NeoChemSynthWave: Data
[![Static Badge](https://img.shields.io/badge/ncsw__data-2025.9.1-%23E68E36?logo=github&style=flat)](https://github.com/neo-chem-synth-wave/ncsw-data/releases/tag/2025.9.1)
[![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)](https://www.isct.ac.jp)
[![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)](https://www.elix-inc.com)

Welcome to the **NeoChemSynthWave: Data** project !!!

Over the past decade, computer-assisted chemical synthesis has re-emerged as a prominent research subject.
Even though the idea of utilizing computers to assist chemical synthesis has existed for nearly as long as computers themselves, the inherent complexity repeatedly exceeded the available resources.
However, recent machine learning approaches have exhibited the potential to break this tendency.
The performance of such approaches is dependent on data that frequently suffer from limited quantity, quality, visibility, and accessibility, posing significant challenges to potential scientific breakthroughs.
Consequently, the primary objective of the **NeoChemSynthWave: Data** project is to provide access to essential open computer-assisted chemical synthesis data.


## Utilization Instructions
The utilization instructions of this repository are structured as follows:

- [Installation of the Package](#installation-of-the-package)
- [Utilization of the Package](#utilization-of-the-package)
- [Utilization of the Scripts and Notebooks](#utilization-of-the-notebooks-and-scripts)


### Installation of the Package
The [ncsw_data](/ncsw_data) package can be installed in an existing environment using the [pip](https://pip.pypa.io) command as follows:

```shell
pip install ncsw-data
```

A local environment can be created using the [git](https://git-scm.com) and [conda](https://conda.io) commands as follows:

```shell
git clone https://github.com/neo-chem-synth-wave/ncsw-data.git

cd ncsw-data

conda env create -f environment.yaml

conda activate ncsw-data-env

pip install .
```


### Utilization of the Package
The [ncsw_data](/ncsw_data) package consists of the following sub-packages:

- [Source](#source)
- [Storage](#storage)


#### Source
The [source](/ncsw_data/source) sub-package supports three alternatives for the downloading, extraction, and formatting of a specific version of computer-assisted chemical synthesis data from a specific source.
The first alternative is by importing and utilizing the individual data source utility classes:

```python
from ncsw_data.source.compound.zinc.utility import (
    ZINCCompoundDatabaseDownloadUtility,
    ZINCCompoundDatabaseExtractionUtility,
    ZINCCompoundDatabaseFormattingUtility
)

ZINCCompoundDatabaseDownloadUtility.download_v_building_block(
    version="v_building_block_bb_30",
    output_directory_path="/path/to/the/directory_a"
)

ZINCCompoundDatabaseExtractionUtility.extract_v_building_block(
    version="v_building_block_bb_30",
    input_directory_path="/path/to/the/directory_a",
    output_directory_path="/path/to/the/directory_b"
)

ZINCCompoundDatabaseFormattingUtility.format_v_building_block(
    version="v_building_block_bb_30",
    input_directory_path="/path/to/the/directory_b",
    output_directory_path="/path/to/the/directory_c"
)
```

The second alternative is by importing and utilizing the individual data source classes:

```python
from ncsw_data.source.compound.zinc import ZINCCompoundDatabase

zinc_compound_db = ZINCCompoundDatabase()

zinc_compound_db.get_supported_versions()

zinc_compound_db.download(
    version="v_building_block_bb_30",
    output_directory_path="/path/to/the/directory_a"
)

zinc_compound_db.extract(
    version="v_building_block_bb_30",
    input_directory_path="/path/to/the/directory_a",
    output_directory_path="/path/to/the/directory_b"
)

zinc_compound_db.format(
    version="v_building_block_bb_30",
    input_directory_path="/path/to/the/directory_b",
    output_directory_path="/path/to/the/directory_c"
)
```

The third alternative is by importing and utilizing the data source category classes:

```python
from ncsw_data.source.compound import CompoundDataSource

compound_data_source = CompoundDataSource()

compound_data_source.get_names_of_supported_data_sources()

compound_data_source.get_supported_versions(
    name="zinc"
)

compound_data_source.download(
    name="zinc",
    version="v_building_block_bb_30",
    output_directory_path="/path/to/the/directory_a"
)

compound_data_source.extract(
    name="zinc",
    version="v_building_block_bb_30",
    input_directory_path="/path/to/the/directory_a",
    output_directory_path="/path/to/the/directory_b"
)

compound_data_source.format(
    name="zinc",
    version="v_building_block_bb_30",
    input_directory_path="/path/to/the/directory_b",
    output_directory_path="/path/to/the/directory_c"
)
```


#### Storage
The [storage](/ncsw_data/storage) sub-package supports the creation, management, and querying of the Computer-assisted Chemical Synthesis (CaCS) database.
The CaCS database can be created or loaded as follows:

```python
from ncsw_data.storage.cacs.sqlite_db import CaCSSQLiteDatabase

cacs_sqlite_db = CaCSSQLiteDatabase(
    db_url="sqlite:////path/to/the/cacs_db.sqlite"
)

cacs_sqlite_db.create_tables()
```

The archive tables of the CaCS database can be populated as follows:

```python
cacs_sqlite_db.insert_archive_compounds(
    ac_smiles_strings=zinc_v_building_block_bb_30_smiles_strings,  # The chemical compound SMILES strings.
    as_name="zinc",
    as_version="v_building_block_bb_30",
    as_file_name="zinc_v_building_block_bb_30.csv"
)

cacs_sqlite_db.insert_archive_compound_patterns(
    acp_smarts_strings=rdkit_v_pains_by_20100204_baell_j_b_and_holloway_g_a_smarts_strings,  # The chemical compound pattern SMARTS strings.
    as_name="rdkit",
    as_version="v_pains_by_20100204_baell_j_b_and_holloway_g_a",
    as_file_name="rdkit_v_pains_by_20100204_baell_j_b_and_holloway_g_a.csv"
)

cacs_sqlite_db.insert_archive_reactions(
    ar_smiles_strings=uspto_v_50k_by_20171116_coley_c_w_et_al_smiles_strings,  # The chemical reaction SMILES strings.
    as_name="uspto",
    as_version="v_50k_by_20171116_coley_c_w_et_al",
    as_file_name="uspto_v_50k_by_20171116_coley_c_w_et_al.csv"
)

cacs_sqlite_db.insert_archive_reaction_patterns(
    arp_smarts_strings=miscellaneous_v_dingos_by_20190701_button_a_et_al_smarts_strings,  # The chemical reaction pattern SMARTS strings.
    as_name="miscellaneous",
    as_version="v_dingos_by_20190701_button_a_et_al",
    as_file_name="miscellaneous_v_dingos_by_20190701_button_a_et_al.csv"
)
```

The data from the archive tables can be standardized and migrated to the workbench tables of the CaCS database as follows:

```python
cacs_sqlite_db.migrate_archive_to_workbench_compounds(
    ac_standardization_function=process_compound_smiles_strings,  # A user-specified function that standardizes the chemical compound SMILES strings.
)

cacs_sqlite_db.migrate_archive_to_workbench_compound_patterns(
    acp_standardization_function=process_compound_pattern_smarts_strings  # A user-specified function that standardizes the chemical compound pattern SMARTS strings.
)

cacs_sqlite_db.migrate_archive_to_workbench_reactions(
    ar_standardization_function=process_reaction_smiles_strings  # A user-specified function that standardizes the chemical reaction SMILES strings.
)

cacs_sqlite_db.migrate_archive_to_workbench_reaction_patterns(
    arp_standardization_function=process_reaction_pattern_smarts_strings  # A user-specified function that standardizes the chemical reaction pattern SMARTS strings.
)
```

The chemical reaction transformation pattern data of the CaCS database can be extracted and stored as follows:

```python
cacs_sqlite_db.extract_workbench_reaction_transformation_patterns(
    wrp_extraction_function=extract_reaction_transformation_pattern_smarts_strings  # A user-specified function that extracts the chemical reaction pattern SMARTS strings from the chemical reaction SMILES strings.
)
```

The data can be queried from the archive and workbench tables of the CaCS database as follows:

```python
archive_compounds = cacs_sqlite_db.select_archive_compounds()

for acs in archive_compounds:
    for ac in acs:
        print(ac.smiles)

workbench_reactions = cacs_sqlite_db.select_workbench_reactions()

for wrs in workbench_reactions:
    for wr in wrs:
        print(wr.smiles)
        print(wr.workbench_reactant_compounds)
        print(wr.workbench_spectator_compounds)
        print(wr.workbench_product_compounds)
```

The chemical synthesis route data for a specified target chemical compound can be queried as follows:

```python
target_compound_synthesis_routes = cacs_sqlite_db.select_reversed_synthesis_routes(
    wc_smiles=target_compound_smiles
)

for target_compound_synthesis_route in target_compound_synthesis_routes:
    print(target_compound_synthesis_route)
```

A user-specified query can be executed as follows:

```python
select_statement_result = cacs_sqlite_db.execute_select_statement(
    select_statement_text="""
        SELECT COUNT(*)
        FROM workbench_reaction_transformation_pattern;
    """
)

print(select_statement_result.fetchone())
```


### Utilization of the Notebooks and Scripts
The [case_study](/case_study) directory consists of the following subdirectories:

- [Notebook](#notebooks)
- [Scripts](#scripts)


#### Notebooks
The purpose of the [notebooks](/case_study/notebooks) directory is to illustrate how to utilize the CaCS database to analyze the current state of the computer-assisted chemical synthesis data.


#### Scripts
The purpose of the [scripts](/case_study/scripts) directory is to illustrate how to download, extract, and format the relevant data and subsequently construct, manage, and query the CaCS database.
First, the [a_download_extract_and_format_data](/case_study/scripts/a_download_extract_and_format_data.py) script can be utilized as follows:

```shell
# Get the chemical reaction data source name information.
python case_study/scripts/a_download_extract_and_format_data.py \
  --data_source_category "reaction" \
  --get_data_source_name_information
```

```shell
# Get the USPTO chemical reaction dataset version information.
python case_study/scripts/a_download_extract_and_format_data.py \
  --data_source_category "reaction" \
  --data_source_name "uspto" \
  --get_data_source_version_information
```

```shell
# Download, extract, and format the data from the USPTO chemical reaction dataset.
python case_study/scripts/a_download_extract_and_format_data.py \
  --data_source_category "reaction" \
  --data_source_name "uspto" \
  --data_source_version "v_50k_by_20171116_coley_c_w_et_al" \
  --output_directory_path "/path/to/the/output/directory"
```

The full list of script arguments is as follows:
- `--data_source_category` or `-dsc` → The category of the data source. (_i.e._, compound, compound_pattern, reaction, or reaction_pattern)
- `--get_data_source_name_information` or `-gdsni` → The indicator of whether to get the data source name information.
- `--data_source_name` or `-dsn` → The name of the data source. (_i.e._, chembl, crd, miscellaneous, ord, rdkit, retro_rules, rhea, uspto, or zinc)
- `--get_data_source_version_information` or `-gdsvi` → The indicator of whether to get the data source version information.
- `--data_source_version` or `-dsv` → The version of the data source.
- `--output_directory_path` or `-odp` → The path to the output directory where the data should be downloaded, extracted, and formatted.
- `--number_of_processes` or `-nop` → The number of processes, if relevant.

Next, the [b_insert_archive_data](/case_study/scripts/b_insert_archive_data.py) script can be utilized as follows:

```shell
python use_case/scripts/b_insert_archive_data.py \
  --sqlite_database_file_path "sqlite:////path/to/the/cacs_db.sqlite" \
  --input_csv_file_path "/path/to/the/uspto_v_50k_by_20171116_coley_c_w_et_al.csv" \
  --smiles_or_smarts_column_name "rxn_smiles" \
  --file_name_column_name "file_name" \
  --data_source_category "reaction" \
  --data_source_name "uspto" \
  --data_source_version "v_50k_by_20171116_coley_c_w_et_al"
```

The full list of script arguments is as follows:
- `--sqlite_database_file_path` or `-sdfp` → The path to the SQLite database file.
- `--input_csv_file_path` or `-icfp` → The path to the input .csv file.
- `--smiles_or_smarts_column_name` or `-soscn` → The name of the SMILES or SMARTS string column.
- `--file_name_column_name` or `-fncn` → The name of the file name column.
- `--data_source_category` or `-dsc` → The category of the data source.
- `--data_source_name` or `-dsn` → The name of the data source.
- `--data_source_version` or `-dsv` → The version of the data source.
- `--database_user` or `-du` → The user of the database.
- `--database_chunk_limit` or `-dcl` → The chunk limit of the database.

Next, the [c_migrate_archive_to_workbench_data](/case_study/scripts/c_migrate_archive_to_workbench_data.py) script can be utilized as follows:

```shell
python use_case/scripts/c_migrate_archive_to_workbench_data.py \
  --sqlite_database_file_path "sqlite:////path/to/the/cacs_db.sqlite" \
  --data_source_category "reaction"
```

The full list of script arguments is as follows:
- `--sqlite_database_file_path` or `-sdfp` → The path to the SQLite database file.
- `--data_source_category` or `-dsc` → The category of the data source.
- `--database_user` or `-du` → The user of the database.
- `--database_chunk_limit` or `-dcl` → The chunk limit of the database.
- `--number_of_processes` or `-nop` → The number of processes, if relevant.
- `--batch_size` or `-bs` → The size of the batch, if relevant.

Ultimately, the [d_update_workbench_data](/case_study/scripts/d_update_workbench_data.py) script can be utilized as follows:

```shell
python use_case/scripts/d_update_workbench_data.py \
  --sqlite_database_file_path "sqlite:////path/to/the/cacs_db.sqlite"
```

The full list of script arguments is as follows:
- `--sqlite_database_file_path` or `-sdfp` → The path to the SQLite database file.
- `--database_user` or `-du` → The user of the database.
- `--database_chunk_limit` or `-dcl` → The chunk limit of the database.
- `--number_of_processes` or `-nop` → The number of processes, if relevant.


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to the individual references for more details regarding the license information of external resources utilized within the repository.


## Contact
If you are interested in contributing to this research project by submitting bugs, questions, and feedback or contributing to the code and data, please refer to the [contribution guidelines](CONTRIBUTING.md).
