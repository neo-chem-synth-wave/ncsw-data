""" The ``ncsw_data.source.reaction_rule.miscellaneous`` package ``miscellaneous`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union

from pandas.io.parsers.readers import read_csv

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class MiscellaneousReactionRuleDataSource(AbstractBaseDataSource):
    """ The miscellaneous chemical reaction rule data source class. """

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
        Get the available versions of the chemical reaction rule data source.

        :returns: The available versions of the chemical reaction rule data source.
        """

        return {
            "zenodo": {
                "v_20180421_avramova_s_et_al": "https://doi.org/10.5281/zenodo.1209313",
            },
        }

    def _download_zenodo(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `zenodo` versions of the chemical reaction rule data source.

        :parameter version: The version of the chemical reaction rule data source.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20180421_avramova_s_et_al":
            self._download_file(
                file_url="https://zenodo.org/records/1209313/files/RetroTransformDB-v-1-0.txt",
                file_name="RetroTransformDB-v-1-0.txt",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
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

        :parameter version: The version of the chemical reaction rule data source.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        try:
            if version in self.available_versions["zenodo"].keys():
                self._download_zenodo(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
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

    def extract(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data.

        :parameter version: The version of the chemical reaction rule data source.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["zenodo"].keys():
                if self.logger is not None:
                    self.logger.warning(
                        msg="The extraction of the {data_source:s} is not required.".format(
                            data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
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

    def _format_zenodo(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `zenodo` versions of the chemical reaction rule data source.

        :parameter version: The version of the chemical reaction rule data source.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20180421_avramova_s_et_al":
            read_csv(
                filepath_or_buffer=Path(input_directory_path, "RetroTransformDB-v-1-0.txt"),
                sep="\t",
                header=0
            ).dropna(
                how="all"
            ).astype(
                dtype={
                    "ID": int,
                }
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_miscellaneous_{version:s}.csv".format(
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
                    data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
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

        :parameter version: The version of the chemical reaction rule data source.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        try:
            if version in self.available_versions["zenodo"].keys():
                self._format_zenodo(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="miscellaneous chemical reaction rule data source ({version:s})".format(
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
