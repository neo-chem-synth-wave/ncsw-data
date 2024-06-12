# NeoChemSynthWave: Data
![Static Badge](https://img.shields.io/badge/ncsw__chemistry-v.2024.06.1-%23ED9B33?logo=github&style=flat)
![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)
![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)

Over the last decade, computer-assisted chemical synthesis has re-emerged as a heavily researched subject in
Chemoinformatics. Even though the idea of utilizing computers for chemical synthesis has existed for as long as
computers themselves, the high level of reliability and innovation expected of such approaches has been repeatedly
proven difficult to achieve. In recent years, however, utilizing machine learning has proven particularly promising,
with novel approaches emerging frequently. Unfortunately, the necessary data is of poor quality and quantity, stored in
various formats, or published behind a paywall, which can be a significant barrier to entry for researchers. The main
objective of the **NeoChemSynthWave: Data** project is to alleviate this barrier by systematically curating and
facilitating access to open-source computer-assisted chemical synthesis data sources through a comprehensive and
easy-to-understand Python package titled [ncsw_data](/ncsw_data).


## Installation
A virtual environment containing the [ncsw_data](/ncsw_data) package can be set up using
[conda](https://docs.conda.io/en/latest) and [pip](https://pip.pypa.io/en/stable) as follows:

```shell
conda env create -f environment.yaml

conda activate ncsw-data

pip install --no-build-isolation -e .
```

## Supported Data Sources
### Chemical Reactions
Currently, the [`ncsw_data`](/ncsw_data) package supports the following open-source chemical reaction data sources:

1. [Chemical Reaction Database](#chemical-reaction-database)
2. [Open Reaction Database](#open-reaction-database)
3. [RDB7 Dataset](#rdb7-dataset)
4. [Rhea Database](#rhea-database)
5. [United States Patent and Trademark Office Dataset](#united-states-patent-and-trademark-office-dataset)
6. [Miscellaneous Data Sources](#miscellaneous-data-sources)


### Chemical Reaction Database
The **Chemical Reaction Database (CRD)** [<sup>[1]</sup>](#References) is a collection of chemical reactions from
scientific and patent literature. Currently, the following versions are supported:

| Version                        | DOI                                             |
|--------------------------------|-------------------------------------------------|
| v_reaction_smiles_2001_to_2021 | https://doi.org/10.6084/m9.figshare.20279733.v1 |
| v_reaction_smiles_2001_to_2023 | https://doi.org/10.6084/m9.figshare.22491730.v1 |
| v_reaction_smiles_2023         | https://doi.org/10.6084/m9.figshare.24921555.v1 |


### Open Reaction Database
The **Open Reaction Database (ORD)** [<sup>[2]</sup>](#References) is an open-source chemical reaction database designed
to support machine learning and related efforts in chemical reaction prediction, chemical synthesis planning, and
experiment design. Currently, the following versions are supported:

| Version           | DOI                                  |
|-------------------|--------------------------------------|
| v_release_v_0_1_0 | https://doi.org/10.1021/jacs.1c09820 |
| v_main            | https://doi.org/10.1021/jacs.1c09820 |


### RDB7 Dataset
The **RDB7 Dataset** [<sup>[3]</sup>](#References)[<sup>[4]</sup>](#References) is an open-source dataset of diverse
chemical reactions generated using Q-Chem whose transition states contain up to seven heavy atoms. Currently, the
following versions are supported:

| Version                                   | DOI                                    |
|-------------------------------------------|----------------------------------------|
| v_20200508_grambow_c_et_al_v_1_0_0        | https://doi.org/10.5281/zenodo.3581267 |
| v_20200508_grambow_c_et_al_v_1_0_1        | https://doi.org/10.5281/zenodo.3715478 |
| v_20200508_grambow_c_et_al_add_on_v_1_0_0 | https://doi.org/10.5281/zenodo.3731554 |
| v_20220718_spiekermann_k_et_al_v_1_0_0    | https://doi.org/10.5281/zenodo.5652098 |
| v_20220718_spiekermann_k_et_al_v_1_0_1    | https://doi.org/10.5281/zenodo.6618262 |


### Rhea Database
The **Rhea Database** [<sup>[5]</sup>](#References) is an open-source expert-curated knowledgebase of chemical and
transport reactions of biological interest. Currently, the following versions are supported:

| Version              | DOI                                      |
|----------------------|------------------------------------------|
| v_release_{ >= 126 } | https://doi.org/10.1021/acs.jcim.0c00675 |


### United States Patent and Trademark Office Dataset
The **United States Patent and Trademark Office (USPTO) Dataset** [<sup>[6]</sup>](#References) is an open-source
chemical reaction dataset constructed by text-mining patent grant and application documents. Currently, the following
versions are supported:

| Version                                     | DOI                                             |
|---------------------------------------------|-------------------------------------------------|
| v_1976_to_2013_by_20121009_lowe_d_m         | https://doi.org/10.6084/m9.figshare.12084729.v1 |
| v_50k_by_20161122_schneider_n_et_al         | https://doi.org/10.1021/acs.jcim.6b00564        |
| v_15k_by_20170418_coley_c_w_et_al           | https://doi.org/10.1021/acscentsci.7b00064      |
| v_1976_to_2016_by_20121009_lowe_d_m         | https://doi.org/10.6084/m9.figshare.5104873.v1  |
| v_50k_by_20171116_coley_c_w_et_al           | https://doi.org/10.1021/acscentsci.7b00355      |
| v_480k_or_mit_by_20171229_jin_w_et_al       | https://doi.org/10.48550/arXiv.1709.04555       |
| v_480k_or_mit_by_20180622_schwaller_p_et_al | https://doi.org/10.1039/C8SC02339E              |
| v_stereo_by_20180622_schwaller_p_et_al      | https://doi.org/10.1039/C8SC02339E              |
| v_1k_tpl_by_20210705_schwaller_p_et_al      | https://doi.org/10.1038/s42256-020-00284-w      |


### Miscellaneous Data Sources
Currently, the following miscellaneous data sources are supported:

| Data Source              | DOI                                        |
|--------------------------|--------------------------------------------|
| v_20131008_kraut_h_et_al | https://doi.org/10.1021/ci400442f          |
| v_20161014_wei_j_n_et_al | https://doi.org/10.1021/acscentsci.6b00219 |


## What's Next?
The following is planned for the [ncsw_data](/ncsw_data) package version **v.2024.07**:

- [ ] Complete the development of the [storage](/ncsw_data/storage) sub-package.
- [ ] Set up a [documentation](/documentation) directory.
- [ ] Set up a [notebooks](/notebooks) directory.
- [ ] Set up a [scripts](/scripts) directory.
- [ ] Set up a [tests](/tests) directory.
- [ ] Publish the package on [PyPI](https://pypi.org).


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to individual
[references](#references) for more details regarding the license information of external resources utilized within this 
repository.


## Contact
If you are interested in contributing to this repository by reporting bugs, suggesting improvements, or submitting
feedback, feel free to use [GitHub Issues](https://github.com/neo-chem-synth-wave/ncsw-data/issues).


## References
<sup>**[1]**</sup> **The Chemical Reaction Database (CRD)**: https://kmt.vander-lingen.nl. Accessed on: June 1st, 2024.
<br>
<sup>**[2]**</sup> Kearnes, S.M., Maser, M.R., Wleklinski, M., Kast, A., Doyle, A.G., Dreher, S.D., Hawkins, J.M.,
Jensen, K.F., and Coley, C.W. **The Open Reaction Database**. _J. Am. Chem. Soc._, 2021, 143, 45, 18820–18826.
DOI: https://doi.org/10.1021/jacs.1c09820.
<br>
<sup>**[3]**</sup> Grambow, C.A., Pattanaik, L., and Green, W.H. **Reactants, Products, and Transition States of
Elementary Chemical Reactions based on Quantum Chemistry**. _Sci. Data_, 7, 137, 2020.
DOI: https://doi.org/10.1038/s41597-020-0460-4.
<br>
<sup>**[4]**</sup> Spiekermann, K., Pattanaik, L., and Green, W.H. **Fast Predictions of Reaction Barrier Heights:
Toward Coupled-cluster Accuracy**. _Sci. Data_, 9, 417, 2022. DOI: https://doi.org/10.1038/s41597-022-01529-6.
<br>
<sup>**[5]**</sup> Bansal, P., Morgat, A., Axelsen, K.B., Muthukrishnan, V., Coudert, E., Aimo, L., Hyka-Nouspikel, N.,
Gasteiger, E., Kerhornou, A., Neto, T.B., Pozzato, M., Blatter, M., Ignatchenko, A., Redaschi, N., and Bridge, A.
**Rhea, the Reaction Knowledgebase in 2022**, _Nucleic Acids Research_, 50, D1, 2022, D693–D700.
DOI: https://doi.org/10.1093/nar/gkab1016.
<br>
<sup>**[6]**</sup> Lowe, D.M. **Extraction of Chemical Structures and Reactions from the Literature**. _Ph.D. Thesis,
University of Cambridge, Department of Chemistry, Pembroke College_, 2012. DOI: https://doi.org/10.17863/CAM.16293.
<br>
<sup>**[7]**</sup> Kraut, H., Eiblmaier, J., Grethe, G., Löw, P., Matuszczyk, H., and Saller, H. **Algorithm for
Reaction Classification**, _J. Chem. Inf. Model._, 2013, 53, 11, 2884–2895. DOI: https://doi.org/10.1021/ci400442f.
<sup>**[8]**</sup> Wei, J.N., Duvenaud, D., and Aspuru-Guzik, A. **Neural Networks for the Prediction of Organic
Chemistry Reactions**, _ACS Cent. Sci._, 2016, 2, 10, 725–732. DOI: https://doi.org/10.1021/acscentsci.6b00219.
