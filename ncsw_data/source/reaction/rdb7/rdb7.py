""" The ``ncsw_data.source.reaction.rdb7`` package ``rdb7`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union

from pandas.core.reshape.concat import concat
from pandas.io.parsers.readers import read_csv

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class RDB7ReactionDataset(AbstractBaseDataSource):
    """ The `RDB7 <https://www.nature.com/articles/s41597-020-0460-4>`_ chemical reaction dataset class. """

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
        Get the available versions of the chemical reaction dataset.

        :returns: The available versions of the chemical reaction dataset.
        """

        return {
            "zenodo": {
                "v_20200508_grambow_c_et_al_v_1_0_0": "https://doi.org/10.5281/zenodo.3581267",
                "v_20200508_grambow_c_et_al_v_1_0_1": "https://doi.org/10.5281/zenodo.3715478",
                "v_20200508_grambow_c_et_al_add_on_v_1_0_0": "https://doi.org/10.5281/zenodo.3731554",
                "v_20220718_spiekermann_k_et_al_v_1_0_0": "https://doi.org/10.5281/zenodo.5652098",
                "v_20220718_spiekermann_k_et_al_v_1_0_1": "https://doi.org/10.5281/zenodo.6618262",
            },
        }

    def _download_zenodo(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `zenodo` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="RDB7 chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_20200508_grambow_c_et_al_v_1_0_0":
            for file_name in [
                "b97d3.csv",
                "wb97xd3.csv",
            ]:
                self._download_file(
                    file_url="https://zenodo.org/records/3581267/files/{file_name:s}".format(
                        file_name=file_name
                    ),
                    file_name=file_name,
                    output_directory_path=output_directory_path
                )

        elif version == "v_20200508_grambow_c_et_al_v_1_0_1":
            for file_name in [
                "b97d3.csv",
                "wb97xd3.csv",
            ]:
                self._download_file(
                    file_url="https://zenodo.org/records/3715478/files/{file_name:s}".format(
                        file_name=file_name
                    ),
                    file_name=file_name,
                    output_directory_path=output_directory_path
                )

        elif version == "v_20200508_grambow_c_et_al_add_on_v_1_0_0":
            for file_name in [
                "b97d3_rad.csv",
                "wb97xd3_rad.csv",
            ]:
                self._download_file(
                    file_url="https://zenodo.org/records/3731554/files/{file_name:s}".format(
                        file_name=file_name
                    ),
                    file_name=file_name,
                    output_directory_path=output_directory_path
                )

        elif version == "v_20220718_spiekermann_k_et_al_v_1_0_0":
            for file_name in [
                "b97d3.csv",
                "wb97xd3.csv",
                "ccsdtf12_dz.csv",
                "ccsdtf12_tz.csv",
            ]:
                self._download_file(
                    file_url="https://zenodo.org/records/5652098/files/{file_name:s}".format(
                        file_name=file_name
                    ),
                    file_name=file_name,
                    output_directory_path=output_directory_path
                )

        else:
            for file_name in [
                "b97d3.csv",
                "wb97xd3.csv",
                "ccsdtf12_dz.csv",
                "ccsdtf12_tz.csv",
            ]:
                self._download_file(
                    file_url="https://zenodo.org/records/6618262/files/{file_name:s}".format(
                        file_name=file_name
                    ),
                    file_name=file_name,
                    output_directory_path=output_directory_path
                )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="RDB7 chemical reaction dataset ({version:s})".format(
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

        :parameter version: The version of the chemical reaction dataset.
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
                            data_source="RDB7 chemical reaction dataset ({version:s})".format(
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

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version in self.available_versions["zenodo"].keys():
                if self.logger is not None:
                    self.logger.warning(
                        msg="The extraction of the {data_source:s} is not required.".format(
                            data_source="RDB7 chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="RDB7 chemical reaction dataset ({version:s})".format(
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
        Format the data from the `zenodo` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="RDB7 chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        rdb7_datasets = list()

        if version in [
            "v_20200508_grambow_c_et_al_v_1_0_0",
            "v_20200508_grambow_c_et_al_v_1_0_1",
        ]:
            for file_name in [
                "b97d3.csv",
                "wb97xd3.csv"
            ]:
                rdb7_dataset = read_csv(
                    filepath_or_buffer=Path(input_directory_path, file_name),
                    header=0
                )

                rdb7_dataset["reaction_smiles"] = rdb7_dataset["rsmi"] + ">>" + rdb7_dataset["psmi"]
                rdb7_dataset["file_name"] = file_name

                rdb7_datasets.append(
                    rdb7_dataset
                )

        elif version == "v_20200508_grambow_c_et_al_add_on_v_1_0_0":
            for file_name in [
                "b97d3_rad.csv",
                "wb97xd3_rad.csv"
            ]:
                rdb7_dataset = read_csv(
                    filepath_or_buffer=Path(input_directory_path, file_name),
                    header=0
                )

                rdb7_dataset["reaction_smiles"] = rdb7_dataset["rsmi"] + ">>" + rdb7_dataset["psmi"]
                rdb7_dataset["file_name"] = file_name

                rdb7_datasets.append(
                    rdb7_dataset
                )

        else:
            for file_name in [
                "b97d3.csv",
                "wb97xd3.csv",
                "ccsdtf12_dz.csv",
                "ccsdtf12_tz.csv",
            ]:
                rdb7_dataset = read_csv(
                    filepath_or_buffer=Path(input_directory_path, file_name),
                    header=0
                )

                rdb7_dataset["reaction_smiles"] = rdb7_dataset["rsmi"] + ">>" + rdb7_dataset["psmi"]
                rdb7_dataset["file_name"] = file_name

                rdb7_datasets.append(
                    rdb7_dataset
                )

        concat(
            objs=rdb7_datasets
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_rdb7_{version:s}.csv".format(
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
                    data_source="RDB7 chemical reaction dataset ({version:s})".format(
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
                            data_source="RDB7 chemical reaction dataset ({version:s})".format(
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
