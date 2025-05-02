""" The ``use_case.scripts`` directory ``update_workbench_data`` script. """

from argparse import ArgumentParser, Namespace
from functools import partial
from logging import Formatter, Logger, StreamHandler, getLogger
from multiprocessing import Pool, cpu_count
from typing import Iterable, List, Optional, Tuple

from ncsw_chemistry.compound.utility import CompoundFormattingUtility, CompoundStandardizationUtility
from ncsw_chemistry.reaction.utility import ReactionCompoundUtility, ReactionReactivityUtility

from ncsw_data.storage.cacs.sqlite_ import CaCSSQLiteDatabase


########################################################################################################################
# workbench_reaction_transformation_pattern
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


def extract_reaction_transformation_pattern_smarts(
        mapped_reaction_smiles: str,
        logger: Optional[Logger] = None
) -> Optional[Tuple[str, List[str], List[str], List[str]]]:
    """
    Extract the transformation pattern SMARTS string from a chemical reaction SMILES string.

    :parameter mapped_reaction_smiles: The SMILES string of the mapped chemical reaction.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The transformation pattern SMARTS string extracted from the chemical reaction SMILES string.
    """

    try:
        (
            reaction_reactant_compound_smiles_strings,
            _,
            reaction_product_compound_smiles_strings,
        ) = ReactionCompoundUtility.extract_compound_smiles_or_smarts(
            reaction_smiles_or_smarts=mapped_reaction_smiles
        )

        reaction_transformation_pattern_smarts = ReactionReactivityUtility.extract_retro_template_using_rdchiral(
            mapped_reactant_compound_smiles_strings=reaction_reactant_compound_smiles_strings,
            mapped_product_compound_smiles=reaction_product_compound_smiles_strings[0]
        )

        if reaction_transformation_pattern_smarts is None:
            return None

        processed_reaction_reactant_compound_smiles_strings = [
            processed_reaction_reactant_compound_smiles
            for processed_reaction_reactant_compound_smiles in [
                process_reaction_compound_smiles(
                    compound_smiles=reaction_reactant_compound_smiles
                ) for reaction_reactant_compound_smiles in reaction_reactant_compound_smiles_strings
            ] if processed_reaction_reactant_compound_smiles is not None
        ]

        processed_reaction_product_compound_smiles = process_reaction_compound_smiles(
            compound_smiles=reaction_product_compound_smiles_strings[0]
        )

        if (
            None in processed_reaction_reactant_compound_smiles_strings or
            processed_reaction_product_compound_smiles is None
        ):
            return None

        reaction_transformation_pattern_outcomes_smiles_strings = (
            ReactionReactivityUtility.apply_retro_template_using_rdchiral(
                retro_template_smarts=reaction_transformation_pattern_smarts,
                compound_smiles=processed_reaction_product_compound_smiles
            )
        )

        processed_reaction_transformation_pattern_outcomes_smiles_strings = set()

        for reaction_transformation_pattern_outcomes_smiles in reaction_transformation_pattern_outcomes_smiles_strings:
            processed_reaction_transformation_pattern_outcome_smiles_strings = list()

            for reaction_transformation_pattern_outcome_smiles in reaction_transformation_pattern_outcomes_smiles.split(
                sep="."
            ):
                processed_reaction_transformation_pattern_outcome_smiles = process_reaction_compound_smiles(
                    compound_smiles=reaction_transformation_pattern_outcome_smiles
                )

                if processed_reaction_transformation_pattern_outcome_smiles is not None:
                    processed_reaction_transformation_pattern_outcome_smiles_strings.append(
                        processed_reaction_transformation_pattern_outcome_smiles
                    )

            processed_reaction_transformation_pattern_outcomes_smiles_strings.add(
                frozenset(processed_reaction_transformation_pattern_outcome_smiles_strings)
            )

        if (
            frozenset(processed_reaction_reactant_compound_smiles_strings) in
            processed_reaction_transformation_pattern_outcomes_smiles_strings
        ):
            (
                reaction_reactant_compound_patterns_smarts_strings,
                reaction_spectator_compound_patterns_smarts_strings,
                reaction_product_compound_patterns_smarts_strings,
            ) = ReactionCompoundUtility.extract_compound_smiles_or_smarts(
                reaction_smiles_or_smarts=reaction_transformation_pattern_smarts
            )

            processed_reaction_reactant_compound_patterns_smarts_strings = [
                processed_reaction_reactant_compound_patterns_smarts
                for processed_reaction_reactant_compound_patterns_smarts in [
                    process_reaction_compound_pattern_smarts(
                        compound_pattern_smarts=reaction_reactant_compound_patterns_smarts
                    ) for reaction_reactant_compound_patterns_smarts
                    in reaction_reactant_compound_patterns_smarts_strings
                ] if processed_reaction_reactant_compound_patterns_smarts is not None
            ]

            processed_reaction_spectator_compound_patterns_smarts_strings = [
                processed_reaction_spectator_compound_patterns_smarts
                for processed_reaction_spectator_compound_patterns_smarts in [
                    process_reaction_compound_pattern_smarts(
                        compound_pattern_smarts=reaction_spectator_compound_patterns_smarts
                    ) for reaction_spectator_compound_patterns_smarts
                    in reaction_spectator_compound_patterns_smarts_strings
                ] if processed_reaction_spectator_compound_patterns_smarts is not None
            ]

            processed_reaction_product_compound_patterns_smarts_strings = [
                processed_reaction_product_compound_patterns_smarts
                for processed_reaction_product_compound_patterns_smarts in [
                    process_reaction_compound_pattern_smarts(
                        compound_pattern_smarts=reaction_product_compound_patterns_smarts
                    ) for reaction_product_compound_patterns_smarts
                    in reaction_product_compound_patterns_smarts_strings
                ] if processed_reaction_product_compound_patterns_smarts is not None
            ]

            return (
                reaction_transformation_pattern_smarts,
                processed_reaction_reactant_compound_patterns_smarts_strings,
                processed_reaction_spectator_compound_patterns_smarts_strings,
                processed_reaction_product_compound_patterns_smarts_strings,
            )

        else:
            return None

    except Exception as exception_handle:
        if logger is not None:
            logger.error(
                msg=(
                    "The extraction of the chemical reaction transformation pattern from the chemical reaction SMILES "
                    "string '{mapped_reaction_smiles:s}' has been unsuccessful."
                ).format(
                    mapped_reaction_smiles=mapped_reaction_smiles
                )
            )

            logger.debug(
                msg=exception_handle,
                exc_info=True
            )

        return None


