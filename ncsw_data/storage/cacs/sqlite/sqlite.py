""" The ``ncsw_data.storage.cacs.sqlite`` package ``sqlite`` module. """

from logging import Logger
from math import ceil
from typing import Generator, Iterable, List, Optional, Sequence, Tuple

from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import distinct, tuple_
from sqlalchemy.sql.functions import count

from tqdm.auto import tqdm

from ncsw_data.storage.base.base import DataStorageBase
from ncsw_data.storage.cacs.sqlite.dml.utility import *
from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.workbench import *

from ncsw_data.storage.cacs.sqlite.typing import (
    CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable,
    CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable,
    CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable,
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable,
    CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable,
)


class CaCSSQLiteDatabase(DataStorageBase):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database class. """

    def __init__(
            self,
            url: str = "sqlite:///",
            logger: Optional[Logger] = None,
            **kwargs
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter url: The URL of the database. The value `sqlite:///` indicates that the SQLite database should be
            created in memory.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions:
            { `sqlalchemy.engine.create.create_engine` }.
        """

        try:
            super().__init__(
                logger=logger
            )

            self.__db_engine = create_engine(
                url=url,
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

    ####################################################################################################################
    # archive_compound AS ac
    ####################################################################################################################

    def insert_archive_compounds(
            self,
            ac_smiles_strings: Sequence[str],
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
                    "Inserting the archive chemical compound data chunks into the database (db_chunk_limit = "
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
                            ac_smiles_strings=ac_smiles_strings_chunk,
                            as_id=as_id,
                            ac_created_by=db_user
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundTuple]]]:
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
                        count(
                            expression="*"
                        )
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundFromSourceTuple]]]:
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
                        count(
                            expression="*"
                        )
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
                    "Inserting the archive chemical reaction data chunks into the database (db_chunk_limit = "
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
                            ar_smiles_strings=ar_smiles_strings_chunk,
                            as_id=as_id,
                            ar_created_by=db_user
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionTuple]]]:
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
                        count(
                            expression="*"
                        )
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionFromSourceTuple]]]:
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
                        count(
                            expression="*"
                        )
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
                    "Inserting the archive chemical compound pattern data chunks into the database (db_chunk_limit = "
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
                            acp_smarts_strings=acp_smarts_strings_chunk,
                            as_id=as_id,
                            acp_created_by=db_user
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundPatternTuple]]]:
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
                        count(
                            expression="*"
                        )
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveCompoundPatternFromSourceTuple]]]:
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
                        count(
                            expression="*"
                        )
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
                    "Inserting the archive chemical reaction pattern data chunks into the database (db_chunk_limit = "
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
                            arp_smarts_strings=arp_smarts_strings_chunk,
                            as_id=as_id,
                            arp_created_by=db_user
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionPatternTuple]]]:
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
                        count(
                            expression="*"
                        )
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
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseArchiveReactionPatternFromSourceTuple]]]:
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
                        count(
                            expression="*"
                        )
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
            wc_is_building_block: bool,
            as_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]],
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Migrate the chemical compounds from the archive to the workbench tables of the database.

        :parameter ac_standardization_function: The standardization function of the archive chemical compounds.
        :parameter wc_is_building_block: The is building block indicator of the workbench chemical compounds.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compounds should be retrieved.
        :parameter db_user: The user of the database.
        :parameter db_chunk_limit: The chunk limit of the database.
        """

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical compound data from the archive to the workbench tables of the"
                        "database has been started."
                    )
                )

            with self.__db_sessionmaker() as db_session:
                ac_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_compound_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_acs_from_sources = db_session.scalar(
                    statement=ac_from_source_select_statement.with_only_columns(
                        count(
                            distinct(
                                tuple_(
                                    CaCSSQLiteDatabaseModelArchiveCompound.id,
                                    CaCSSQLiteDatabaseModelArchiveCompound.smiles
                                )
                            )
                        )
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

                    wc_smiles_strings = ac_standardization_function([
                        ac.smiles
                        for ac in acs
                    ])

                    ac_id_to_wc_smiles, ac_id_to_wc_is_building_block = dict(), dict()

                    for ac_index, ac in enumerate(acs):
                        if wc_smiles_strings[ac_index] is not None:
                            ac_id_to_wc_smiles[ac.id] = wc_smiles_strings[ac_index]
                            ac_id_to_wc_is_building_block[ac.id] = wc_is_building_block

                    if len(ac_id_to_wc_smiles.keys()) == 0:
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
                            ac_id_to_wc_smiles=ac_id_to_wc_smiles,
                            ac_id_to_wc_is_building_block=ac_id_to_wc_is_building_block,
                            wc_created_by=db_user
                        )

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The migration of the chemical compound data from the archive to the workbench tables of the"
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
            wc_is_building_block: Optional[bool],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchCompoundTuple]]]:
        """
        Select the workbench chemical compounds from the database.

        :parameter wc_is_building_block: The is building block indicator of the workbench chemical compounds.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compounds from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wc_select_statement = CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_select_statement(
                    wc_is_building_block=wc_is_building_block
                )

                number_of_wcs = db_session.scalar(
                    statement=wc_select_statement.with_only_columns(
                        count(
                            expression="*"
                        )
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
            wc_is_building_block: Optional[bool],
            as_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]],
            db_chunk_limit: int = 10000
    ) -> Generator[Sequence[Row[CaCSSQLiteDatabaseWorkbenchCompoundFromSourceTuple]]]:
        """
        Select the workbench chemical compounds from sources in the database.

        :parameter wc_is_building_block: The is building block indicator of the workbench chemical compounds.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical compounds should be retrieved.
        :parameter db_chunk_limit: The chunk limit of the database.

        :returns: The generator of the workbench chemical compounds from sources in the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                wc_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_workbench_compound_from_source_select_statement(
                        wc_is_building_block=wc_is_building_block,
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_wcs_from_sources = db_session.scalar(
                    statement=wc_from_source_select_statement.with_only_columns(
                        count(
                            expression="*"
                        )
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
            as_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]],
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
                    statement=ar_from_source_select_statement.with_only_columns(
                        count(
                            distinct(
                                tuple_(
                                    CaCSSQLiteDatabaseModelArchiveReaction.id,
                                    CaCSSQLiteDatabaseModelArchiveReaction.smiles
                                )
                            )
                        )
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

                    ar_id_to_wr_smiles, ar_id_to_wrrc_smiles_strings, ar_id_to_wrsc_smiles_strings, \
                        ar_id_to_wrpc_smiles_strings = dict(), dict(), dict(), dict()

                    # TODO: Check this because there might be an ID conflict. Also for reaction patterns.
                    # TODO: Also check empty insertion attempts.
                    for ar_index, ar in enumerate(ars):
                        if standardized_ars[ar_index] is not None:
                            for standardized_ar in standardized_ars[ar_index]:
                                (
                                    ar_id_to_wr_smiles[ar.id],
                                    ar_id_to_wrrc_smiles_strings[ar.id],
                                    ar_id_to_wrsc_smiles_strings[ar.id],
                                    ar_id_to_wrpc_smiles_strings[ar.id],
                                ) = standardized_ar

                    if len(ar_id_to_wr_smiles.keys()) == 0:
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
                            ar_id_to_wr_smiles=ar_id_to_wr_smiles,
                            ar_id_to_wrrc_smiles_strings=ar_id_to_wrrc_smiles_strings,
                            ar_id_to_wrsc_smiles_strings=ar_id_to_wrsc_smiles_strings,
                            ar_id_to_wrpc_smiles_strings=ar_id_to_wrpc_smiles_strings,
                            wr_created_by=db_user
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
                        count(
                            expression="*"
                        )
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
            as_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]],
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
            # TODO: Merge the select methods into one.
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
                        count(
                            expression="*"
                        )
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
            as_names_versions_and_file_names: Optional[Sequence[Tuple[str, str, str]]],
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
                    statement=acp_from_source_select_statement.with_only_columns(
                        count(
                            distinct(
                                tuple_(
                                    CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                                    CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts
                                )
                            )
                        )
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

                    wcp_smarts_strings = acp_standardization_function([
                        acp.smarts
                        for acp in acps
                    ])

                    acp_id_to_wcp_smarts = dict()

                    for acp_index, acp in enumerate(acps):
                        if wcp_smarts_strings[acp_index] is not None:
                            acp_id_to_wcp_smarts[acp.id] = wcp_smarts_strings[acp_index]

                    if len(acp_id_to_wcp_smarts.keys()) == 0:
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
                            acp_id_to_wcp_smarts=acp_id_to_wcp_smarts,
                            wcp_created_by=db_user
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
                        count(
                            expression="*"
                        )
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
                        count(
                            expression="*"
                        )
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
    # workbench_reaction_pattern AS wcp
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
                    statement=arp_from_source_select_statement.with_only_columns(
                        count(
                            distinct(
                                tuple_(
                                    CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                                    CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts
                                )
                            )
                        )
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

                    arp_id_to_wrp_smarts, arp_id_to_wrrcp_smarts_strings, arp_id_to_wrscp_smarts_strings, \
                        arp_id_to_wrpcp_smarts_strings = dict(), dict(), dict(), dict()

                    for arp_index, arp in enumerate(arps):
                        if standardized_arps[arp_index] is not None:
                            for standardized_arp in standardized_arps[arp_index]:
                                (
                                    arp_id_to_wrp_smarts[arp.id],
                                    arp_id_to_wrrcp_smarts_strings[arp.id],
                                    arp_id_to_wrscp_smarts_strings[arp.id],
                                    arp_id_to_wrpcp_smarts_strings[arp.id],
                                ) = standardized_arp

                    if len(arp_id_to_wrp_smarts.keys()) == 0:
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
                            arp_id_to_wrp_smarts=arp_id_to_wrp_smarts,
                            arp_id_to_wrrcp_smarts_strings=arp_id_to_wrrcp_smarts_strings,
                            arp_id_to_wrscp_smarts_strings=arp_id_to_wrscp_smarts_strings,
                            arp_id_to_wrpcp_smarts_strings=arp_id_to_wrpcp_smarts_strings,
                            wrp_created_by=db_user
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

    def extract_workbench_reaction_transformation_patterns(
            self,
            wrp_extraction_function: CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable,
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]],
            db_user: str = "user",
            db_chunk_limit: int = 10000
    ) -> None:
        """
        Extract the workbench chemical reaction transformation patterns of the database.

        :parameter wrp_extraction_function: The extraction function of the workbench chemical reaction patterns.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical reactions should be retrieved.
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
                wr_from_source_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_archive_reaction_from_source_select_statement(
                        as_names_versions_and_file_names=as_names_versions_and_file_names
                    )

                number_of_wrs_from_sources = db_session.scalar(
                    statement=wr_from_source_select_statement.with_only_columns(
                        count(
                            distinct(
                                tuple_(
                                    CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                                    CaCSSQLiteDatabaseModelWorkbenchReaction.smiles
                                )
                            )
                        )
                    )
                )

                tqdm_description = (
                    "Extracting and inserting the workbench chemical reaction transformation pattern data chunks into "
                    "the database (db_chunk_limit = {db_chunk_limit:d})"
                ).format(
                    db_chunk_limit=db_chunk_limit
                )

                for db_chunk_offset in tqdm(
                    iterable=range(0, number_of_wrs_from_sources, db_chunk_limit),
                    desc=tqdm_description,
                    total=ceil(number_of_wrs_from_sources / db_chunk_limit),
                    ncols=len(tqdm_description) + 50
                ):
                    wrs = db_session.execute(
                        statement=wr_from_source_select_statement.with_only_columns(
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

                    wr_id_to_wrp_smarts, wr_id_to_wrrcp_smarts_strings, wr_id_to_wrscp_smarts_strings, \
                        wr_id_to_wrpcp_smarts_strings = dict(), dict(), dict(), dict()

                    for wr_index, wr in enumerate(wrs):
                        if extracted_wrps[wr_index] is not None:
                            for extracted_wrp in extracted_wrps[wr_index]:
                                (
                                    wr_id_to_wrp_smarts[wr.id],
                                    wr_id_to_wrrcp_smarts_strings[wr.id],
                                    wr_id_to_wrscp_smarts_strings[wr.id],
                                    wr_id_to_wrpcp_smarts_strings[wr.id],
                                ) = extracted_wrp

                    if len(wr_id_to_wrp_smarts.keys()) == 0:
                        if self.logger is not None:
                            self.logger.warning(
                                msg=(
                                    "The workbench chemical reaction transformation pattern data chunk "
                                    "[{data_chunk_start_index:d}, {data_chunk_end_index:d}) is empty and insertion is "
                                    "skipped."
                                ).format(
                                    data_chunk_start_index=db_chunk_offset,
                                    data_chunk_end_index=min(
                                        db_chunk_offset + db_chunk_limit,
                                        number_of_wrs_from_sources
                                    )
                                )
                            )

                        continue

                    with db_session.begin_nested():
                        CaCSSQLiteDatabaseInsertUtility.insert_workbench_reaction_transformation_patterns(
                            db_session=db_session,
                            wr_id_to_wrp_smarts=wr_id_to_wrp_smarts,
                            wr_id_to_wrrcp_smarts_strings=wr_id_to_wrrcp_smarts_strings,
                            wr_id_to_wrscp_smarts_strings=wr_id_to_wrscp_smarts_strings,
                            wr_id_to_wrpcp_smarts_strings=wr_id_to_wrpcp_smarts_strings,
                            wrp_created_by=db_user
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
                        count(
                            expression="*"
                        )
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
                        count(
                            expression="*"
                        )
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
    # synthesis_route AS sr
    ####################################################################################################################

    def select_reversed_synthesis_routes(
            self,
            wc_smiles: str,
            reversed_sr_maximum_depth: int
    ) -> List[ReversedSynthesisRouteTuple]:
        """
        Select the reversed chemical synthesis routes from the database.

        :parameter wc_smiles: The SMILES string of the workbench chemical compound.
        :parameter reversed_sr_maximum_depth: The maximum depth of the reversed chemical synthesis routes.

        :returns: The generator of the reversed chemical synthesis routes from the database.
        """

        try:
            with self.__db_sessionmaker() as db_session:
                reversed_sr_select_statement = \
                    CaCSSQLiteDatabaseSelectUtility.construct_reversed_synthesis_route_select_statement(
                        wc_smiles=wc_smiles,
                        reversed_sr_maximum_depth=reversed_sr_maximum_depth
                    )

                reversed_srs = list()

                for reversed_sr in db_session.execute(
                    statement=reversed_sr_select_statement
                ).all():
                    reversed_srs.append(
                        dict(reversed_sr._mapping)
                    )

                return reversed_srs

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=exception_handle
                )

            raise

    ####################################################################################################################
    ####################################################################################################################
