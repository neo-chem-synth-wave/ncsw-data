""" The ``use_case.scripts`` directory ``migrate_archive_to_workbench_data`` script. """

from argparse import ArgumentParser, Namespace
from functools import partial
from logging import Formatter, Logger, StreamHandler, getLogger
from multiprocessing import Pool, cpu_count
from typing import Iterable, List, Optional, Tuple

from ncsw_chemistry.compound.utility import CompoundFormattingUtility, CompoundStandardizationUtility
from ncsw_chemistry.reaction.utility import ReactionCompoundUtility

from rxnmapper.batched_mapper import BatchedMapper

from ncsw_data.storage.cacs.sqlite_ import CaCSSQLiteDatabase


########################################################################################################################
# workbench_compound
########################################################################################################################


def process_compound_smiles(
        compound_smiles: str,
        logger: Optional[Logger] = None
) -> Optional[str]:
    """
    Process the SMILES string of a chemical compound.

    :parameter compound_smiles: The SMILES string of the chemical compound.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMILES string of the chemical compound.
    """

    try:
        compound_mol = CompoundFormattingUtility.convert_compound_smiles_to_mol(
            compound_smiles=compound_smiles,
            remove_compound_atom_map_numbers=True,
            sanitize=False
        )

        CompoundStandardizationUtility.sanitize_compound(
            compound_mol=compound_mol,
            deep_copy=False
        )

        return CompoundFormattingUtility.convert_compound_mol_to_smiles(
            compound_mol=compound_mol
        )

    except Exception as exception_handle:
        if logger is not None:
            logger.error(
                msg=(
                    "The processing of the chemical compound SMILES string '{compound_smiles:s}' has been unsuccessful."
                ).format(
                    compound_smiles=compound_smiles
                )
            )

            logger.debug(
                msg=exception_handle,
                exc_info=True
            )

        return None


def process_compound_smiles_strings(
        compound_smiles_strings: Iterable[str],
        number_of_processes: int = 1,
        logger: Optional[Logger] = None
) -> List[Optional[str]]:
    """
    Process the SMILES strings of the chemical compounds.

    :parameter compound_smiles_strings: The SMILES strings of the chemical compounds.
    :parameter number_of_processes: The number of processes.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMILES strings of the chemical compounds.
    """

    processed_compound_smiles_strings = list()

    with Pool(
        processes=min(number_of_processes, cpu_count())
    ) as process_pool:
        for processed_compound_smiles in process_pool.map(
            func=partial(
                process_compound_smiles,
                logger=logger
            ),
            iterable=compound_smiles_strings
        ):
            processed_compound_smiles_strings.append(
                processed_compound_smiles
            )

        process_pool.close()
        process_pool.join()

    return processed_compound_smiles_strings


########################################################################################################################
# workbench_compound_pattern
########################################################################################################################


def process_compound_pattern_smarts(
        compound_pattern_smarts: str,
        logger: Optional[Logger] = None
) -> Optional[str]:
    """
    Process the SMARTS string of a chemical compound pattern.

    :parameter compound_pattern_smarts: The SMARTS string of the chemical compound pattern.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMARTS string of the chemical compound pattern.
    """

    try:
        compound_pattern_mol = CompoundFormattingUtility.convert_compound_smarts_to_mol(
            compound_smarts=compound_pattern_smarts,
            remove_compound_atom_map_numbers=True
        )

        return CompoundFormattingUtility.convert_compound_mol_to_smarts(
            compound_mol=compound_pattern_mol
        )

    except Exception as exception_handle:
        if logger is not None:
            logger.error(
                msg=(
                    "The processing of the chemical compound pattern SMARTS string '{compound_pattern_smarts:s}' has "
                    "been unsuccessful."
                ).format(
                    compound_pattern_smarts=compound_pattern_smarts
                )
            )

            logger.debug(
                msg=exception_handle,
                exc_info=True
            )

        return None


def process_compound_pattern_smarts_strings(
        compound_pattern_smarts_strings: Iterable[str],
        number_of_processes: int = 1,
        logger: Optional[Logger] = None
) -> List[Optional[str]]:
    """
    Process the SMARTS strings of the chemical compound patterns.

    :parameter compound_pattern_smarts_strings: The SMARTS strings of the chemical compound patterns.
    :parameter number_of_processes: The number of processes.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMARTS strings of the chemical compound patterns.
    """

    processed_compound_pattern_smarts_strings = list()

    with Pool(
        processes=min(number_of_processes, cpu_count())
    ) as process_pool:
        for processed_compound_pattern_smarts in process_pool.map(
            func=partial(
                process_compound_pattern_smarts,
                logger=logger
            ),
            iterable=compound_pattern_smarts_strings
        ):
            processed_compound_pattern_smarts_strings.append(
                processed_compound_pattern_smarts
            )

        process_pool.close()
        process_pool.join()

    return processed_compound_pattern_smarts_strings


########################################################################################################################
# workbench_reaction
########################################################################################################################


def process_reaction_compound_smiles(
        compound_smiles: str
) -> Optional[str]:
    """
    Process the SMILES string of a chemical reaction compound.

    :parameter compound_smiles: The SMILES string of the chemical reaction compound.

    :returns: The processed SMILES string of the chemical reaction compound.
    """

    reaction_compound_mol = CompoundFormattingUtility.convert_compound_smiles_to_mol(
        compound_smiles=compound_smiles,
        remove_compound_atom_map_numbers=True,
        sanitize=False
    )

    CompoundStandardizationUtility.sanitize_compound(
        compound_mol=reaction_compound_mol,
        deep_copy=False
    )

    return CompoundFormattingUtility.convert_compound_mol_to_smiles(
        compound_mol=reaction_compound_mol
    )


def pre_process_reaction_smiles(
        reaction_smiles: str,
        logger: Optional[Logger] = None
) -> Optional[str]:
    """
    Pre-process the SMILES string of a chemical reaction.

    :parameter reaction_smiles: The SMILES string of the chemical reaction.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The pre-processed SMILES string of the chemical reaction.
    """

    try:
        (
            reaction_reactant_compound_smiles_strings,
            reaction_spectator_compound_smiles_strings,
            reaction_product_compound_smiles_strings,
        ) = ReactionCompoundUtility.extract_compound_smiles_or_smarts(
            reaction_smiles_or_smarts=reaction_smiles
        )

        reaction_reactant_compound_smiles_strings += reaction_spectator_compound_smiles_strings

        if len(reaction_reactant_compound_smiles_strings) == 0 or len(reaction_product_compound_smiles_strings) == 0:
            return None

        pre_processed_reaction_reactant_compound_smiles_strings = [
            pre_processed_reaction_reactant_compound_smiles
            for pre_processed_reaction_reactant_compound_smiles in [
                process_reaction_compound_smiles(
                    compound_smiles=reaction_reactant_compound_smiles
                ) for reaction_reactant_compound_smiles in reaction_reactant_compound_smiles_strings
            ] if pre_processed_reaction_reactant_compound_smiles is not None
        ]

        pre_processed_reaction_product_compound_smiles_strings = [
            pre_processed_reaction_product_compound_smiles
            for pre_processed_reaction_product_compound_smiles in [
                process_reaction_compound_smiles(
                    compound_smiles=reaction_product_compound_smiles
                ) for reaction_product_compound_smiles in reaction_product_compound_smiles_strings
            ] if pre_processed_reaction_product_compound_smiles is not None
        ]

        if (
            len(pre_processed_reaction_reactant_compound_smiles_strings) == 0 or
            len(pre_processed_reaction_product_compound_smiles_strings) == 0
        ):
            return None

        return (
            "{pre_processed_reaction_reactant_compounds_smiles:s}>>{pre_processed_reaction_product_compounds_smiles:s}"
        ).format(
            pre_processed_reaction_reactant_compounds_smiles=".".join([
                pre_processed_reaction_reactant_compound_smiles
                for pre_processed_reaction_reactant_compound_smiles
                in pre_processed_reaction_reactant_compound_smiles_strings
            ]),
            pre_processed_reaction_product_compounds_smiles=".".join([
                pre_processed_reaction_product_compound_smiles
                for pre_processed_reaction_product_compound_smiles
                in pre_processed_reaction_product_compound_smiles_strings
            ])
        )

    except Exception as exception_handle:
        if logger is not None:
            logger.error(
                msg=(
                    "The pre-processing of the chemical reaction SMILES string '{reaction_smiles:s}' has been "
                    "unsuccessful."
                ).format(
                    reaction_smiles=reaction_smiles
                )
            )

            logger.debug(
                msg=exception_handle,
                exc_info=True
            )

        return None


def post_process_reaction_smiles(
        reaction_smiles: str,
        logger: Optional[Logger] = None
) -> Optional[List[Tuple[str, List[str], List[str], List[str]]]]:
    """
    Post-process the SMILES string of a chemical reaction.

    :parameter reaction_smiles: The SMILES string of the chemical reaction.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The post-processed SMILES string of the chemical reaction.
    """

    try:
        (
            reaction_reactant_compound_smiles_strings,
            _,
            reaction_product_compound_smiles_strings,
        ) = ReactionCompoundUtility.extract_compound_smiles_or_smarts(
            reaction_smiles_or_smarts=reaction_smiles
        )

        reaction_reactant_compound_mols = [
            CompoundFormattingUtility.convert_compound_smiles_to_mol(
                compound_smiles=reaction_reactant_compound_smiles
            ) for reaction_reactant_compound_smiles in reaction_reactant_compound_smiles_strings
        ]

        reaction_product_compound_mols = [
            CompoundFormattingUtility.convert_compound_smiles_to_mol(
                compound_smiles=reaction_product_compound_smiles
            ) for reaction_product_compound_smiles in reaction_product_compound_smiles_strings
        ]

        reaction_reactant_compound_atom_map_numbers = [{
            atom.GetAtomMapNum()
            for atom in reaction_reactant_compound_mol.GetAtoms()
            if atom.HasProp(
                key="molAtomMapNumber"
            )
        } for reaction_reactant_compound_mol in reaction_reactant_compound_mols]

        reaction_product_compound_atom_map_numbers = [{
            atom.GetAtomMapNum()
            for atom in reaction_product_compound_mol.GetAtoms()
            if atom.HasProp(
                key="molAtomMapNumber"
            )
        } for reaction_product_compound_mol in reaction_product_compound_mols]

        post_processed_reaction_smiles_strings = list()

        for reaction_product_compound_index in range(len(reaction_product_compound_smiles_strings)):
            if (
                reaction_product_compound_mols[reaction_product_compound_index] is None or
                len(reaction_product_compound_atom_map_numbers[reaction_product_compound_index]) == 0
            ):
                continue

            relevant_reaction_reactant_compound_indices = list()

            for reaction_reactant_compound_index in range(len(reaction_reactant_compound_smiles_strings)):
                if (
                    reaction_reactant_compound_mols[reaction_reactant_compound_index] is None or
                    len(reaction_reactant_compound_atom_map_numbers[reaction_reactant_compound_index]) == 0
                ):
                    continue

                if not reaction_reactant_compound_atom_map_numbers[reaction_reactant_compound_index].isdisjoint(
                    reaction_product_compound_atom_map_numbers[reaction_product_compound_index]
                ):
                    relevant_reaction_reactant_compound_indices.append(
                        reaction_reactant_compound_index
                    )

            if len(relevant_reaction_reactant_compound_indices) == 0:
                continue

            post_processed_reaction_smiles = (
                "{post_processed_reaction_reactant_compounds_smiles:s}>>"
                "{post_processed_reaction_product_compound_smiles:s}"
            ).format(
                post_processed_reaction_reactant_compounds_smiles=".".join([
                    CompoundFormattingUtility.convert_compound_mol_to_smiles(
                        compound_mol=reaction_reactant_compound_mols[relevant_reaction_reactant_compound_index]
                    ) for relevant_reaction_reactant_compound_index in relevant_reaction_reactant_compound_indices
                ]),
                post_processed_reaction_product_compound_smiles=(
                    CompoundFormattingUtility.convert_compound_mol_to_smiles(
                        compound_mol=reaction_product_compound_mols[reaction_product_compound_index]
                    )
                )
            )

            post_processed_reaction_reactant_compound_smiles_strings = [
                process_reaction_compound_smiles(
                    compound_smiles=reaction_reactant_compound_smiles_strings[relevant_reaction_reactant_compound_index]
                ) for relevant_reaction_reactant_compound_index in relevant_reaction_reactant_compound_indices
            ]

            if None in post_processed_reaction_reactant_compound_smiles_strings:
                continue

            post_processed_reaction_product_compound_smiles = process_reaction_compound_smiles(
                compound_smiles=reaction_product_compound_smiles_strings[reaction_product_compound_index]
            )

            if post_processed_reaction_product_compound_smiles is None:
                continue

            post_processed_reaction_smiles_strings.append((
                post_processed_reaction_smiles,
                post_processed_reaction_reactant_compound_smiles_strings,
                list(),
                [post_processed_reaction_product_compound_smiles, ],
            ))

        if len(post_processed_reaction_smiles_strings) == 0:
            return None

        return post_processed_reaction_smiles_strings

    except Exception as exception_handle:
        if logger is not None:
            logger.error(
                msg=(
                    "The post-processing of the chemical reaction SMILES string '{reaction_smiles:s}' has been "
                    "unsuccessful."
                ).format(
                    reaction_smiles=reaction_smiles
                )
            )

            logger.debug(
                msg=exception_handle,
                exc_info=True
            )

        return None


