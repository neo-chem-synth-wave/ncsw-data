""" The ``ncsw_data.source.reaction.rhea`` package ``rhea`` module. """

from functools import lru_cache
from os import PathLike
from re import search
from typing import Dict, Union

from ncsw_data.source.base.base import DataSourceBase
from ncsw_data.source.base.utility.download import DataSourceDownloadUtility
from ncsw_data.source.reaction.rhea.utility.download import RheaReactionDatabaseDownloadUtility
from ncsw_data.source.reaction.rhea.utility.extraction import RheaReactionDatabaseExtractionUtility
from ncsw_data.source.reaction.rhea.utility.formatting import RheaReactionDatabaseFormattingUtility


class RheaReactionDatabase(DataSourceBase):
    """ The `Rhea <https://www.rhea-db.org>`_ chemical reaction database class. """

    @lru_cache(
        maxsize=None
    )
    def get_supported_versions(
            self
    ) -> Dict[str, str]:
        """
        Get the supported versions of the database.

        :returns: The supported versions of the database.
        """

        try:
            http_get_request_url = "https://ftp.expasy.org/databases/rhea/rhea-release.properties"

            http_get_request_response = DataSourceDownloadUtility.send_http_get_request(
                http_get_request_url=http_get_request_url
            )

            latest_release_number = int(
                search(
                    pattern=r"rhea\.release\.number=(\d+)",
                    string=http_get_request_response.text
                ).group(1)
            )

            return {
                "v_release_{release_number:d}".format(
                    release_number=release_number
                ): "https://doi.org/10.1093/nar/gkab1016"
                for release_number in range(126, latest_release_number + 1)
            }

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def download(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Download the data from the database.

        :parameter version: The version of the database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been started.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version.startswith("v_release"):
                    RheaReactionDatabaseDownloadUtility.download_v_release(
                        version=version,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been completed.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The download of the data from the {data_source:s} is not supported.".format(
                        data_source="Rhea chemical reaction database ({version:s})".format(
                            version=version
                        )
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def extract(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Extract the data from the database.

        :parameter version: The version of the database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been started.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version.startswith("v_release"):
                    RheaReactionDatabaseExtractionUtility.extract_v_release(
                        version=version,
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been completed.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The extraction of the data from the {data_source:s} is not supported.".format(
                        data_source="Rhea chemical reaction database ({version:s})".format(
                            version=version
                        )
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def format(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Format the data from the database.

        :parameter version: The version of the database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been started.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version.startswith("v_release"):
                    RheaReactionDatabaseFormattingUtility.format_v_release(
                        version=version,
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been completed.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The formatting of the data from the {data_source:s} is not supported.".format(
                        data_source="Rhea chemical reaction database ({version:s})".format(
                            version=version
                        )
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise
