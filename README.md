# NeoChemSynthWave: Data
![Static Badge](https://img.shields.io/badge/ncsw__chemistry-v.2024.06.1-%23ED9B33?logo=github&style=flat)
![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)
![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)

Over the last decade, computer-assisted chemical synthesis has re-emerged as a heavily researched subject in
Chemoinformatics. Even though the idea of utilizing computers for chemical synthesis has existed for as long as
computers themselves, the high level of reliability and innovation expected of such approaches has been repeatedly
proven difficult to achieve. In recent years, however, utilizing machine learning has proven particularly promising,
with novel approaches emerging frequently.

Unfortunately, the available open-source computer-assisted chemical synthesis data are lacking in quality and quantity,
stored in various formats, or published behind a paywall, all of which can represent significant barriers to entry,
especially for novice researchers. The main objective of the **NeoChemSynthWave: Data** project is to lower such
barriers to entry by systematically curating and facilitating access to relevant data sources.


## Installation
A minimal virtual environment can be created using [Conda](https://docs.conda.io/en/latest) as follows:

```shell
conda env create -f environment.yaml

conda activate ncsw-data
```

The package can be locally installed using [pip](https://pip.pypa.io/en/stable) as follows:

```shell
pip install --no-build-isolation -e .
```


## Data Sources
The following types of computer-assisted chemical synthesis data are currently supported:

1. [Chemical Compounds](#chemical-compounds)
2. [Chemical Reactions](#chemical-reactions)
3. [Chemical Reaction Rules](#chemical-reaction-rules)


### Chemical Compounds
The following chemical compound data sources are currently supported:

1. [ChEMBL](#chembl)
2. [ZINC20](#zinc20)


#### ChEMBL
The **ChEMBL <sup>[[1]](#References)</sup>** database is a manually curated collection of bioactive chemical compounds
with drug-like properties that brings together chemical, bioactivity, and genomic data to aid the translation of genomic
information into effective new drugs. The following versions are currently supported:

|                                                            Version                                                            | DOI                                                        |
|:-----------------------------------------------------------------------------------------------------------------------------:|------------------------------------------------------------|
| v_release_[{release_number}](https://chembl.gitbook.io/chembl-interface-documentation/downloads#chembl-database-release-dois) | `https://doi.org/10.6019/CHEMBL.database.{release_number}` |
|                                                     _e.g._, v_release_34                                                      | _e.g._, `https://doi.org/10.6019/CHEMBL.database.34`       |


#### ZINC20
The **ZINC20 <sup>[[2]](#References)</sup>** database is a collection of commercially available chemical compounds for
virtual screening. The following versions are currently supported:

|                                Version                                 |                        DOI                         |
|:----------------------------------------------------------------------:|:--------------------------------------------------:|
| v_[{building_block_subset_name}](https://files.docking.org/bb/current) |     `https://doi.org/10.1021/acs.jcim.0c00675`     |
|                            _e.g._, v_bb_10                             | _e.g._, `https://doi.org/10.1021/acs.jcim.0c00675` |
|     v_[{catalog_name}](https://files.docking.org/catalogs/source)      |     `https://doi.org/10.1021/acs.jcim.0c00675`     |
|                            _e.g._, v_wuxi-v                            | _e.g._, `https://doi.org/10.1021/acs.jcim.0c00675` |


### Chemical Reactions
The following chemical reaction data sources are currently supported:

1. [United States Patent and Trademark Office (USPTO)](#united-states-patent-and-trademark-office-uspto)
2. [Open Reaction Database (ORD)](#open-reaction-database-ord)
3. [Chemical Reaction Database (CRD)](#chemical-reaction-database-crd)
4. [Rhea](#rhea)
5. [RDB7](#rdb7)
6. [Miscellaneous](#miscellaneous)


#### United States Patent and Trademark Office (USPTO)
The **United States Patent and Trademark Office (USPTO) <sup>[[3]](#References)</sup>** dataset is an open-source
collection of chemical reactions constructed by text-mining patent grant and application documents. The following
versions are currently supported:

|                    Version                    |                        DOI                         |
|:---------------------------------------------:|:--------------------------------------------------:|
|      v_1976_to_2013_by_20121009_lowe_d_m      | `https://doi.org/10.6084/m9.figshare.12084729.v1`  |
|      v_50k_by_20161122_schneider_n_et_al      |     `https://doi.org/10.1021/acs.jcim.6b00564`     |
|       v_15k_by_20170418_coley_c_w_et_al       |    `https://doi.org/10.1021/acscentsci.7b00064`    |
|      v_1976_to_2016_by_20121009_lowe_d_m      |  `https://doi.org/10.6084/m9.figshare.5104873.v1`  |
|       v_50k_by_20171116_coley_c_w_et_al       |    `https://doi.org/10.1021/acscentsci.7b00355`    |
|     v_480k_or_mit_by_20171229_jin_w_et_al     |    `https://doi.org/10.48550/arXiv.1709.04555`     |
|  v_480k_or_mit_by_20180622_schwaller_p_et_al  |        `https://doi.org/10.1039/C8SC02339E`        |
|    v_stereo_by_20180622_schwaller_p_et_al     |        `https://doi.org/10.1039/C8SC02339E`        |
|    v_1k_tpl_by_20210705_schwaller_p_et_al     |    `https://doi.org/10.1038/s42256-020-00284-w`    |


#### Open Reaction Database (ORD)
The **Open Reaction Database (ORD) <sup>[[4]](#References)</sup>** is an open-source collection of chemical reactions
designed to support machine learning and related efforts in chemical reaction prediction, chemical synthesis planning,
and experiment design. The following versions are currently supported:

|      Version      |                  DOI                   |
|:-----------------:|:--------------------------------------:|
| v_release_v_0_1_0 | `https://doi.org/10.1021/jacs.1c09820` |
|      v_main       | `https://doi.org/10.1021/jacs.1c09820` |


#### Chemical Reaction Database (CRD)
The **Chemical Reaction Database (CRD) <sup>[[5]](#References)</sup>** is a collection of chemical reactions from
scientific and patent literature. The following versions are currently supported:

|            Version             |                        DOI                        |
|:------------------------------:|:-------------------------------------------------:|
| v_reaction_smiles_2001_to_2021 | `https://doi.org/10.6084/m9.figshare.20279733.v1` |
| v_reaction_smiles_2001_to_2023 | `https://doi.org/10.6084/m9.figshare.22491730.v1` |
|     v_reaction_smiles_2023     | `https://doi.org/10.6084/m9.figshare.24921555.v1` |


#### Rhea
The **Rhea <sup>[[6]](#References)</sup>** database is an open-source expert-curated knowledgebase of chemical and
transport reactions of biological interest. The following versions are currently supported:

|                                      Version                                       |                        DOI                         |
|:----------------------------------------------------------------------------------:|:--------------------------------------------------:|
| v_release_[{release_number}](https://ftp.expasy.org/databases/rhea/old%5Freleases) |     `https://doi.org/10.1021/acs.jcim.0c00675`     |
|                               _e.g._, v_release_133                                | _e.g._, `https://doi.org/10.1021/acs.jcim.0c00675` |


#### RDB7
The **RDB7 <sup>[[7]](#References)[[8]](#References)</sup>** dataset is an open-source collection of diverse chemical
reactions whose transition states contain up to seven heavy atoms. The following versions are currently supported:

|                  Version                  |                   DOI                    |
|:-----------------------------------------:|:----------------------------------------:|
|    v_20200508_grambow_c_et_al_v_1_0_0     | `https://doi.org/10.5281/zenodo.3581267` |
|    v_20200508_grambow_c_et_al_v_1_0_1     | `https://doi.org/10.5281/zenodo.3715478` |
| v_20200508_grambow_c_et_al_add_on_v_1_0_0 | `https://doi.org/10.5281/zenodo.3731554` |
|  v_20220718_spiekermann_k_et_al_v_1_0_0   | `https://doi.org/10.5281/zenodo.5652098` |
|  v_20220718_spiekermann_k_et_al_v_1_0_1   | `https://doi.org/10.5281/zenodo.6618262` |


#### Miscellaneous
The following miscellaneous chemical reaction data sources are currently supported:

|       Data Source        |                     DOI                      |
|:------------------------:|:--------------------------------------------:|
| v_20131008_kraut_h_et_al |     `https://doi.org/10.1021/ci400442f`      |
| v_20161014_wei_j_n_et_al | `https://doi.org/10.1021/acscentsci.6b00219` |


### Chemical Reaction Rules
The following chemical reaction rule data sources are currently supported:

1. [RetroRules](#retrorules)
2. [Miscellaneous](#miscellaneous-1)


#### RetroRules
The **RetroRules <sup>[[9]](#References)</sup>** database is an open-source collection of chemical reaction rules for
metabolic pathway discovery and metabolic engineering. The following versions are currently supported:

|         Version         |                   DOI                    |
|:-----------------------:|:----------------------------------------:|
|  v_release_rr01_rp2_hs  | `https://doi.org/10.5281/zenodo.5827427` |
|  v_release_rr02_rp2_hs  | `https://doi.org/10.5281/zenodo.5828017` |
|  v_release_rr02_rp3_hs  | `https://doi.org/10.5281/zenodo.5827977` |
| v_release_rr02_rp3_nohs | `https://doi.org/10.5281/zenodo.5827969` |


#### Miscellaneous
The following miscellaneous chemical reaction rule data sources are currently supported:

|         Data Source         |                   DOI                    |
|:---------------------------:|:----------------------------------------:|
| v_20180421_avramova_s_et_al | `https://doi.org/10.5281/zenodo.1209313` |


## What's Next?
The following updates are currently planned for version **v.2024.07**:

- [ ] Complete the development of the _/ncsw_data/storage_ sub-package.
- [ ] Create the _/documentation_ directory.
- [ ] Create the _/notebooks_ directory.
- [ ] Create the _/scripts_ directory.
- [ ] Create the _/tests_ directory.
- [ ] Publish the package on [PyPI](https://pypi.org).


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to individual
[references](#references) for more details regarding the license information of external resources utilized within this 
repository.


## Contact
If you are interested in contributing to this repository by reporting bugs, suggesting improvements, or submitting
feedback, feel free to use [GitHub Issues](https://github.com/neo-chem-synth-wave/ncsw-data/issues).


## References
**[[1]](https://doi.org/10.1093/nar/gkad1004)** Zdrazil, B., Felix, E., Hunter, F., Manners, E.J., Blackshaw, J.,
Corbett, S., de Veij, M., Ioannidis, H., Lopez, D.M., Mosquera, J.F., Magarinos, M.P., Bosc, N., Arcila, R.,
Kizilören, T., Gaulton, A., Bento, A.P., Adasme, M.F., Monecke, P., Landrum, G.A., and Leach, A.R. **The ChEMBL Database
in 2023: A Drug Discovery Platform Spanning Multiple Bioactivity Data Types and Time Periods**,
_Nucleic Acids Research_, 52, D1, 2024, D1180-D1192.

**[[2]](https://doi.org/10.1021/acs.jcim.0c00675)** Irwin, J.J., Tang, K.G., Young, J., Dandarchuluun, C., Wong, B.R.,
Khurelbaatar, M., Moroz, Y.S., Mayfield, J., and Sayle, R.A. **ZINC20 - A Free Ultralarge-Scale Chemical Database for
Ligand Discovery**. _J. Chem. Inf. Model._, 2020, 60, 12, 6065-6073.

**[[3]](https://doi.org/10.17863/CAM.16293)** Lowe, D.M. **Extraction of Chemical Structures and Reactions from the
Literature**. _Ph.D. Thesis, University of Cambridge, Department of Chemistry, Pembroke College_, 2012.

**[[4]](https://doi.org/10.1021/jacs.1c09820)** Kearnes, S.M., Maser, M.R., Wleklinski, M., Kast, A., Doyle, A.G.,
Dreher, S.D., Hawkins, J.M., Jensen, K.F., and Coley, C.W. **The Open Reaction Database**. _J. Am. Chem. Soc._, 2021,
143, 45, 18820–18826.

**[[5]](https://kmt.vander-lingen.nl)** **The Chemical Reaction Database (CRD)**: https://kmt.vander-lingen.nl. Accessed
on: June 1st, 2024.

**[[6]](https://doi.org/10.1093/nar/gkab1016)** Bansal, P., Morgat, A., Axelsen, K.B., Muthukrishnan, V., Coudert, E.,
Aimo, L., Hyka-Nouspikel, N., Gasteiger, E., Kerhornou, A., Neto, T.B., Pozzato, M., Blatter, M., Ignatchenko, A.,
Redaschi, N., and Bridge, A. **Rhea, the Reaction Knowledgebase in 2022**, _Nucleic Acids Research_, 50, D1, 2022,
D693–D700.

**[[7]](https://doi.org/10.1038/s41597-020-0460-4)** Grambow, C.A., Pattanaik, L., and Green, W.H. **Reactants,
Products, and Transition States of Elementary Chemical Reactions based on Quantum Chemistry**. _Sci. Data_, 7,
137, 2020.

**[[8]](https://doi.org/10.1038/s41597-022-01529-6)** Spiekermann, K., Pattanaik, L., and Green, W.H. **Fast Predictions
of Reaction Barrier Heights: Toward Coupled-cluster Accuracy**. _Sci. Data_, 9, 417, 2022.

**[[9]](https://doi.org/10.1093/nar/gky940)** Duigou, T., du Lac, M., Carbonell, P., and Faulon, J. **RetroRules: A
Database of Reaction Rules for Engineering Biology**. _Nucleic Acids Research_, 47, D1, 2018, D1229–D1235.
