""" The ``ncsw_data.storage.cacs.sqlite_db.utility`` package ``select_`` module. """

from typing import Any, Iterable, Optional, Tuple

from sqlalchemy.sql import and_, bindparam, case, cast, intersect, not_, or_, select, tuple_
from sqlalchemy.sql.elements import literal
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.sqltypes import String

from ncsw_data.storage.cacs.sqlite_db.model.archive import *
from ncsw_data.storage.cacs.sqlite_db.model.workbench import *

from ncsw_data.storage.cacs.sqlite_db.utility.typing import (
    CaCSSQLiteDatabaseArchiveCompoundTuple,
    CaCSSQLiteDatabaseArchiveCompoundFromSourceTuple,
    CaCSSQLiteDatabaseArchiveCompoundPatternTuple,
    CaCSSQLiteDatabaseArchiveCompoundPatternFromSourceTuple,
    CaCSSQLiteDatabaseArchiveReactionTuple,
    CaCSSQLiteDatabaseArchiveReactionFromSourceTuple,
    CaCSSQLiteDatabaseArchiveReactionPatternTuple,
    CaCSSQLiteDatabaseArchiveReactionPatternFromSourceTuple,
    CaCSSQLiteDatabaseWorkbenchCompoundTuple,
    CaCSSQLiteDatabaseWorkbenchCompoundFromSourceTuple,
    CaCSSQLiteDatabaseWorkbenchCompoundPatternTuple,
    CaCSSQLiteDatabaseWorkbenchCompoundPatternFromSourceTuple,
    CaCSSQLiteDatabaseWorkbenchReactionTuple,
    CaCSSQLiteDatabaseWorkbenchReactionFromSourceTuple,
    CaCSSQLiteDatabaseWorkbenchReactionPatternTuple,
    CaCSSQLiteDatabaseWorkbenchReactionPatternFromSourceTuple,
)


