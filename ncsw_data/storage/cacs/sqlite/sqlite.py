""" The ``ncsw_data.storage.cacs.sqlite`` package ``sqlite`` module. """

from logging import Logger
from math import ceil
from typing import Generator, Iterable, Optional, Sequence, Tuple

from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import count

from tqdm.auto import tqdm

from ncsw_data.storage.base.base import DataStorageBase
from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.utility import *


class CaCSSQLiteDatabase(DataStorageBase):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database class. """

    def __init__(
            self,
            database_url: str = "sqlite:///",
            logger: Optional[Logger] = None,
            **kwargs
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter database_url: The URL of the database.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `sqlalchemy.engine.create.create_engine` }.
        """

        try:
            super().__init__(
                logger=logger
            )

            self.__database_engine = create_engine(
                url=database_url,
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
            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the archive chemical compounds into the database"

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

                    with database_session.begin_nested():
                        archive_compound_smiles_to_id = \
                            CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_compounds(
                                database_session=database_session,
                                smiles_strings=archive_compound_smiles_strings_chunk,
                                created_by=database_user
                            )

                        CaCSSQLiteDatabaseInsertUtility.insert_archive_compound_sources(
                            database_session=database_session,
                            archive_compound_ids=archive_compound_smiles_to_id.values(),
                            archive_source_id=archive_source_id
                        )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

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
            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the archive chemical compound patterns into the database"

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

                    with database_session.begin_nested():
                        archive_compound_pattern_smarts_to_id = \
                            CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_compound_patterns(
                                database_session=database_session,
                                smarts_strings=archive_compound_pattern_smarts_strings_chunk,
                                created_by=database_user
                            )

                        CaCSSQLiteDatabaseInsertUtility.insert_archive_compound_pattern_sources(
                            database_session=database_session,
                            archive_compound_pattern_ids=archive_compound_pattern_smarts_to_id.values(),
                            archive_source_id=archive_source_id
                        )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

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
            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the archive chemical reactions into the database"

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

                    with database_session.begin_nested():
                        archive_reaction_smiles_to_id = \
                            CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_reactions(
                                database_session=database_session,
                                smiles_strings=archive_reaction_smiles_strings_chunk,
                                created_by=database_user
                            )

                        CaCSSQLiteDatabaseInsertUtility.insert_archive_reaction_sources(
                            database_session=database_session,
                            archive_reaction_ids=archive_reaction_smiles_to_id.values(),
                            archive_source_id=archive_source_id
                        )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

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
            with self.__database_sessionmaker() as database_session:
                with database_session.begin_nested():
                    archive_source_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        database_session=database_session,
                        name=archive_source_name,
                        version=archive_source_version,
                        file_name=archive_source_file_name,
                        created_by=database_user
                    )

                tqdm_description = "Inserting the archive chemical reaction patterns into the database"

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

                    with database_session.begin_nested():
                        archive_reaction_pattern_smarts_to_id = \
                            CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_reaction_patterns(
                                database_session=database_session,
                                smarts_strings=archive_reaction_pattern_smarts_strings_chunk,
                                created_by=database_user
                            )

                        CaCSSQLiteDatabaseInsertUtility.insert_archive_reaction_pattern_sources(
                            database_session=database_session,
                            archive_reaction_pattern_ids=archive_reaction_pattern_smarts_to_id.values(),
                            archive_source_id=archive_source_id
                        )

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
    ) -> Generator[Sequence[Row[Tuple[CaCSSQLiteDatabaseModelArchiveCompound, CaCSSQLiteDatabaseModelArchiveSource]]], None, None]:
        """
        Select the archive chemical compounds from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical compounds should be retrieved. The value `None` indicates that the chemical
            compounds should be retrieved from all archive sources.
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

    def select_archive_compound_patterns_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[Tuple[CaCSSQLiteDatabaseModelArchiveCompoundPattern, CaCSSQLiteDatabaseModelArchiveSource]]], None, None]:
        """
        Select the archive chemical compound patterns from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical compound patterns should be retrieved. The value `None` indicates that the
            chemical compound patterns should be retrieved from all archive sources.
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

    def select_archive_reactions_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[Tuple[CaCSSQLiteDatabaseModelArchiveReaction, CaCSSQLiteDatabaseModelArchiveSource]]], None, None]:
        """
        Select the archive chemical reactions from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical reactions should be retrieved. The value `None` indicates that the chemical
            reactions should be retrieved from all archive sources.
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

    def select_archive_reaction_patterns_from_sources(
            self,
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None,
            database_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[Tuple[CaCSSQLiteDatabaseModelArchiveReactionPattern, CaCSSQLiteDatabaseModelArchiveSource]]], None, None]:
        """
        Select the archive chemical reaction patterns from sources in the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical reaction patterns should be retrieved. The value `None` indicates that the
            chemical reaction patterns should be retrieved from all archive sources.
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
