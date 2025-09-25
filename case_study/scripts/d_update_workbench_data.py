""" The ``case_study.scripts`` directory ``d_update_workbench_data`` script. """

from argparse import ArgumentParser, Namespace
from functools import partial
from logging import Formatter, Logger, StreamHandler, getLogger
from multiprocessing import Process, Queue, cpu_count
from typing import Iterable, List, Optional, Tuple

from multiprocessing.dummy import Pool

from rdchiral.main import rdchiralReactants, rdchiralReaction, rdchiralRun
from rdchiral.template_extractor import extract_from_reaction

from rdkit.Chem import MolFromSmarts, MolFromSmiles, MolToSmarts, MolToSmiles, SanitizeMol

from ncsw_data.storage.cacs.sqlite_db import CaCSSQLiteDatabase


########################################################################################################################
# workbench_reaction_transformation_pattern
########################################################################################################################


def extract_compound_smiles_or_smarts(
        reaction_smiles_or_smarts: str
) -> Tuple[List[str], List[str], List[str]]:
    """
    Extract the compound SMILES or SMARTS strings from a chemical reaction.

    :parameter reaction_smiles_or_smarts: The SMILES or SMARTS string of the chemical reaction.

    :returns: The extracted compound SMILES or SMARTS strings from the chemical reaction.
    """

    compound_smiles_or_smarts_strings = (list(), list(), list(), )

    for compounds_index, compounds_smiles_or_smarts in enumerate(reaction_smiles_or_smarts.split(
        sep=">"
    )):
        if compounds_smiles_or_smarts != "":
            for compound_smiles_or_smarts in compounds_smiles_or_smarts.split()[0].split(
                sep="."
            ):
                if compound_smiles_or_smarts != "":
                    compound_smiles_or_smarts_strings[compounds_index].append(
                        compound_smiles_or_smarts
                    )

    return compound_smiles_or_smarts_strings


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
        compound_mol = MolFromSmiles(
            SMILES=compound_smiles,
            sanitize=False
        )

        for atom in compound_mol.GetAtoms():
            atom.ClearProp(
                key="molAtomMapNumber"
            )

        SanitizeMol(
            compound_mol
        )

        return MolToSmiles(
            mol=compound_mol
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
        compound_pattern_mol = MolFromSmarts(
            SMARTS=compound_pattern_smarts
        )

        for atom in compound_pattern_mol.GetAtoms():
            atom.ClearProp(
                key="molAtomMapNumber"
            )

        return MolToSmarts(
            mol=compound_pattern_mol
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


def extract_reaction_transformation_pattern_smarts(
        mapped_reaction_smiles: str,
        logger: Optional[Logger] = None
) -> Optional[List[Tuple[str, List[str], List[str], List[str]]]]:
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
        ) = extract_compound_smiles_or_smarts(
            reaction_smiles_or_smarts=mapped_reaction_smiles
        )

        reaction_transformation_pattern_smarts = extract_from_reaction({
            "_id": None,
            "reactants": ".".join(reaction_reactant_compound_smiles_strings),
            "products": reaction_product_compound_smiles_strings[0],
        }).get("reaction_smarts", None)

        if reaction_transformation_pattern_smarts is None:
            return None

        processed_reaction_reactant_compound_smiles_strings = [
            processed_reaction_reactant_compound_smiles
            for processed_reaction_reactant_compound_smiles in [
                process_compound_smiles(
                    compound_smiles=reaction_reactant_compound_smiles,
                    logger=logger
                ) for reaction_reactant_compound_smiles in reaction_reactant_compound_smiles_strings
            ]
        ]

        processed_reaction_product_compound_smiles = process_compound_smiles(
            compound_smiles=reaction_product_compound_smiles_strings[0],
            logger=logger
        )

        if (
            None in processed_reaction_reactant_compound_smiles_strings or
            processed_reaction_product_compound_smiles is None
        ):
            return None

        reaction_transformation_pattern_outcomes_smiles_strings = rdchiralRun(
            rxn=rdchiralReaction(
                reaction_smarts=reaction_transformation_pattern_smarts
            ),
            reactants=rdchiralReactants(
                reactant_smiles=processed_reaction_product_compound_smiles
            )
        )

        processed_reaction_transformation_pattern_outcomes_smiles_strings = set()

        for reaction_transformation_pattern_outcomes_smiles in reaction_transformation_pattern_outcomes_smiles_strings:
            processed_reaction_transformation_pattern_outcome_smiles_strings = list()

            for reaction_transformation_pattern_outcome_smiles in reaction_transformation_pattern_outcomes_smiles.split(
                sep="."
            ):
                processed_reaction_transformation_pattern_outcome_smiles = process_compound_smiles(
                    compound_smiles=reaction_transformation_pattern_outcome_smiles,
                    logger=logger
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
            ) = extract_compound_smiles_or_smarts(
                reaction_smiles_or_smarts=reaction_transformation_pattern_smarts
            )

            processed_reaction_reactant_compound_patterns_smarts_strings = [
                processed_reaction_reactant_compound_patterns_smarts
                for processed_reaction_reactant_compound_patterns_smarts in [
                    process_compound_pattern_smarts(
                        compound_pattern_smarts=reaction_reactant_compound_patterns_smarts,
                        logger=logger
                    ) for reaction_reactant_compound_patterns_smarts
                    in reaction_reactant_compound_patterns_smarts_strings
                ] if processed_reaction_reactant_compound_patterns_smarts is not None
            ]

            processed_reaction_spectator_compound_patterns_smarts_strings = [
                processed_reaction_spectator_compound_patterns_smarts
                for processed_reaction_spectator_compound_patterns_smarts in [
                    process_compound_pattern_smarts(
                        compound_pattern_smarts=reaction_spectator_compound_patterns_smarts,
                        logger=logger
                    ) for reaction_spectator_compound_patterns_smarts
                    in reaction_spectator_compound_patterns_smarts_strings
                ] if processed_reaction_spectator_compound_patterns_smarts is not None
            ]

            processed_reaction_product_compound_patterns_smarts_strings = [
                processed_reaction_product_compound_patterns_smarts
                for processed_reaction_product_compound_patterns_smarts in [
                    process_compound_pattern_smarts(
                        compound_pattern_smarts=reaction_product_compound_patterns_smarts,
                        logger=logger
                    ) for reaction_product_compound_patterns_smarts
                    in reaction_product_compound_patterns_smarts_strings
                ] if processed_reaction_product_compound_patterns_smarts is not None
            ]

            return [(
                reaction_transformation_pattern_smarts,
                processed_reaction_reactant_compound_patterns_smarts_strings,
                processed_reaction_spectator_compound_patterns_smarts_strings,
                processed_reaction_product_compound_patterns_smarts_strings,
            ), ]

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


def extract_reaction_transformation_pattern_smarts_process(
        process_queue: Queue,
        mapped_reaction_smiles: str,
        logger: Optional[Logger] = None
) -> Optional[List[Tuple[str, List[str], List[str], List[str]]]]:
    """
    Extract the transformation pattern SMARTS string from a chemical reaction SMILES string.

    :parameter process_queue: The process queue.
    :parameter mapped_reaction_smiles: The SMILES string of the mapped chemical reaction.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

    :returns: The transformation pattern SMARTS string extracted from the chemical reaction SMILES string.
    """

    processed_reaction_pattern_smarts = None

    try:
        processed_reaction_pattern_smarts = extract_reaction_transformation_pattern_smarts(
            mapped_reaction_smiles=mapped_reaction_smiles,
            logger=logger
        )

    except:
        processed_reaction_pattern_smarts = None

    finally:
        process_queue.put(
            processed_reaction_pattern_smarts
        )


def extract_reaction_transformation_pattern_smarts_process_with_timeout(
    mapped_reaction_smiles: str,
    logger: Optional[Logger] = None,
    timeout_period_in_s: int = 10
) -> Optional[List[Tuple[str, List[str], List[str], List[str]]]]:
    """
    Extract the transformation pattern SMARTS string from a chemical reaction SMILES string.

    :parameter mapped_reaction_smiles: The SMILES string of the mapped chemical reaction.
    :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
    :parameter timeout_period_in_s: The timeout period in seconds.

    :returns: The transformation pattern SMARTS string extracted from the chemical reaction SMILES string.
    """

    process_queue = Queue()

    process = Process(
        target=extract_reaction_transformation_pattern_smarts_process,
        args=(
            process_queue,
            mapped_reaction_smiles,
            logger
        )
    )

    process.start()

    process.join(
        timeout=timeout_period_in_s
    )

    if process.is_alive():
        process.terminate()
        process.join()

        return None

    return process_queue.get()


def extract_reaction_transformation_pattern_smarts_strings(
        mapped_reaction_smiles_strings: Iterable[str],
        timeout_period_in_s: int = 10,
        number_of_processes: int = 1,
        logger: Optional[Logger] = None
) -> List[Optional[List[Tuple[str, List[str], List[str], List[str]]]]]:
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
                    func=extract_reaction_transformation_pattern_smarts_process_with_timeout,
                    args=(
                        mapped_reaction_smiles,
                        logger,
                        timeout_period_in_s,
                    )
                )
            )

        for async_result in async_results:
            try:
                processed_reaction_pattern_smarts_strings.append(
                    async_result.get()
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

    argument_parser.add_argument(
        "-nop",
        "--number_of_processes",
        default=1,
        type=int,
        help="The number of processes, if relevant."
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
