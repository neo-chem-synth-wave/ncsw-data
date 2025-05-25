# NeoChemSynthWave: Data
[![Static Badge](https://img.shields.io/badge/ncsw__data-2025.5.1-%23E68E36?logo=github&style=flat)](https://github.com/neo-chem-synth-wave/ncsw-data/releases/tag/2025.5.1)
[![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)](https://www.isct.ac.jp)
[![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)](https://www.elix-inc.com)

Welcome to the **NeoChemSynthWave: Data** project !!!

Over the past decade, computer-assisted chemical synthesis has re-emerged as a prominent research subject. Even though
the idea of utilizing computers to assist chemical synthesis has existed for nearly as long as computers themselves, the
inherent complexity repeatedly exceeded the available resources. However, recent machine learning approaches have
exhibited the potential to break this tendency. The performance of such approaches is dependent on data that frequently
suffer from limited quantity, quality, visibility, and accessibility, posing significant challenges to potential
scientific breakthroughs. Consequently, the primary objective of the **NeoChemSynthWave: Data** project is to provide
access to essential open computer-assisted chemical synthesis data.


## Installation
An environment can be created using the [git](https://git-scm.com) and [conda](https://conda.io) commands as follows:

```shell
git clone https://github.com/neo-chem-synth-wave/ncsw-data.git

cd ncsw-data

conda env create -f environment.yaml

conda activate ncsw-data-env
```

The [ncsw_data](/ncsw_data) package can be installed using the [pip](https://pip.pypa.io) command as follows:

```shell
pip install .
```


## Utilization
The purpose of the [case_study](/case_study) directory is to illustrate how to download, extract, and format the
preferred data and subsequently construct, manage, and query a version of the Computer-assisted Chemical Synthesis
(CaCS) database that reflects the current state of computer-assisted chemical synthesis data.

First, the [a_download_extract_and_format_data](/case_study/scripts/a_download_extract_and_format_data.py) script can be
utilized as follows:

```shell
python use_case/scripts/a_download_extract_and_format_data.py \
  --data_source_category "reaction" \
  --data_source_name "uspto" \
  --data_source_version "v_50k_by_20171116_coley_c_w_et_al" \
  --output_directory_path "/path/to/the/output/directory"
```

Next, the [b_insert_archive_data](/case_study/scripts/b_insert_archive_data.py) script can be utilized as follows:

```shell
python use_case/scripts/b_insert_archive_data.py \
  --sqlite_database_file_path "sqlite:////path/to/the/cacs_db.sqlite" \
  --input_csv_file_path "/path/to/the/input_csv_file.csv" \
  --smiles_or_smarts_column_name "reaction_smiles" \
  --file_name_column_name "file_name" \
  --data_source_category "reaction" \
  --data_source_name "uspto" \
  --data_source_version "v_50k_by_20171116_coley_c_w_et_al"
```

Next, the [c_migrate_archive_to_workbench_data](/case_study/scripts/c_migrate_archive_to_workbench_data.py) script can
be utilized as follows:

```shell
python use_case/scripts/c_migrate_archive_to_workbench_data.py \
  --sqlite_database_file_path "sqlite:////path/to/the/cacs_db.sqlite" \
  --data_source_category "reaction"
```

Ultimately, the [d_update_workbench_data](/case_study/scripts/d_update_workbench_data.py) script can be utilized as
follows:

```shell
python use_case/scripts/d_update_workbench_data.py \
  --sqlite_database_file_path "sqlite:////path/to/the/cacs_db.sqlite"
```

The relevant [SQLite](https://www.sqlite.org) scripts and [Jupyter](https://jupyter.org) notebooks of the case study
illustrating the utilization of the CaCS database can be found in the [notebooks](/case_study/notebooks) directory.


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to the individual
references for more details regarding the license information of external resources utilized within the repository.


## Contact
If you are interested in contributing to this research project by reporting bugs, suggesting improvements, or submitting
feedback, feel free to do so using [GitHub Issues](https://github.com/neo-chem-synth-wave/ncsw-data/issues).
