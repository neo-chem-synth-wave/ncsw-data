""" The ``ncsw_data.storage.cacs.sqlite_`` package ``sqlite_`` module. """

from logging import Logger
from math import ceil
from typing import Collection, Generator, Iterable, Optional, Sequence, Tuple

from sqlalchemy.engine import Result, Row, create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import select, text
from sqlalchemy.sql.functions import count

from tqdm.auto import tqdm

from ncsw_data.storage.base.base import DataStorageBase

from ncsw_data.storage.cacs.sqlite_.model.archive.compound import CaCSSQLiteDatabaseModelArchiveCompound
from ncsw_data.storage.cacs.sqlite_.model.archive.compound_pattern import CaCSSQLiteDatabaseModelArchiveCompoundPattern
from ncsw_data.storage.cacs.sqlite_.model.archive.reaction import CaCSSQLiteDatabaseModelArchiveReaction
from ncsw_data.storage.cacs.sqlite_.model.archive.reaction_pattern import CaCSSQLiteDatabaseModelArchiveReactionPattern
from ncsw_data.storage.cacs.sqlite_.model.workbench.reaction import CaCSSQLiteDatabaseModelWorkbenchReaction

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite_.utility import *

from ncsw_data.storage.cacs.sqlite_.typing_ import (
    CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable,
    CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable,
    CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable,
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable,
    CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable,
)