def process_reaction_smiles_strings(
        reaction_smiles_strings: Iterable[str],
        number_of_processes: int = 1,
        batch_size: int = 32,
        logger: Optional[Logger] = None
) -> List[Optional[List[Tuple[str, List[str], List[str], List[str]]]]]:
    """
    Process the SMILES strings of the chemical reactions.

    :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
    :parameter number_of_processes: The number of processes.
    :parameter batch_size: The size of the batch.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMILES strings of the chemical reactions.
    """

    pre_processed_reaction_smiles_strings = list()

    with Pool(
        processes=min(number_of_processes, cpu_count())
    ) as process_pool:
        for pre_processed_reaction_smiles in process_pool.map(
            func=partial(
                pre_process_reaction_smiles,
                logger=logger
            ),
            iterable=reaction_smiles_strings
        ):
            pre_processed_reaction_smiles_strings.append(
                pre_processed_reaction_smiles
            )

        process_pool.close()
        process_pool.join()

    batched_mapper = BatchedMapper(
        batch_size=batch_size
    )

    mapped_reaction_smiles_strings = batched_mapper.map_reactions(
        reaction_smiles=pre_processed_reaction_smiles_strings
    )

    post_processed_reaction_smiles_strings = list()

    with Pool(
        processes=min(number_of_processes, cpu_count())
    ) as process_pool:
        for post_processed_reaction_smiles in process_pool.map(
            func=partial(
                post_process_reaction_smiles,
                logger=logger
            ),
            iterable=mapped_reaction_smiles_strings
        ):
            post_processed_reaction_smiles_strings.append(
                post_processed_reaction_smiles
            )

        process_pool.close()
        process_pool.join()

    return post_processed_reaction_smiles_strings


########################################################################################################################
# workbench_reaction_pattern
########################################################################################################################


