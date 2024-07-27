""" The ``ncsw_data.source.reaction`` package ``uspto`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from shutil import copyfileobj
from typing import Dict, Optional, Union

from pandas.core.reshape.concat import concat
from pandas.io.parsers.readers import read_csv

from py7zr.py7zr import SevenZipFile

from zipfile import ZipFile

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class USPTOReactionDataset(AbstractBaseDataSource):
    """
    The `United States Patent and Trademark Office (USPTO) <https://doi.org/10.17863/CAM.16293>`_ chemical reaction
    dataset class.
    """

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
    ) -> Dict[str, str]:
        """
        Get the available versions of the chemical reaction dataset.

        :returns: The available versions of the chemical reaction dataset.
        """

        return {
            "v_1976_to_2016_by_20121009_lowe_d_m": "https://doi.org/10.6084/m9.figshare.5104873.v1",
        }

    # ------------------------------------------------------------------------------------------------------------------
    #  Version: v_1976_to_2016_by_20121009_lowe_d_m
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _download_v_1976_to_2016_by_20121009_lowe_d_m(
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `v_1976_to_2016_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        AbstractBaseDataSource._download_file(
            file_url="https://figshare.com/ndownloader/articles/5104873/versions/1",
            file_name="5104873.zip",
            output_directory_path=output_directory_path
        )

    @staticmethod
    def _extract_v_1976_to_2016_by_20121009_lowe_d_m(
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `v_1976_to_2016_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        with ZipFile(
            file=Path(input_directory_path, "5104873.zip")
        ) as zip_archive_file_handle:
            for seven_zip_archive_file_name in [
                "1976_Sep2016_USPTOgrants_smiles.7z",
                "2001_Sep2016_USPTOapplications_smiles.7z",
            ]:
                with zip_archive_file_handle.open(
                    name=seven_zip_archive_file_name
                ) as seven_zip_archive_file_handle:
                    with open(
                        file=Path(output_directory_path, seven_zip_archive_file_name),
                        mode="wb"
                    ) as destination_file_handle:
                        copyfileobj(
                            fsrc=seven_zip_archive_file_handle,
                            fdst=destination_file_handle
                        )

                with SevenZipFile(
                    file=Path(input_directory_path, seven_zip_archive_file_name)
                ) as seven_zip_archive_file_handle:
                    seven_zip_archive_file_handle.extractall(
                        path=output_directory_path
                    )

    @staticmethod
    def _format_v_1976_to_2016_by_20121009_lowe_d_m(
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `v_1976_to_2016_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        dataframes = list()

        for file_name in [
            "1976_Sep2016_USPTOgrants_smiles.rsmi",
            "2001_Sep2016_USPTOapplications_smiles.rsmi",
        ]:
            dataframe = read_csv(
                filepath_or_buffer=Path(input_directory_path, file_name),
                sep="\t",
                header=0,
                low_memory=False
            )

            dataframe["FileName"] = file_name

            dataframes.append(
                dataframe
            )

        concat(
            objs=dataframes
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_uspto_v_1976_to_2016_by_20121009_lowe_d_m.csv".format(
                    timestamp=datetime.now().strftime(
                        format="%Y%m%d%H%M%S"
                    )
                )
            ),
            index=False
        )

    def download(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        try:
            if version in self.available_versions.keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been started.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version == "v_1976_to_2016_by_20121009_lowe_d_m":
                    self._download_v_1976_to_2016_by_20121009_lowe_d_m(
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been completed.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The {data_source:s} is not supported.".format(
                        data_source="USPTO chemical reaction dataset ({version:s})".format(
                            version=version
                        )
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

    def extract(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions.keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been started.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version == "v_1976_to_2016_by_20121009_lowe_d_m":
                    self._extract_v_1976_to_2016_by_20121009_lowe_d_m(
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been completed.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The {data_source:s} is not supported.".format(
                        data_source="USPTO chemical reaction dataset ({version:s})".format(
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
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        try:
            if version in self.available_versions.keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been started.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version == "v_1976_to_2016_by_20121009_lowe_d_m":
                    self._format_v_1976_to_2016_by_20121009_lowe_d_m(
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been completed.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The {data_source:s} is not supported.".format(
                        data_source="USPTO chemical reaction dataset ({version:s})".format(
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
