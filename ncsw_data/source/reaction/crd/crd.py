""" The ``ncsw_data.source.reaction.crd`` package ``crd`` module. """

from logging import Logger
from os import PathLike
from typing import Dict, Optional, Union

from ncsw_data.source.base.base import BaseDataSource

from ncsw_data.source.reaction.crd.utility.download import ChemicalReactionDatabaseDownloadUtility
from ncsw_data.source.reaction.crd.utility.formatting import ChemicalReactionDatabaseFormattingUtility


class ChemicalReactionDatabase(BaseDataSource):
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

    def get_supported_versions(
            self,
            **kwargs
    ) -> Dict[str, str]:
        """
        Get the supported versions of the chemical reaction database.

        :parameter kwargs: The keyword arguments.

        :returns: The supported versions of the chemical reaction database.
        """

        try:
            return {
                "v_reaction_smiles_2001_to_2021": "https://doi.org/10.6084/m9.figshare.20279733.v1",
                "v_reaction_smiles_2001_to_2023": "https://doi.org/10.6084/m9.figshare.22491730.v1",
                "v_reaction_smiles_2023": "https://doi.org/10.6084/m9.figshare.24921555.v1",
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
        Download the data from the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        :parameter kwargs: The keyword arguments.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been started.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version.startswith("v_reaction_smiles"):
                    ChemicalReactionDatabaseDownloadUtility.download_v_reaction_smiles(
                        version=version,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been completed.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The {data_source:s} is not supported.".format(
                        data_source="Chemical Reaction Database version '{version:s}'".format(
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
        Extract the data from the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        :parameter kwargs: The keyword arguments.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been started.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been completed.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The {data_source:s} is not supported.".format(
                        data_source="Chemical Reaction Database version '{version:s}'".format(
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
        Format the data from the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        :parameter kwargs: The keyword arguments.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been started.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version.startswith("v_reaction_smiles"):
                    ChemicalReactionDatabaseFormattingUtility.format_v_reaction_smiles(
                        version=version,
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path
                    )

                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been completed.".format(
                            data_source="Chemical Reaction Database ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                raise ValueError(
                    "The {data_source:s} is not supported.".format(
                        data_source="Chemical Reaction Database version '{version:s}'".format(
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
