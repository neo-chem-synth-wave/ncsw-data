""" The ``ncsw_data.source.compound`` package ``compound`` module. """

from logging import Logger
from os import PathLike
from typing import Dict, List, Optional, Union

from ncsw_data.source.base.base import BaseDataSource

from ncsw_data.source.compound.zinc.zinc import ZINCCompoundDatabase


class CompoundDataSource(BaseDataSource):
    """ The chemical compound data source class. """

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

        self.supported_data_sources = {
            "zinc": ZINCCompoundDatabase(
                logger=logger
            ),
        }

    def get_names_of_supported_data_sources(
            self
    ) -> List[str]:
        """
        Get the names of the supported chemical compound data sources.

        :returns: The names of the supported chemical compound data sources.
        """

        return list(self.supported_data_sources.keys())

    def get_supported_versions(
            self,
            name: str,
            **kwargs
    ) -> Dict[str, str]:
        """
        Get the supported versions of a chemical compound data source.

        :parameter name: The name of the chemical compound data source.
        :parameter kwargs: The keyword arguments.

        :returns: The supported versions of the chemical compound data source.
        """

        if name in self.get_names_of_supported_data_sources():
            return self.supported_data_sources[name].get_supported_versions(
                **kwargs
            )

        else:
            self._raise_and_log_exception(
                exception_class=ValueError,
                exception_message="The chemical compound data source name '{name:s}' is not supported.".format(
                    name=name
                )
            )

    def download(
            self,
            name: str,
            version: str,
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Download the data from a chemical compound data source.

        :parameter name: The name of the chemical compound data source.
        :parameter version: The version of the chemical compound data source.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        :parameter kwargs: The keyword arguments.
        """

        if name in self.get_names_of_supported_data_sources():
            self.supported_data_sources[name].download(
                version=version,
                output_directory_path=output_directory_path,
                **kwargs
            )

        else:
            self._raise_and_log_exception(
                exception_class=ValueError,
                exception_message="The chemical compound data source name '{name:s}' is not supported.".format(
                    name=name
                )
            )

    def extract(
            self,
            name: str,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Extract the data from a chemical compound data source.

        :parameter name: The name of the chemical compound data source.
        :parameter version: The version of the chemical compound data source.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        :parameter kwargs: The keyword arguments.
        """

        if name in self.get_names_of_supported_data_sources():
            self.supported_data_sources[name].extract(
                version=version,
                input_directory_path=input_directory_path,
                output_directory_path=output_directory_path,
                **kwargs
            )

        else:
            self._raise_and_log_exception(
                exception_class=ValueError,
                exception_message="The chemical compound data source name '{name:s}' is not supported.".format(
                    name=name
                )
            )

    def format(
            self,
            name: str,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            **kwargs
    ) -> None:
        """
        Format the data from a chemical compound data source.

        :parameter name: The name of the chemical compound data source.
        :parameter version: The version of the chemical compound data source.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        :parameter kwargs: The keyword arguments.
        """

        if name in self.get_names_of_supported_data_sources():
            self.supported_data_sources[name].format(
                version=version,
                input_directory_path=input_directory_path,
                output_directory_path=output_directory_path,
                **kwargs
            )

        else:
            self._raise_and_log_exception(
                exception_class=ValueError,
                exception_message="The chemical compound data source name '{name:s}' is not supported.".format(
                    name=name
                )
            )
