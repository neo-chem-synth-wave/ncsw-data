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
facilitating access to open-source computer-assisted chemical synthesis data sources through a Python package titled
[ncsw_data](/ncsw_data).


## Installation
A virtual environment containing the [ncsw_data](/ncsw_data) package can be set up using
[conda](https://docs.conda.io/en/latest) and [pip](https://pip.pypa.io/en/stable) as follows:

```shell
conda env create -f environment.yaml

conda activate ncsw-data

pip install --no-build-isolation -e .
```


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
1. **RDKit: Open-source Cheminformatics**: https://www.rdkit.org. Accessed on: June 1st, 2024.
