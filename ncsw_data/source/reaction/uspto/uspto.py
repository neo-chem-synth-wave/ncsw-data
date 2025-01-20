""" The ``ncsw_data.source.reaction.uspto`` package ``uspto`` module. """

from os import PathLike
from typing import Dict, Union

from ncsw_data.source.base.base import BaseDataSource

from ncsw_data.source.reaction.uspto.utility.download import USPTOReactionDatasetDownloadUtility
from ncsw_data.source.reaction.uspto.utility.extraction import USPTOReactionDatasetExtractionUtility
from ncsw_data.source.reaction.uspto.utility.formatting import USPTOReactionDatasetFormattingUtility


class USPTOReactionDataset(BaseDataSource):
    """
    The `United States Patent and Trademark Office (USPTO) <https://www.repository.cam.ac.uk/handle/1810/244727>`_
    chemical reaction dataset class.
    """

    @staticmethod
    def get_supported_versions() -> Dict[str, str]:
        """
        Get the supported versions of the dataset.

        :returns: The supported versions of the dataset.
        """

        return {
            "v_1976_to_2016_rsmi_by_20121009_lowe_d_m": "https://doi.org/10.6084/m9.figshare.5104873.v1",
            "v_50k_by_20171116_coley_c_w_et_al": "https://doi.org/10.1021/acscentsci.7b00355",
        }

    def download(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Download the data from the dataset.

        :parameter version: The version of the dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
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

                if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
                    USPTOReactionDatasetDownloadUtility.download_v_1976_to_2016_by_20121009_lowe_d_m(
                        version=version,
                        output_directory_path=output_directory_path
                    )

                if version == "v_50k_by_20171116_coley_c_w_et_al":
                    USPTOReactionDatasetDownloadUtility.download_v_50k_by_20171116_coley_c_w_et_al(
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
                    "The download of the data from the {data_source:s} is not supported.".format(
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

    def extract(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Extract the data from the dataset.

        :parameter version: The version of the dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
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

                if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
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
                    "The extraction of the data from the {data_source:s} is not supported.".format(
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
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Format the data from the dataset.

        :parameter version: The version of the dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
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

                if version == "v_1976_to_2016_rsmi_by_20121009_lowe_d_m":
                    USPTOReactionDatasetFormattingUtility.format_v_1976_to_2016_by_20121009_lowe_d_m(
                        version=version,
                        input_directory_path=input_directory_path,
                        output_directory_path=output_directory_path
                    )

                if version == "v_50k_by_20171116_coley_c_w_et_al":
                    USPTOReactionDatasetFormattingUtility.format_v_50k_by_20171116_coley_c_w_et_al(
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
                    "The formatting of the data from the {data_source:s} is not supported.".format(
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
