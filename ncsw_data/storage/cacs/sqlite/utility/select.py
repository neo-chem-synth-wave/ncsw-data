""" The ``ncsw_data.storage.cacs.sqlite.utility`` package ``select`` module. """

from typing import Iterable, Optional, Tuple, Union

from sqlalchemy.sql import and_, bindparam, case, cast, intersect, not_, or_, select, tuple_
from sqlalchemy.sql.elements import literal
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.sqltypes import String

from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.workbench import *

from ncsw_data.storage.cacs.sqlite.utility.typing import (
    ArchiveCompoundsTuple,
    ArchiveCompoundsFromSourcesTuple,
    ArchiveCompoundPatternsTuple,
    ArchiveCompoundPatternsFromSourcesTuple,
    ArchiveReactionsTuple,
    ArchiveReactionsFromSourcesTuple,
    ArchiveReactionPatternsTuple,
    ArchiveReactionPatternsFromSourcesTuple,
    WorkbenchCompoundsTuple,
    WorkbenchCompoundsFromSourcesTuple,
    WorkbenchCompoundPatternsTuple,
    WorkbenchCompoundPatternsFromSourcesTuple,
    WorkbenchReactionsTuple,
    WorkbenchReactionsFromSourcesTuple,
    WorkbenchReactionPatternsTuple,
    WorkbenchReactionPatternsFromSourcesTuple,
)


