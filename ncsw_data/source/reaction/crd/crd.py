""" The ``ncsw_data.source.reaction.crd`` package ``crd`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union

from pandas.io.parsers.readers import read_csv

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class ChemicalReactionDatabase(AbstractBaseDataSource):
    """ The `Chemical Reaction Database (CRD) <https://kmt.vander-lingen.nl>`_ class. """

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

        return {
            "figshare": {
                "v_reaction_smiles_2001_to_2021": "https://doi.org/10.6084/m9.figshare.20279733.v1",
                "v_reaction_smiles_2001_to_2023": "https://doi.org/10.6084/m9.figshare.22491730.v1",
                "v_reaction_smiles_2023": "https://doi.org/10.6084/m9.figshare.24921555.v1",
            },
        }

    def _download_figshare(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `figshare` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="Chemical Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_reaction_smiles_2001_to_2021":
            self._download_file(
                file_url="https://figshare.com/ndownloader/files/36222051",
                file_name="reactionSmilesFigShare.txt",
                output_directory_path=output_directory_path
            )

        elif version == "v_reaction_smiles_2001_to_2023":
            self._download_file(
                file_url="https://figshare.com/ndownloader/files/39944236",
                file_name="reactionSmilesFigShare2023.txt",
                output_directory_path=output_directory_path
            )

        else:
            self._download_file(
                file_url="https://figshare.com/ndownloader/files/43858050",
                file_name="reactionSmilesFigShareUSPTO2023.txt",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="Chemical Reaction Database ({version:s})".format(
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
            if version in self.available_versions["figshare"].keys():
                self._download_figshare(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
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

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["figshare"].keys():
                if self.logger is not None:
                    self.logger.warning(
                        msg="The extraction of the {data_source:s} is not required.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
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

    def _format_figshare(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `figshare` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="Chemical Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_reaction_smiles_2001_to_2021":
            input_file_path = Path(input_directory_path, "reactionSmilesFigShare.txt")

        elif version == "v_reaction_smiles_2001_to_2023":
            input_file_path = Path(input_directory_path, "reactionSmilesFigShare2023.txt")

        else:
            input_file_path = Path(input_directory_path, "reactionSmilesFigShareUSPTO2023.txt")

        read_csv(
            filepath_or_buffer=input_file_path,
            header=None
        ).rename(
            columns={
                0: "reaction_smiles",
            }
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_crd_{version:s}.csv".format(
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
                    data_source="Chemical Reaction Database ({version:s})".format(
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
            if version in self.available_versions["figshare"].keys():
                self._format_figshare(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
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
