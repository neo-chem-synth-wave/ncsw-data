""" The ``ncsw_data.source.reaction.uspto`` package ``uspto`` module. """

from datetime import datetime
from logging import Logger
from os import PathLike
from pathlib import Path
from shutil import copyfileobj
from typing import Dict, Optional, Union

from gzip import open as open_gz_archive_file

from pandas.core.reshape.concat import concat
from pandas.io.parsers.readers import read_csv

from py7zr.py7zr import SevenZipFile

from zipfile import ZipFile

from ncsw_data.source.abstract_base.abstract_base import AbstractBaseDataSource


class USPTOReactionDataset(AbstractBaseDataSource):
    """
    The `United States Patent and Trademark Office (USPTO) <https://doi.org/10.17863/CAM.16293>`_ chemical reaction
    dataset class.
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

    @property
    def available_versions(
            self
    ) -> Dict[str, Dict[str, str]]:
        """
        Get the available versions of the chemical reaction dataset.

        :returns: The available versions of the chemical reaction dataset.
        """

        return {
            "acs": {
                "v_50k_by_20161122_schneider_n_et_al": "https://doi.org/10.1021/acs.jcim.6b00564",
            },
            "figshare": {
                "v_1976_to_2013_by_20121009_lowe_d_m": "https://doi.org/10.6084/m9.figshare.12084729.v1",
                "v_1976_to_2016_by_20121009_lowe_d_m": "https://doi.org/10.6084/m9.figshare.5104873.v1",
            },
            "github": {
                "v_15k_by_20170418_coley_c_w_et_al": "https://doi.org/10.1021/acscentsci.7b00064",
                "v_50k_by_20171116_coley_c_w_et_al": "https://doi.org/10.1021/acscentsci.7b00355",
                "v_480k_or_mit_by_20171229_jin_w_et_al": "https://doi.org/10.48550/arXiv.1709.04555",
            },
            "ibm_box": {
                "v_480k_or_mit_by_20180622_schwaller_p_et_al": "https://doi.org/10.1039/C8SC02339E",
                "v_stereo_by_20180622_schwaller_p_et_al": "https://doi.org/10.1039/C8SC02339E",
                "v_1k_tpl_by_20210705_schwaller_p_et_al": "https://doi.org/10.1038/s42256-020-00284-w",
            },
        }

    def _download_acs(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `acs` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_50k_by_20161122_schneider_n_et_al":
            self._download_file(
                file_url="https://ndownloader.figstatic.com/files/7005749",
                file_name="ci6b00564_si_002.zip",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _download_figshare(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `figshare` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_1976_to_2013_by_20121009_lowe_d_m":
            self._download_file(
                file_url="https://figshare.com/ndownloader/articles/12084729/versions/1",
                file_name="12084729.zip",
                output_directory_path=output_directory_path
            )

        else:
            self._download_file(
                file_url="https://figshare.com/ndownloader/articles/5104873/versions/1",
                file_name="5104873.zip",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
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
        Download the data from the `github` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_15k_by_20170418_coley_c_w_et_al":
            self._download_file(
                file_url="https://raw.githubusercontent.com/wengong-jin/nips17-rexgen/master/USPTO-15K/data.zip",
                file_name="data.zip",
                output_directory_path=output_directory_path
            )

        elif version == "v_50k_by_20171116_coley_c_w_et_al":
            self._download_file(
                file_url="https://raw.githubusercontent.com/connorcoley/{file_url_suffix:s}".format(
                    file_url_suffix="retrosim/master/retrosim/data/data_processed.csv"
                ),
                file_name="data_processed.csv",
                output_directory_path=output_directory_path
            )

        else:
            self._download_file(
                file_url="https://raw.githubusercontent.com/wengong-jin/nips17-rexgen/master/USPTO/data.zip",
                file_name="data.zip",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _download_ibm_box(
            self,
            version: str,
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Download the data from the `ibm_box` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter output_directory_path: The path to the output directory where the data should be downloaded.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version in [
            "v_480k_or_mit_by_20180622_schwaller_p_et_al",
            "v_stereo_by_20180622_schwaller_p_et_al",
        ]:
            self._download_file(
                file_url=self._send_http_get_request(
                    http_get_request_url="{url:s}?{folder_id:s}&{vanity_name:s}&{rm:s}".format(
                        url="https://ibm.ent.box.com/index.php",
                        folder_id="folder_id=40552708120",
                        vanity_name="q[shared_item][vanity_name]=ReactionSeq2SeqDataset",
                        rm="rm=box_v2_zip_shared_folder"
                    )
                ).json()["download_url"],
                file_name="ReactionSeq2Seq_Dataset.zip",
                output_directory_path=output_directory_path
            )

        else:
            self._download_file(
                file_url=self._send_http_get_request(
                    http_get_request_url="{url:s}?{folder_id:s}&{vanity_name:s}&{rm:s}".format(
                        url="https://ibm.ent.box.com/index.php",
                        folder_id="folder_id=124192222443",
                        vanity_name="q[shared_item][vanity_name]=MappingChemicalReactions",
                        rm="rm=box_v2_zip_shared_folder"
                    )
                ).json()["download_url"],
                file_name="MappingChemicalReactions.zip",
                output_directory_path=output_directory_path
            )

        if self.logger is not None:
            self.logger.info(
                msg="The download of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
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
            if version in self.available_versions["acs"].keys():
                self._download_acs(
                    version=version,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["figshare"].keys():
                self._download_figshare(
                    version=version,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["github"].keys():
                self._download_github(
                    version=version,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["ibm_box"].keys():
                self._download_ibm_box(
                    version=version,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.exception(
                    msg=exception_handle
                )

    def _extract_acs(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `acs` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_50k_by_20161122_schneider_n_et_al":
            with ZipFile(
                file=Path(input_directory_path, "ci6b00564_si_002.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _extract_figshare(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `figshare` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_1976_to_2013_by_20121009_lowe_d_m":
            with ZipFile(
                file=Path(input_directory_path, "12084729.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

            for file_name in [
                "1976-2013_USPTOgrants_reactionSmiles_feb2014filters.7z",
                "2001-2013_USPTOapplications_reactionSmiles_feb2014filters.7z",
            ]:
                with SevenZipFile(
                    file=Path(input_directory_path, file_name)
                ) as seven_zip_archive_file_handle:
                    seven_zip_archive_file_handle.extractall(
                        path=output_directory_path
                    )

        else:
            with ZipFile(
                file=Path(input_directory_path, "5104873.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

            for file_name in [
                "1976_Sep2016_USPTOgrants_smiles.7z",
                "2001_Sep2016_USPTOapplications_smiles.7z",
            ]:
                with SevenZipFile(
                    file=Path(input_directory_path, file_name)
                ) as seven_zip_archive_file_handle:
                    seven_zip_archive_file_handle.extractall(
                        path=output_directory_path
                    )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _extract_github(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `github` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version in [
            "v_15k_by_20170418_coley_c_w_et_al",
            "v_480k_or_mit_by_20171229_jin_w_et_al",
        ]:
            with ZipFile(
                file=Path(input_directory_path, "data.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _extract_ibm_box(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Extract the data from the `ibm_box` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version in [
            "v_480k_or_mit_by_20180622_schwaller_p_et_al",
            "v_stereo_by_20180622_schwaller_p_et_al",
        ]:
            with ZipFile(
                file=Path(input_directory_path, "ReactionSeq2Seq_Dataset.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

        else:
            with ZipFile(
                file=Path(input_directory_path, "MappingChemicalReactions.zip")
            ) as zip_archive_file_handle:
                zip_archive_file_handle.extractall(
                    path=output_directory_path
                )

            for file_name in [
                "uspto_1k_TPL_test.tsv.gzip",
                "uspto_1k_TPL_train_valid.tsv.gzip",
            ]:
                with open_gz_archive_file(
                    filename=Path(input_directory_path, "data_set", file_name)
                ) as gz_archive_file_handle:
                    with open(
                        file=Path(output_directory_path, file_name[:-5]),
                        mode="wb"
                    ) as file_handle:
                        copyfileobj(
                            fsrc=gz_archive_file_handle,
                            fdst=file_handle
                        )

        if self.logger is not None:
            self.logger.info(
                msg="The extraction of the {data_source:s} has been successfully completed.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
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

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is downloaded.
        :parameter output_directory_path: The path to the output directory where the data should be extracted.
        """

        try:
            if version == "v_50k_by_20171116_coley_c_w_et_al":
                if self.logger is not None:
                    self.logger.warning(
                        msg="The extraction of the {data_source:s} is not required.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
                                version=version
                            )
                        )
                    )

            elif version in self.available_versions["acs"].keys():
                self._extract_acs(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["figshare"].keys():
                self._extract_figshare(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["github"].keys():
                self._extract_github(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            elif version in self.available_versions["ibm_box"].keys():
                self._extract_ibm_box(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
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
        Format the data from the `acs` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_50k_by_20161122_schneider_n_et_al":
            dataset_a = read_csv(
                filepath_or_buffer=Path(input_directory_path, "data", "dataSetA.csv"),
                sep=",",
                header=0
            )

            dataset_a["file_Name"] = "dataSetA.csv"

            dataset_b = read_csv(
                filepath_or_buffer=Path(input_directory_path, "data", "dataSetB.csv"),
                sep=",",
                header=0
            )

            dataset_b["file_Name"] = "dataSetB.csv"

            concat(
                objs=[
                    dataset_a,
                    dataset_b,
                ]
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
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
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _format_figshare(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `figshare` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_1976_to_2013_by_20121009_lowe_d_m":
            uspto_grants = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "1976-2013_USPTOgrants_reactionSmiles_feb2014filters.rsmi"
                ),
                sep="\t",
                header=None,
                low_memory=False
            )

            uspto_grants["file_name"] = "1976-2013_USPTOgrants_reactionSmiles_feb2014filters.rsmi"

            uspto_applications = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "2001-2013_USPTOapplications_reactionSmiles_feb2014filters.rsmi"
                ),
                sep="\t",
                header=None,
                low_memory=False
            )

            uspto_applications["file_name"] = "2001-2013_USPTOapplications_reactionSmiles_feb2014filters.rsmi"

            concat([
                uspto_grants,
                uspto_applications,
            ]).rename(
                columns={
                    0: "reaction_smiles",
                    1: "document_id",
                    2: "paragraph_id",
                }
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
                        timestamp=datetime.now().strftime(
                            format="%Y%m%d%H%M%S"
                        ),
                        version=version
                    )
                ),
                index=False
            )

        else:
            uspto_grants = read_csv(
                filepath_or_buffer=Path(input_directory_path, "1976_Sep2016_USPTOgrants_smiles.rsmi"),
                sep="\t",
                header=0,
                low_memory=False
            )

            uspto_grants["FileName"] = "1976_Sep2016_USPTOgrants_smiles.rsmi"

            uspto_applications = read_csv(
                filepath_or_buffer=Path(input_directory_path, "2001_Sep2016_USPTOapplications_smiles.rsmi"),
                sep="\t",
                header=0,
                low_memory=False
            )

            uspto_applications["FileName"] = "2001_Sep2016_USPTOapplications_smiles.rsmi"

            concat(
                objs=[
                    uspto_grants,
                    uspto_applications,
                ]
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
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
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
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
        Format the data from the `github` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version in [
            "v_15k_by_20170418_coley_c_w_et_al",
            "v_480k_or_mit_by_20171229_jin_w_et_al",
        ]:
            train = read_csv(
                filepath_or_buffer=Path(input_directory_path, "data", "train.txt"),
                sep="\t",
                header=None
            )

            train["file_name"] = "train.txt"

            valid = read_csv(
                filepath_or_buffer=Path(input_directory_path, "data", "valid.txt"),
                sep="\t",
                header=None
            )

            valid["file_name"] = "valid.txt"

            test = read_csv(
                filepath_or_buffer=Path(input_directory_path, "data", "test.txt"),
                sep="\t",
                header=None
            )

            test["file_name"] = "test.txt"

            concat(
                objs=[
                    train,
                    valid,
                    test,
                ]
            ).rename(
                columns={
                    0: "reaction_smiles",
                }
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
                        timestamp=datetime.now().strftime(
                            format="%Y%m%d%H%M%S"
                        ),
                        version=version
                    )
                ),
                index=False
            )

        else:
            read_csv(
                filepath_or_buffer=Path(input_directory_path, "data_processed.csv"),
                header=0,
                index_col=0
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
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
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

    def _format_ibm_box(
            self,
            version: str,
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `ibm_box` versions of the chemical reaction dataset.

        :parameter version: The version of the chemical reaction dataset.
        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        if self.logger is not None:
            self.logger.info(
                msg="The formatting of the {data_source:s} has been started.".format(
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
                        version=version
                    )
                )
            )

        if version == "v_480k_or_mit_by_20180622_schwaller_p_et_al":
            train = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "ReactionSeq2Seq_Dataset",
                    "Jin_USPTO_1product_train.txt"
                ),
                sep="\t",
                header=None,
                skiprows=[0, ]
            )

            train["file_name"] = "Jin_USPTO_1product_train.txt"

            valid = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "ReactionSeq2Seq_Dataset",
                    "Jin_USPTO_1product_valid.txt"
                ),
                sep="\t",
                header=None,
                skiprows=[0, ]
            )

            valid["file_name"] = "Jin_USPTO_1product_valid.txt"

            test = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "ReactionSeq2Seq_Dataset",
                    "Jin_USPTO_1product_test.txt"
                ),
                sep="\t",
                header=None,
                skiprows=[0, ]
            )

            test["file_name"] = "Jin_USPTO_1product_test.txt"

            concat(
                objs=[
                    train,
                    valid,
                    test,
                ]
            ).rename(
                columns={
                    0: "reaction_smiles",
                }
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
                        timestamp=datetime.now().strftime(
                            format="%Y%m%d%H%M%S"
                        ),
                        version=version
                    )
                ),
                index=False
            )

        elif version == "v_stereo_by_20180622_schwaller_p_et_al":
            train = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "ReactionSeq2Seq_Dataset",
                    "US_patents_1976-Sep2016_1product_reactions_test.csv"
                ),
                sep="\t",
                header=2
            )

            train["FileName"] = "US_patents_1976-Sep2016_1product_reactions_test.csv"

            valid = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "ReactionSeq2Seq_Dataset",
                    "US_patents_1976-Sep2016_1product_reactions_valid.csv"
                ),
                sep="\t",
                header=2
            )

            valid["FileName"] = "US_patents_1976-Sep2016_1product_reactions_valid.csv"

            test = read_csv(
                filepath_or_buffer=Path(
                    input_directory_path,
                    "ReactionSeq2Seq_Dataset",
                    "US_patents_1976-Sep2016_1product_reactions_test.csv"
                ),
                sep="\t",
                header=2
            )

            test["FileName"] = "US_patents_1976-Sep2016_1product_reactions_test.csv"

            concat(
                objs=[
                    train,
                    valid,
                    test,
                ]
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
                        timestamp=datetime.now().strftime(
                            format="%Y%m%d%H%M%S"
                        ),
                        version=version
                    )
                ),
                index=False
            )

        else:
            valid = read_csv(
                filepath_or_buffer=Path(input_directory_path, "uspto_1k_TPL_train_valid.tsv"),
                sep="\t",
                header=0,
                index_col=0
            )

            valid["file_name"] = "uspto_1k_TPL_train_valid.tsv"

            test = read_csv(
                filepath_or_buffer=Path(input_directory_path, "uspto_1k_TPL_test.tsv"),
                sep="\t",
                header=0,
                index_col=0
            )

            test["file_name"] = "uspto_1k_TPL_test.tsv"

            concat(
                objs=[
                    valid,
                    test,
                ]
            ).to_csv(
                path_or_buf=Path(
                    output_directory_path,
                    "{timestamp:s}_uspto_{version:s}.csv".format(
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
                    data_source="USPTO chemical reaction dataset ({version:s})".format(
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

        :parameter version: The version of the chemical reaction dataset.
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

            elif version in self.available_versions["figshare"].keys():
                self._format_figshare(
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

            elif version in self.available_versions["ibm_box"].keys():
                self._format_ibm_box(
                    version=version,
                    input_directory_path=input_directory_path,
                    output_directory_path=output_directory_path
                )

            else:
                if self.logger is not None:
                    self.logger.warning(
                        msg="The {data_source:s} is not available.".format(
                            data_source="USPTO chemical reaction dataset ({version:s})".format(
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
