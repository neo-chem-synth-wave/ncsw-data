""" The ``ncsw_data.source.compound.chembl`` package ``chembl`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from re import search
from shutil import copyfileobj
from typing import Dict, Optional, Union

from gzip import open as open_gz_archive_file

from pandas.io.parsers.readers import read_csv

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class ChEMBLCompoundDatabase(AbstractBaseDataSource):
    """ The `ChEMBL <https://www.ebi.ac.uk/chembl>`_ chemical compound database class. """

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
        Get the available versions of the chemical compound database.

        :returns: The available versions of the chemical compound database.
        """

        try:
            http_get_request_response = self._send_http_get_request(
                http_get_request_url="https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/README"
            )

            latest_release_number = int(
                search(
                    pattern=r"Release:\s*chembl_(\d+)",
                    string=str(http_get_request_response.content)
                ).group(1)
            )

            return {
                "ftp": {
                    "v_release_{release_number:d}".format(
                        release_number=release_number
                    ): "https://doi.org/10.6019/CHEMBL.database.{release_number:d}".format(
                        release_number=release_number
                    ) for release_number in range(25, latest_release_number + 1)
                }
            }

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
        Download the data from the `ftp` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="ChEMBL chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        self._download_file(
            file_url="https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/{file_url_suffix:s}".format(
                file_url_suffix="chembl_{release_number:s}/chembl_{release_number:s}_chemreps.txt.gz".format(
                    release_number=version.split(
                        sep="_"
                    )[-1]
                )
            ),
            file_name="chembl_{release_number:s}_chemreps.txt.gz".format(
                release_number=version.split(
                    sep="_"
                )[-1]
            ),
            output_directory_path=output_directory_path
        )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="ChEMBL chemical compound database ({version:s})".format(
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

        :parameter version: The version of the chemical compound database.
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
                            data_source="ChEMBL chemical compound database ({version:s})".format(
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
        Extract the data from the `ftp` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="ChEMBL chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        with open_gz_archive_file(
            filename=Path(
                input_directory_path,
                "chembl_{release_number:s}_chemreps.txt.gz".format(
                    release_number=version.split(
                        sep="_"
                    )[-1]
                )
            )
        ) as gz_archive_file_handle:
            with open(
                file=Path(
                    output_directory_path,
                    "chembl_{release_number:s}_chemreps.txt".format(
                        release_number=version.split(
                            sep="_"
                        )[-1]
                    )
                ),
                mode="wb"
            ) as file_handle:
                copyfileobj(
                    fsrc=gz_archive_file_handle,
                    fdst=file_handle
                )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="ChEMBL chemical compound database ({version:s})".format(
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

        :parameter version: The version of the chemical compound database.
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
                            data_source="ChEMBL chemical compound database ({version:s})".format(
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
        Format the data from the `ftp` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="ChEMBL chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        read_csv(
            filepath_or_buffer=Path(
                input_directory_path,
                "chembl_{release_number:s}_chemreps.txt".format(
                    release_number=version.split(
                        sep="_"
                    )[-1]
                )
            ),
            sep="\t",
            header=0
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_chembl_{version:s}.csv".format(
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
                    data_source="ChEMBL chemical compound database ({version:s})".format(
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

        :parameter version: The version of the chemical compound database.
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
                            data_source="ChEMBL chemical compound database ({version:s})".format(
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
