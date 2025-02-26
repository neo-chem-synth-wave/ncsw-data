""" The ``ncsw_data.storage.cacs.sqlite.utility`` package ``insert`` module. """

from itertools import chain
from typing import Dict, Iterable, Mapping, Optional, Sequence

from sqlalchemy.dialects.sqlite.dml import insert
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import and_, select

from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.workbench import *


class CaCSSQLiteDatabaseInsertUtility:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database insert utility class. """

    ####################################################################################################################
    # Archive Sources
    ####################################################################################################################

    @staticmethod
    def insert_and_select_archive_source(
            database_session: Session,
            name: str,
            version: str,
            file_name: str,
            created_by: str
    ) -> int:
        """
        Insert and select an archive source from the database.

        :parameter database_session: The session of the database.
        :parameter name: The name of the archive source.
        :parameter version: The version of the archive source.
        :parameter file_name: The file name of the archive source.
        :parameter created_by: The user of the database inserting the archive source.

        :returns: The ID of the archive source.
        """

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveSource
            ).values(
                name=name,
                version=version,
                file_name=file_name,
                created_by=created_by
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name,
                ]
            )
        )

        return database_session.scalar(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveSource.id
            ).where(
                CaCSSQLiteDatabaseModelArchiveSource.name == name,
                CaCSSQLiteDatabaseModelArchiveSource.version == version,
                CaCSSQLiteDatabaseModelArchiveSource.file_name == file_name
            )
        )

    ####################################################################################################################
    # Archive Compounds
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_compounds(
            database_session: Session,
            smiles_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the archive chemical compounds from the database.

        :parameter database_session: The session of the database.
        :parameter smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter created_by: The user of the database inserting the archive chemical compounds.

        :returns: The archive chemical compound SMILES string to ID dictionary.
        """

        archive_compounds = list()

        for smiles in smiles_strings:
            archive_compounds.append({
                "smiles": smiles,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompound.id,
                    CaCSSQLiteDatabaseModelArchiveCompound.smiles,
                ]
            ),
            params=archive_compounds
        )

        archive_compounds = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveCompound.id,
                CaCSSQLiteDatabaseModelArchiveCompound.smiles
            ).where(
                CaCSSQLiteDatabaseModelArchiveCompound.smiles.in_(
                    other=smiles_strings
                )
            )
        ).all()

        archive_compound_smiles_to_id = dict()

        for archive_compound in archive_compounds:
            archive_compound_smiles_to_id[archive_compound.smiles] = archive_compound.id

        return archive_compound_smiles_to_id

    @staticmethod
    def _insert_archive_compound_sources(
            database_session: Session,
            archive_compound_ids: Iterable[int],
            archive_source_id: int
    ) -> None:
        """
        Insert the archive chemical compound sources into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_ids: The IDs of the archive chemical compounds.
        :parameter archive_source_id: The ID of the archive source.
        """

        archive_compound_sources = list()

        for archive_compound_id in archive_compound_ids:
            archive_compound_sources.append({
                "archive_compound_id": archive_compound_id,
                "archive_source_id": archive_source_id,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompoundSource.archive_compound_id,
                    CaCSSQLiteDatabaseModelArchiveCompoundSource.archive_source_id,
                ]
            ),
            params=archive_compound_sources
        )

    @staticmethod
    def insert_archive_compounds(
            database_session: Session,
            archive_compound_smiles_strings: Iterable[str],
            archive_source_id: int,
            archive_compound_created_by: str
    ) -> None:
        """
        Insert the archive chemical compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter archive_source_id: The ID of the archive source.
        :parameter archive_compound_created_by: The user of the database inserting the archive chemical compounds.
        """

        archive_compound_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_compounds(
            database_session=database_session,
            smiles_strings=archive_compound_smiles_strings,
            created_by=archive_compound_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_compound_sources(
            database_session=database_session,
            archive_compound_ids=archive_compound_smiles_to_id.values(),
            archive_source_id=archive_source_id
        )

    ####################################################################################################################
    # Workbench Compounds
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_compounds(
            database_session: Session,
            smiles_strings: Iterable[str],
            are_building_blocks: Optional[Sequence[bool]],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compounds from the database.

        :parameter database_session: The session of the database.
        :parameter smiles_strings: The SMILES strings of the workbench chemical compounds.
        :parameter are_building_blocks: The boolean indicators of whether the workbench chemical compounds are building
            blocks.
        :parameter created_by: The user of the database inserting the workbench chemical compounds.

        :returns: The workbench chemical compound SMILES string to ID dictionary.
        """

        workbench_compounds = list()

        for smiles_index, smiles in enumerate(smiles_strings):
            workbench_compound = {
                "smiles": smiles,
            }

            if are_building_blocks is not None:
                workbench_compound["is_building_block"] = are_building_blocks[smiles_index]

            workbench_compound["created_by"] = created_by

            workbench_compounds.append(
                workbench_compound
            )

        statement = insert(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        ).values(
            workbench_compounds
        )

        if are_building_blocks is None:
            statement = statement.on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles,
                ]
            )

        else:
            statement = statement.on_conflict_do_update(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles,
                ],
                set_={
                    "is_building_block": statement.excluded.is_building_block
                },
                where=and_(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block.is_(False),
                    statement.excluded.is_building_block.is_(True)
                )
            )

        database_session.execute(
            statement=statement
        )

        workbench_compounds = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                CaCSSQLiteDatabaseModelWorkbenchCompound.smiles
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                    other=smiles_strings
                )
            )
        ).all()

        workbench_compound_smiles_to_id = dict()

        for workbench_compound in workbench_compounds:
            workbench_compound_smiles_to_id[workbench_compound.smiles] = workbench_compound.id

        return workbench_compound_smiles_to_id

    @staticmethod
    def _insert_workbench_compound_archives(
            database_session: Session,
            archive_compound_id_to_workbench_compound_smiles: Mapping[int, str],
            workbench_compound_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound archives into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_id_to_workbench_compound_smiles: The archive chemical compound ID to workbench
            chemical compound SMILES string mapping.
        :parameter workbench_compound_smiles_to_id: The workbench chemical compound SMILES string to ID mapping.
        """

        workbench_compound_archives = list()

        for archive_compound_id, workbench_compound_smiles in archive_compound_id_to_workbench_compound_smiles.items():
            workbench_compound_archives.append({
                "workbench_compound_id": workbench_compound_smiles_to_id[workbench_compound_smiles],
                "archive_compound_id": archive_compound_id,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundArchive.workbench_compound_id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundArchive.archive_compound_id,
                ]
            ),
            params=workbench_compound_archives
        )

    @staticmethod
    def insert_workbench_compounds(
            database_session: Session,
            archive_compound_id_to_workbench_compound_smiles: Mapping[int, str],
            workbench_compound_are_building_blocks: Optional[Sequence[bool]],
            workbench_compound_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_id_to_workbench_compound_smiles: The archive chemical compound ID to workbench
            chemical compound SMILES string mapping.
        :parameter workbench_compound_are_building_blocks: The boolean indicators of whether the workbench chemical
            compounds are building blocks.
        :parameter workbench_compound_created_by: The user of the database inserting the workbench chemical compounds.
        """

        workbench_compound_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            database_session=database_session,
            smiles_strings=archive_compound_id_to_workbench_compound_smiles.values(),
            are_building_blocks=workbench_compound_are_building_blocks,
            created_by=workbench_compound_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_archives(
            database_session=database_session,
            archive_compound_id_to_workbench_compound_smiles=archive_compound_id_to_workbench_compound_smiles,
            workbench_compound_smiles_to_id=workbench_compound_smiles_to_id
        )

    ####################################################################################################################
    # Archive Reactions
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_reactions(
            database_session: Session,
            smiles_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the archive chemical reactions from the database.

        :parameter database_session: The session of the database.
        :parameter smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter created_by: The user of the database inserting the archive chemical reactions.

        :returns: The archive chemical reaction SMILES string to ID dictionary.
        """

        archive_reactions = list()

        for smiles in smiles_strings:
            archive_reactions.append({
                "smiles": smiles,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReaction
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReaction.id,
                    CaCSSQLiteDatabaseModelArchiveReaction.smiles,
                ]
            ),
            params=archive_reactions
        )

        archive_reactions = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveReaction.id,
                CaCSSQLiteDatabaseModelArchiveReaction.smiles
            ).where(
                CaCSSQLiteDatabaseModelArchiveReaction.smiles.in_(
                    other=smiles_strings
                )
            )
        ).all()

        archive_reaction_smiles_to_id = dict()

        for archive_reaction in archive_reactions:
            archive_reaction_smiles_to_id[archive_reaction.smiles] = archive_reaction.id

        return archive_reaction_smiles_to_id

    @staticmethod
    def _insert_archive_reaction_sources(
            database_session: Session,
            archive_reaction_ids: Iterable[int],
            archive_source_id: int
    ) -> None:
        """
        Insert the archive chemical reaction sources into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_ids: The IDs of the archive chemical reactions.
        :parameter archive_source_id: The ID of the archive source.
        """

        archive_reaction_sources = list()

        for archive_reaction_id in archive_reaction_ids:
            archive_reaction_sources.append({
                "archive_reaction_id": archive_reaction_id,
                "archive_source_id": archive_source_id,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReactionSource.archive_reaction_id,
                    CaCSSQLiteDatabaseModelArchiveReactionSource.archive_source_id,
                ]
            ),
            params=archive_reaction_sources
        )

    @staticmethod
    def insert_archive_reactions(
            database_session: Session,
            archive_reaction_smiles_strings: Iterable[str],
            archive_source_id: int,
            archive_reaction_created_by: str
    ) -> None:
        """
        Insert the archive chemical reactions into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter archive_source_id: The ID of the archive source.
        :parameter archive_reaction_created_by: The user of the database inserting the archive chemical reactions.
        """

        archive_reaction_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_reactions(
            database_session=database_session,
            smiles_strings=archive_reaction_smiles_strings,
            created_by=archive_reaction_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_reaction_sources(
            database_session=database_session,
            archive_reaction_ids=archive_reaction_smiles_to_id.values(),
            archive_source_id=archive_source_id
        )

    ####################################################################################################################
    # Workbench Reactions
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_reactions(
            database_session: Session,
            smiles_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical reactions from the database.

        :parameter database_session: The session of the database.
        :parameter smiles_strings: The SMILES strings of the workbench chemical reactions.
        :parameter created_by: The user of the database inserting the workbench chemical reactions.

        :returns: The workbench chemical reaction SMILES string to ID dictionary.
        """

        workbench_reactions = list()

        for smiles in smiles_strings:
            workbench_reactions.append({
                "smiles": smiles,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReaction
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                    CaCSSQLiteDatabaseModelWorkbenchReaction.smiles,
                ]
            ),
            params=workbench_reactions
        )

        workbench_reactions = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                CaCSSQLiteDatabaseModelWorkbenchReaction.smiles
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.smiles.in_(
                    other=smiles_strings
                )
            )
        ).all()

        workbench_reaction_smiles_to_id = dict()

        for workbench_reaction in workbench_reactions:
            workbench_reaction_smiles_to_id[workbench_reaction.smiles] = workbench_reaction.id

        return workbench_reaction_smiles_to_id

    @staticmethod
    def _insert_workbench_reaction_archives(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            workbench_reaction_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction archives into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        """

        workbench_reaction_archives = list()

        for archive_reaction_id, workbench_reaction_smiles in archive_reaction_id_to_workbench_reaction_smiles.items():
            workbench_reaction_archives.append({
                "workbench_reaction_id": workbench_reaction_smiles_to_id[workbench_reaction_smiles],
                "archive_reaction_id": archive_reaction_id,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionArchive.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionArchive.archive_reaction_id,
                ]
            ),
            params=workbench_reaction_archives
        )

    @staticmethod
    def _insert_workbench_reaction_reactant_compounds(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_smiles_to_id: Mapping[str, int],
            workbench_compound_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction reactant compound SMILES strings mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        :parameter workbench_compound_created_by: The user of the database inserting the workbench chemical reaction
            reactant compounds.
        """

        workbench_reaction_reactant_compound_smiles_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
                database_session=database_session,
                smiles_strings=chain.from_iterable(
                    archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings.values()
                ),
                are_building_blocks=None,
                created_by=workbench_compound_created_by
            )

        workbench_reaction_reactant_compounds = list()

        for archive_reaction_id, workbench_reaction_smiles in archive_reaction_id_to_workbench_reaction_smiles.items():
            for workbench_reaction_reactant_compound_smiles in \
                    archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings[archive_reaction_id]:
                workbench_reaction_reactant_compounds.append({
                    "workbench_reaction_id": workbench_reaction_smiles_to_id[workbench_reaction_smiles],
                    "workbench_compound_id": workbench_reaction_reactant_compound_smiles_to_id[
                        workbench_reaction_reactant_compound_smiles
                    ],
                })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_compound_id,
                ]
            ),
            params=workbench_reaction_reactant_compounds
        )

    @staticmethod
    def _insert_workbench_reaction_spectator_compounds(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_smiles_to_id: Mapping[str, int],
            workbench_compound_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction spectator compound SMILES strings mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        :parameter workbench_compound_created_by: The user of the database inserting the workbench chemical reaction
            spectator compounds.
        """

        workbench_reaction_spectator_compound_smiles_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
                database_session=database_session,
                smiles_strings=chain.from_iterable(
                    archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings.values()
                ),
                are_building_blocks=None,
                created_by=workbench_compound_created_by
            )

        workbench_reaction_spectator_compounds = list()

        for archive_reaction_id, workbench_reaction_smiles in archive_reaction_id_to_workbench_reaction_smiles.items():
            for workbench_reaction_spectator_compound_smiles in \
                    archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings[archive_reaction_id]:
                workbench_reaction_spectator_compounds.append({
                    "workbench_reaction_id": workbench_reaction_smiles_to_id[workbench_reaction_smiles],
                    "workbench_compound_id": workbench_reaction_spectator_compound_smiles_to_id[
                        workbench_reaction_spectator_compound_smiles
                    ],
                })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_compound_id,
                ]
            ),
            params=workbench_reaction_spectator_compounds
        )

    @staticmethod
    def _insert_workbench_reaction_product_compounds(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_smiles_to_id: Mapping[str, int],
            workbench_compound_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction product compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction product compound SMILES strings mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        :parameter workbench_compound_created_by: The user of the database inserting the workbench chemical reaction
            product compounds.
        """

        workbench_reaction_product_compound_smiles_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
                database_session=database_session,
                smiles_strings=chain.from_iterable(
                    archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings.values()
                ),
                are_building_blocks=None,
                created_by=workbench_compound_created_by
            )

        workbench_reaction_product_compounds = list()

        for archive_reaction_id, workbench_reaction_smiles in archive_reaction_id_to_workbench_reaction_smiles.items():
            for workbench_reaction_product_compound_smiles in \
                    archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings[archive_reaction_id]:
                workbench_reaction_product_compounds.append({
                    "workbench_reaction_id": workbench_reaction_smiles_to_id[workbench_reaction_smiles],
                    "workbench_compound_id": workbench_reaction_product_compound_smiles_to_id[
                        workbench_reaction_product_compound_smiles
                    ],
                })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_compound_id,
                ]
            ),
            params=workbench_reaction_product_compounds
        )

    @staticmethod
    def insert_workbench_reactions(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings: Mapping[int, Iterable[str]],
            archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings: Optional[Mapping[int, Iterable[str]]],
            archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reactions into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction reactant compound SMILES strings mapping.
        :parameter archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction spectator compound SMILES strings mapping.
        :parameter archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction product compound SMILES strings mapping.
        :parameter workbench_reaction_created_by: The user of the database inserting the workbench chemical reactions.
        """

        workbench_reaction_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reactions(
            database_session=database_session,
            smiles_strings=archive_reaction_id_to_workbench_reaction_smiles.values(),
            created_by=workbench_reaction_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_archives(
            database_session=database_session,
            archive_reaction_id_to_workbench_reaction_smiles=archive_reaction_id_to_workbench_reaction_smiles,
            workbench_reaction_smiles_to_id=workbench_reaction_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compounds(
            database_session=database_session,
            archive_reaction_id_to_workbench_reaction_smiles=archive_reaction_id_to_workbench_reaction_smiles,
            archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings=(
                archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings
            ),
            workbench_reaction_smiles_to_id=workbench_reaction_smiles_to_id,
            workbench_compound_created_by=workbench_reaction_created_by
        )

        if archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings is not None:
            CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compounds(
                database_session=database_session,
                archive_reaction_id_to_workbench_reaction_smiles=archive_reaction_id_to_workbench_reaction_smiles,
                archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings=(
                    archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings
                ),
                workbench_reaction_smiles_to_id=workbench_reaction_smiles_to_id,
                workbench_compound_created_by=workbench_reaction_created_by
            )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compounds(
            database_session=database_session,
            archive_reaction_id_to_workbench_reaction_smiles=archive_reaction_id_to_workbench_reaction_smiles,
            archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings=(
                archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings
            ),
            workbench_reaction_smiles_to_id=workbench_reaction_smiles_to_id,
            workbench_compound_created_by=workbench_reaction_created_by
        )

    ####################################################################################################################
    # Archive Compound Patterns
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_compound_patterns(
            database_session: Session,
            smarts_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the archive chemical compound patterns from the database.

        :parameter database_session: The session of the database.
        :parameter smarts_strings: The SMARTS strings of the archive chemical compound patterns.
        :parameter created_by: The user of the database inserting the archive chemical compound patterns.

        :returns: The archive chemical compound pattern SMARTS string to ID dictionary.
        """

        archive_compound_patterns = list()

        for smarts in smarts_strings:
            archive_compound_patterns.append({
                "smarts": smarts,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                    CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts,
                ]
            ),
            params=archive_compound_patterns
        )

        archive_compound_patterns = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts
            ).where(
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts.in_(
                    other=smarts_strings
                )
            )
        ).all()

        archive_compound_pattern_smarts_to_id = dict()

        for archive_compound_pattern in archive_compound_patterns:
            archive_compound_pattern_smarts_to_id[archive_compound_pattern.smarts] = archive_compound_pattern.id

        return archive_compound_pattern_smarts_to_id

    @staticmethod
    def _insert_archive_compound_pattern_sources(
            database_session: Session,
            archive_compound_pattern_ids: Iterable[int],
            archive_source_id: int
    ) -> None:
        """
        Insert the archive chemical compound pattern sources into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_pattern_ids: The IDs of the archive chemical compound patterns.
        :parameter archive_source_id: The ID of the archive source.
        """

        archive_compound_pattern_sources = list()

        for archive_compound_pattern_id in archive_compound_pattern_ids:
            archive_compound_pattern_sources.append({
                "archive_compound_pattern_id": archive_compound_pattern_id,
                "archive_source_id": archive_source_id,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundPatternSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompoundPatternSource.archive_compound_pattern_id,
                    CaCSSQLiteDatabaseModelArchiveCompoundPatternSource.archive_source_id,
                ]
            ),
            params=archive_compound_pattern_sources
        )

    @staticmethod
    def insert_archive_compound_patterns(
            database_session: Session,
            archive_compound_pattern_smarts_strings: Iterable[str],
            archive_source_id: int,
            archive_compound_pattern_created_by: str
    ) -> None:
        """
        Insert the archive chemical compound patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_pattern_smarts_strings: The SMARTS strings of the archive chemical compound
            patterns.
        :parameter archive_source_id: The ID of the archive source.
        :parameter archive_compound_pattern_created_by: The user of the database inserting the archive chemical compound
            patterns.
        """

        archive_compound_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_compound_patterns(
                database_session=database_session,
                smarts_strings=archive_compound_pattern_smarts_strings,
                created_by=archive_compound_pattern_created_by
            )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_compound_pattern_sources(
            database_session=database_session,
            archive_compound_pattern_ids=archive_compound_pattern_smarts_to_id.values(),
            archive_source_id=archive_source_id
        )

    ####################################################################################################################
    # Workbench Compound Patterns
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_compound_patterns(
            database_session: Session,
            smarts_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compound patterns from the database.

        :parameter database_session: The session of the database.
        :parameter smarts_strings: The SMARTS strings of the workbench chemical compound patterns.
        :parameter created_by: The user of the database inserting the workbench chemical compound patterns.

        :returns: The workbench chemical compound pattern SMARTS string to ID dictionary.
        """

        workbench_compound_patterns = list()

        for smarts in smarts_strings:
            workbench_compound_patterns.append({
                "smarts": smarts,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts,
                ]
            ),
            params=workbench_compound_patterns
        )

        workbench_compound_patterns = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id,
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                    other=smarts_strings
                )
            )
        ).all()

        workbench_compound_pattern_smarts_to_id = dict()

        for workbench_compound_pattern in workbench_compound_patterns:
            workbench_compound_pattern_smarts_to_id[workbench_compound_pattern.smarts] = workbench_compound_pattern.id

        return workbench_compound_pattern_smarts_to_id

    @staticmethod
    def _insert_workbench_compound_pattern_archives(
            database_session: Session,
            archive_compound_pattern_id_to_workbench_compound_pattern_smarts: Mapping[int, str],
            workbench_compound_pattern_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound pattern archives into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_pattern_id_to_workbench_compound_pattern_smarts: The archive chemical compound
            pattern ID to workbench chemical compound pattern SMARTS string mapping.
        :parameter workbench_compound_pattern_smarts_to_id: The workbench chemical compound pattern SMARTS string to ID
            mapping.
        """

        workbench_compound_pattern_archives = list()

        for archive_compound_pattern_id, workbench_compound_pattern_smarts in \
                archive_compound_pattern_id_to_workbench_compound_pattern_smarts.items():
            workbench_compound_pattern_archives.append({
                "workbench_compound_pattern_id": workbench_compound_pattern_smarts_to_id[
                    workbench_compound_pattern_smarts
                ],
                "archive_compound_pattern_id": archive_compound_pattern_id,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive.workbench_compound_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive.archive_compound_pattern_id,
                ]
            ),
            params=workbench_compound_pattern_archives
        )

    @staticmethod
    def insert_workbench_compound_patterns(
            database_session: Session,
            archive_compound_pattern_id_to_workbench_compound_pattern_smarts: Mapping[int, str],
            workbench_compound_pattern_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compound patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_compound_pattern_id_to_workbench_compound_pattern_smarts: The archive chemical compound
            pattern ID to workbench chemical compound pattern SMARTS string mapping.
        :parameter workbench_compound_pattern_created_by: The user of the database inserting the workbench chemical
            compound patterns.
        """

        workbench_compound_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
                database_session=database_session,
                smarts_strings=archive_compound_pattern_id_to_workbench_compound_pattern_smarts.values(),
                created_by=workbench_compound_pattern_created_by
            )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_pattern_archives(
            database_session=database_session,
            archive_compound_pattern_id_to_workbench_compound_pattern_smarts=(
                archive_compound_pattern_id_to_workbench_compound_pattern_smarts
            ),
            workbench_compound_pattern_smarts_to_id=workbench_compound_pattern_smarts_to_id
        )

    ####################################################################################################################
    # Archive Reaction Patterns
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_reaction_patterns(
            database_session: Session,
            smarts_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the archive chemical reaction patterns from the database.

        :parameter database_session: The session of the database.
        :parameter smarts_strings: The SMARTS strings of the archive chemical reaction patterns.
        :parameter created_by: The user of the database inserting the archive chemical reaction patterns.

        :returns: The archive chemical reaction pattern SMARTS string to ID dictionary.
        """

        archive_reaction_patterns = list()

        for smarts in smarts_strings:
            archive_reaction_patterns.append({
                "smarts": smarts,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                    CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts,
                ]
            ),
            params=archive_reaction_patterns
        )

        archive_reaction_patterns = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts
            ).where(
                CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts.in_(
                    other=smarts_strings
                )
            )
        ).all()

        archive_reaction_pattern_smarts_to_id = dict()

        for archive_reaction_pattern in archive_reaction_patterns:
            archive_reaction_pattern_smarts_to_id[archive_reaction_pattern.smarts] = archive_reaction_pattern.id

        return archive_reaction_pattern_smarts_to_id

    @staticmethod
    def _insert_archive_reaction_pattern_sources(
            database_session: Session,
            archive_reaction_pattern_ids: Iterable[int],
            archive_source_id: int
    ) -> None:
        """
        Insert the archive chemical reaction pattern sources into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_ids: The IDs of the archive chemical reaction patterns.
        :parameter archive_source_id: The ID of the archive source.
        """

        archive_reaction_pattern_sources = list()

        for archive_reaction_pattern_id in archive_reaction_pattern_ids:
            archive_reaction_pattern_sources.append({
                "archive_reaction_pattern_id": archive_reaction_pattern_id,
                "archive_source_id": archive_source_id,
            })

        database_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionPatternSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_source_id,
                ]
            ),
            params=archive_reaction_pattern_sources
        )

    @staticmethod
    def insert_archive_reaction_patterns(
            database_session: Session,
            archive_reaction_pattern_smarts_strings: Iterable[str],
            archive_source_id: int,
            archive_reaction_pattern_created_by: str
    ) -> None:
        """
        Insert the archive chemical reaction patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_smarts_strings: The SMARTS strings of the archive chemical reaction
            patterns.
        :parameter archive_source_id: The ID of the archive source.
        :parameter archive_reaction_pattern_created_by: The user of the database inserting the archive chemical reaction
            patterns.

        :returns: The archive chemical reaction pattern SMARTS string to ID dictionary.
        """

        archive_reaction_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_reaction_patterns(
                database_session=database_session,
                smarts_strings=archive_reaction_pattern_smarts_strings,
                created_by=archive_reaction_pattern_created_by
            )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_reaction_pattern_sources(
            database_session=database_session,
            archive_reaction_pattern_ids=archive_reaction_pattern_smarts_to_id.values(),
            archive_source_id=archive_source_id
        )

    ####################################################################################################################
    # Workbench Reaction Patterns
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_reaction_patterns(
            database_session: Session,
            smarts_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical reaction patterns from the database.

        :parameter database_session: The session of the database.
        :parameter smarts_strings: The SMARTS strings of the workbench chemical reaction patterns.
        :parameter created_by: The user of the database inserting the workbench chemical reaction patterns.

        :returns: The workbench chemical reaction pattern SMARTS string to ID dictionary.
        """

        workbench_reaction_patterns = list()

        for smarts in smarts_strings:
            workbench_reaction_patterns.append({
                "smarts": smarts,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.smarts,
                ]
            ),
            params=workbench_reaction_patterns
        )

        workbench_reaction_patterns = database_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id,
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.smarts
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.smarts.in_(
                    other=smarts_strings
                )
            )
        ).all()

        workbench_reaction_pattern_smarts_to_id = dict()

        for workbench_reaction_pattern in workbench_reaction_patterns:
            workbench_reaction_pattern_smarts_to_id[workbench_reaction_pattern.smarts] = workbench_reaction_pattern.id

        return workbench_reaction_pattern_smarts_to_id

    @staticmethod
    def _insert_workbench_reaction_pattern_archives(
            database_session: Session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: Mapping[int, str],
            workbench_reaction_pattern_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction pattern archives into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: The archive chemical reaction
            pattern ID to workbench chemical reaction pattern SMARTS string mapping.
        :parameter workbench_reaction_pattern_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID
            mapping.
        """

        workbench_reaction_pattern_archives = list()

        for archive_reaction_pattern_id, workbench_reaction_pattern_smarts in \
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts.items():
            workbench_reaction_pattern_archives.append({
                "workbench_reaction_pattern_id": workbench_reaction_pattern_smarts_to_id[
                    workbench_reaction_pattern_smarts
                ],
                "archive_reaction_pattern_id": archive_reaction_pattern_id,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive.archive_reaction_pattern_id,
                ]
            ),
            params=workbench_reaction_pattern_archives
        )

    @staticmethod
    def _insert_workbench_reaction_reactant_compound_patterns(
            database_session: Session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: Mapping[int, str],
            archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings: Mapping[int, Iterable[str]],
            workbench_reaction_pattern_smarts_to_id: Mapping[str, int],
            workbench_compound_pattern_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compound patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: The archive chemical reaction
            pattern ID to workbench chemical reaction pattern SMARTS string mapping.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings: The
            archive chemical reaction pattern ID to workbench chemical reaction reactant compound pattern SMARTS strings
            mapping.
        :parameter workbench_reaction_pattern_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID
            mapping.
        :parameter workbench_compound_pattern_created_by: The user of the database inserting the workbench chemical
            reaction reactant compound patterns.
        """

        workbench_reaction_reactant_compound_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
                database_session=database_session,
                smarts_strings=chain.from_iterable(
                    archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings.values()
                ),
                created_by=workbench_compound_pattern_created_by
            )

        workbench_reaction_reactant_compound_patterns = list()

        for archive_reaction_pattern_id, workbench_reaction_pattern_smarts in \
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts.items():
            for workbench_reaction_pattern_reactant_compound_smarts in \
                    archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings[
                        archive_reaction_pattern_id
                    ]:
                workbench_reaction_reactant_compound_patterns.append({
                    "workbench_reaction_pattern_id": workbench_reaction_pattern_smarts_to_id[
                        workbench_reaction_pattern_smarts
                    ],
                    "workbench_compound_pattern_id": workbench_reaction_reactant_compound_pattern_smarts_to_id[
                        workbench_reaction_pattern_reactant_compound_smarts
                    ],
                })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_compound_pattern_id,
                ]
            ),
            params=workbench_reaction_reactant_compound_patterns
        )

    @staticmethod
    def _insert_workbench_reaction_spectator_compound_patterns(
            database_session: Session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: Mapping[int, str],
            archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings: Mapping[int, Iterable[str]],
            workbench_reaction_pattern_smarts_to_id: Mapping[str, int],
            workbench_compound_pattern_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compound patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: The archive chemical reaction
            pattern ID to workbench chemical reaction pattern SMARTS string mapping.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings: The
            archive chemical reaction pattern ID to workbench chemical reaction spectator compound pattern SMARTS
            strings mapping.
        :parameter workbench_reaction_pattern_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID
            mapping.
        :parameter workbench_compound_pattern_created_by: The user of the database inserting the workbench chemical
            reaction spectator compound patterns.
        """

        workbench_reaction_spectator_compound_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
                database_session=database_session,
                smarts_strings=chain.from_iterable(
                    archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings.values()
                ),
                created_by=workbench_compound_pattern_created_by
            )

        workbench_reaction_spectator_compound_patterns = list()

        for archive_reaction_pattern_id, workbench_reaction_pattern_smarts in \
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts.items():
            for workbench_reaction_spectator_compound_pattern_smarts in \
                    archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings[
                        archive_reaction_pattern_id
                    ]:
                workbench_reaction_spectator_compound_patterns.append({
                    "workbench_reaction_pattern_id": workbench_reaction_pattern_smarts_to_id[
                        workbench_reaction_pattern_smarts
                    ],
                    "workbench_compound_pattern_id": workbench_reaction_spectator_compound_pattern_smarts_to_id[
                        workbench_reaction_spectator_compound_pattern_smarts
                    ],
                })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_compound_pattern_id,
                ]
            ),
            params=workbench_reaction_spectator_compound_patterns
        )

    @staticmethod
    def _insert_workbench_reaction_product_compound_patterns(
            database_session: Session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: Mapping[int, str],
            archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings: Mapping[int, Iterable[str]],
            workbench_reaction_pattern_smarts_to_id: Mapping[str, int],
            workbench_compound_pattern_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction product compound patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: The archive chemical reaction
            pattern ID to workbench chemical reaction pattern SMARTS string mapping.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings: The
            archive chemical reaction pattern ID to workbench chemical reaction product compound pattern SMARTS strings
            mapping.
        :parameter workbench_reaction_pattern_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID
            mapping.
        :parameter workbench_compound_pattern_created_by: The user of the database inserting the workbench chemical
            reaction product compound patterns.
        """

        workbench_reaction_product_compound_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
                database_session=database_session,
                smarts_strings=chain.from_iterable(
                    archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings.values()
                ),
                created_by=workbench_compound_pattern_created_by
            )

        workbench_reaction_product_compound_patterns = list()

        for archive_reaction_pattern_id, workbench_reaction_pattern_smarts in \
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts.items():
            for workbench_reaction_product_compound_pattern_smarts in \
                    archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings[
                        archive_reaction_pattern_id
                    ]:
                workbench_reaction_product_compound_patterns.append({
                    "workbench_reaction_pattern_id": workbench_reaction_pattern_smarts_to_id[
                        workbench_reaction_pattern_smarts
                    ],
                    "workbench_compound_pattern_id": workbench_reaction_product_compound_pattern_smarts_to_id[
                        workbench_reaction_product_compound_pattern_smarts
                    ],
                })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_compound_pattern_id,
                ]
            ),
            params=workbench_reaction_product_compound_patterns
        )

    @staticmethod
    def insert_workbench_reaction_patterns(
            database_session: Session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: Mapping[int, str],
            archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings: Mapping[int, Iterable[str]],
            archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings: Optional[Mapping[int, Iterable[str]]],
            archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings: Mapping[int, Iterable[str]],
            workbench_reaction_pattern_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction patterns into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts: The archive chemical reaction
            pattern ID to workbench chemical reaction pattern SMARTS string mapping.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings: The
            archive chemical reaction pattern ID to workbench chemical reaction reactant compound pattern SMARTS strings
            mapping.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings: The
            archive chemical reaction pattern ID to workbench chemical reaction spectator compound pattern SMARTS
            strings mapping.
        :parameter archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings: The
            archive chemical reaction pattern ID to workbench chemical reaction product compound pattern SMARTS strings
            mapping.
        :parameter workbench_reaction_pattern_created_by: The user of the database inserting the workbench chemical
            reaction patterns.
        """

        workbench_reaction_pattern_smarts_to_id = \
            CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reaction_patterns(
                database_session=database_session,
                smarts_strings=archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts.values(),
                created_by=workbench_reaction_pattern_created_by
            )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_pattern_archives(
            database_session=database_session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts=(
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts
            ),
            workbench_reaction_pattern_smarts_to_id=workbench_reaction_pattern_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compound_patterns(
            database_session=database_session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts=(
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts
            ),
            archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings=(
                archive_reaction_pattern_id_to_workbench_reaction_reactant_compound_pattern_smarts_strings
            ),
            workbench_reaction_pattern_smarts_to_id=workbench_reaction_pattern_smarts_to_id,
            workbench_compound_pattern_created_by=workbench_reaction_pattern_created_by
        )

        if archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings.keys() is not \
                None:
            CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compound_patterns(
                database_session=database_session,
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts=(
                    archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts
                ),
                archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings=(
                    archive_reaction_pattern_id_to_workbench_reaction_spectator_compound_pattern_smarts_strings
                ),
                workbench_reaction_pattern_smarts_to_id=workbench_reaction_pattern_smarts_to_id,
                workbench_compound_pattern_created_by=workbench_reaction_pattern_created_by
            )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compound_patterns(
            database_session=database_session,
            archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts=(
                archive_reaction_pattern_id_to_workbench_reaction_pattern_smarts
            ),
            archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings=(
                archive_reaction_pattern_id_to_workbench_reaction_product_compound_pattern_smarts_strings
            ),
            workbench_reaction_pattern_smarts_to_id=workbench_reaction_pattern_smarts_to_id,
            workbench_compound_pattern_created_by=workbench_reaction_pattern_created_by
        )

    ####################################################################################################################
    ####################################################################################################################