def extract_reaction_transformation_pattern_smarts_strings(
        mapped_reaction_smiles_strings: Iterable[str],
        timeout_period_in_s: int = 10,
        number_of_processes: int = 1,
        logger: Optional[Logger] = None
) -> List[Optional[Tuple[str, List[str], List[str], List[str]]]]:
    """
    Extract the transformation pattern SMARTS strings from the chemical reaction SMILES strings.

    :parameter mapped_reaction_smiles_strings: The SMILES strings of the mapped chemical reactions.
    :parameter timeout_period_in_s: The timeout period in seconds.
    :parameter number_of_processes: The number of processes.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The transformation pattern SMARTS strings extracted from the chemical reaction SMILES strings.
    """

    processed_reaction_pattern_smarts_strings = list()

    with Pool(
        processes=min(number_of_processes, cpu_count())
    ) as process_pool:
        async_results = list()

        for mapped_reaction_smiles in mapped_reaction_smiles_strings:
            async_results.append(
                process_pool.apply_async(
                    func=extract_reaction_transformation_pattern_smarts,
                    args=(mapped_reaction_smiles, ),
                    kwds={
                        "logger": logger
                    }
                )
            )

        for async_result in async_results:
            try:
                processed_reaction_pattern_smarts_strings.append(
                    async_result.get(
                        timeout=timeout_period_in_s
                    )
                )

            except Exception as exception_handle:
                if logger is not None:
                    logger.error(
                        msg=(
                            "The extraction of the chemical reaction transformation pattern from the chemical reaction SMILES "
                            "string '{mapped_reaction_smiles:s}' has been unsuccessful."
                        ).format(
                            mapped_reaction_smiles=mapped_reaction_smiles
                        )
                    )

                    logger.debug(
                        msg=exception_handle,
                        exc_info=True
                    )

                processed_reaction_pattern_smarts_strings.append(
                    None
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

    sqlite_database.extract_workbench_reaction_transformation_patterns(
        wrp_extraction_function=partial(
            extract_reaction_transformation_pattern_smarts_strings,
            number_of_processes=script_arguments.number_of_processes,
            logger=script_logger
        ),
        db_user=script_arguments.database_user,
        db_chunk_limit=script_arguments.database_chunk_limit
    )
