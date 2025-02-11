""" The ``ncsw_data.source.reaction.ord.utility`` package ``download`` module. """

from os import PathLike
from typing import Union

from ncsw_data.source.base.utility.download import DataSourceDownloadUtility


class OpenReactionDatabaseDownloadUtility:
    """ The `Open Reaction Database (ORD) <https://open-reaction-database.org>`_ download utility class. """

    @staticmethod
    def download_v_release(
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from a `v_release_*` version of the database.

        :parameter version: The version of the database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if version == "v_release_0_1_0":
            file_url = "https://github.com/open-reaction-database/ord-data/archive/refs/tags/v0.1.0.zip"
            file_name = "ord-data-0.1.0.zip"

        elif version == "v_release_main":
            file_url = "https://github.com/open-reaction-database/ord-data/archive/refs/heads/main.zip"
            file_name = "ord-data-main.zip"

        else:
            raise ValueError(
                "The download of the data from the {data_source:s} is not supported.".format(
                    data_source="Open Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

        DataSourceDownloadUtility.download_file(
            url=file_url,
            name=file_name,
            output_directory_path=output_directory_path
        )
