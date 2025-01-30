""" The ``ncsw_data.storage.cacs.sqlite.utility`` package ``insert`` module. """

from itertools import chain
from typing import Dict, Iterable, Mapping

from sqlalchemy.dialects.sqlite.dml import insert
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import select

from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.workbench import *


class CaCSSQLiteDatabaseInsertUtility:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database insert utility class. """

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
            ).on_conflict_do_nothing()
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

    @staticmethod
    def insert_and_select_archive_compounds(
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
            ).on_conflict_do_nothing(),
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
    def insert_archive_compound_sources(
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
            ).on_conflict_do_nothing(),
            params=archive_compound_sources
        )

    @staticmethod
    def insert_and_select_archive_compound_patterns(
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
            ).on_conflict_do_nothing(),
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
    def insert_archive_compound_pattern_sources(
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
            ).on_conflict_do_nothing(),
            params=archive_compound_pattern_sources
        )

    @staticmethod
    def insert_and_select_archive_reactions(
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
            ).on_conflict_do_nothing(),
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
    def insert_archive_reaction_sources(
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
            ).on_conflict_do_nothing(),
            params=archive_reaction_sources
        )

    @staticmethod
    def insert_and_select_archive_reaction_patterns(
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
            ).on_conflict_do_nothing(),
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
    def insert_archive_reaction_pattern_sources(
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
            ).on_conflict_do_nothing(),
            params=archive_reaction_pattern_sources
        )

    @staticmethod
    def insert_and_select_workbench_compounds(
            database_session: Session,
            smiles_strings: Iterable[str],
            created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compounds from the database.

        :parameter database_session: The session of the database.
        :parameter smiles_strings: The SMILES strings of the workbench chemical compounds.
        :parameter created_by: The user of the database inserting the workbench chemical compounds.

        :returns: The workbench chemical compound SMILES string to ID dictionary.
        """

        workbench_compounds = list()

        for smiles in smiles_strings:
            workbench_compounds.append({
                "smiles": smiles,
                "created_by": created_by,
            })

        database_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompound
            ).on_conflict_do_nothing(),
            params=workbench_compounds
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
    def insert_workbench_compound_archives(
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
            ).on_conflict_do_nothing(),
            params=workbench_compound_archives
        )

    @staticmethod
    def insert_and_select_workbench_reactions(
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
            ).on_conflict_do_nothing(),
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
    def insert_workbench_reaction_archives(
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
            ).on_conflict_do_nothing(),
            params=workbench_reaction_archives
        )

    @staticmethod
    def insert_workbench_reaction_reactant_compounds(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_smiles_to_id: Mapping[str, int],
            created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction reactant compound SMILES strings mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        :parameter created_by: The user of the database inserting the workbench chemical reaction reactant compounds.
        """

        workbench_reaction_reactant_compound_smiles_to_id = \
            CaCSSQLiteDatabaseInsertUtility.insert_and_select_workbench_compounds(
                database_session=database_session,
                smiles_strings=list(
                    chain.from_iterable(
                        archive_reaction_id_to_workbench_reaction_reactant_compound_smiles_strings.values()
                    )
                ),
                created_by=created_by
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
            ).on_conflict_do_nothing(),
            params=workbench_reaction_reactant_compounds
        )

    @staticmethod
    def insert_workbench_reaction_spectator_compounds(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_smiles_to_id: Mapping[str, int],
            created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction spectator compound SMILES strings mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        :parameter created_by: The user of the database inserting the workbench chemical reaction spectator compounds.
        """

        workbench_reaction_spectator_compound_smiles_to_id = \
            CaCSSQLiteDatabaseInsertUtility.insert_and_select_workbench_compounds(
                database_session=database_session,
                smiles_strings=list(
                    chain.from_iterable(
                        archive_reaction_id_to_workbench_reaction_spectator_compound_smiles_strings.values()
                    )
                ),
                created_by=created_by
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
            ).on_conflict_do_nothing(),
            params=workbench_reaction_spectator_compounds
        )

    @staticmethod
    def insert_workbench_reaction_product_compounds(
            database_session: Session,
            archive_reaction_id_to_workbench_reaction_smiles: Mapping[int, str],
            archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings: Mapping[int, Iterable[str]],
            workbench_reaction_smiles_to_id: Mapping[str, int],
            created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction product compounds into the database.

        :parameter database_session: The session of the database.
        :parameter archive_reaction_id_to_workbench_reaction_smiles: The archive chemical reaction ID to workbench
            chemical reaction SMILES string mapping.
        :parameter archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings: The archive chemical
            reaction ID to workbench chemical reaction product compound SMILES strings mapping.
        :parameter workbench_reaction_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        :parameter created_by: The user of the database inserting the workbench chemical reaction product compounds.
        """

        workbench_reaction_product_compound_smiles_to_id = \
            CaCSSQLiteDatabaseInsertUtility.insert_and_select_workbench_compounds(
                database_session=database_session,
                smiles_strings=list(
                    chain.from_iterable(
                        archive_reaction_id_to_workbench_reaction_product_compound_smiles_strings.values()
                    )
                ),
                created_by=created_by
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
            ).on_conflict_do_nothing(),
            params=workbench_reaction_product_compounds
        )
