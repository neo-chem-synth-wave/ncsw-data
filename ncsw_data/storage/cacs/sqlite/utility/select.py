""" The ``ncsw_data.storage.cacs.sqlite.utility`` package ``select`` module. """

from typing import Iterable, Optional, Tuple

from sqlalchemy.sql import select, tuple_
from sqlalchemy.sql.selectable import Select

from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.workbench import *


class CaCSSQLiteDatabaseSelectUtility:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database select utility class. """

    @staticmethod
    def construct_archive_compounds_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None
    ) -> Select[Tuple[CaCSSQLiteDatabaseModelArchiveCompound, CaCSSQLiteDatabaseModelArchiveSource]]:
        """
        Construct the archive chemical compounds from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical compounds should be retrieved. The value `None` indicates that the chemical
            compounds should be retrieved from all archive sources.

        :returns: The archive chemical compounds from sources query of the database.
        """

        archive_compounds_from_sources_query = select(
            CaCSSQLiteDatabaseModelArchiveCompound,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveCompoundSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveCompound.id ==
                CaCSSQLiteDatabaseModelArchiveCompoundSource.archive_compound_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveCompoundSource.archive_source_id ==
                CaCSSQLiteDatabaseModelArchiveSource.id
            )
        )

        if archive_source_names_versions_and_file_names is not None:
            archive_compounds_from_sources_query = archive_compounds_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return archive_compounds_from_sources_query

    @staticmethod
    def construct_archive_compound_patterns_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None
    ) -> Select[Tuple[CaCSSQLiteDatabaseModelArchiveCompoundPattern, CaCSSQLiteDatabaseModelArchiveSource]]:
        """
        Construct the archive chemical compound patterns from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical compound patterns should be retrieved. The value `None` indicates that the
            chemical compound patterns should be retrieved from all archive sources.

        :returns: The archive chemical compound patterns from sources query of the database.
        """

        archive_compound_patterns_from_sources_query = select(
            CaCSSQLiteDatabaseModelArchiveCompoundPattern,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveCompoundPatternSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.id ==
                CaCSSQLiteDatabaseModelArchiveCompoundPatternSource.archive_compound_pattern_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveCompoundPatternSource.archive_source_id ==
                CaCSSQLiteDatabaseModelArchiveSource.id
            )
        )

        if archive_source_names_versions_and_file_names is not None:
            archive_compound_patterns_from_sources_query = archive_compound_patterns_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return archive_compound_patterns_from_sources_query

    @staticmethod
    def construct_archive_reactions_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None
    ) -> Select[Tuple[CaCSSQLiteDatabaseModelArchiveReaction, CaCSSQLiteDatabaseModelArchiveSource]]:
        """
        Construct the archive chemical reactions from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical reactions should be retrieved. The value `None` indicates that the chemical
            reactions should be retrieved from all archive sources.

        :returns: The archive chemical reactions from sources query of the database.
        """

        archive_reactions_from_sources_query = select(
            CaCSSQLiteDatabaseModelArchiveReaction,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveReactionSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveReaction.id ==
                CaCSSQLiteDatabaseModelArchiveReactionSource.archive_reaction_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveReactionSource.archive_source_id ==
                CaCSSQLiteDatabaseModelArchiveSource.id
            )
        )

        if archive_source_names_versions_and_file_names is not None:
            archive_reactions_from_sources_query = archive_reactions_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return archive_reactions_from_sources_query

    @staticmethod
    def construct_archive_reaction_patterns_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]] = None
    ) -> Select[Tuple[CaCSSQLiteDatabaseModelArchiveReactionPattern, CaCSSQLiteDatabaseModelArchiveSource]]:
        """
        Construct the archive chemical reaction patterns from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the chemical reaction patterns should be retrieved. The value `None` indicates that the
            chemical reaction patterns should be retrieved from all archive sources.

        :returns: The archive chemical reaction patterns from sources query of the database.
        """

        archive_reaction_patterns_from_sources_query = select(
            CaCSSQLiteDatabaseModelArchiveReactionPattern,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveReactionPatternSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveReactionPattern.id ==
                CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_reaction_pattern_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_source_id ==
                CaCSSQLiteDatabaseModelArchiveSource.id
            )
        )

        if archive_source_names_versions_and_file_names is not None:
            archive_reaction_patterns_from_sources_query = archive_reaction_patterns_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return archive_reaction_patterns_from_sources_query

    @staticmethod
    def construct_workbench_compounds_query() -> Select[Tuple[CaCSSQLiteDatabaseModelWorkbenchCompound]]:
        """
        Construct the workbench chemical compounds query of the database.

        :returns: The workbench chemical compounds query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        )

    @staticmethod
    def construct_workbench_reactions_query() -> Select[Tuple[CaCSSQLiteDatabaseModelWorkbenchReaction]]:
        """
        Construct the workbench chemical reactions query of the database.

        :returns: The workbench chemical reactions query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelWorkbenchReaction
        )
