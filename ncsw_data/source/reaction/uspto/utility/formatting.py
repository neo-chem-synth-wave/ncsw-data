""" The ``ncsw_data.source.reaction.uspto.utility`` package ``formatting`` module. """

from datetime import datetime
from os import PathLike, walk
from pathlib import Path
from typing import List, Optional, Tuple, Union

from pandas import DataFrame, concat, read_csv

from pqdm.processes import pqdm

from xml.etree import ElementTree


class USPTOReactionDatasetFormattingUtility:
    """
    The `United States Patent and Trademark Office (USPTO) <https://www.repository.cam.ac.uk/handle/1810/244727>`_
    chemical reaction dataset formatting utility class.
    """

    @staticmethod
    def _parse_v_1976_to_2016_cml_by_20121009_lowe_d_m_file(
            file_path: Union[str, PathLike[str]]
    ) -> List[Tuple[Optional[Union[int, str]], ...]]:
        """
        Parse a file from the `v_1976_to_2016_cml_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter file_path: The path to the file that should be parsed.

        :returns: The chemical reaction data.
        """

        reaction_data = list()

        for reaction_xml_element in ElementTree.parse(
            source=file_path
        ).getroot():
            document_id = reaction_xml_element.find(
                path="{xml_element_name_prefix:s}{xml_element_name:s}".format(
                    xml_element_name_prefix="{http://bitbucket.org/dan2097}source/{http://bitbucket.org/dan2097}",
                    xml_element_name="documentId"
                )
            )

            paragraph_number = reaction_xml_element.find(
                path="{xml_element_name_prefix:s}{xml_element_name:s}".format(
                    xml_element_name_prefix="{http://bitbucket.org/dan2097}source/{http://bitbucket.org/dan2097}",
                    xml_element_name="paragraphNum"
                )
            )

            heading_text = reaction_xml_element.find(
                path="{xml_element_name_prefix:s}{xml_element_name:s}".format(
                    xml_element_name_prefix="{http://bitbucket.org/dan2097}source/{http://bitbucket.org/dan2097}",
                    xml_element_name="headingText"
                )
            )

            paragraph_text = reaction_xml_element.find(
                path="{xml_element_name_prefix:s}{xml_element_name:s}".format(
                    xml_element_name_prefix="{http://bitbucket.org/dan2097}source/{http://bitbucket.org/dan2097}",
                    xml_element_name="paragraphText"
                )
            )

            reaction_smiles = reaction_xml_element.find(
                path="{xml_element_name_prefix:s}{xml_element_name:s}".format(
                    xml_element_name_prefix="{http://bitbucket.org/dan2097}",
                    xml_element_name="reactionSmiles"
                )
            )

            reaction_data.append((
                int(file_path.split(
                    sep="/"
                )[-2]),
                document_id.text if document_id is not None else None,
                paragraph_number.text if paragraph_number is not None else None,
                heading_text.text if heading_text is not None else None,
                paragraph_text.text if paragraph_text is not None else None,
                reaction_smiles.text if reaction_smiles is not None else None,
            ))

        return reaction_data

    @staticmethod
    def format_v_1976_to_2016_cml_by_20121009_lowe_d_m(
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]],
            number_of_processes: int = 1
    ) -> None:
        """
        Format the data from the `v_1976_to_2016_cml_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        :parameter number_of_processes: The number of processes.
        """

        file_paths = list()

        for directory_name in [
            "grants",
            "applications",
        ]:
            for directory_path, _, file_names in walk(
                top=Path(input_directory_path, directory_name)
            ):
                for file_name in file_names:
                    if file_name.endswith(".xml"):
                        file_paths.append(
                            Path(directory_path, file_name).resolve().as_posix()
                        )

        dataframe_rows = list()

        for reaction_data in pqdm(
            array=file_paths,
            function=USPTOReactionDatasetFormattingUtility._parse_v_1976_to_2016_cml_by_20121009_lowe_d_m_file,
            n_jobs=number_of_processes,
            desc="Parsing the files",
            total=len(file_paths),
            ncols=150
        ):
            dataframe_rows.extend(
                reaction_data
            )

        DataFrame(
            data=dataframe_rows,
            columns=[
                "year",
                "document_id",
                "paragraph_number",
                "heading_text",
                "paragraph_text",
                "reaction_smiles",
            ]
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_v_1976_to_2016_cml_by_20121009_lowe_d_m.csv".format(
                    timestamp=datetime.now().strftime(
                        format="%Y%m%d%H%M%S"
                    )
                )
            ),
            index=False
        )

    @staticmethod
    def format_v_1976_to_2016_rsmi_by_20121009_lowe_d_m(
            input_directory_path: Union[str, PathLike[str]],
            output_directory_path: Union[str, PathLike[str]]
    ) -> None:
        """
        Format the data from the `v_1976_to_2016_rsmi_by_20121009_lowe_d_m` version of the chemical reaction dataset.

        :parameter input_directory_path: The path to the input directory where the data is extracted.
        :parameter output_directory_path: The path to the output directory where the data should be formatted.
        """

        dataframes = list()

        for file_name in [
            "1976_Sep2016_USPTOgrants_smiles.rsmi",
            "2001_Sep2016_USPTOapplications_smiles.rsmi",
        ]:
            dataframe = read_csv(
                filepath_or_buffer=Path(input_directory_path, file_name),
                sep="\t",
                header=0,
                low_memory=False
            )

            dataframe["FileName"] = file_name

            dataframes.append(
                dataframe
            )

        concat(
            objs=dataframes
        ).to_csv(
            path_or_buf=Path(
                output_directory_path,
                "{timestamp:s}_v_1976_to_2016_rsmi_by_20121009_lowe_d_m.csv".format(
                    timestamp=datetime.now().strftime(
                        format="%Y%m%d%H%M%S"
                    )
                )
            ),
            index=False
        )