class CaCSSQLiteDatabaseSelectUtility:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database select utility class. """

    ####################################################################################################################
    # Archive Compounds
    ####################################################################################################################

    @staticmethod
    def construct_archive_compounds_query() -> Select[ArchiveCompoundsTuple]:
        """
        Construct the archive chemical compounds query of the database.

        :returns: The archive chemical compounds query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveCompound
        )

    @staticmethod
    def construct_archive_compounds_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[ArchiveCompoundsFromSourcesTuple]:
        """
        Construct the archive chemical compounds from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical compounds should be retrieved.

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

    ####################################################################################################################
    # Workbench Compounds
    ####################################################################################################################

    @staticmethod
    def construct_workbench_compounds_query(
            workbench_compound_is_building_block: Optional[bool]
    ) -> Select[WorkbenchCompoundsTuple]:
        """
        Construct the workbench chemical compounds query of the database.

        :parameter workbench_compound_is_building_block: The boolean indicator of whether the workbench building block
            chemical compounds should be retrieved.

        :returns: The workbench chemical compounds query of the database.
        """

        workbench_compounds_query = select(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        )

        if workbench_compound_is_building_block is not None:
            workbench_compounds_query = workbench_compounds_query.where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block == workbench_compound_is_building_block
            )

        return workbench_compounds_query

    @staticmethod
    def construct_workbench_compounds_from_sources_query(
            workbench_compound_is_building_block: Optional[bool],
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[WorkbenchCompoundsFromSourcesTuple]:
        """
        Construct the workbench chemical compounds from sources query of the database.

        :parameter workbench_compound_is_building_block: The boolean indicator of whether the workbench building block
            chemical compounds should be retrieved.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical compounds should be retrieved.

        :returns: The workbench chemical compounds from sources query of the database.
        """

        workbench_compounds_from_sources_query = select(
            CaCSSQLiteDatabaseModelWorkbenchCompound,
            CaCSSQLiteDatabaseModelArchiveCompound,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelWorkbenchCompoundArchive,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchCompound.id ==
                CaCSSQLiteDatabaseModelWorkbenchCompoundArchive.workbench_compound_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveCompound,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchCompoundArchive.archive_compound_id ==
                CaCSSQLiteDatabaseModelArchiveCompound.id
            )
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

        if workbench_compound_is_building_block is not None:
            workbench_compounds_from_sources_query = workbench_compounds_from_sources_query.where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block == workbench_compound_is_building_block
            )

        if archive_source_names_versions_and_file_names is not None:
            workbench_compounds_from_sources_query = workbench_compounds_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return workbench_compounds_from_sources_query

    ####################################################################################################################
    # Archive Reactions
    ####################################################################################################################

    @staticmethod
    def construct_archive_reactions_query() -> Select[ArchiveReactionsTuple]:
        """
        Construct the archive chemical reactions query of the database.

        :returns: The archive chemical reactions query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveReaction
        )

    @staticmethod
    def construct_archive_reactions_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[ArchiveReactionsFromSourcesTuple]:
        """
        Construct the archive chemical reactions from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical reactions should be retrieved.

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

    ####################################################################################################################
    # Workbench Reactions
    ####################################################################################################################

    @staticmethod
    def construct_workbench_reactions_query(
            workbench_reaction_reactant_compound_smiles_strings: Optional[Iterable[str]],
            workbench_reaction_spectator_compound_smiles_strings: Optional[Iterable[str]],
            workbench_reaction_product_compound_smiles_strings: Optional[Iterable[str]]
    ) -> Select[WorkbenchReactionsTuple]:
        """
        Construct the workbench chemical reactions query of the database.

        :parameter workbench_reaction_reactant_compound_smiles_strings: The SMILES strings of the reactant compounds
            that should be present in the workbench chemical reaction.
        :parameter workbench_reaction_spectator_compound_smiles_strings: The SMILES strings of the spectator compounds
            that should be present in the workbench chemical reaction.
        :parameter workbench_reaction_product_compound_smiles_strings: The SMILES strings of the product compounds that
            should be present in the workbench chemical reaction.

        :returns: The workbench chemical reactions query of the database.
        """

        workbench_reactions_queries = list()

        if workbench_reaction_reactant_compound_smiles_strings is not None:
            workbench_reactions_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_reaction_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_compound_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompound.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                        other=workbench_reaction_reactant_compound_smiles_strings
                    )
                ).distinct()
            )

        if workbench_reaction_spectator_compound_smiles_strings is not None:
            workbench_reactions_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_reaction_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_compound_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompound.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                        other=workbench_reaction_spectator_compound_smiles_strings
                    )
                ).distinct()
            )

        if workbench_reaction_product_compound_smiles_strings is not None:
            workbench_reactions_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_reaction_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_compound_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompound.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                        other=workbench_reaction_product_compound_smiles_strings
                    )
                ).distinct()
            )

        workbench_reactions_query = select(
            CaCSSQLiteDatabaseModelWorkbenchReaction
        )

        if len(workbench_reactions_queries) > 0:
            workbench_reactions_query = workbench_reactions_query.where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id.in_(
                    intersect(
                        *workbench_reactions_queries
                    )
                )
            )

        return workbench_reactions_query

    @staticmethod
    def construct_workbench_reactions_from_sources_query(
            workbench_reaction_reactant_compound_smiles_strings: Optional[Iterable[str]],
            workbench_reaction_spectator_compound_smiles_strings: Optional[Iterable[str]],
            workbench_reaction_product_compound_smiles_strings: Optional[Iterable[str]],
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[WorkbenchReactionsFromSourcesTuple]:
        """
        Construct the workbench chemical reactions from sources query of the database.

        :parameter workbench_reaction_reactant_compound_smiles_strings: The SMILES strings of the reactant compounds
            that should be present in the workbench chemical reaction.
        :parameter workbench_reaction_spectator_compound_smiles_strings: The SMILES strings of the spectator compounds
            that should be present in the workbench chemical reaction.
        :parameter workbench_reaction_product_compound_smiles_strings: The SMILES strings of the product compounds that
            should be present in the workbench chemical reaction.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical reactions should be retrieved.

        :returns: The workbench chemical reactions from sources query of the database.
        """

        workbench_reactions_from_sources_queries = list()

        if workbench_reaction_reactant_compound_smiles_strings is not None:
            workbench_reactions_from_sources_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_reaction_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_compound_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompound.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                        other=workbench_reaction_reactant_compound_smiles_strings
                    )
                ).distinct()
            )

        if workbench_reaction_spectator_compound_smiles_strings is not None:
            workbench_reactions_from_sources_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_reaction_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_compound_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompound.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                        other=workbench_reaction_spectator_compound_smiles_strings
                    )
                ).distinct()
            )

        if workbench_reaction_product_compound_smiles_strings is not None:
            workbench_reactions_from_sources_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_reaction_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompound,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_compound_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompound.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                        other=workbench_reaction_product_compound_smiles_strings
                    )
                ).distinct()
            )

        workbench_reactions_from_sources_query = select(
            CaCSSQLiteDatabaseModelWorkbenchReaction,
            CaCSSQLiteDatabaseModelArchiveReaction,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelWorkbenchReactionArchive,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id ==
                CaCSSQLiteDatabaseModelWorkbenchReactionArchive.workbench_reaction_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveReaction,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchReactionArchive.archive_reaction_id ==
                CaCSSQLiteDatabaseModelArchiveReaction.id
            )
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

        if len(workbench_reactions_from_sources_queries) > 0:
            workbench_reactions_from_sources_query = workbench_reactions_from_sources_query.where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id.in_(
                    other=intersect(
                        *workbench_reactions_from_sources_queries
                    )
                )
            )

        if archive_source_names_versions_and_file_names is not None:
            workbench_reactions_from_sources_query = workbench_reactions_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return workbench_reactions_from_sources_query

    ####################################################################################################################
    # Archive Compound Patterns
    ####################################################################################################################

    @staticmethod
    def construct_archive_compound_patterns_query() -> Select[ArchiveCompoundPatternsTuple]:
        """
        Construct the archive chemical compound patterns query of the database.

        :returns: The archive chemical compound patterns query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveCompoundPattern
        )

    @staticmethod
    def construct_archive_compound_patterns_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[ArchiveCompoundPatternsFromSourcesTuple]:
        """
        Construct the archive chemical compound patterns from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical compound patterns should be retrieved.

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

    ####################################################################################################################
    # Workbench Compound Patterns
    ####################################################################################################################

    @staticmethod
    def construct_workbench_compound_patterns_query() -> Select[WorkbenchCompoundPatternsTuple]:
        """
        Construct the workbench chemical compound patterns query of the database.

        :returns: The workbench chemical compound patterns query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
        )

    @staticmethod
    def construct_workbench_compound_patterns_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[WorkbenchCompoundPatternsFromSourcesTuple]:
        """
        Construct the workbench chemical compound patterns from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical compound patterns should be retrieved.

        :returns: The workbench chemical compound patterns from sources query of the database.
        """

        workbench_compound_patterns_from_sources_query = select(
            CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
            CaCSSQLiteDatabaseModelArchiveCompoundPattern,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id ==
                CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive.workbench_compound_pattern_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveCompoundPattern,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive.archive_compound_pattern_id ==
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.id
            )
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
            workbench_compound_patterns_from_sources_query = workbench_compound_patterns_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return workbench_compound_patterns_from_sources_query

    ####################################################################################################################
    # Archive Reaction Patterns
    ####################################################################################################################

    @staticmethod
    def construct_archive_reaction_patterns_query() -> Select[ArchiveReactionPatternsTuple]:
        """
        Construct the archive chemical reaction patterns query of the database.

        :returns: The archive chemical reaction patterns query of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveReactionPattern
        )

    @staticmethod
    def construct_archive_reaction_patterns_from_sources_query(
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[ArchiveReactionPatternsFromSourcesTuple]:
        """
        Construct the archive chemical reaction patterns from sources query of the database.

        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the archive chemical reaction patterns should be retrieved.

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

    ####################################################################################################################
    # Workbench Reaction Patterns
    ####################################################################################################################

    @staticmethod
    def construct_workbench_reaction_patterns_query(
            workbench_reaction_pattern_reactant_compound_smarts_strings: Optional[Iterable[str]],
            workbench_reaction_pattern_spectator_compound_smarts_strings: Optional[Iterable[str]],
            workbench_reaction_pattern_product_compound_smarts_strings: Optional[Iterable[str]]
    ) -> Select[WorkbenchReactionPatternsTuple]:
        """
        Construct the workbench chemical reaction patterns query of the database.

        :parameter workbench_reaction_pattern_reactant_compound_smarts_strings: The SMARTS strings of the reactant
            compound patterns that should be present in the workbench chemical reaction patterns.
        :parameter workbench_reaction_pattern_spectator_compound_smarts_strings: The SMARTS strings of the spectator
            compound patterns that should be present in the workbench chemical reaction patterns.
        :parameter workbench_reaction_pattern_product_compound_smarts_strings: The SMARTS strings of the product
            compound patterns that should be present in the workbench chemical reaction patterns.

        :returns: The workbench chemical reaction patterns query of the database.
        """

        workbench_reaction_pattern_queries = list()

        if workbench_reaction_pattern_reactant_compound_smarts_strings is not None:
            workbench_reaction_pattern_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_reaction_pattern_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_compound_pattern_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        other=workbench_reaction_pattern_reactant_compound_smarts_strings
                    )
                ).distinct()
            )

        if workbench_reaction_pattern_spectator_compound_smarts_strings is not None:
            workbench_reaction_pattern_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_reaction_pattern_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_compound_pattern_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        other=workbench_reaction_pattern_spectator_compound_smarts_strings
                    )
                ).distinct()
            )

        if workbench_reaction_pattern_product_compound_smarts_strings is not None:
            workbench_reaction_pattern_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_reaction_pattern_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_compound_pattern_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        other=workbench_reaction_pattern_product_compound_smarts_strings
                    )
                ).distinct()
            )

        if len(workbench_reaction_pattern_queries) == 0:
            return select(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern
            )

        else:
            return select(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id.in_(
                    other=intersect(
                        *workbench_reaction_pattern_queries
                    )
                )
            )

    @staticmethod
    def construct_workbench_reaction_patterns_from_sources_query(
            workbench_reaction_pattern_reactant_compound_smarts_strings: Optional[Iterable[str]],
            workbench_reaction_pattern_spectator_compound_smarts_strings: Optional[Iterable[str]],
            workbench_reaction_pattern_product_compound_smarts_strings: Optional[Iterable[str]],
            archive_source_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[WorkbenchReactionPatternsFromSourcesTuple]:
        """
        Construct the workbench chemical reaction patterns query of the database.

        :parameter workbench_reaction_pattern_reactant_compound_smarts_strings: The SMARTS strings of the reactant
            compound patterns that should be present in the workbench chemical reaction patterns.
        :parameter workbench_reaction_pattern_spectator_compound_smarts_strings: The SMARTS strings of the spectator
            compound patterns that should be present in the workbench chemical reaction patterns.
        :parameter workbench_reaction_pattern_product_compound_smarts_strings: The SMARTS strings of the product
            compound patterns that should be present in the workbench chemical reaction patterns.
        :parameter archive_source_names_versions_and_file_names: The names, versions, and file names of the archive
            sources from which the workbench chemical reaction patterns should be retrieved.

        :returns: The workbench chemical reaction patterns query of the database.
        """

        workbench_reaction_patterns_from_sources_queries = list()

        if workbench_reaction_pattern_reactant_compound_smarts_strings is not None:
            workbench_reaction_patterns_from_sources_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_reaction_pattern_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_compound_pattern_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        other=workbench_reaction_pattern_reactant_compound_smarts_strings
                    )
                ).distinct()
            )

        if workbench_reaction_pattern_spectator_compound_smarts_strings is not None:
            workbench_reaction_patterns_from_sources_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_reaction_pattern_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_compound_pattern_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        other=workbench_reaction_pattern_spectator_compound_smarts_strings
                    )
                ).distinct()
            )

        if workbench_reaction_pattern_product_compound_smarts_strings is not None:
            workbench_reaction_patterns_from_sources_queries.append(
                select(
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_reaction_pattern_id
                    )
                ).join(
                    target=CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
                    onclause=(
                        CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_compound_pattern_id ==
                        CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        other=workbench_reaction_pattern_product_compound_smarts_strings
                    )
                ).distinct()
            )

        workbench_reaction_patterns_from_sources_query = select(
            CaCSSQLiteDatabaseModelWorkbenchReactionPattern,
            CaCSSQLiteDatabaseModelArchiveReactionPattern,
            CaCSSQLiteDatabaseModelArchiveSource
        ).join(
            target=CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id ==
                CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive.workbench_reaction_pattern_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveReactionPattern,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive.archive_reaction_pattern_id ==
                CaCSSQLiteDatabaseModelArchiveReactionPattern.id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveReactionPatternSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveReactionPattern.id ==
                CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_reaction_pattern_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelArchiveSource,
            onclause=(
                CaCSSQLiteDatabaseModelArchiveReactionSource.archive_source_id ==
                CaCSSQLiteDatabaseModelArchiveSource.id
            )
        )

        if len(workbench_reaction_patterns_from_sources_queries) > 0:
            workbench_reaction_patterns_from_sources_query = workbench_reaction_patterns_from_sources_query.where(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id.in_(
                    other=intersect(
                        *workbench_reaction_patterns_from_sources_queries
                    )
                )
            )

        if archive_source_names_versions_and_file_names is not None:
            workbench_reaction_patterns_from_sources_query = workbench_reaction_patterns_from_sources_query.where(
                tuple_(
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name
                ).in_(
                    other=archive_source_names_versions_and_file_names
                )
            )

        return workbench_reaction_patterns_from_sources_query

    ####################################################################################################################
    # Workbench Chemical Synthesis Routes
    ####################################################################################################################

    @staticmethod
    def construct_reversed_synthesis_routes_of_workbench_compound_query(
            workbench_compound_id_or_smiles: Union[int, str],
            reversed_synthesis_routes_maximum_depth: int
    ) -> Select[Tuple[int, int, str, bool,  bool,  Optional[int],  Optional[int],  Optional[str]]]:
        """
        Construct the reversed chemical synthesis routes of a workbench chemical compound query of the database.

        :parameter workbench_compound_id_or_smiles: The ID or SMILES string of the workbench chemical compound.
        :parameter reversed_synthesis_routes_maximum_depth: The maximum depth of the reversed chemical synthesis routes.

        :returns: The reversed chemical synthesis routes of a workbench chemical compound query of the database.
        """

        if isinstance(workbench_compound_id_or_smiles, int):
            workbench_compound_id_or_smiles_column = CaCSSQLiteDatabaseModelWorkbenchCompound.id

        else:
            workbench_compound_id_or_smiles_column = CaCSSQLiteDatabaseModelWorkbenchCompound.smiles

        workbench_synthesis_routes_base_query = select(
            cast(
                expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                type_=String
            ).label(
                name="synthesis_route"
            ),
            literal(
                value=0
            ).label(
                name="synthesis_route_depth"
            ),
            not_(
                CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block
            ).label(
                name="expand_synthesis_route"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.id.label(
                name="reaction_product_compound_id"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.label(
                name="reaction_product_compound_smiles"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block.label(
                name="reaction_product_compound_is_building_block"
            ),
            literal(
                value=None
            ).label(
                name="prior_reaction_id"
            ),
            CaCSSQLiteDatabaseModelWorkbenchReaction.id.label(
                name="posterior_reaction_id"
            ),
            CaCSSQLiteDatabaseModelWorkbenchReaction.smiles.label(
                name="posterior_reaction_smiles"
            )
        ).select_from(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        ).join(
            target=CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchCompound.id ==
                CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_compound_id
            )
        ).join(
            target=CaCSSQLiteDatabaseModelWorkbenchReaction,
            onclause=(
                CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_reaction_id ==
                CaCSSQLiteDatabaseModelWorkbenchReaction.id
            )
        ).where(
            workbench_compound_id_or_smiles_column == bindparam(
                key="workbench_compound_id_or_smiles",
                value=workbench_compound_id_or_smiles
            )
        ).cte(
            recursive=True
        )

        synthesis_route_column_value = workbench_synthesis_routes_base_query.c.synthesis_route + literal(
            value="->"
        ) + cast(
            expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id,
            type_=String
        )

        synthesis_route_depth_column_value = workbench_synthesis_routes_base_query.c.synthesis_route_depth + 1

        expand_synthesis_route_column_value = and_(
            workbench_synthesis_routes_base_query.c.expand_synthesis_route,
            not_(
                or_(
                    func.instr(
                        workbench_synthesis_routes_base_query.c.synthesis_route,
                        literal(
                            value="->"
                        ) + cast(
                            expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                            type_=String
                        )
                    ) > 0,
                    and_(
                        workbench_compound_id_or_smiles_column == bindparam(
                            key="workbench_compound_id_or_smiles",
                            value=workbench_compound_id_or_smiles
                        ),
                        synthesis_route_depth_column_value > literal(
                            value=1
                        )
                    )
                )
            )
        )

        workbench_synthesis_routes_recursive_query = select(
            synthesis_route_column_value.label(
                name="synthesis_route"
            ),
            synthesis_route_depth_column_value.label(
                name="synthesis_route_depth"
            ),
            expand_synthesis_route_column_value.label(
                name="expand_synthesis_route"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.id.label(
                name="reaction_product_compound_id"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.label(
                name="reaction_product_compound_smiles"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block.label(
                name="reaction_product_compound_is_building_block"
            ),
            workbench_synthesis_routes_base_query.c.posterior_reaction_id.label(
                name="prior_reaction_id"
            ),
            case(
                (expand_synthesis_route_column_value, CaCSSQLiteDatabaseModelWorkbenchReaction.id),
                else_=literal(
                    value=None
                )
            ).label(
                name="posterior_reaction_id"
            ),
            case(
                (expand_synthesis_route_column_value, CaCSSQLiteDatabaseModelWorkbenchReaction.smiles),
                else_=literal(
                    value=None
                )
            ).label(
                name="posterior_reaction_smiles"
            )
        ).select_from(
            workbench_synthesis_routes_base_query.join(
                right=CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound,
                onclause=(
                    workbench_synthesis_routes_base_query.c.posterior_reaction_id ==
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_reaction_id
                )
            ).join(
                right=CaCSSQLiteDatabaseModelWorkbenchCompound,
                onclause=(
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_compound_id ==
                    CaCSSQLiteDatabaseModelWorkbenchCompound.id
                )
            ).outerjoin(
                right=CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound,
                onclause=(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.id ==
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_compound_id
                )
            ).outerjoin(
                right=CaCSSQLiteDatabaseModelWorkbenchReaction,
                onclause=(
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_reaction_id ==
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id
                )
            )
        ).where(
            workbench_synthesis_routes_base_query.c.synthesis_route_depth < bindparam(
                key="reversed_synthesis_routes_maximum_depth",
                value=reversed_synthesis_routes_maximum_depth
            )
        )

        workbench_synthesis_routes_query = workbench_synthesis_routes_base_query.union_all(
            workbench_synthesis_routes_recursive_query
        )

        reaction_product_compound_is_dead_end = case(
            (or_(
                workbench_synthesis_routes_query.c.posterior_reaction_id.is_(
                    None
                ),
                workbench_synthesis_routes_query.c.expand_synthesis_route == literal(
                    value=False
                )
            ), literal(
                value=True
            )),
            else_=literal(
                value=False
            )
        )

        return select(
            workbench_synthesis_routes_query.c.synthesis_route_depth,
            workbench_synthesis_routes_query.c.reaction_product_compound_id,
            workbench_synthesis_routes_query.c.reaction_product_compound_smiles,
            workbench_synthesis_routes_query.c.reaction_product_compound_is_building_block,
            reaction_product_compound_is_dead_end.label(
                name="reaction_product_compound_is_dead_end"
            ),
            workbench_synthesis_routes_query.c.prior_reaction_id,
            workbench_synthesis_routes_query.c.posterior_reaction_id,
            workbench_synthesis_routes_query.c.posterior_reaction_smiles
        ).order_by(
            workbench_synthesis_routes_query.c.synthesis_route_depth,
            workbench_synthesis_routes_query.c.prior_reaction_id,
            workbench_synthesis_routes_query.c.reaction_product_compound_id
        )

    ####################################################################################################################
    ####################################################################################################################
