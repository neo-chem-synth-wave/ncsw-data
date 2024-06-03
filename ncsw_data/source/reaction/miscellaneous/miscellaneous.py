""" The ``ncsw_data.source.reaction.miscellaneous`` package ``miscellaneous`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union

from pandas.core.frame import DataFrame
from pandas.core.reshape.concat import concat
from pandas.io.parsers.readers import read_csv

from rdkit.Chem.rdChemReactions import ReactionFromRxnBlock, ReactionToSmiles

from zipfile import ZipFile

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class MiscellaneousReactionDataSource(AbstractBaseDataSource):
    """ The miscellaneous chemical reaction data source class. """

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
        Get the available versions of the chemical reaction data source.

        :returns: The available versions of the chemical reaction data source.
        """

        return {
            "acs": {
                "v_20131008_kraut_h_et_al": "https://doi.org/10.1021/ci400442f",
            },
            "github": {
                "v_20161014_wei_j_n_et_al": "https://doi.org/10.1021/acscentsci.6b00219",
            },
        }

    def _download_acs(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `acs` versions of the chemical reaction data source.

        :parameter version: The version of the chemical reaction data source.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20131008_kraut_h_et_al":
            self._download_file(
                file_url="https://ndownloader.figstatic.com/files/3988891",
                file_name="ci400442f_si_002.zip",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

    def _download_github(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `github` versions of the chemical reaction data source.

        :parameter version: The version of the chemical reaction data source.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20161014_wei_j_n_et_al":
            for file_name in [
                "Wade8_47.ans_smi.txt",
                "Wade8_48.ans_smi.txt",
            ]:
                self._download_file(
                    file_url="https://raw.githubusercontent.com/jnwei/{file_url_suffix:s}".format(
                        file_url_suffix="neural_reaction_fingerprint/master/data/test_questions/{file_name:s}".format(
                            file_name=file_name
                        )
                    ),
                    file_name=file_name,
                    output_directory_path=output_directory_path
                )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
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

        :parameter version: The version of the chemical reaction data source.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        try:
            if version in self.available_versions["acs"].keys():
                self._download_acs(
                    version=version,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["github"].keys():
                self._download_github(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="miscellaneous chemical reaction data source ({version:s})".format(
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

    def _extract_acs(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `acs` versions of the chemical reaction data source.

        :parameter version: The version of the chemical reaction data source.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20131008_kraut_h_et_al":
            with ZipFile(
                file=Path(input_directory_path, "ci400442f_si_002.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
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

        :parameter version: The version of the chemical reaction data source.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["acs"].keys():
                self._extract_acs(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["github"].keys():
                if self.logger is not None:
                    self.logger.warning(
                        msg="The extraction of the {data_source:s} is not required.".format(
                            data_source="miscellaneous chemical reaction data source ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="miscellaneous chemical reaction data source ({version:s})".format(
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

    def _format_acs(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `acs` versions of the chemical reaction data source.

        :parameter version: The version of the chemical reaction data source.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20131008_kraut_h_et_al":
            miscellaneous_reaction_data_source_rows = list()

            for file_name in [
                "MapTestExamplesV1.0.rdf",
                "MapTestExamplesV1_ICMapRctCpy.rdf",
                "MapTestExamplesV1_ICMap.rdf",
            ]:
                with open(
                    file=Path(input_directory_path, file_name)
                ) as file_handle:
                    for reaction_rxn_block_without_identifier in file_handle.read().split("$RXN")[1:]:
                        reaction_rxn = ReactionFromRxnBlock(
                            "$RXN{0:s}".format(
                                reaction_rxn_block_without_identifier
                            )
                        )

                        if reaction_rxn is not None:
                            reaction_smiles = ReactionToSmiles(reaction_rxn)

                            if reaction_smiles is not None:
                                miscellaneous_reaction_data_source_rows.append((
                                    reaction_smiles,
                                    "smarts" if "*" in reaction_smiles else "smiles",
                                    file_name,
                                ))

            DataFrame(
                data=miscellaneous_reaction_data_source_rows,
                columns=[
                    "reaction_string",
                    "reaction_string_type",
                    "file_name",
                ]
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
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

    def _format_github(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `github` versions of the chemical reaction data source.

        :parameter version: The version of the chemical reaction data source.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
                        version=version
                    )
                )
            )

            if version == "v_20161014_wei_j_n_et_al":
                miscellaneous_reaction_data_sources = list()

                for file_name in [
                    "Wade8_47.ans_smi.txt",
                    "Wade8_48.ans_smi.txt",
                ]:
                    miscellaneous_reaction_data_source = read_csv(
                        filepath_or_buffer=Path(input_directory_path, file_name),
                        header=None
                    ).rename(
                        columns={
                            0: "reaction_smiles",
                        }
                    )

                    miscellaneous_reaction_data_source["file_name"] = file_name

                    miscellaneous_reaction_data_sources.append(
                        miscellaneous_reaction_data_source
                    )

                concat(
                    objs=miscellaneous_reaction_data_sources
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
                    data_source="miscellaneous chemical reaction data source ({version:s})".format(
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

        :parameter version: The version of the chemical reaction data source.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        try:
            if version in self.available_versions["acs"].keys():
                self._format_acs(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["github"].keys():
                self._format_github(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="miscellaneous chemical reaction data source ({version:s})".format(
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
