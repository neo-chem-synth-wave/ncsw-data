""" The ``case_study.scripts`` directory ``b_insert_archive_data`` script. """

from argparse import ArgumentParser, Namespace
from logging import Formatter, Logger, StreamHandler, getLogger

from pandas import read_csv

from ncsw_data.storage.cacs.sqlite_ import CaCSSQLiteDatabase


def get_script_arguments() -> Namespace:
    """
    Get the script arguments.

    :returns: The script arguments.
    """

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-sdfp",
        "--sqlite_database_file_path",
        type=str,
        help="The path to the SQLite database file."
    )

    argument_parser.add_argument(
        "-icfp",
        "--input_csv_file_path",
        type=str,
        help="The path to the input .csv file."
    )

    argument_parser.add_argument(
        "-soscn",
        "--smiles_or_smarts_column_name",
        type=str,
        help="The name of the SMILES or SMARTS string column."
    )

    argument_parser.add_argument(
        "-fncn",
        "--file_name_column_name",
        type=str,
        help="The name of the file name column."
    )

    argument_parser.add_argument(
        "-dsc",
        "--data_source_category",
        type=str,
        choices=[
            "compound",
            "compound_pattern",
            "reaction",
            "reaction_pattern",
        ],
        help="The category of the data source."
    )

    argument_parser.add_argument(
        "-dsn",
        "--data_source_name",
        type=str,
        help="The name of the data source."
    )

    argument_parser.add_argument(
        "-dsv",
        "--data_source_version",
        type=str,
        help="The version of the data source."
    )

    argument_parser.add_argument(
        "-du",
        "--database_user",
        default="admin",
        type=str,
        help="The user of the database."
    )

    argument_parser.add_argument(
        "-dcl",
        "--database_chunk_limit",
        default=10000,
        type=int,
        help="The chunk limit of the database."
    )

    return argument_parser.parse_args()


def get_script_logger() -> Logger:
    """
    Get the script logger.

    :returns: The script logger.
    """

    logger = getLogger(
        name="script_logger"
    )

    logger.setLevel(
        level="DEBUG"
    )

    formatter = Formatter(
        fmt="[{name:s} @ {asctime:s}] {levelname:s}: \"{message:s}\"",
        style="{"
    )

    stream_handler = StreamHandler()

    stream_handler.setLevel(
        level="DEBUG"
    )

    stream_handler.setFormatter(
        fmt=formatter
    )

    logger.addHandler(
        hdlr=stream_handler
    )

    return logger


if __name__ == "__main__":
    script_arguments = get_script_arguments()

    script_logger = get_script_logger()

    sqlite_database = CaCSSQLiteDatabase(
        db_url=script_arguments.sqlite_database_file_path,
        logger=script_logger
    )

    sqlite_database.create_tables()

    archive_dataframe = read_csv(
        filepath_or_buffer=script_arguments.input_csv_file_path,
        low_memory=False
    )

    if script_arguments.data_source_category == "compound":
        for file_name in archive_dataframe[script_arguments.file_name_column_name].unique():
            sqlite_database.insert_archive_compounds(
                ac_smiles_strings=archive_dataframe[
                    archive_dataframe[script_arguments.file_name_column_name] == file_name
                ][script_arguments.smiles_or_smarts_column_name].values.tolist(),
                as_name=script_arguments.data_source_name,
                as_version=script_arguments.data_source_version,
                as_file_name=file_name,
                db_user=script_arguments.database_user,
                db_chunk_limit=script_arguments.database_chunk_limit
            )

    elif script_arguments.data_source_category == "compound_pattern":
        for file_name in archive_dataframe[script_arguments.file_name_column_name].unique():
            sqlite_database.insert_archive_compound_patterns(
                acp_smarts_strings=archive_dataframe[
                    archive_dataframe[script_arguments.file_name_column_name] == file_name
                ][script_arguments.smiles_or_smarts_column_name].values.tolist(),
                as_name=script_arguments.data_source_name,
                as_version=script_arguments.data_source_version,
                as_file_name=file_name,
                db_user=script_arguments.database_user,
                db_chunk_limit=script_arguments.database_chunk_limit
            )

    elif script_arguments.data_source_category == "reaction":
        for file_name in archive_dataframe[script_arguments.file_name_column_name].unique():
            sqlite_database.insert_archive_reactions(
                ar_smiles_strings=archive_dataframe[
                    archive_dataframe[script_arguments.file_name_column_name] == file_name
                ][script_arguments.smiles_or_smarts_column_name].values.tolist(),
                as_name=script_arguments.data_source_name,
                as_version=script_arguments.data_source_version,
                as_file_name=file_name,
                db_user=script_arguments.database_user,
                db_chunk_limit=script_arguments.database_chunk_limit
            )

    elif script_arguments.data_source_category == "reaction_pattern":
        for file_name in archive_dataframe[script_arguments.file_name_column_name].unique():
            sqlite_database.insert_archive_reaction_patterns(
                arp_smarts_strings=archive_dataframe[
                    archive_dataframe[script_arguments.file_name_column_name] == file_name
                ][script_arguments.smiles_or_smarts_column_name].values.tolist(),
                as_name=script_arguments.data_source_name,
                as_version=script_arguments.data_source_version,
                as_file_name=file_name,
                db_user=script_arguments.database_user,
                db_chunk_limit=script_arguments.database_chunk_limit
            )

    else:
        script_logger.error(
            msg="The data source category '{category:s}' is not supported.".format(
                category=script_arguments.data_source_category
            )
        )
