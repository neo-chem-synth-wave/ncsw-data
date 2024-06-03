""" The ``ncsw_data.source.reaction_rule.retro_rules`` package ``retro_rules`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union

from pandas.io.parsers.readers import read_csv

from tarfile import open as open_tar_archive_file

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class RetroRulesReactionRuleDatabase(AbstractBaseDataSource):
    """ The `RetroRules <https://retrorules.org>`_ chemical reaction rule database class. """

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
        Get the available versions of the chemical reaction rule database.

        :returns: The available versions of the chemical reaction rule database.
        """

        return {
            "zenodo": {
                "v_release_rr01_rp2_hs": "https://doi.org/10.5281/zenodo.5827427",
                "v_release_rr02_rp2_hs": "https://doi.org/10.5281/zenodo.5828017",
                "v_release_rr02_rp3_hs": "https://doi.org/10.5281/zenodo.5827977",
                "v_release_rr02_rp3_nohs": "https://doi.org/10.5281/zenodo.5827969",
            },
        }

    def _download_zenodo(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `zenodo` versions of the chemical reaction rule database.

        :parameter version: The version of the chemical reaction rule database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="RetroRules chemical reaction rule database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_release_rr01_rp2_hs":
            self._download_file(
                file_url="https://zenodo.org/records/5827427/files/retrorules_rr01_rp2.tar.gz",
                file_name="retrorules_rr01_rp2.tar.gz",
                output_directory_path=output_directory_path
            )

        elif version == "v_release_rr02_rp2_hs":
            self._download_file(
                file_url="https://zenodo.org/records/5828017/files/retrorules_rr02_rp2_hs.tar.gz",
                file_name="retrorules_rr02_rp2_hs.tar.gz",
                output_directory_path=output_directory_path
            )

        elif version == "v_release_rr02_rp3_hs":
            self._download_file(
                file_url="https://zenodo.org/records/5827977/files/retrorules_rr02_rp3_hs.tar.gz",
                file_name="retrorules_rr02_rp3_hs.tar.gz",
                output_directory_path=output_directory_path
            )

        else:
            self._download_file(
                file_url="https://zenodo.org/records/5827969/files/retrorules_rr02_rp3_nohs.tar.gz",
                file_name="retrorules_rr02_rp3_nohs.tar.gz",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="RetroRules chemical reaction rule database ({version:s})".format(
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

        :parameter version: The version of the chemical reaction rule database.
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
                            data_source="RetroRules chemical reaction rule database ({version:s})".format(
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

    def _extract_zenodo(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `zenodo` versions of the chemical reaction rule database.

        :parameter version: The version of the chemical reaction rule database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="RetroRules chemical reaction rule database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_release_rr01_rp2_hs":
            input_file_path = Path(input_directory_path, "retrorules_rr01_rp2.tar.gz")

        elif version == "v_release_rr02_rp2_hs":
            input_file_path = Path(input_directory_path, "retrorules_rr02_rp2_hs.tar.gz")

        elif version == "v_release_rr02_rp3_hs":
            input_file_path = Path(input_directory_path, "retrorules_rr02_rp3_hs.tar.gz")

        else:
            input_file_path = Path(input_directory_path, "retrorules_rr02_rp3_nohs.tar.gz")

        with open_tar_archive_file(
            name=input_file_path,
            mode="r:gz"
        ) as tar_archive_file_handle:
            tar_archive_file_handle.extractall(
                path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="RetroRules chemical reaction rule database ({version:s})".format(
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

        :parameter version: The version of the chemical reaction rule database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["zenodo"].keys():
                self._extract_zenodo(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="RetroRules chemical reaction rule database ({version:s})".format(
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
        Format the data from the `zenodo` versions of the chemical reaction rule database.

        :parameter version: The version of the chemical reaction rule database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="RetroRules chemical reaction rule database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_release_rr01_rp2_hs":
            retro_rules_database = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "retrorules_rr01_rp2",
                    "retrorules_rr01_rp2_flat_all.csv"
                ),
                header=0
            )

        elif version == "v_release_rr02_rp2_hs":
            retro_rules_database = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "retrorules_rr02_rp2_hs",
                    "retrorules_rr02_rp2_flat_all.csv"
                ),
                header=0
            )

        elif version == "v_release_rr02_rp3_hs":
            retro_rules_database = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "retrorules_rr02_rp3_hs",
                    "retrorules_rr02_flat_all.tsv"
                ),
                sep="\t",
                header=0
            )

        else:
            retro_rules_database = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "retrorules_rr02_rp3_nohs",
                    "retrorules_rr02_flat_all.tsv"
                ),
                sep="\t",
                header=0
            )

        retro_rules_database.to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_retro_rules_{version:s}.csv".format(
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
                    data_source="RetroRules chemical reaction rule database ({version:s})".format(
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

        :parameter version: The version of the chemical reaction rule database.
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
                            data_source="RetroRules chemical reaction rule database ({version:s})".format(
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
