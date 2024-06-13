""" The ``ncsw_data.source.reaction.ord`` package ``ord`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike, walk
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from ord_schema.message_helpers import get_reaction_smiles, load_message
from ord_schema.proto.dataset_pb2 import Dataset
from ord_schema.proto.reaction_pb2 import Reaction

from pandas.core.frame import DataFrame

from pqdm.processes import pqdm

from rdkit.RDLogger import DisableLog

from zipfile import ZipFile

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class OpenReactionDatabase(AbstractBaseDataSource):
    """ The `Open Reaction Database (ORD) <https://open-reaction-database.org>`_ class. """

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
            "github": {
                "v_release_v_0_1_0": "https://doi.org/10.1021/jacs.1c09820",
                "v_main": "https://doi.org/10.1021/jacs.1c09820",
            },
        }

    def _download_github(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `github` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="Open Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_release_v_0_1_0":
            self._download_file(
                file_url="https://github.com/open-reaction-database/ord-data/archive/refs/tags/v0.1.0.zip",
                file_name="ord-data-0.1.0.zip",
                output_directory_path=output_directory_path
            )

        else:
            self._download_file(
                file_url="https://github.com/open-reaction-database/ord-data/archive/refs/heads/main.zip",
                file_name="ord-data-main.zip",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="Open Reaction Database ({version:s})".format(
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
            if version in self.available_versions["github"].keys():
                self._download_github(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Open Reaction Database ({version:s})".format(
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

    def _extract_github(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `github` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="Open Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_release_v_0_1_0":
            input_file_path = Path(input_directory_path, "ord-data-0.1.0.zip")

        else:
            input_file_path = Path(input_directory_path, "ord-data-main.zip")

        with ZipFile(
            file=input_file_path
        ) as zip_archive_file_handle:
            zip_archive_file_handle.extractall(
                path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="Open Reaction Database ({version:s})".format(
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

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["github"].keys():
                self._extract_github(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Open Reaction Database ({version:s})".format(
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

    def _parse_reaction_message(
            self,
            message: Reaction,
            **kwargs
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse a chemical reaction Protocol Buffer message.

        :parameter message: The chemical reaction Protocol Buffer message.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `ord_schema.message_helpers.get_reaction_smiles` }.

        :returns: The chemical reaction identifier and SMILES string.
        """

        try:
            return message.reaction_id, get_reaction_smiles(
                message=message,
                **kwargs
            )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

            return None, None

    def _parse_reaction_dataset_message_file(
            self,
            file_path: str
    ) -> Tuple[Optional[str], Optional[List[Tuple[Optional[str], Optional[str]]]]]:
        """
        Parse a chemical reaction dataset Protocol Buffer message file.

        :parameter file_path: The path to the chemical reaction dataset Protocol Buffer message file.

        :returns: The chemical reaction dataset identifier, and chemical reaction identifiers and SMILES strings.
        """

        try:
            reaction_dataset_message = load_message(
                filename=file_path,
                message_type=Dataset
            )

            parsed_reaction_messages = list()

            for reaction_message in reaction_dataset_message.reactions:
                parsed_reaction_messages.append(
                    self._parse_reaction_message(
                        message=reaction_message,
                        generate_if_missing=True,
                        canonical=False
                    )
                )

            return reaction_dataset_message.dataset_id, parsed_reaction_messages

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

            return None, None

    def _format_github(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            number_of_cpu_cores: int = 1
    ) -> None:
        """
        Format the data from the `github` versions of the chemical reaction database.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        :parameter number_of_cpu_cores: The number of CPU cores that should be utilized.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="Open Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_release_v_0_1_0":
            input_directory_path = Path(input_directory_path, "ord-data-0.1.0", "data")

        else:
            input_directory_path = Path(input_directory_path, "ord-data-main", "data")

        reaction_dataset_message_file_paths = list()

        for directory_path, _, file_names in walk(
            top=input_directory_path
        ):
            for file_name in file_names:
                if file_name.endswith(".pb.gz"):
                    reaction_dataset_message_file_paths.append(
                        Path(directory_path, file_name).resolve().as_posix()
                    )

        open_reaction_database_rows = list()

        DisableLog(
            spec="rdApp.*"
        )

        for reaction_dataset_message_identifier, parsed_reaction_messages in pqdm(
            array=reaction_dataset_message_file_paths,
            function=self._parse_reaction_dataset_message_file,
            n_jobs=number_of_cpu_cores,
            total=len(reaction_dataset_message_file_paths),
            desc="Formatting the Open Reaction Database ({version:s}) files".format(
                version=version
            ),
            ncols=120
        ):
            if parsed_reaction_messages is not None:
                for reaction_message_identifier, reaction_smiles in parsed_reaction_messages:
                    if reaction_smiles is not None:
                        open_reaction_database_rows.append((
                            reaction_dataset_message_identifier,
                            reaction_message_identifier,
                            reaction_smiles,
                        ))

        DataFrame(
            data=open_reaction_database_rows,
            columns=[
                "dataset_id",
                "reaction_id",
                "reaction_smiles",
            ]
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_ord_{version:s}.csv".format(
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
                    data_source="Open Reaction Database ({version:s})".format(
                        version=version
                    )
                )
            )

    def format(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            number_of_cpu_cores: int = 1
    ) -> None:
        """
        Format the data.

        :parameter version: The version of the chemical reaction database.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        :parameter number_of_cpu_cores: The number of CPU cores that should be utilized.
        """

        try:
            if version in self.available_versions["github"].keys():
                self._format_github(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path,
                    number_of_cpu_cores=number_of_cpu_cores
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="Open Reaction Database ({version:s})".format(
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