class CaCSSQLiteDatabaseSelectUtility:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database select utility class. """

    ####################################################################################################################
    # archive_source AS as
    ####################################################################################################################

    @staticmethod
    def _add_archive_source_where_clause_to_select_statement(
            select_statement: Select[Any],
            as_names_versions_and_file_names: Iterable[Tuple[str, str, str]]
    ) -> Select[Any]:
        """
        Add the archive source where clause to a select statement of the database.

        :parameter select_statement: The select statement of the database.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources.

        :returns: The select statement of the database with the archive source where clause.
        """

        return select_statement.where(
            tuple_(
                CaCSSQLiteDatabaseModelArchiveSource.name,
                CaCSSQLiteDatabaseModelArchiveSource.version,
                CaCSSQLiteDatabaseModelArchiveSource.file_name
            ).in_(
                as_names_versions_and_file_names
            )
        )

    ####################################################################################################################
    # archive_compound AS ac
    ####################################################################################################################

    @staticmethod
    def construct_archive_compound_select_statement(
    ) -> Select[CaCSSQLiteDatabaseArchiveCompoundTuple]:
        """
        Construct the archive chemical compound select statement of the database.

        :returns: The archive chemical compound select statement of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveCompound
        )

    @staticmethod
    def construct_archive_compound_from_source_select_statement(
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseArchiveCompoundFromSourceTuple]:
        """
        Construct the archive chemical compound from source select statement of the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compounds should be retrieved.

        :returns: The archive chemical compound from source select statement of the database.
        """

        ac_from_source_select_statement = select(
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

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=ac_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return ac_from_source_select_statement

    ####################################################################################################################
    # archive_reaction AS ar
    ####################################################################################################################

    @staticmethod
    def construct_archive_reaction_select_statement(
    ) -> Select[CaCSSQLiteDatabaseArchiveReactionTuple]:
        """
        Construct the archive chemical reaction select statement of the database.

        :returns: The archive chemical reaction select statement of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveReaction
        )

    @staticmethod
    def construct_archive_reaction_from_source_select_statement(
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseArchiveReactionFromSourceTuple]:
        """
        Construct the archive chemical reaction from source select statement of the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical reactions should be retrieved.

        :returns: The archive chemical reaction from source select statement of the database.
        """

        ar_from_source_select_statement = select(
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

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=ar_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return ar_from_source_select_statement

    ####################################################################################################################
    # archive_compound_pattern AS acp
    ####################################################################################################################

    @staticmethod
    def construct_archive_compound_pattern_select_statement(
    ) -> Select[CaCSSQLiteDatabaseArchiveCompoundPatternTuple]:
        """
        Construct the archive chemical compound pattern select statement of the database.

        :returns: The archive chemical compound pattern select statement of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveCompoundPattern
        )

    @staticmethod
    def construct_archive_compound_pattern_from_source_select_statement(
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseArchiveCompoundPatternFromSourceTuple]:
        """
        Construct the archive chemical compound pattern from source select statement of the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical compound patterns should be retrieved.

        :returns: The archive chemical compound pattern from source select statement of the database.
        """

        acp_from_source_select_statement = select(
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

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=acp_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return acp_from_source_select_statement

    ####################################################################################################################
    # archive_reaction_pattern AS arp
    ####################################################################################################################

    @staticmethod
    def construct_archive_reaction_pattern_select_statement(
    ) -> Select[CaCSSQLiteDatabaseArchiveReactionPatternTuple]:
        """
        Construct the archive chemical reaction pattern select statement of the database.

        :returns: The archive chemical reaction pattern select statement of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelArchiveReactionPattern
        )

    @staticmethod
    def construct_archive_reaction_pattern_from_source_select_statement(
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseArchiveReactionPatternFromSourceTuple]:
        """
        Construct the archive chemical reaction pattern from source select statement of the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the archive chemical reaction patterns should be retrieved.

        :returns: The archive chemical reaction pattern from source select statement of the database.
        """

        arp_from_source_select_statement = select(
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

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=arp_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return arp_from_source_select_statement

    ####################################################################################################################
    # workbench_compound AS wc
    ####################################################################################################################

    @staticmethod
    def construct_workbench_compound_select_statement(
            wcs_are_building_blocks: Optional[bool]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchCompoundTuple]:
        """
        Construct the workbench chemical compound select statement of the database.

        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.

        :returns: The workbench chemical compound select statement of the database.
        """

        wc_select_statement = select(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        )

        if wcs_are_building_blocks is not None:
            return wc_select_statement.where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block == wcs_are_building_blocks
            )

        return wc_select_statement

    @staticmethod
    def construct_workbench_compound_from_source_select_statement(
            wcs_are_building_blocks: Optional[bool],
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchCompoundFromSourceTuple]:
        """
        Construct the workbench chemical compound from source select statement of the database.

        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical compounds should be retrieved.

        :returns: The workbench chemical compound from source select statement of the database.
        """

        wc_from_source_select_statement = select(
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

        if wcs_are_building_blocks is not None:
            wc_from_source_select_statement = wc_from_source_select_statement.where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block == wcs_are_building_blocks
            )

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=wc_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return wc_from_source_select_statement

    ####################################################################################################################
    # workbench_reaction AS wr
    ####################################################################################################################

    @staticmethod
    def construct_workbench_reaction_select_statement(
            wrrc_smiles_strings: Optional[Iterable[str]],
            wrsc_smiles_strings: Optional[Iterable[str]],
            wrpc_smiles_strings: Optional[Iterable[str]]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchReactionTuple]:
        """
        Construct the workbench chemical reaction select statement of the database.

        :parameter wrrc_smiles_strings: The SMILES strings of the workbench chemical reaction reactant compounds.
        :parameter wrsc_smiles_strings: The SMILES strings of the workbench chemical reaction spectator compounds.
        :parameter wrpc_smiles_strings: The SMILES strings of the workbench chemical reaction product compounds.

        :returns: The workbench chemical reaction select statement of the database.
        """

        wr_select_statements = list()

        if wrrc_smiles_strings is not None:
            wr_select_statements.append(
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
                        wrrc_smiles_strings
                    )
                ).distinct()
            )

        if wrsc_smiles_strings is not None:
            wr_select_statements.append(
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
                        wrsc_smiles_strings
                    )
                ).distinct()
            )

        if wrpc_smiles_strings is not None:
            wr_select_statements.append(
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
                        wrpc_smiles_strings
                    )
                ).distinct()
            )

        wr_select_statement = select(
            CaCSSQLiteDatabaseModelWorkbenchReaction
        )

        if len(wr_select_statements) > 0:
            return wr_select_statement.where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id.in_(
                    intersect(
                        *wr_select_statements
                    )
                )
            )

        return wr_select_statement

    @staticmethod
    def construct_workbench_reaction_from_source_select_statement(
            wrrc_smiles_strings: Optional[Iterable[str]],
            wrsc_smiles_strings: Optional[Iterable[str]],
            wrpc_smiles_strings: Optional[Iterable[str]],
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchReactionFromSourceTuple]:
        """
        Construct the workbench chemical reaction from source select statement of the database.

        :parameter wrrc_smiles_strings: The SMILES strings of the workbench chemical reaction reactant compounds.
        :parameter wrsc_smiles_strings: The SMILES strings of the workbench chemical reaction spectator compounds.
        :parameter wrpc_smiles_strings: The SMILES strings of the workbench chemical reaction product compounds.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical reactions should be retrieved.

        :returns: The workbench chemical reaction from source select statement of the database.
        """

        wr_from_source_select_statements = list()

        if wrrc_smiles_strings is not None:
            wr_from_source_select_statements.append(
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
                        wrrc_smiles_strings
                    )
                ).distinct()
            )

        if wrsc_smiles_strings is not None:
            wr_from_source_select_statements.append(
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
                        wrsc_smiles_strings
                    )
                ).distinct()
            )

        if wrpc_smiles_strings is not None:
            wr_from_source_select_statements.append(
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
                        wrpc_smiles_strings
                    )
                ).distinct()
            )

        wr_from_source_select_statement = select(
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

        if len(wr_from_source_select_statements) > 0:
            wr_from_source_select_statement = wr_from_source_select_statement.where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id.in_(
                    intersect(
                        *wr_from_source_select_statements
                    )
                )
            )

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=wr_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return wr_from_source_select_statement

    ####################################################################################################################
    # workbench_compound_pattern AS wcp
    ####################################################################################################################

    @staticmethod
    def construct_workbench_compound_pattern_select_statement(
    ) -> Select[CaCSSQLiteDatabaseWorkbenchCompoundPatternTuple]:
        """
        Construct the workbench chemical compound pattern select statement of the database.

        :returns: The workbench chemical compound pattern select statement of the database.
        """

        return select(
            CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
        )

    @staticmethod
    def construct_workbench_compound_pattern_from_source_select_statement(
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchCompoundPatternFromSourceTuple]:
        """
        Construct the workbench chemical compound pattern from source select statement of the database.

        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical compound patterns should be retrieved.

        :returns: The workbench chemical compound pattern from source select statement of the database.
        """

        wcp_from_source_select_statement = select(
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

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=wcp_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return wcp_from_source_select_statement

    ####################################################################################################################
    # workbench_reaction_pattern AS wrp
    ####################################################################################################################

    @staticmethod
    def construct_workbench_reaction_pattern_select_statement(
            wrrcp_smarts_strings: Optional[Iterable[str]],
            wrscp_smarts_strings: Optional[Iterable[str]],
            wrpcp_smarts_strings: Optional[Iterable[str]]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchReactionPatternTuple]:
        """
        Construct the workbench chemical reaction pattern select statement of the database.

        :parameter wrrcp_smarts_strings: The SMARTS strings of the workbench chemical reaction reactant compound
            patterns.
        :parameter wrscp_smarts_strings: The SMARTS strings of the workbench chemical reaction spectator compound
            patterns.
        :parameter wrpcp_smarts_strings: The SMARTS strings of the workbench chemical reaction product compound
            patterns.

        :returns: The workbench chemical reaction pattern select statement of the database.
        """

        wrp_select_statements = list()

        if wrrcp_smarts_strings is not None:
            wrp_select_statements.append(
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
                        wrrcp_smarts_strings
                    )
                ).distinct()
            )

        if wrscp_smarts_strings is not None:
            wrp_select_statements.append(
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
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_compound_pattern_id
                        == CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        wrscp_smarts_strings
                    )
                ).distinct()
            )

        if wrpcp_smarts_strings is not None:
            wrp_select_statements.append(
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
                        wrpcp_smarts_strings
                    )
                ).distinct()
            )

        wrp_select_statement = select(
            CaCSSQLiteDatabaseModelWorkbenchReactionPattern
        )

        if len(wrp_select_statements) > 0:
            return wrp_select_statement.where(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id.in_(
                    intersect(
                        *wrp_select_statements
                    )
                )
            )

        return wrp_select_statement

    @staticmethod
    def construct_workbench_reaction_pattern_from_source_select_statement(
            wrrcp_smarts_strings: Optional[Iterable[str]],
            wrscp_smarts_strings: Optional[Iterable[str]],
            wrpcp_smarts_strings: Optional[Iterable[str]],
            as_names_versions_and_file_names: Optional[Iterable[Tuple[str, str, str]]]
    ) -> Select[CaCSSQLiteDatabaseWorkbenchReactionPatternFromSourceTuple]:
        """
        Construct the workbench chemical reaction pattern from source select statement of the database.

        :parameter wrrcp_smarts_strings: The SMARTS strings of the workbench chemical reaction reactant compound
            patterns.
        :parameter wrscp_smarts_strings: The SMARTS strings of the workbench chemical reaction spectator compound
            patterns.
        :parameter wrpcp_smarts_strings: The SMARTS strings of the workbench chemical reaction product compound
            patterns.
        :parameter as_names_versions_and_file_names: The names, versions, and file names of the archive sources from
            which the workbench chemical reaction patterns should be retrieved.

        :returns: The workbench chemical reaction pattern from source select statement of the database.
        """

        wrp_from_source_select_statements = list()

        if wrrcp_smarts_strings is not None:
            wrp_from_source_select_statements.append(
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
                        wrrcp_smarts_strings
                    )
                ).distinct()
            )

        if wrscp_smarts_strings is not None:
            wrp_from_source_select_statements.append(
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
                        CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_compound_pattern_id
                        == CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id
                    )
                ).where(
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                        wrscp_smarts_strings
                    )
                ).distinct()
            )

        if wrpcp_smarts_strings is not None:
            wrp_from_source_select_statements.append(
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
                        wrpcp_smarts_strings
                    )
                ).distinct()
            )

        wrp_from_source_select_statement = select(
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
                CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_source_id ==
                CaCSSQLiteDatabaseModelArchiveSource.id
            )
        )

        if len(wrp_from_source_select_statements) > 0:
            wrp_from_source_select_statement = wrp_from_source_select_statement.where(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id.in_(
                    intersect(
                        *wrp_from_source_select_statements
                    )
                )
            )

        if as_names_versions_and_file_names is not None:
            return CaCSSQLiteDatabaseSelectUtility._add_archive_source_where_clause_to_select_statement(
                select_statement=wrp_from_source_select_statement,
                as_names_versions_and_file_names=as_names_versions_and_file_names
            )

        return wrp_from_source_select_statement

    ####################################################################################################################
    # synthesis_route AS sr
    ####################################################################################################################

    @staticmethod
    def construct_reversed_synthesis_route_select_statement(
            wc_smiles: str,
            reversed_sr_maximum_depth: int
    ) -> Select[Tuple[int, int, str, bool, bool, Optional[int], Optional[int], Optional[str]]]:
        """
        Construct the reversed chemical synthesis route select statement of the database.

        :parameter wc_smiles: The SMILES string of the workbench chemical compound.
        :parameter reversed_sr_maximum_depth: The maximum depth of the reversed chemical synthesis routes.

        :returns: The reversed chemical synthesis route select statement of the database.
        """

        reversed_sr_base_select_statement = select(
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
                name="target_compound_id"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.label(
                name="target_compound_smiles"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block.label(
                name="target_compound_is_building_block"
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
            CaCSSQLiteDatabaseModelWorkbenchCompound.smiles == bindparam(
                key="wc_smiles",
                value=wc_smiles
            )
        ).cte(
            recursive=True
        )

        synthesis_route_column_value = reversed_sr_base_select_statement.c.synthesis_route + literal(
            value="->"
        ) + cast(
            expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id,
            type_=String
        )

        synthesis_route_depth_column_value = reversed_sr_base_select_statement.c.synthesis_route_depth + 1

        expand_synthesis_route_column_value = and_(
            reversed_sr_base_select_statement.c.expand_synthesis_route,
            not_(
                or_(
                    func.instr(
                        reversed_sr_base_select_statement.c.synthesis_route,
                        literal(
                            value="->"
                        ) + cast(
                            expression=CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                            type_=String
                        )
                    ) > 0,
                    and_(
                        CaCSSQLiteDatabaseModelWorkbenchCompound.smiles == bindparam(
                            key="wc_smiles",
                            value=wc_smiles
                        ),
                        synthesis_route_depth_column_value > literal(
                            value=1
                        )
                    )
                )
            )
        )

        reversed_sr_recursive_select_statement = select(
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
                name="target_compound_id"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.label(
                name="target_compound_smiles"
            ),
            CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block.label(
                name="target_compound_is_building_block"
            ),
            reversed_sr_base_select_statement.c.posterior_reaction_id.label(
                name="prior_reaction_id"
            ),
            case(
                (
                    expand_synthesis_route_column_value,
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                ),
                else_=literal(
                    value=None
                )
            ).label(
                name="posterior_reaction_id"
            ),
            case(
                (
                    expand_synthesis_route_column_value,
                    CaCSSQLiteDatabaseModelWorkbenchReaction.smiles
                ),
                else_=literal(
                    value=None
                )
            ).label(
                name="posterior_reaction_smiles"
            )
        ).select_from(
            reversed_sr_base_select_statement.join(
                right=CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound,
                onclause=(
                    reversed_sr_base_select_statement.c.posterior_reaction_id ==
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
            reversed_sr_base_select_statement.c.synthesis_route_depth < bindparam(
                key="reversed_sr_maximum_depth",
                value=reversed_sr_maximum_depth
            )
        )

        reversed_sr_select_statement = reversed_sr_base_select_statement.union_all(
            reversed_sr_recursive_select_statement
        )

        target_compound_is_dead_end_column_value = case(
            (
                or_(
                    reversed_sr_select_statement.c.posterior_reaction_id.is_(
                        None
                    ),
                    reversed_sr_select_statement.c.expand_synthesis_route == literal(
                        value=False
                    )
                ),
                literal(
                    value=True
                )
            ),
            else_=literal(
                value=False
            )
        )

        return select(
            reversed_sr_select_statement.c.synthesis_route_depth,
            reversed_sr_select_statement.c.target_compound_id,
            reversed_sr_select_statement.c.target_compound_smiles,
            reversed_sr_select_statement.c.target_compound_is_building_block,
            target_compound_is_dead_end_column_value.label(
                name="target_compound_is_dead_end"
            ),
            reversed_sr_select_statement.c.prior_reaction_id,
            reversed_sr_select_statement.c.posterior_reaction_id,
            reversed_sr_select_statement.c.posterior_reaction_smiles
        ).order_by(
            reversed_sr_select_statement.c.synthesis_route_depth,
            reversed_sr_select_statement.c.prior_reaction_id,
            reversed_sr_select_statement.c.target_compound_id
        )
