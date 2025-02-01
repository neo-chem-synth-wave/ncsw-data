""" The ``ncsw_data.storage.cacs.sqlite.utility`` package ``select`` module. """

from typing import Iterable, Optional, Tuple, Union

from sqlalchemy.sql import and_, bindparam, case, cast, intersect, not_, or_, select, tuple_
from sqlalchemy.sql.elements import literal
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.sqltypes import String

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
    def construct_workbench_reactions_query(
            workbench_reaction_reactant_compound_smiles_strings: Optional[Iterable[str]] = None,
            workbench_reaction_spectator_compound_smiles_strings: Optional[Iterable[str]] = None,
            workbench_reaction_product_compound_smiles_strings: Optional[Iterable[str]] = None
    ) -> Select[Tuple[CaCSSQLiteDatabaseModelWorkbenchReaction]]:
        """
        Construct the workbench chemical reactions query of the database.

        :parameter workbench_reaction_reactant_compound_smiles_strings: The reactant compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the reactant chemical compounds.
        :parameter workbench_reaction_spectator_compound_smiles_strings: The spectator compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the spectator chemical compounds.
        :parameter workbench_reaction_product_compound_smiles_strings: The product compound SMILES strings of the
            workbench chemical reactions that should be retrieved. The value `None` indicates that the workbench
            chemical reactions should be retrieved regardless of the product chemical compounds.

        :returns: The workbench chemical reactions query of the database.
        """

        workbench_reaction_queries = list()

        if workbench_reaction_reactant_compound_smiles_strings is not None:
            workbench_reaction_queries.append(
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
            workbench_reaction_queries.append(
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
            workbench_reaction_queries.append(
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

        if len(workbench_reaction_queries) == 0:
            return select(
                CaCSSQLiteDatabaseModelWorkbenchReaction
            )

        else:
            return select(
                CaCSSQLiteDatabaseModelWorkbenchReaction
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id.in_(
                    intersect(
                        *workbench_reaction_queries
                    )
                )
            )

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
