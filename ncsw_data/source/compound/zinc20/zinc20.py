""" The ``ncsw_data.source.compound.zinc20`` package ``zinc20`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from re import findall
from shutil import copyfileobj
from typing import Dict, Optional, Union

from gzip import open as open_gz_archive_file

from pandas.io.parsers.readers import read_csv

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class ZINC20CompoundDatabase(AbstractBaseDataSource):
    """ The `ZINC20 <https://zinc20.docking.org>`_ chemical compound database class. """

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

        available_versions = {
            "building_blocks": dict(),
            "catalogs": dict()
        }

        for file_name in findall(
            pattern=r"href=\"([^\.]+)\.smi\.gz",
            string=self._send_http_get_request(
                http_get_request_url="https://files.docking.org/bb/current"
            ).text
        ):
            available_versions["building_blocks"][
                "v_{file_name:s}".format(
                    file_name=file_name
                )
            ] = "https://doi.org/10.1021/acs.jcim.0c00675"

        for file_name in findall(
            pattern=r"href=\"([^\.]+)\.src\.txt",
            string=self._send_http_get_request(
                http_get_request_url="https://files.docking.org/catalogs/source"
            ).text
        ):
            available_versions["catalogs"][
                "v_{file_name:s}".format(
                    file_name=file_name
                )
            ] = "https://doi.org/10.1021/acs.jcim.0c00675"

        return available_versions

    def _download_building_blocks(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `building_blocks` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        self._download_file(
            file_url="https://files.docking.org/bb/current/{file_name:s}.smi.gz".format(
                file_name=version.split(
                    sep="_",
                    maxsplit=1
                )[1]
            ),
            file_name="{file_name:s}.smi.gz".format(
                file_name=version.split(
                    sep="_",
                    maxsplit=1
                )[1]
            ),
            output_directory_path=output_directory_path
        )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

    def _download_catalogs(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `catalogs` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        self._download_file(
            file_url="https://files.docking.org/catalogs/source/{file_name:s}.src.txt".format(
                file_name=version.split(
                    sep="_",
                    maxsplit=1
                )[1]
            ),
            file_name="{file_name:s}.src.txt".format(
                file_name=version.split(
                    sep="_",
                    maxsplit=1
                )[1]
            ),
            output_directory_path=output_directory_path
        )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
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
            if version in self.available_versions["building_blocks"].keys():
                self._download_building_blocks(
                    version=version,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["catalogs"].keys():
                self._download_catalogs(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="ZINC20 chemical compound database ({version:s})".format(
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

    def _extract_building_blocks(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `building_blocks` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        with open_gz_archive_file(
            filename=Path(
                input_directory_path,
                "{file_name:s}.smi.gz".format(
                    file_name=version.split(
                        sep="_",
                        maxsplit=1
                    )[1]
                )
            )
        ) as gz_archive_file_handle:
            with open(
                file=Path(
                    output_directory_path,
                    "{file_name:s}.smi".format(
                        file_name=version.split(
                            sep="_",
                            maxsplit=1
                        )[1]
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
                    data_source="ZINC20 chemical compound database ({version:s})".format(
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
            if version in self.available_versions["building_blocks"].keys():
                self._extract_building_blocks(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["catalogs"].keys():
                self.logger.warning(
                    msg="The extraction of the {data_source:s} is not required.".format(
                        data_source="ZINC20 chemical compound database ({version:s})".format(
                            version=version
                        )
                    )
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="ZINC20 chemical compound database ({version:s})".format(
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

    def _format_building_blocks(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `building_blocks` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        read_csv(
            filepath_or_buffer=Path(
                input_directory_path,
                "{file_name:s}.smi".format(
                    file_name=version.split(
                        sep="_",
                        maxsplit=1
                    )[1]
                )
            ),
            sep=r"\s+",
            header=None
        ).rename(
            columns={
                0: "smiles",
                1: "id",
            }
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_zinc20_{version:s}.csv".format(
                    timestamp=datetime.now().strftime(
                        format="%Y%m%d%H%M%S"
                    ),
                    version=version.replace("-", "_")
                )
            ),
            index=False
        )

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been successfully completed.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

    def _format_catalogs(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `catalogs` versions of the chemical compound database.

        :parameter version: The version of the chemical compound database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
                        version=version
                    )
                )
            )

        read_csv(
            filepath_or_buffer=Path(
                input_directory_path,
                "{file_name:s}.src.txt".format(
                    file_name=version.split(
                        sep="_",
                        maxsplit=1
                    )[1]
                )
            ),
            sep=r"\s+",
            header=None
        ).rename(
            columns={
                0: "smiles",
                1: "id",
            }
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_zinc20_{version:s}.csv".format(
                    timestamp=datetime.now().strftime(
                        format="%Y%m%d%H%M%S"
                    ),
                    version=version.replace("-", "_")
                )
            ),
            index=False
        )

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been successfully completed.".format(
                    data_source="ZINC20 chemical compound database ({version:s})".format(
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
            if version in self.available_versions["building_blocks"].keys():
                self._format_building_blocks(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["catalogs"].keys():
                self._format_catalogs(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="ZINC20 chemical compound database ({version:s})".format(
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
