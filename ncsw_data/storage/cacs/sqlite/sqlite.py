""" The ``ncsw_data.storage.cacs.sqlite`` package ``sqlite`` module. """

from logging import Logger
from math import ceil
from typing import Callable, Dict, Generator, Iterable, List, Optional, Sequence, Tuple, Union

from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import count

from tqdm.auto import tqdm

from ncsw_data.storage.base.base import DataStorageBase
from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.workbench import *
from ncsw_data.storage.cacs.sqlite.utility import *


class CaCSSQLiteDatabase(DataStorageBase):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database class. """

    ####################################################################################################################
    # Database
    ####################################################################################################################

    def __init__(
            self,
            url: str = "sqlite:///",
            logger: Optional[Logger] = None,
            **kwargs
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter url: The URL of the database. The value `sqlite:///` indicates that the database should be created in
            memory.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `sqlalchemy.engine.create.create_engine` }.
        """

        try:
            super().__init__(
                logger=logger
            )

            self.__database_engine = create_engine(
                url=url,
                **kwargs
            )

            self.__database_sessionmaker = sessionmaker(
                bind=self.__database_engine
            )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def create_tables(
            self,
            **kwargs
    ) -> None:
        """
        Create the tables of the database.

        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `sqlalchemy.sql.schema.MetaData.create_all` }.
        """

        CaCSSQLiteDatabaseModelBase.metadata.create_all(
            bind=self.__database_engine,
            **kwargs
        )

    def drop_tables(
            self,
            **kwargs
    ) -> None:
        """
        Drop the tables of the database.

        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `sqlalchemy.sql.schema.MetaData.drop_all` }.
        """

        CaCSSQLiteDatabaseModelBase.metadata.drop_all(
            bind=self.__database_engine,
            **kwargs
        )

    ####################################################################################################################
    # Archive Compounds
    ####################################################################################################################

    def insert_archive_compounds(
            self,
            archive_compound_smiles_strings: Sequence[str],
            archive_source_name: str,
            archive_source_version: str,
            archive_source_file_name: str,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical compounds into the database.

        :parameter archive_compound_smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter archive_source_name: The name of the archive source.
        :parameter archive_source_version: The version of the archive source.
        :parameter archive_source_file_name: The file name of the archive source.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been started.".format(
                        data="archive chemical compounds"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the {data:s} into the database".format(
                    data="archive chemical compounds"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, len(archive_compound_smiles_strings), database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(archive_compound_smiles_strings) / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_compound_smiles_strings_chunk = archive_compound_smiles_strings[
                        database_chunk_offset: min(
                            database_chunk_offset + database_chunk_limit,
                            len(archive_compound_smiles_strings)
                        )
                    ]

                    if len(archive_compound_smiles_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="archive chemical compounds",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            len(archive_compound_smiles_strings)
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_compounds(
                            database_session=database_session,
                            archive_compound_smiles_strings=archive_compound_smiles_strings_chunk,
                            archive_source_id=archive_source_id,
                            archive_compound_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been completed.".format(
                        data="archive chemical compounds"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_compounds(
            self,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveCompoundsTuple]]]:
        """
        Select the archive chemical compounds from the database.

        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compounds from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_compounds_query = CaCSSQLiteDatabaseSelectUtility.construct_archive_compounds_query()

                number_of_archive_compounds = database_session.scalar(
                    statement=archive_compounds_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveCompound.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_compounds, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_compounds_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_compounds_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveCompoundsFromSourcesTuple]]]:
        """
        Select the archive chemical compounds from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical compounds should be retrieved. The value `None` indicates that the
            archive chemical compounds should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compounds from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_compounds_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compounds_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_compounds_from_sources = database_session.scalar(
                    statement=archive_compounds_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveCompound.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_compounds_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_compounds_from_sources_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Workbench Compounds
    ####################################################################################################################

    def migrate_archive_to_workbench_compounds(
            self,
            archive_compound_standardization_function: Callable[[Sequence[str]], List[Optional[str]]],
            workbench_compounds_is_building_block: Union[bool, Sequence[bool]],
            archive_source_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]] = None,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical compounds from the archive to the workbench tables of the database.

        :parameter archive_compound_standardization_function: The standardization function of the archive chemical
            compounds.
        :parameter workbench_compounds_is_building_block: The boolean indicator or indicators of whether the workbench
            chemical compounds are building blocks.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical compounds should be retrieved. The value `None` indicates that the
            archive chemical compounds should be retrieved from all archive sources.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been started.".format(
                        data="chemical compounds from the archive to the workbench tables"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                archive_compounds_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compounds_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_compounds_from_sources = database_session.scalar(
                    statement=archive_compounds_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveCompound.id
                        )
                    ).distinct()
                )

                tqdm_description = "Migrating the {data:s} of the database".format(
                    data="chemical compounds from the archive to the workbench tables"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, number_of_archive_compounds_from_sources, database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_archive_compounds_from_sources / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_compounds = database_session.execute(
                        statement=archive_compounds_from_sources_query.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveCompound.id,
                            CaCSSQLiteDatabaseModelArchiveCompound.smiles
                        ).distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

                    standardized_archive_compounds = archive_compound_standardization_function([
                        archive_compound.smiles
                        for archive_compound in archive_compounds
                    ])

                    archive_compound_id_to_workbench_compound_smiles = dict()
                    workbench_compound_are_building_blocks = list()

                    for archive_compound_index, archive_compound in enumerate(archive_compounds):
                        if standardized_archive_compounds[archive_compound_index] is not None:
                            archive_compound_id_to_workbench_compound_smiles[
                                archive_compound.id
                            ] = standardized_archive_compounds[archive_compound_index]

                            if isinstance(workbench_compounds_is_building_block, bool):
                                workbench_compound_are_building_blocks.append(
                                    workbench_compounds_is_building_block
                                )

                            else:
                                workbench_compound_are_building_blocks.append(
                                    workbench_compounds_is_building_block[archive_compound_index]
                                )

                    if len(archive_compound_id_to_workbench_compound_smiles.keys()) == 0 or \
                            len(workbench_compound_are_building_blocks) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="workbench chemical compounds",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            number_of_archive_compounds_from_sources
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_compounds(
                            database_session=database_session,
                            archive_compound_id_to_workbench_compound_smiles=(
                                archive_compound_id_to_workbench_compound_smiles
                            ),
                            workbench_compound_are_building_blocks=workbench_compound_are_building_blocks,
                            workbench_compound_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been completed.".format(
                        data="chemical compounds from the archive to the workbench tables"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_compounds(
            self,
            workbench_compound_is_building_block: Optional[bool] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchCompoundsTuple]]]:
        """
        Select the workbench chemical compounds from the database.

        :parameter workbench_compound_is_building_block: The boolean indicator of whether the workbench building block
            chemical compounds should be retrieved. The value `None` indicates that the workbench chemical compounds
            should be retrieved irrespective of whether they are building blocks.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compounds from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_compounds_query = CaCSSQLiteDatabaseSelectUtility.construct_workbench_compounds_query(
                    workbench_compound_is_building_block=workbench_compound_is_building_block
                )

                number_of_workbench_compounds = database_session.scalar(
                    statement=workbench_compounds_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_compounds, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_compounds_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_compounds_from_sources(
            self,
            workbench_compound_is_building_block: Optional[bool] = None,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchCompoundsFromSourcesTuple]]]:
        """
        Select the workbench chemical compounds from sources in the database.

        :parameter workbench_compound_is_building_block: The boolean indicator of whether the workbench building block
            chemical compounds should be retrieved. The value `None` indicates that the workbench chemical compounds
            should be retrieved irrespective of whether they are building blocks.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical compounds should be retrieved. The value `None` indicates that the
            workbench chemical compounds should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compounds from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_compounds_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_compounds_from_sources_query(
                        workbench_compound_is_building_block=workbench_compound_is_building_block,
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_workbench_compounds_from_sources = database_session.scalar(
                    statement=workbench_compounds_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_workbench_compounds_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_compounds_from_sources_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Archive Reactions
    ####################################################################################################################

    def insert_archive_reactions(
            self,
            archive_reaction_smiles_strings: Sequence[str],
            archive_source_name: str,
            archive_source_version: str,
            archive_source_file_name: str,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical reactions into the database.

        :parameter archive_reaction_smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter archive_source_name: The name of the archive source.
        :parameter archive_source_version: The version of the archive source.
        :parameter archive_source_file_name: The file name of the archive source.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been started.".format(
                        data="archive chemical reactions"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the {data:s} into the database".format(
                    data="archive chemical reactions"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, len(archive_reaction_smiles_strings), database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(archive_reaction_smiles_strings) / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_reaction_smiles_strings_chunk = archive_reaction_smiles_strings[
                        database_chunk_offset: min(
                            database_chunk_offset + database_chunk_limit,
                            len(archive_reaction_smiles_strings)
                        )
                    ]

                    if len(archive_reaction_smiles_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="archive chemical reactions",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            len(archive_reaction_smiles_strings)
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_reactions(
                            database_session=database_session,
                            archive_reaction_smiles_strings=archive_reaction_smiles_strings_chunk,
                            archive_source_id=archive_source_id,
                            archive_reaction_created_by=database_user
                        )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_reactions(
            self,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveReactionsTuple]], None, None]:
        """
        Select the archive chemical reactions from the database.

        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reactions from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_reactions_query = CaCSSQLiteDatabaseSelectUtility.construct_archive_reactions_query()

                number_of_archive_reactions = database_session.scalar(
                    statement=archive_reactions_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveReaction.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_reactions, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_reactions_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_reactions_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveReactionsFromSourcesTuple]], None, None]:
        """
        Select the archive chemical reactions from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical reactions should be retrieved. The value `None` indicates that the
            archive chemical reactions should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reactions from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_reactions_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reactions_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_reactions_from_sources = database_session.scalar(
                    statement=archive_reactions_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveReaction.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_reactions_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_reactions_from_sources_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Workbench Reactions
    ####################################################################################################################

    def migrate_archive_to_workbench_reactions(
            self,
            archive_reaction_standardization_function: Callable[[Sequence[str]], List[Optional[List[Tuple[str, List[str], List[str], List[str]]]]]],
            archive_source_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]] = None,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical reactions from the archive to the workbench tables of the database.

        :parameter archive_reaction_standardization_function: The standardization function of the archive chemical
            reactions.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical reactions should be retrieved. The value `None` indicates that the
            archive chemical reactions should be retrieved from all archive sources.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been started.".format(
                        data="chemical reactions from the archive to the workbench tables"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                archive_reactions_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reactions_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_reactions_from_sources = database_session.scalar(
                    statement=archive_reactions_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveReaction.id
                        )
                    ).distinct()
                )

                tqdm_description = "Migrating the {data:s} of the database".format(
                    data="chemical reactions from the archive to the workbench tables"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, number_of_archive_reactions_from_sources, database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_archive_reactions_from_sources / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_reactions = database_session.execute(
                        statement=archive_reactions_from_sources_query.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveReaction.id,
                            CaCSSQLiteDatabaseModelArchiveReaction.smiles
                        ).distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

                    standardized_reaction_smiles_strings = archive_reaction_standardization_function([
                        archive_reaction.smiles
                        for archive_reaction in archive_reactions
                    ])

                    archive_reaction_id_to_workbench_reaction_smiles = dict()
                    archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings = dict()
                    archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings = dict()
                    archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings = dict()

                    for archive_reaction_index, archive_reaction in enumerate(archive_reactions):
                        if standardized_reaction_smiles_strings[archive_reaction_index] is not None:
                            for standardized_reaction_smiles in standardized_reaction_smiles_strings[archive_reaction_index]:
                                workbench_reaction_smiles, \
                                    workbench_reaction_reactant_compound_smiles_strings, \
                                    workbench_reaction_spectator_compound_smiles_strings, \
                                    workbench_reaction_product_compound_smiles_strings = standardized_reaction_smiles

                                archive_reaction_id_to_workbench_reaction_smiles[
                                    archive_reaction.id
                                ] = workbench_reaction_smiles

                                archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings[
                                    archive_reaction.id
                                ] = workbench_reaction_reactant_compound_smiles_strings

                                if len(workbench_reaction_spectator_compound_smiles_strings) > 0:
                                    archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings[
                                        archive_reaction.id
                                    ] = workbench_reaction_spectator_compound_smiles_strings

                                archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings[
                                    archive_reaction.id
                                ] = workbench_reaction_product_compound_smiles_strings

                    if len(archive_reaction_id_to_workbench_reaction_smiles.keys()) == 0 or \
                            len(archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings) == 0 or \
                            len(archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="workbench chemical reactions",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            number_of_archive_reactions_from_sources
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_reactions(
                            database_session=database_session,
                            archive_reaction_id_to_workbench_reaction_smiles=(
                                archive_reaction_id_to_workbench_reaction_smiles
                            ),
                            archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings=(
                                archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings
                            ),
                            archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings=(
                                archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings if
                                len(archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings.keys()) > 0
                                else None
                            ),
                            archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings=(
                                archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings
                            ),
                            workbench_reaction_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been completed.".format(
                        data="chemical reactions from the archive to the workbench tables"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_reactions(
            self,
            workbench_reaction_reactant_compound_smiles_strings: Optional[Iterable[str]] = None,
            workbench_reaction_spectator_compound_smiles_strings: Optional[Iterable[str]] = None,
            workbench_reaction_product_compound_smiles_strings: Optional[Iterable[str]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchReactionsTuple]], None, None]:
        """
        Select the workbench chemical reactions from the database.

        :parameter workbench_reaction_reactant_compound_smiles_strings: The reactant compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the reactant chemical compounds.
        :parameter workbench_reaction_spectator_compound_smiles_strings: The spectator compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the spectator chemical compounds.
        :parameter workbench_reaction_product_compound_smiles_strings: The product compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the product chemical compounds.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reactions from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_reactions_query = CaCSSQLiteDatabaseSelectUtility.construct_workbench_reactions_query(
                    workbench_reaction_reactant_compound_smiles_strings=(
                        workbench_reaction_reactant_compound_smiles_strings
                    ),
                    workbench_reaction_spectator_compound_smiles_strings=(
                        workbench_reaction_spectator_compound_smiles_strings
                    ),
                    workbench_reaction_product_compound_smiles_strings=(
                        workbench_reaction_product_compound_smiles_strings
                    ),
                )

                number_of_workbench_reactions = database_session.scalar(
                    statement=workbench_reactions_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchReaction.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_reactions, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_reactions_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_reactions_from_sources(
            self,
            workbench_reaction_reactant_compound_smiles_strings: Optional[Iterable[str]] = None,
            workbench_reaction_spectator_compound_smiles_strings: Optional[Iterable[str]] = None,
            workbench_reaction_product_compound_smiles_strings: Optional[Iterable[str]] = None,
            archive_source_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchReactionsFromSourcesTuple]], None, None]:
        """
        Select the workbench chemical reactions from sources of the database.

        :parameter workbench_reaction_reactant_compound_smiles_strings: The reactant compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the reactant chemical compounds.
        :parameter workbench_reaction_spectator_compound_smiles_strings: The spectator compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the spectator chemical compounds.
        :parameter workbench_reaction_product_compound_smiles_strings: The product compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the product chemical compounds.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical reactions should be retrieved. The value `None` indicates that the
            workbench chemical reactions should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reactions from sources of the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_reactions_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_reactions_from_sources_query(
                        workbench_reaction_reactant_compound_smiles_strings=(
                            workbench_reaction_reactant_compound_smiles_strings
                        ),
                        workbench_reaction_spectator_compound_smiles_strings=(
                            workbench_reaction_spectator_compound_smiles_strings
                        ),
                        workbench_reaction_product_compound_smiles_strings=(
                            workbench_reaction_product_compound_smiles_strings
                        ),
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_workbench_reactions_from_sources = database_session.scalar(
                    statement=workbench_reactions_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchReaction.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_reactions_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_reactions_from_sources_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Archive Compound Patterns
    ####################################################################################################################

    def insert_archive_compound_patterns(
            self,
            archive_compound_pattern_smarts_strings: Sequence[str],
            archive_source_name: str,
            archive_source_version: str,
            archive_source_file_name: str,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical compound patterns into the database.

        :parameter archive_compound_pattern_smarts_strings: The SMARTS strings of the archive chemical compound
            patterns.
        :parameter archive_source_name: The name of the archive source.
        :parameter archive_source_version: The version of the archive source.
        :parameter archive_source_file_name: The file name of the archive source.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been started.".format(
                        data="archive chemical compound patterns"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the {data:s} into the database".format(
                    data="archive chemical compound patterns"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, len(archive_compound_pattern_smarts_strings), database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(archive_compound_pattern_smarts_strings) / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_compound_pattern_smarts_strings_chunk = archive_compound_pattern_smarts_strings[
                        database_chunk_offset: min(
                            database_chunk_offset + database_chunk_limit,
                            len(archive_compound_pattern_smarts_strings)
                        )
                    ]

                    if len(archive_compound_pattern_smarts_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="archive chemical compound patterns",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            len(archive_compound_pattern_smarts_strings)
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_compound_patterns(
                            database_session=database_session,
                            archive_compound_pattern_smarts_strings=archive_compound_pattern_smarts_strings_chunk,
                            archive_source_id=archive_source_id,
                            archive_compound_pattern_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been completed.".format(
                        data="archive chemical compound patterns"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_compound_patterns(
            self,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveCompoundPatternsTuple]], None, None]:
        """
        Select the archive chemical compound patterns from the database.

        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compound patterns from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_compound_patterns_query = CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_patterns_query()

                number_of_archive_compound_patterns = database_session.scalar(
                    statement=archive_compound_patterns_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveCompoundPattern.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_compound_patterns, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_compound_patterns_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_compound_patterns_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveCompoundPatternsFromSourcesTuple]], None, None]:
        """
        Select the archive chemical compound patterns from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical compound patterns should be retrieved. The value `None` indicates
            that the archive chemical compound patterns should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compound patterns from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_compound_patterns_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_patterns_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_compound_patterns_from_sources = database_session.scalar(
                    statement=archive_compound_patterns_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveCompoundPattern.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_compound_patterns_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_compound_patterns_from_sources_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Workbench Compound Patterns
    ####################################################################################################################

    def migrate_archive_to_workbench_compound_patterns(
            self,
            archive_compound_pattern_standardization_function: Callable[[Sequence[str]], List[Optional[str]]],
            archive_source_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]] = None,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical compound patterns from the archive to the workbench tables of the database.

        :parameter archive_compound_pattern_standardization_function: The standardization function of the archive
            chemical compound patterns.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical compound patterns should be retrieved. The value `None` indicates
            that the chemical compound patterns should be retrieved from all archive sources.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been started.".format(
                        data="chemical compound patterns from the archive to the workbench tables"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                archive_compound_patterns_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_patterns_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_compound_patterns_from_sources = database_session.scalar(
                    statement=archive_compound_patterns_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveCompoundPattern.id
                        )
                    ).distinct()
                )

                tqdm_description = "Migrating the {data:s} of the database".format(
                    data="chemical compound patterns from the archive to the workbench tables"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, number_of_archive_compound_patterns_from_sources, database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_archive_compound_patterns_from_sources / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_compound_patterns = database_session.execute(
                        statement=archive_compound_patterns_from_sources_query.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                            CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts
                        ).distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

                    archive_compound_pattern_id_to_workbench_compound_pattern_smarts = dict()

                    standardized_compound_pattern_smarts_strings = archive_compound_pattern_standardization_function([
                        archive_compound_pattern.smarts
                        for archive_compound_pattern in archive_compound_patterns
                    ])

                    for archive_compound_pattern_index, archive_compound_pattern in enumerate(archive_compound_patterns):
                        if standardized_compound_pattern_smarts_strings[archive_compound_pattern_index] is not None:
                            archive_compound_pattern_id_to_workbench_compound_pattern_smarts[
                                archive_compound_pattern.id
                            ] = standardized_compound_pattern_smarts_strings[archive_compound_pattern_index]

                    if len(archive_compound_pattern_id_to_workbench_compound_pattern_smarts.keys()) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="workbench chemical compound patterns",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            number_of_archive_compound_patterns_from_sources
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_compound_patterns(
                            database_session=database_session,
                            archive_compound_pattern_id_to_workbench_compound_pattern_smarts=(
                                archive_compound_pattern_id_to_workbench_compound_pattern_smarts
                            ),
                            workbench_compound_pattern_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been completed.".format(
                        data="chemical compound patterns from the archive to the workbench tables"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_compound_patterns(
            self,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchCompoundPatternsTuple]], None, None]:
        """
        Select the workbench chemical compound patterns from the database.

        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compound patterns from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_compound_patterns_query = CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_patterns_query()

                number_of_workbench_compound_patterns = database_session.scalar(
                    statement=workbench_compound_patterns_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_compound_patterns, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_compound_patterns_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_compound_patterns_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchCompoundPatternsFromSourcesTuple]], None, None]:
        """
        Select the workbench chemical compound patterns from sources in the database.

        :parameter database_chunk_limit: The chunk limit of the database.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical compound patterns should be retrieved. The value `None` indicates
            that the workbench chemical compound patterns should be retrieved from all archive sources.

        :returns: The generator of the workbench chemical compound patterns from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_compound_patterns_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_patterns_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_workbench_compound_patterns_from_sources = database_session.scalar(
                    statement=workbench_compound_patterns_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_compound_patterns_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_compound_patterns_from_sources_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Archive Reaction Patterns
    ####################################################################################################################

    def insert_archive_reaction_patterns(
            self,
            archive_reaction_pattern_smarts_strings: Sequence[str],
            archive_source_name: str,
            archive_source_version: str,
            archive_source_file_name: str,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical reaction patterns into the database.

        :parameter archive_reaction_pattern_smarts_strings: The SMARTS strings of the archive chemical reaction
            patterns.
        :parameter archive_source_name: The name of the archive source.
        :parameter archive_source_version: The version of the archive source.
        :parameter archive_source_file_name: The file name of the archive source.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been started.".format(
                        data="archive chemical reaction patterns"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the {data:s} into the database".format(
                    data="archive chemical reaction patterns"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, len(archive_reaction_pattern_smarts_strings), database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(archive_reaction_pattern_smarts_strings) / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_reaction_pattern_smarts_strings_chunk = archive_reaction_pattern_smarts_strings[
                        database_chunk_offset: min(
                            database_chunk_offset + database_chunk_limit,
                            len(archive_reaction_pattern_smarts_strings)
                        )
                    ]

                    if len(archive_reaction_pattern_smarts_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="archive chemical reaction patterns",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            len(archive_reaction_pattern_smarts_strings)
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_reaction_patterns(
                            database_session=database_session,
                            archive_reaction_pattern_smarts_strings=archive_reaction_pattern_smarts_strings_chunk,
                            archive_source_id=archive_source_id,
                            archive_reaction_pattern_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the {data:s} into the database has been completed.".format(
                        data="archive chemical reaction patterns"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_reaction_patterns(
            self,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveReactionPatternsTuple]], None, None]:
        """
        Select the archive chemical reaction patterns from the database.

        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reaction patterns in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_reaction_patterns_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_patterns_query()

                number_of_archive_reaction_patterns = database_session.scalar(
                    statement=archive_reaction_patterns_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveReactionPattern.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_reaction_patterns, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_reaction_patterns_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_reaction_patterns_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[ArchiveReactionPatternsFromSourcesTuple]], None, None]:
        """
        Select the archive chemical reaction patterns from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical reaction patterns should be retrieved. The value `None` indicates
            that the archive chemical reaction patterns should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reaction patterns from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                archive_reaction_patterns_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_patterns_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_reaction_patterns_from_sources = database_session.scalar(
                    statement=archive_reaction_patterns_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveReactionPattern.id
                        )
                    ).distinct()
                )

                for database_chunk_offset in range(0, number_of_archive_reaction_patterns_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=archive_reaction_patterns_from_sources_query.distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Workbench Reaction Patterns
    ####################################################################################################################

    def migrate_archive_to_workbench_reaction_patterns(
            self,
            archive_reaction_pattern_standardization_function: Callable[[Sequence[str]], List[Optional[List[Tuple[str, List[str], List[str], List[str]]]]]],
            archive_source_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]] = None,
            database_user: str = "user",
            database_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical reaction patterns from the archive to the workbench tables of the database.

        :parameter archive_reaction_pattern_standardization_function: The standardization function of the archive
            chemical reaction patterns.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical reaction patterns should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved from all archive sources.
        :parameter database_user: The user of the database.
        :parameter database_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been started.".format(
                        data="chemical reaction patterns from the archive to the workbench tables"
                    )
                )

            with self.__database_sessionmaker() as database_session:
                archive_reaction_patterns_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_patterns_from_sources_query(
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_archive_reaction_patterns_from_sources = database_session.scalar(
                    statement=archive_reaction_patterns_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelArchiveReactionPattern.id
                        )
                    ).distinct()
                )

                tqdm_description = "Migrating the {data:s} of the database".format(
                    data="chemical reaction patterns from the archive to the workbench tables"
                )

                for database_chunk_offset in tqdm(
                    iterable=range(0, number_of_archive_reaction_patterns_from_sources, database_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_archive_reaction_patterns_from_sources / database_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    archive_reaction_patterns = database_session.execute(
                        statement=archive_reaction_patterns_from_sources_query.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                            CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts
                        ).distinct().limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

                    standardized_reaction_pattern_smarts_strings = archive_reaction_pattern_standardization_function([
                        archive_reaction_pattern.smiles
                        for archive_reaction_pattern in archive_reaction_patterns
                    ])

                    archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts = dict()
                    archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings = dict()
                    archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings = dict()
                    archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings = dict()

                    for archive_reaction_pattern_index, archive_reaction_pattern in enumerate(archive_reaction_patterns):
                        if standardized_reaction_pattern_smarts_strings[archive_reaction_pattern_index] is not None:
                            for standardized_reaction_pattern_smarts in standardized_reaction_pattern_smarts_strings[
                                archive_reaction_pattern_index
                            ]:
                                workbench_reaction_pattern_smarts, \
                                    workbench_reaction_reactant_compound_pattern_smarts_strings, \
                                    workbench_reaction_spectator_compound_pattern_smarts_strings, \
                                    workbench_reaction_product_compound_pattern_smarts_strings = standardized_reaction_pattern_smarts

                                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts[
                                    archive_reaction_pattern.id
                                ] = workbench_reaction_pattern_smarts

                                archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings[
                                    archive_reaction_pattern.id
                                ] = workbench_reaction_reactant_compound_pattern_smarts_strings

                                if len(workbench_reaction_spectator_compound_pattern_smarts_strings) > 0:
                                    archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings[
                                        archive_reaction_pattern.id
                                    ] = workbench_reaction_spectator_compound_pattern_smarts_strings

                                archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings[
                                    archive_reaction_pattern.id
                                ] = workbench_reaction_product_compound_pattern_smarts_strings

                    if len(archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts.keys()) == 0 or \
                            len(archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings) == 0 or \
                            len(archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg="The {data:s} chunk {data_chunk:s} is empty and has been skipped.".format(
                                    data="workbench chemical reaction patterns",
                                    data_chunk="[{data_chunk_start_index:d}, {data_chunk_end_index:d})".format(
                                        data_chunk_start_index=database_chunk_offset,
                                        data_chunk_end_index=min(
                                            database_chunk_offset + database_chunk_limit,
                                            number_of_archive_reaction_patterns_from_sources
                                        )
                                    )
                                )
                            )

                        continue

                    with database_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_reaction_patterns(
                            database_session=database_session,
                            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts=(
                                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts
                            ),
                            archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings=(
                                archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings
                            ),
                            archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings=(
                                archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings if
                                len(archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings.keys()) > 0
                                else None
                            ),
                            archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings=(
                                archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings
                            ),
                            workbench_reaction_pattern_created_by=database_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The migration of the {data:s} of the database has been completed.".format(
                        data="chemical reaction patterns from the archive to the workbench tables"
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_reaction_patterns(
            self,
            workbench_reaction_pattern_reactant_compound_smarts_strings: Optional[Iterable[str]] = None,
            workbench_reaction_pattern_spectator_compound_smarts_strings: Optional[Iterable[str]] = None,
            workbench_reaction_pattern_product_compound_smarts_strings: Optional[Iterable[str]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchReactionPatternsTuple]], None, None]:
        """
        Select the workbench chemical reaction patterns from the database.

        :parameter workbench_reaction_pattern_reactant_compound_smarts_strings: The reactant compound pattern SMARTS
            strings of the workbench chemical reaction patterns that should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved regardless of the reactant chemical
            compound patterns.
        :parameter workbench_reaction_pattern_spectator_compound_smarts_strings: The spectator compound pattern SMARTS
            strings of the workbench chemical reaction patterns that should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved regardless of the spectator chemical
            compound patterns.
        :parameter workbench_reaction_pattern_product_compound_smarts_strings: The product compound pattern SMARTS
            strings of the workbench chemical reaction patterns that should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved regardless of the product chemical
            compound patterns.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reaction patterns from the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_reaction_patterns_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_patterns_query(
                        workbench_reaction_pattern_reactant_compound_smarts_strings=(
                            workbench_reaction_pattern_reactant_compound_smarts_strings
                        ),
                        workbench_reaction_pattern_spectator_compound_smarts_strings=(
                            workbench_reaction_pattern_spectator_compound_smarts_strings
                        ),
                        workbench_reaction_pattern_product_compound_smarts_strings=(
                            workbench_reaction_pattern_product_compound_smarts_strings
                        ),
                    )

                number_of_workbench_reaction_patterns = database_session.scalar(
                    statement=workbench_reaction_patterns_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_reaction_patterns, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_reaction_patterns_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_workbench_reaction_patterns_from_sources(
            self,
            workbench_reaction_pattern_reactant_compound_smarts_strings: Optional[Iterable[str]] = None,
            workbench_reaction_pattern_spectator_compound_smarts_strings: Optional[Iterable[str]] = None,
            workbench_reaction_pattern_product_compound_smarts_strings: Optional[Iterable[str]] = None,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[WorkbenchReactionPatternsFromSourcesTuple]], None, None]:
        """
        Select the workbench chemical reaction patterns from sources in the database.

        :parameter workbench_reaction_pattern_reactant_compound_smarts_strings: The reactant compound pattern SMARTS
            strings of the workbench chemical reaction patterns that should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved regardless of the reactant chemical
            compound patterns.
        :parameter workbench_reaction_pattern_spectator_compound_smarts_strings: The spectator compound pattern SMARTS
            strings of the workbench chemical reaction patterns that should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved regardless of the spectator chemical
            compound patterns.
        :parameter workbench_reaction_pattern_product_compound_smarts_strings: The product compound pattern SMARTS
            strings of the workbench chemical reaction patterns that should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved regardless of the product chemical
            compound patterns.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical reaction patterns should be retrieved. The value `None` indicates
            that the workbench chemical reaction patterns should be retrieved from all archive sources.
        :parameter database_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reaction patterns from sources in the database.
        """

        try:
            with self.__database_sessionmaker() as database_session:
                workbench_reaction_patterns_from_sources_query = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_patterns_from_sources_query(
                        workbench_reaction_pattern_reactant_compound_smarts_strings=(
                            workbench_reaction_pattern_reactant_compound_smarts_strings
                        ),
                        workbench_reaction_pattern_spectator_compound_smarts_strings=(
                            workbench_reaction_pattern_spectator_compound_smarts_strings
                        ),
                        workbench_reaction_pattern_product_compound_smarts_strings=(
                            workbench_reaction_pattern_product_compound_smarts_strings
                        ),
                        archive_source_names_versions_and_file_names=archive_source_names_versions_and_file_names
                    )

                number_of_workbench_reaction_patterns_from_sources = database_session.scalar(
                    statement=workbench_reaction_patterns_from_sources_query.with_only_columns(
                        count(
                            expression=CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                        )
                    )
                )

                for database_chunk_offset in range(0, number_of_workbench_reaction_patterns_from_sources, database_chunk_limit):
                    yield database_session.execute(
                        statement=workbench_reaction_patterns_from_sources_query.limit(
                            limit=database_chunk_limit
                        ).offset(
                            offset=database_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # Workbench Chemical Synthesis Routes
    ####################################################################################################################

    def select_reversed_synthesis_routes_of_workbench_compound(
            self,
            workbench_compound_id_or_smiles: Union[int, str],
            reversed_synthesis_routes_maximum_depth: int = 10
    ) -> List[Dict[str, Union[None, bool, int, str]]]:
        """
        Select the reversed chemical synthesis routes of a workbench chemical compound from the database.

        :parameter workbench_compound_id_or_smiles: The ID or SMILES string of the workbench chemical compound.
        :parameter reversed_synthesis_routes_maximum_depth: The maximum depth of the reversed chemical synthesis routes.

        :returns: The generator of reversed chemical synthesis routes of the workbench chemical compound from the
            database.
        """

        try:
            reversed_synthesis_routes_of_workbench_compound_query = \
                CaCSSQLiteDatabaseSelectUtility.construct_reversed_synthesis_routes_of_workbench_compound_query(
                    workbench_compound_id_or_smiles=workbench_compound_id_or_smiles,
                    reversed_synthesis_routes_maximum_depth=reversed_synthesis_routes_maximum_depth
                )

            reversed_synthesis_routes_of_workbench_compound = list()

            with self.__database_sessionmaker() as session:
                for reversed_synthesis_route_of_workbench_compound in session.execute(
                    statement=reversed_synthesis_routes_of_workbench_compound_query,
                    params={
                        "workbench_compound_id_or_smiles": workbench_compound_id_or_smiles,
                        "reversed_synthesis_routes_maximum_depth": reversed_synthesis_routes_maximum_depth,
                    }
                ).all():
                    reversed_synthesis_routes_of_workbench_compound.append(
                        dict(reversed_synthesis_route_of_workbench_compound._mapping)
                    )

            return reversed_synthesis_routes_of_workbench_compound

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    ####################################################################################################################
