""" The ``ncsw_data.source.reaction.uspto`` package ``uspto`` module. """

from logging import Logger
from os import PathLike
from typing import Dict, Optional, Union

from ncsw_data.source.base.base import BaseDataSource

from ncsw_data.source.reaction.uspto.utility.download import USPTOReactionDatasetDownloadUtility
from ncsw_data.source.reaction.uspto.utility.extraction import USPTOReactionDatasetExtractionUtility
from ncsw_data.source.reaction.uspto.utility.formatting import USPTOReactionDatasetFormattingUtility


class USPTOReactionDataset(BaseDataSource):
    """
    The `United States Patent and Trademark Office (USPTO) <https://www.repository.cam.ac.uk/handle/1810/244727>`_
    chemical reaction dataset class.
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

    def get_supported_versions(
            self,
            **kwargs
    ) -> Dict[str, str]:
        """
        Get the supported versions of the chemical reaction dataset.

        :parameter kwargs: The keyword arguments.

        :returns: The supported versions of the chemical reaction dataset.
        """

        try:
            return {
                "v_1976_to_2016_cml_by_20121009_lowe_d_m": "https://doi.org/10.6084/m9.figshare.5104873.v1",
                "v_1976_to_2016_rsmi_by_20121009_lowe_d_m": "https://doi.org/10.6084/m9.figshare.5104873.v1",
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
        Download the data from the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        :parameter kwargs: The keyword arguments.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The download of the data from the {data_source:s} has been started.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version in [
                    "v_1976_to_2016_cml_by_20121009_lowe_d_m",
                    "v_1976_to_2016_rsmi_by_20121009_lowe_d_m",
                ]:
                    USPTOReactionDatasetDownloadUtility.download_v_1976_to_2016_by_20121009_lowe_d_m(
                        version=version,
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
                        data_source="USPTO chemical reaction dataset version '{version:s}'".format(
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
        Extract the data from the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        :parameter kwargs: The keyword arguments.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The extraction of the data from the {data_source:s} has been started.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version in [
                    "v_1976_to_2016_cml_by_20121009_lowe_d_m",
                    "v_1976_to_2016_rsmi_by_20121009_lowe_d_m",
                ]:
                    USPTOReactionDatasetExtractionUtility.extract_v_1976_to_2016_by_20121009_lowe_d_m(
                        version=version,
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
                        data_source="USPTO chemical reaction dataset version '{version:s}'".format(
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
        Format the data from the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        :parameter kwargs: The keyword arguments.
        """

        try:
            if version in self.get_supported_versions().keys():
                if self.logger is not None:
                    self.logger.info(
                        msg="The formatting of the data from the {data_source:s} has been started.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

                if version == "v_1976_to_2016_cml_by_20121009_lowe_d_m":
                    USPTOReactionDatasetFormattingUtility.format_v_1976_to_2016_cml_by_20121009_lowe_d_m(
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path,
                        **kwargs
                    )

                if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
                    USPTOReactionDatasetFormattingUtility.format_v_1976_to_2016_rsmi_by_20121009_lowe_d_m(
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
                        data_source="USPTO chemical reaction dataset version '{version:s}'".format(
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
