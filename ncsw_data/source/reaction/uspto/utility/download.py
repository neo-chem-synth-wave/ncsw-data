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
        Download the data from a `v_1976_to_2016_*_by_20121009_lowe_d_m` version of the dataset.

        :parameter version: The version of the dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
            file_urls_and_names = [
                (
                    "https://figshare.com/ndownloader/files/8664379",
                    "1976_Sep2016_USPTOgrants_smiles.7z",
                ),
                (
                    "https://figshare.com/ndownloader/files/8664370",
                    "2001_Sep2016_USPTOapplications_smiles.7z",
                ),
            ]

        else:
            raise ValueError(
                "The download of the data from the {data_source:s} is not supported.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        for file_url, file_name in file_urls_and_names:
            BaseDataSourceDownloadUtility.download_file(
                file_url=file_url,
                file_name=file_name,
                output_directory_path=output_directory_path
            )

    @staticmethod
    def download_v_50k_by_20171116_coley_c_w_et_al(
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `v_50k_by_20171116_coley_c_w_et_al` version of the dataset.

        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        file_url = "https://raw.githubusercontent.com/connorcoley/retrosim/master/retrosim/data/data_processed.csv"

        BaseDataSourceDownloadUtility.download_file(
            file_url=file_url,
            file_name=file_url.split(
                sep="/"
            )[-1],
            output_directory_path=output_directory_path
        )
