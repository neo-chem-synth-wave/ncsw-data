""" The ``ncsw_data.source.reaction.rhea`` package ``rhea`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from re import search
from typing import Dict, Optional, Union

from pandas.io.parsers.readers import read_csv

from tarfile import open as open_tar_archive_file

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class RheaReactionDatabase(AbstractBaseDataSource):
    """ The `Rhea <https://www.rhea-db.org>`_ chemical reaction database class. """

    def __init__(
            self,
            logger: Optional[Logger] = None
    ) -> None:
        """
        The constructor method of the class.

        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        """

        super().__init__(
            logger=logger
        )

    @property
    def available_versions(
            self
    ) -> Dict[str, Dict[str, str]]:
        """
        Get the available versions of the chemical reaction database.

        :returns: The available versions of the chemical reaction database.
        """

        try:
            available_versions = {
                "ftp": dict(),
            }

            http_get_request_response = self._send_http_get_request(
                http_get_request_url="https://ftp.expasy.org/databases/rhea/rhea-release.properties"
            )

            latest_release_number = int(
                search(
                    pattern=r"rhea\.release\.number=(\d+)",
                    string=str(http_get_request_response.content)
                ).group(1)
            )

            for release_number in range(126, latest_release_number + 1):
                available_versions["ftp"][
                    "v_release_{release_number:d}".format(
                        release_number=release_number
                    )
                ] = "https://doi.org/10.1021/acs.jcim.0c00675"

            return available_versions

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.exception(
                    msg=exception_handle
                )

            raise

    def _download_ftp(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `ftp` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="Rhea chemical reaction database ({version:s})".format(
                        version=version
                    )
                )
            )

        self._download_file(
            file_url="https://ftp.expasy.org/databases/rhea/old_releases/{release_number:s}.tar.bz2".format(
                release_number=version.split(
                    sep="_"
                )[-1]
            ),
            file_name="{release_number:s}.tar.bz2".format(
                release_number=version.split(
                    sep="_"
                )[-1]
            ),
            output_directory_path=output_directory_path
        )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="Rhea chemical reaction database ({version:s})".format(
                        version=version
                    )
                )
            )

    def download(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data.

        :parameter version: The version of the chemical reaction database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        try:
            if version in self.available_versions["ftp"].keys():
                self._download_ftp(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.exception(
                    msg=exception_handle
                )

            raise

    def _extract_ftp(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `ftp` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="Rhea chemical reaction database ({version:s})".format(
                        version=version
                    )
                )
            )

        with open_tar_archive_file(
            name=Path(
                input_directory_path,
                "{release_number:s}.tar.bz2".format(
                    release_number=version.split(
                        sep="_"
                    )[-1]
                )
            ),
            mode="r:bz2"
        ) as tar_archive_file_handle:
            tar_archive_file_handle.extractall(
                path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="Rhea chemical reaction database ({version:s})".format(
                        version=version
                    )
                )
            )

    def extract(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["ftp"].keys():
                self._extract_ftp(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.exception(
                    msg=exception_handle
                )

            raise

    def _format_ftp(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `ftp` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="Rhea chemical reaction database ({version:s})".format(
                        version=version
                    )
                )
            )

        read_csv(
            filepath_or_buffer=Path(
                input_directory_path,
                "{release_number:s}/tsv/rhea-reaction-smiles.tsv".format(
                    release_number=version.split(
                        sep="_"
                    )[-1]
                )
            ),
            sep="\t",
            header=None
        ).rename(
            columns={
                0: "id",
                1: "reaction_smiles",
            }
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_rhea_{version:s}.csv".format(
                    timestamp=datetime.now().strftime(
                        format="%Y%m%d%H%M%S"
                    ),
                    version=version
                )
            ),
            index=False
        )

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been successfully completed.".format(
                    data_source="Rhea chemical reaction database ({version:s})".format(
                        version=version
                    )
                )
            )

    def format(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        try:
            if version in self.available_versions["ftp"].keys():
                self._format_ftp(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Rhea chemical reaction database ({version:s})".format(
                                version=version
                            )
                        )
                    )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.exception(
                    msg=exception_handle
                )

            raise