def process_reaction_compound_pattern_smarts(
        compound_pattern_smarts: str
) -> Optional[str]:
    """
    Process the SMARTS string of a chemical reaction compound pattern.

    :parameter compound_pattern_smarts: The SMARTS string of the chemical reaction compound pattern.

    :returns: The processed SMARTS string of the chemical reaction compound pattern.
    """

    reaction_compound_pattern_mol = CompoundFormattingUtility.convert_compound_smarts_to_mol(
        compound_smarts=compound_pattern_smarts,
        remove_compound_atom_map_numbers=True
    )

    return CompoundFormattingUtility.convert_compound_mol_to_smarts(
        compound_mol=reaction_compound_pattern_mol
    )


def process_reaction_pattern_smarts(
        reaction_pattern_smarts: str,
        logger: Optional[Logger] = None
) -> Optional[Tuple[str, List[str], List[str], List[str]]]:
    """
    Process the SMARTS string of a chemical reaction pattern.

    :parameter reaction_pattern_smarts: The SMARTS string of the chemical reaction pattern.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMARTS string of the chemical reaction pattern.
    """

    try:
        (
            reaction_pattern_reactant_compound_pattern_smarts_strings,
            reaction_pattern_spectator_compound_pattern_smarts_strings,
            reaction_pattern_product_compound_pattern_smarts_strings,
        ) = ReactionCompoundUtility.extract_compound_smiles_or_smarts(
            reaction_smiles_or_smarts=reaction_pattern_smarts
        )

        processed_reaction_pattern_reactant_compound_pattern_smarts_strings = [
            processed_reaction_pattern_reactant_compound_pattern_smarts
            for processed_reaction_pattern_reactant_compound_pattern_smarts in [
                process_reaction_compound_pattern_smarts(
                    compound_pattern_smarts=reaction_pattern_reactant_compound_pattern_smarts
                ) for reaction_pattern_reactant_compound_pattern_smarts
                in reaction_pattern_reactant_compound_pattern_smarts_strings
            ] if processed_reaction_pattern_reactant_compound_pattern_smarts is not None
        ]

        processed_reaction_pattern_spectator_compound_pattern_smarts_strings = [
            processed_reaction_pattern_spectator_compound_pattern_smarts
            for processed_reaction_pattern_spectator_compound_pattern_smarts in [
                process_reaction_compound_pattern_smarts(
                    compound_pattern_smarts=reaction_pattern_spectator_compound_pattern_smarts
                ) for reaction_pattern_spectator_compound_pattern_smarts
                in reaction_pattern_spectator_compound_pattern_smarts_strings
            ] if processed_reaction_pattern_spectator_compound_pattern_smarts is not None
        ]

        processed_reaction_pattern_product_compound_pattern_smarts_strings = [
            processed_reaction_pattern_product_compound_pattern_smarts
            for processed_reaction_pattern_product_compound_pattern_smarts in [
                process_reaction_compound_pattern_smarts(
                    compound_pattern_smarts=reaction_pattern_product_compound_pattern_smarts
                ) for reaction_pattern_product_compound_pattern_smarts
                in reaction_pattern_product_compound_pattern_smarts_strings
            ] if processed_reaction_pattern_product_compound_pattern_smarts is not None
        ]

        if (
            len(processed_reaction_pattern_reactant_compound_pattern_smarts_strings) == 0 or
            len(processed_reaction_pattern_product_compound_pattern_smarts_strings) == 0
        ):
            return None

        return (
            reaction_pattern_smarts,
            processed_reaction_pattern_reactant_compound_pattern_smarts_strings,
            processed_reaction_pattern_spectator_compound_pattern_smarts_strings,
            processed_reaction_pattern_product_compound_pattern_smarts_strings,
        )

    except Exception as exception_handle:
        if logger is not None:
            logger.error(
                msg=(
                    "The processing of the chemical reaction pattern SMARTS string '{reaction_pattern_smarts:s}' has "
                    "been unsuccessful."
                ).format(
                    reaction_pattern_smarts=reaction_pattern_smarts
                )
            )

            logger.debug(
                msg=exception_handle,
                exc_info=True
            )

        return None


