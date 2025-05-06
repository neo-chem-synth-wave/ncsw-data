""" The ``ncsw_data.source.reaction_pattern.retro_rules.utility`` package ``formatting`` module. """

from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Union

from pandas import read_csv


class RetroRulesReactionPatternDatabaseFormattingUtility:
    """ The `RetroRules <https://retrorules.org>`_ chemical reaction pattern database formatting utility class. """

    @staticmethod
    def format_v_release(
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from a `v_release_*` version of the database.

        :parameter version: The version of the database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if version == "v_release_rr01_rp2_hs":
            input_file_name = "retrorules_rr01_rp2_flat_all.csv"
            column_name = "File name"

        elif version == "v_release_rr02_rp2_hs":
            input_file_name = "retrorules_rr02_rp2_flat_all.csv"
            column_name = "File name"

        elif version in [
            "v_release_rr02_rp3_hs",
            "v_release_rr02_rp3_nohs",
        ]:
            input_file_name = "retrorules_rr02_flat_all.tsv"
            column_name = "File_name"

        else:
            raise ValueError(
                "The formatting of the data from the {data_source:s} is not supported.".format(
                    data_source="RetroRules chemical reaction pattern database ({version:s})".format(
                        version=version
                    )
                )
            )

        output_file_name = "{timestamp:s}_retro_rules_{version:s}.csv".format(
            timestamp=datetime.now().strftime(
                format="%Y%m%d%H%M%S"
            ),
            version=version
        )

        dataframe = read_csv(
            filepath_or_buffer=Path(input_directory_path, input_file_name),
            sep="\t" if input_file_name.endswith(".tsv") else ",",
            header=0
        )

        dataframe[column_name] = input_file_name

        dataframe.to_csv(
            path_or_buf=Path(output_directory_path, output_file_name),
            index=False
        )
