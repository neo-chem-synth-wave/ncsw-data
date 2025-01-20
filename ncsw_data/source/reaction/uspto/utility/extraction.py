""" The ``ncsw_data.source.reaction.uspto.utility`` package ``extraction`` module. """

from os import PathLike
from pathlib import Path
from typing import Union

from py7zr.py7zr import SevenZipFile


class USPTOReactionDatasetExtractionUtility:
    """
    The `United States Patent and Trademark Office (USPTO) <https://www.repository.cam.ac.uk/handle/1810/244727>`_
    chemical reaction dataset extraction utility class.
    """

    @staticmethod
    def extract_v_1976_to_2016_by_20121009_lowe_d_m(
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from a `v_1976_to_2016_*_by_20121009_lowe_d_m` version of the dataset.

        :parameter version: The version of the dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
            input_file_names = [
                "1976_Sep2016_USPTOgrants_smiles.7z",
                "2001_Sep2016_USPTOapplications_smiles.7z",
            ]

        else:
            raise ValueError(
                "The extraction of the data from the {data_source:s} is not supported.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        for input_file_name in input_file_names:
            with SevenZipFile(
                file=Path(input_directory_path, input_file_name)
            ) as seven_zip_archive_file_handle:
                seven_zip_archive_file_handle.extractall(
                    path=output_directory_path
                )