def process_reaction_pattern_smarts_strings(
        reaction_pattern_smarts_strings: Iterable[str],
        number_of_processes: int = 1,
        logger: Optional[Logger] = None
) -> List[Optional[Tuple[str, List[str], List[str], List[str]]]]:
    """
    Process the SMARTS strings of the chemical reaction patterns.

    :parameter reaction_pattern_smarts_strings: The SMARTS strings of the chemical reaction patterns.
    :parameter number_of_processes: The number of processes.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The processed SMARTS strings of the chemical reaction patterns.
    """

    processed_reaction_pattern_smarts_strings = list()

    with Pool(
        processes=min(number_of_processes, cpu_count())
    ) as process_pool:
        for processed_reaction_pattern_smarts in process_pool.map(
            func=partial(
                process_reaction_pattern_smarts,
                logger=logger
            ),
            iterable=reaction_pattern_smarts_strings
        ):
            processed_reaction_pattern_smarts_strings.append(
                processed_reaction_pattern_smarts
            )

        process_pool.close()
        process_pool.join()

    return processed_reaction_pattern_smarts_strings


########################################################################################################################
# script
########################################################################################################################


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
        "-dsc",
        "--data_source_category",
        type=str,
        choices=[
            "compound",
            "compound_pattern",
            "reaction",
            "reaction_pattern",
        ],
        help="The indicator of the data source category."
    )

    argument_parser.add_argument(
        "-du",
        "--database_user",
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

    argument_parser.add_argument(
        "-nop",
        "--number_of_processes",
        default=1,
        type=int,
        help="The number of the processes, if relevant."
    )

    argument_parser.add_argument(
        "-bs",
        "--batch_size",
        default=10,
        type=int,
        help="The size of the batch, if relevant."
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

    if script_arguments.data_source_category == "compound":
        sqlite_database.migrate_archive_to_workbench_compounds(
            ac_standardization_function=partial(
                process_compound_smiles_strings,
                number_of_processes=script_arguments.number_of_processes,
                logger=script_logger
            ),
            wcs_are_building_blocks=True,
            as_names_versions_and_file_names=None,
            db_user=script_arguments.database_user,
            db_chunk_limit=script_arguments.database_chunk_limit
        )

    elif script_arguments.data_source_category == "compound_pattern":
        sqlite_database.migrate_archive_to_workbench_compound_patterns(
            acp_standardization_function=partial(
                process_compound_pattern_smarts_strings,
                number_of_processes=script_arguments.number_of_processes,
                logger=script_logger
            ),
            as_names_versions_and_file_names=None,
            db_user=script_arguments.database_user,
            db_chunk_limit=script_arguments.database_chunk_limit
        )

    elif script_arguments.data_source_category == "reaction":
        sqlite_database.migrate_archive_to_workbench_reactions(
            ar_standardization_function=partial(
                process_reaction_smiles_strings,
                number_of_processes=script_arguments.number_of_processes,
                batch_size=script_arguments.batch_size,
                logger=script_logger
            ),
            as_names_versions_and_file_names=None,
            db_user=script_arguments.database_user,
            db_chunk_limit=script_arguments.database_chunk_limit
        )

    elif script_arguments.data_source_category == "reaction_pattern":
        sqlite_database.migrate_archive_to_workbench_reaction_patterns(
            arp_standardization_function=partial(
                process_reaction_pattern_smarts_strings,
                number_of_processes=script_arguments.number_of_processes,
                logger=script_logger
            ),
            as_names_versions_and_file_names=None,
            db_user=script_arguments.database_user,
            db_chunk_limit=script_arguments.database_chunk_limit
        )

    else:
        script_logger.error(
            msg="The data source category '{category:s}' is not supported.".format(
                category=script_arguments.data_source_category
            )
        )
