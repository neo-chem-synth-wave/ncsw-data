""" The ``ncsw_data.source.reaction.uspto.utility`` package ``download`` module. """

from os import PathLike
from typing import Union

from ncsw_data.source.base.utility.download import BaseDataSourceDownloadUtility


class USPTOReactionDatasetDownloadUtility:
    """
    The `United States Patent and Trademark Office (USPTO) <https://www.repository.cam.ac.uk/handle/1810/244727>`_
    chemical reaction dataset download utility class.
    """

    @staticmethod
    def download_v_1976_to_2016_by_20121009_lowe_d_m(
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from a `v_1976_to_2016_*_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if version == "v_1976_to_2016_cml_by_20121009_lowe_d_m":
            file_url_suffixes_and_names = [
                ("files/8664364", "1976_Sep2016_USPTOgrants_cml.7z", ),
                ("files/8664367", "2001_Sep2016_USPTOapplications_cml.7z", ),
            ]

        elif version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
            file_url_suffixes_and_names = [
                ("files/8664379", "1976_Sep2016_USPTOgrants_smiles.7z", ),
                ("files/8664370", "2001_Sep2016_USPTOapplications_smiles.7z", ),
            ]

        else:
            file_url_suffixes_and_names = [
                ("articles/5104873/versions/1", "5104873.zip", ),
            ]

        for file_url_suffix, file_name in file_url_suffixes_and_names:
            BaseDataSourceDownloadUtility.download_file(
                file_url="https://figshare.com/ndownloader/{file_url_suffix:s}".format(
                    file_url_suffix=file_url_suffix
                ),
                file_name=file_name,
                output_directory_path=output_directory_path
            )
