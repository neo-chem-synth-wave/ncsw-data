""" The ``ncsw_data.source.reaction.uspto.utility`` package ``formatting`` module. """

from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Union

from pandas.core.reshape.concat import concat
from pandas.io.parsers.readers import read_csv


class USPTOReactionDatasetFormattingUtility:
    """
    The `United States Patent and Trademark Office (USPTO) <https://www.repository.cam.ac.uk/handle/1810/244727>`_
    chemical reaction dataset formatting utility class.
    """

    @staticmethod
    def format_v_1976_to_2016_by_20121009_lowe_d_m(
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from a `v_1976_to_2016_*_by_20121009_lowe_d_m` version of the dataset.

        :parameter version: The version of the dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
            input_file_names = [
                "1976_Sep2016_USPTOgrants_smiles.rsmi",
                "2001_Sep2016_USPTOapplications_smiles.rsmi",
            ]

            dataframes = list()

            for input_file_name in input_file_names:
                dataframe = read_csv(
                    filepath_or_buffer=Path(input_directory_path, input_file_name),
                    sep="\t",
                    header=0,
                    low_memory=False
                )

                dataframe["FileName"] = input_file_name

                dataframes.append(
                    dataframe
                )

            dataframe = concat(
                objs=dataframes
            )

        else:
            raise ValueError(
                "The formatting of the data from the {data_source:s} is not supported.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        output_file_name = "{timestamp:s}_uspto_{version:s}.csv".format(
            timestamp=datetime.now().strftime(
                format="%Y%m%d%H%M%S"
            ),
            version=version
        )

        dataframe.to_csv(
            path_or_buf=Path(output_directory_path, output_file_name),
            index=False
        )

    @staticmethod
    def format_v_50k_by_20171116_coley_c_w_et_al(
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `v_50k_by_20171116_coley_c_w_et_al` version of the dataset.

        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        input_file_name = "data_processed.csv"

        output_file_name = "{timestamp:s}_uspto_v_50k_by_20171116_coley_c_w_et_al.csv".format(
            timestamp=datetime.now().strftime(
                format="%Y%m%d%H%M%S"
            )
        )

        dataframe = read_csv(
            filepath_or_buffer=Path(input_directory_path, input_file_name),
            header=0,
            index_col=0
        )

        dataframe["file_name"] = input_file_name

        dataframe.to_csv(
            path_or_buf=Path(output_directory_path, output_file_name),
            index=False
        )