class CaCSSQLiteDatabase(DataStorageBase):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database class. """

    ####################################################################################################################
    # database AS db
    ####################################################################################################################

    def __init__(
            self,
            db_url: str = "sqlite:///",
            logger: Optional[Logger] = None,
            **kwargs
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter db_url: The URL of the database. The value `sqlite:///` indicates that the SQLite database should be
            created in memory.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `sqlalchemy.engine.create.create_engine` }.
        """

        try:
            super().__init__(
                logger=logger
            )

            kwargs.pop("url", None)

            self.__db_engine = create_engine(
                url=db_url,
                **kwargs
            )

            self.__db_sessionmaker = sessionmaker(
                bind=self.__db_engine
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
            bind=self.__db_engine,
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
            bind=self.__db_engine,
            **kwargs
        )

    def execute_select_statement(
            self,
            select_statement_text: str
    ) -> Result:
        """
        Execute a select statement.

        :parameter select_statement_text: The text of the select statement.

        :returns: The result of the select statement.
        """

        try:
            with self.__db_sessionmaker() as database_session:
                return database_session.execute(
                    statement=text(
                        text=select_statement_text
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.exception(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # archive_compound AS ac
    ####################################################################################################################

    def insert_archive_compounds(
            self,
            ac_smiles_strings: Collection[str],
            as_name: str,
            as_version: str,
            as_file_name: str,
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical compounds into the database.

        :parameter ac_smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter as_name: The name of the archive source.
        :parameter as_version: The version of the archive source.
        :parameter as_file_name: The file name of the archive source.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the archive chemical compound data into the database has been started."
                )

            with self.__db_sessionmaker() as db_session:
                with db_session.begin_nested():
                    as_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        db_session=db_session,
                        as_name=as_name,
                        as_version=as_version,
                        as_file_name=as_file_name,
                        as_created_by=db_user
                    )

                tqdm_description = (
                    "Inserting the archive chemical compound data into the database (db_chunk_limit = "
                    "{db_chunk_limit:d})"
                ).format(
                    db_chunk_limit=db_chunk_limit
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, len(ac_smiles_strings), db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(ac_smiles_strings) / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    ac_smiles_strings_chunk = ac_smiles_strings[
                        db_chunk_offset: min(db_chunk_offset + db_chunk_limit, len(ac_smiles_strings))
                    ]

                    if len(ac_smiles_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The archive chemical compound data chunk [{data_chunk_start_index:d}, "
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(db_chunk_offset + db_chunk_limit, len(ac_smiles_strings))
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_compounds(
                            db_session=db_session,
                            acs=ac_smiles_strings_chunk,
                            as_id=as_id,
                            acs_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the archive chemical compound data into the database has been completed."
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_compounds(
            self,
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundTuple]], None, None]:
        """
        Select the archive chemical compounds from the database.

        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compounds from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                ac_select_statement = CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_select_statement()

                number_of_acs = db_session.scalar(
                    statement=ac_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_acs, db_chunk_limit):
                    yield db_session.execute(
                        statement=ac_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundFromSourceTuple]], None, None]:
        """
        Select the archive chemical compounds from sources in the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compounds should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compounds from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                ac_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_acs_from_sources = db_session.scalar(
                    statement=ac_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_acs_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=ac_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # archive_reaction AS ar
    ####################################################################################################################

    def insert_archive_reactions(
            self,
            ar_smiles_strings: Sequence[str],
            as_name: str,
            as_version: str,
            as_file_name: str,
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical reactions into the database.

        :parameter ar_smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter as_name: The name of the archive source.
        :parameter as_version: The version of the archive source.
        :parameter as_file_name: The file name of the archive source.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the archive chemical reaction data into the database has been started."
                )

            with self.__db_sessionmaker() as db_session:
                with db_session.begin_nested():
                    as_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        db_session=db_session,
                        as_name=as_name,
                        as_version=as_version,
                        as_file_name=as_file_name,
                        as_created_by=db_user
                    )

                tqdm_description = (
                    "Inserting the archive chemical reaction data into the database (db_chunk_limit = "
                    "{db_chunk_limit:d})"
                ).format(
                    db_chunk_limit=db_chunk_limit
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, len(ar_smiles_strings), db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(ar_smiles_strings) / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    ar_smiles_strings_chunk = ar_smiles_strings[
                        db_chunk_offset: min(db_chunk_offset + db_chunk_limit, len(ar_smiles_strings))
                    ]

                    if len(ar_smiles_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The archive chemical reaction data chunk [{data_chunk_start_index:d}, "
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(db_chunk_offset + db_chunk_limit, len(ar_smiles_strings))
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_reactions(
                            db_session=db_session,
                            ars=ar_smiles_strings_chunk,
                            as_id=as_id,
                            ars_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg="The insertion of the archive chemical reaction data into the database has been completed."
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    def select_archive_reactions(
            self,
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionTuple]], None, None]:
        """
        Select the archive chemical reactions from the database.

        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reactions from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                ar_select_statement = CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_select_statement()

                number_of_ars = db_session.scalar(
                    statement=ar_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_ars, db_chunk_limit):
                    yield db_session.execute(
                        statement=ar_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionFromSourceTuple]], None, None]:
        """
        Select the archive chemical reactions from sources in the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical reactions should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reactions from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                ar_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_ars_from_sources = db_session.scalar(
                    statement=ar_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_ars_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=ar_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # archive_compound_pattern AS acp
    ####################################################################################################################

    def insert_archive_compound_patterns(
            self,
            acp_smarts_strings: Sequence[str],
            as_name: str,
            as_version: str,
            as_file_name: str,
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical compound patterns into the database.

        :parameter acp_smarts_strings: The SMARTS strings of the archive chemical compound patterns.
        :parameter as_name: The name of the archive source.
        :parameter as_version: The version of the archive source.
        :parameter as_file_name: The file name of the archive source.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The insertion of the archive chemical compound pattern data into the database has been "
                        "started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                with db_session.begin_nested():
                    as_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        db_session=db_session,
                        as_name=as_name,
                        as_version=as_version,
                        as_file_name=as_file_name,
                        as_created_by=db_user
                    )

                tqdm_description = (
                    "Inserting the archive chemical compound pattern data into the database (db_chunk_limit = "
                    "{db_chunk_limit:d})"
                ).format(
                    db_chunk_limit=db_chunk_limit
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, len(acp_smarts_strings), db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(acp_smarts_strings) / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    acp_smarts_strings_chunk = acp_smarts_strings[
                        db_chunk_offset: min(db_chunk_offset + db_chunk_limit, len(acp_smarts_strings))
                    ]

                    if len(acp_smarts_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The archive chemical compound pattern data chunk [{data_chunk_start_index:d}, "
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(db_chunk_offset + db_chunk_limit, len(acp_smarts_strings))
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_compound_patterns(
                            db_session=db_session,
                            acps=acp_smarts_strings_chunk,
                            as_id=as_id,
                            acps_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The insertion of the archive chemical compound pattern data into the database has been "
                        "completed."
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
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundPatternTuple]], None, None]:
        """
        Select the archive chemical compound patterns from the database.

        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compound patterns from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                acp_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_pattern_select_statement()

                number_of_acps = db_session.scalar(
                    statement=acp_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_acps, db_chunk_limit):
                    yield db_session.execute(
                        statement=acp_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundPatternFromSourceTuple]], None, None]:
        """
        Select the archive chemical compound patterns from sources in the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compound patterns should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical compound patterns from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                acp_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_pattern_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_acps_from_sources = db_session.scalar(
                    statement=acp_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_acps_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=acp_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # archive_reaction_pattern AS arp
    ####################################################################################################################

    def insert_archive_reaction_patterns(
            self,
            arp_smarts_strings: Sequence[str],
            as_name: str,
            as_version: str,
            as_file_name: str,
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Insert the archive chemical reaction patterns into the database.

        :parameter arp_smarts_strings: The SMARTS strings of the archive chemical reaction patterns.
        :parameter as_name: The name of the archive source.
        :parameter as_version: The version of the archive source.
        :parameter as_file_name: The file name of the archive source.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The insertion of the archive chemical reaction pattern data into the database has been "
                        "started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                with db_session.begin_nested():
                    as_id = CaCSSQLiteDatabaseInsertUtility.insert_and_select_archive_source(
                        db_session=db_session,
                        as_name=as_name,
                        as_version=as_version,
                        as_file_name=as_file_name,
                        as_created_by=db_user
                    )

                tqdm_description = (
                    "Inserting the archive chemical reaction pattern data into the database (db_chunk_limit = "
                    "{db_chunk_limit:d})"
                ).format(
                    db_chunk_limit=db_chunk_limit
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, len(arp_smarts_strings), db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(len(arp_smarts_strings) / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    arp_smarts_strings_chunk = arp_smarts_strings[
                        db_chunk_offset: min(db_chunk_offset + db_chunk_limit, len(arp_smarts_strings))
                    ]

                    if len(arp_smarts_strings_chunk) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The archive chemical reaction pattern data chunk [{data_chunk_start_index:d}, "
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(db_chunk_offset + db_chunk_limit, len(arp_smarts_strings))
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_archive_reaction_patterns(
                            db_session=db_session,
                            arps=arp_smarts_strings_chunk,
                            as_id=as_id,
                            arps_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The insertion of the archive chemical reaction pattern data into the database has been "
                        "completed."
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
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionPatternTuple]], None, None]:
        """
        Select the archive chemical reaction patterns from the database.

        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reaction patterns from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                arp_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_pattern_select_statement()

                number_of_arps = db_session.scalar(
                    statement=arp_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_arps, db_chunk_limit):
                    yield db_session.execute(
                        statement=arp_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionPatternFromSourceTuple]], None, None]:
        """
        Select the archive chemical reaction patterns from sources in the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical reaction patterns should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the archive chemical reaction patterns from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                arp_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_pattern_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_arps_from_sources = db_session.scalar(
                    statement=arp_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_arps_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=arp_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # workbench_compound AS wc
    ####################################################################################################################

    def migrate_archive_to_workbench_compounds(
            self,
            ac_standardization_function: CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable,
            wcs_are_building_blocks: bool,
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical compounds from the archive to the workbench tables of the database.

        :parameter ac_standardization_function: The standardization function of the archive chemical compounds.
        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compounds should be retrieved.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical compound data from the archive to the workbench tables of the "
                        "database has been started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                ac_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_acs_from_sources = db_session.scalar(
                    statement=select(
                        count()
                    ).select_from(
                        ac_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveCompound.id,
                            CaCSSQLiteDatabaseModelArchiveCompound.smiles
                        ).distinct().subquery()
                    )
                )

                tqdm_description = (
                    "Migrating the chemical compound data from the archive to the workbench tables of the database"
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, number_of_acs_from_sources, db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_acs_from_sources / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    acs = db_session.execute(
                        statement=ac_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveCompound.id,
                            CaCSSQLiteDatabaseModelArchiveCompound.smiles
                        ).distinct().limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

                    standardized_acs = ac_standardization_function([
                        ac.smiles
                        for ac in acs
                    ])

                    wcs = list()

                    for ac_index, ac in enumerate(acs):
                        if standardized_acs[ac_index] is not None:
                            wcs.append((
                                ac.id,
                                standardized_acs[ac_index],
                            ))

                    if len(wcs) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The workbench chemical compound data chunk [{chunk_start_index:d}, "
                                    "{chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(
                                        db_chunk_offset + db_chunk_limit,
                                        number_of_acs_from_sources
                                    )
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_compounds(
                            db_session=db_session,
                            wcs=wcs,
                            wcs_are_building_blocks=wcs_are_building_blocks,
                            wcs_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical compound data from the archive to the workbench tables of the "
                        "database has been completed."
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
            wcs_are_building_blocks: Optional[bool],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchCompoundTuple]], None, None]:
        """
        Select the workbench chemical compounds from the database.

        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compounds from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wc_select_statement = CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_select_statement(
                    wcs_are_building_blocks=wcs_are_building_blocks
                )

                number_of_wcs = db_session.scalar(
                    statement=wc_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wcs, db_chunk_limit):
                    yield db_session.execute(
                        statement=wc_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            wcs_are_building_blocks: Optional[bool],
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchCompoundFromSourceTuple]], None, None]:
        """
        Select the workbench chemical compounds from sources in the database.

        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical compounds should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compounds from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wc_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_from_source_select_statement(
                        wcs_are_building_blocks=wcs_are_building_blocks,
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_wcs_from_sources = db_session.scalar(
                    statement=wc_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for database_chunk_offset in range(0, number_of_wcs_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=wc_from_source_select_statement.limit(
                            limit=db_chunk_limit
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
    # workbench_reaction AS wr
    ####################################################################################################################

    def migrate_archive_to_workbench_reactions(
            self,
            ar_standardization_function: CaCSSQLiteDatabaseArchiveReactionStandardizationCallable,
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical reactions from the archive to the workbench tables of the database.

        :parameter ar_standardization_function: The standardization function of the archive chemical reactions.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical reactions should be retrieved.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical reaction data from the archive to the workbench tables of the "
                        "database has been started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                ar_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_ars_from_sources = db_session.scalar(
                    statement=select(
                        count()
                    ).select_from(
                        ar_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveReaction.id,
                            CaCSSQLiteDatabaseModelArchiveReaction.smiles
                        ).distinct().subquery()
                    )
                )

                tqdm_description = (
                    "Migrating the chemical reaction data from the archive to the workbench tables of the database"
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, number_of_ars_from_sources, db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_ars_from_sources / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    ars = db_session.execute(
                        statement=ar_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveReaction.id,
                            CaCSSQLiteDatabaseModelArchiveReaction.smiles
                        ).distinct().limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

                    standardized_ars = ar_standardization_function([
                        ar.smiles
                        for ar in ars
                    ])

                    wrs = list()

                    for ar_index, ar in enumerate(ars):
                        if standardized_ars[ar_index] is not None:
                            for (
                                wr_smiles,
                                wrrc_smiles_strings,
                                wrsc_smiles_strings,
                                wrpc_smiles_strings,
                            ) in standardized_ars[ar_index]:
                                wrs.append((
                                    ar.id,
                                    wr_smiles,
                                    wrrc_smiles_strings,
                                    wrsc_smiles_strings,
                                    wrpc_smiles_strings,
                                ))

                    if len(wrs) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The workbench chemical reaction data chunk [{data_chunk_start_index:d},"
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(
                                        db_chunk_offset + db_chunk_limit,
                                        number_of_ars_from_sources
                                    )
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_reactions(
                            db_session=db_session,
                            wrs=wrs,
                            wrs_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical reaction data from the archive to the workbench tables of the "
                        "database has been completed."
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
            wrrc_smiles_strings: Optional[Iterable[str]],
            wrsc_smiles_strings: Optional[Iterable[str]],
            wrpc_smiles_strings: Optional[Iterable[str]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchReactionTuple]], None, None]:
        """
        Select the workbench chemical reactions from the database.

        :parameter wrrc_smiles_strings: The SMILES strings of the workbench chemical reaction reactant compounds.
        :parameter wrsc_smiles_strings: The SMILES strings of the workbench chemical reaction spectator compounds.
        :parameter wrpc_smiles_strings: The SMILES strings of the workbench chemical reaction product compounds.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reactions from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wr_select_statement = CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_select_statement(
                    wrrc_smiles_strings=wrrc_smiles_strings,
                    wrsc_smiles_strings=wrsc_smiles_strings,
                    wrpc_smiles_strings=wrpc_smiles_strings,
                )

                number_of_wrs = db_session.scalar(
                    statement=wr_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wrs, db_chunk_limit):
                    yield db_session.execute(
                        statement=wr_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            wrrc_smiles_strings: Optional[Iterable[str]],
            wrsc_smiles_strings: Optional[Iterable[str]],
            wrpc_smiles_strings: Optional[Iterable[str]],
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchReactionFromSourceTuple]], None, None]:
        """
        Select the workbench chemical reactions from sources of the database.

        :parameter wrrc_smiles_strings: The SMILES strings of the workbench chemical reaction reactant compounds.
        :parameter wrsc_smiles_strings: The SMILES strings of the workbench chemical reaction spectator compounds.
        :parameter wrpc_smiles_strings: The SMILES strings of the workbench chemical reaction product compounds.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical reactions should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reactions from sources of the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wr_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_from_source_select_statement(
                        wrrc_smiles_strings=wrrc_smiles_strings,
                        wrsc_smiles_strings=wrsc_smiles_strings,
                        wrpc_smiles_strings=wrpc_smiles_strings,
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_wrs_from_sources = db_session.scalar(
                    statement=wr_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wrs_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=wr_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # workbench_compound_pattern AS wcp
    ####################################################################################################################

    def migrate_archive_to_workbench_compound_patterns(
            self,
            acp_standardization_function: CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable,
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical compound patterns from the archive to the workbench tables of the database.

        :parameter acp_standardization_function: The standardization function of the archive chemical compound patterns.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compound patterns should be retrieved.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical compound pattern data from the archive to the workbench tables "
                        "of the database has been started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                acp_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_pattern_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_acps_from_sources = db_session.scalar(
                    statement=select(
                        count()
                    ).select_from(
                        acp_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                            CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts
                        ).distinct().subquery()
                    )
                )

                tqdm_description = (
                    "Migrating the chemical compound pattern data from the archive to the workbench tables of the "
                    "database"
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, number_of_acps_from_sources, db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_acps_from_sources / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    acps = db_session.execute(
                        statement=acp_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                            CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts
                        ).distinct().limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

                    standardized_acps = acp_standardization_function([
                        acp.smarts
                        for acp in acps
                    ])

                    wcps = list()

                    for acp_index, acp in enumerate(acps):
                        if standardized_acps[acp_index] is not None:
                            wcps.append((
                                acp.id,
                                standardized_acps[acp_index],
                            ))

                    if len(wcps) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The workbench chemical compound pattern data chunk [{data_chunk_start_index:d}, "
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(
                                        db_chunk_offset + db_chunk_limit,
                                        number_of_acps_from_sources
                                    )
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_compound_patterns(
                            db_session=db_session,
                            wcps=wcps,
                            wcps_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical compound pattern data from the archive to the workbench tables "
                        "of the database has been completed."
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
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchCompoundPatternTuple]], None, None]:
        """
        Select the workbench chemical compound patterns from the database.

        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compound patterns from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wcp_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_pattern_select_statement()

                number_of_wcps = db_session.scalar(
                    statement=wcp_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wcps, db_chunk_limit):
                    yield db_session.execute(
                        statement=wcp_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            as_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchCompoundPatternFromSourceTuple]], None, None]:
        """
        Select the workbench chemical compound patterns from sources in the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical compound patterns should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compound patterns from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wcp_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_pattern_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_wcps_from_sources = db_session.scalar(
                    statement=wcp_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wcps_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=wcp_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # workbench_reaction_pattern AS wrp
    ####################################################################################################################

    def migrate_archive_to_workbench_reaction_patterns(
            self,
            arp_standardization_function: CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable,
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical reaction patterns from the archive to the workbench tables of the database.

        :parameter arp_standardization_function: The standardization function of the archive chemical reaction patterns.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical reaction patterns should be retrieved.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical reaction pattern data from the archive to the workbench tables "
                        "of the database has been started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                arp_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_pattern_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_arps_from_sources = db_session.scalar(
                    statement=select(
                        count()
                    ).select_from(
                        arp_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                            CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts
                        ).distinct().subquery()
                    )
                )

                tqdm_description = (
                    "Migrating the chemical reaction pattern data from the archive to the workbench tables of the "
                    "database"
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, number_of_arps_from_sources, db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_arps_from_sources / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    arps = db_session.execute(
                        statement=arp_from_source_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                            CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts
                        ).distinct().limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

                    standardized_arps = arp_standardization_function([
                        arp.smarts
                        for arp in arps
                    ])

                    wrps = list()

                    for arp_index, arp in enumerate(arps):
                        if standardized_arps[arp_index] is not None:
                            for (
                                wrp_smarts,
                                wrrcp_smarts_strings,
                                wrscp_smarts_strings,
                                wrpcp_smarts_strings,
                            ) in standardized_arps[arp_index]:
                                wrps.append((
                                    arp.id,
                                    wrp_smarts,
                                    wrrcp_smarts_strings,
                                    wrscp_smarts_strings,
                                    wrpcp_smarts_strings,
                                ))

                    if len(wrps) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The workbench chemical reaction pattern data chunk [{data_chunk_start_index:d}, "
                                    "{data_chunk_end_index:d}) is empty and insertion is skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(
                                        db_chunk_offset + db_chunk_limit,
                                        number_of_arps_from_sources
                                    )
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_reaction_patterns(
                            db_session=db_session,
                            wrps=wrps,
                            wrps_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical reaction pattern data from the archive to the workbench tables "
                        "of the database has been completed."
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
            wrrcp_smarts_strings: Optional[Iterable[str]],
            wrscp_smarts_strings: Optional[Iterable[str]],
            wrpcp_smarts_strings: Optional[Iterable[str]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchReactionPatternTuple]], None, None]:
        """
        Select the workbench chemical reaction patterns from the database.

        :parameter wrrcp_smarts_strings: The SMARTS strings of the workbench chemical reaction reactant compound
            patterns.
        :parameter wrscp_smarts_strings: The SMARTS strings of the workbench chemical reaction spectator compound
            patterns.
        :parameter wrpcp_smarts_strings: The SMARTS strings of the workbench chemical reaction product compound
            patterns.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reaction patterns from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wrp_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_pattern_select_statement(
                        wrrcp_smarts_strings=wrrcp_smarts_strings,
                        wrscp_smarts_strings=wrscp_smarts_strings,
                        wrpcp_smarts_strings=wrpcp_smarts_strings,
                    )

                number_of_wrps = db_session.scalar(
                    statement=wrp_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wrps, db_chunk_limit):
                    yield db_session.execute(
                        statement=wrp_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
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
            wrrcp_smarts_strings: Optional[Iterable[str]],
            wrscp_smarts_strings: Optional[Iterable[str]],
            wrpcp_smarts_strings: Optional[Iterable[str]],
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchReactionPatternFromSourceTuple]], None, None]:
        """
        Select the workbench chemical reaction patterns from sources in the database.

        :parameter wrrcp_smarts_strings: The SMARTS strings of the workbench chemical reaction reactant compound
            patterns.
        :parameter wrscp_smarts_strings: The SMARTS strings of the workbench chemical reaction spectator compound
            patterns.
        :parameter wrpcp_smarts_strings: The SMARTS strings of the workbench chemical reaction product compound
            patterns.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical reaction patterns should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical reaction patterns from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wrp_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_pattern_from_source_select_statement(
                        wrrcp_smarts_strings=wrrcp_smarts_strings,
                        wrscp_smarts_strings=wrscp_smarts_strings,
                        wrpcp_smarts_strings=wrpcp_smarts_strings,
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_wrps_from_sources = db_session.scalar(
                    statement=wrp_from_source_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                for db_chunk_offset in range(0, number_of_wrps_from_sources, db_chunk_limit):
                    yield db_session.execute(
                        statement=wrp_from_source_select_statement.limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # workbench_reaction_transformation_pattern AS wrtp
    ####################################################################################################################

    def extract_workbench_reaction_transformation_patterns(
            self,
            wrp_extraction_function: CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable,
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Extract the workbench chemical reaction transformation patterns of the database.

        :parameter wrp_extraction_function: The extraction function of the workbench chemical reaction patterns.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The extraction of the workbench chemical reaction transformation pattern data has been "
                        "started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                wr_select_statement = CaCSSQLiteDatabaseSelectUtility.construct_workbench_reaction_select_statement(
                    wrrc_smiles_strings=None,
                    wrsc_smiles_strings=None,
                    wrpc_smiles_strings=None
                )

                number_of_wrs = db_session.scalar(
                    statement=wr_select_statement.with_only_columns(
                        count(),
                        maintain_column_froms=True
                    )
                )

                tqdm_description = (
                    "Extracting and inserting the workbench chemical reaction transformation pattern data into the "
                    "database (db_chunk_limit = {db_chunk_limit:d})"
                ).format(
                    db_chunk_limit=db_chunk_limit
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, number_of_wrs, db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_wrs / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    wrs = db_session.execute(
                        statement=wr_select_statement.with_only_columns(
                            CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                            CaCSSQLiteDatabaseModelWorkbenchReaction.smiles
                        ).distinct().limit(
                            limit=db_chunk_limit
                        ).offset(
                            offset=db_chunk_offset
                        )
                    ).all()

                    extracted_wrps = wrp_extraction_function([
                        wr.smiles
                        for wr in wrs
                    ])

                    wrtps = list()

                    for wr_index, wr in enumerate(wrs):
                        if extracted_wrps[wr_index] is not None:
                            for (
                                wrp_smarts,
                                wrrc_smiles_strings_and_wrrcp_smarts_strings,
                                wrsc_smiles_strings_and_wrscp_smarts_strings,
                                wrpc_smiles_strings_and_wrpcp_smarts_strings,
                            ) in extracted_wrps[wr_index]:
                                wrtps.append((
                                    wr.id,
                                    wrp_smarts,
                                    wrrc_smiles_strings_and_wrrcp_smarts_strings,
                                    wrsc_smiles_strings_and_wrscp_smarts_strings,
                                    wrpc_smiles_strings_and_wrpcp_smarts_strings,
                                ))

                    if len(wrtps) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The workbench chemical reaction transformation pattern data chunk "
                                    "[{data_chunk_start_index:d}, {data_chunk_end_index:d}) is empty and insertion is "
                                    "skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(db_chunk_offset + db_chunk_limit, number_of_wrs)
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_reaction_transformation_patterns(
                            db_session=db_session,
                            wrtps=wrtps,
                            wrtps_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The extraction of the workbench chemical reaction transformation pattern data has been "
                        "completed."
                    )
                )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    # synthesis_route AS sr
    ####################################################################################################################

    def select_reversed_synthesis_routes(
            self,
            wc_smiles: str,
            reversed_sr_maximum_depth: int = 10
    ) -> Sequence[Row[Tuple[int, int, str, bool, bool, Optional[int], Optional[int], Optional[str]]]]:
        """
        Select the reversed chemical synthesis routes from the database.

        :parameter wc_smiles: The SMILES string of the workbench chemical compound.
        :parameter reversed_sr_maximum_depth: The maximum depth of the reversed chemical synthesis routes.

        :returns: The reversed chemical synthesis routes from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                reversed_sr_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_reversed_synthesis_route_select_statement(
                        wc_smiles=wc_smiles,
                        reversed_sr_maximum_depth=reversed_sr_maximum_depth
                    )

                return db_session.execute(
                    statement=reversed_sr_select_statement
                ).all()

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise
