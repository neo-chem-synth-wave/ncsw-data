""" The ``ncsw_data.storage.cacs.sqlite.dml.utility`` package ``insert`` module. """

from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from sqlalchemy.dialects.sqlite.dml import insert
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import select

from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.workbench import *


class CaCSSQLiteDatabaseInsertUtility:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database insert utility class. """

    ####################################################################################################################
    # archive_source AS as
    ####################################################################################################################

    @staticmethod
    def insert_and_select_archive_source(
            db_session: Session,
            as_name: str,
            as_version: str,
            as_file_name: str,
            as_created_by: str
    ) -> int:
        """
        Insert and select an archive source from the database.

        :parameter db_session: The session of the database.
        :parameter as_name: The name of the archive source.
        :parameter as_version: The version of the archive source.
        :parameter as_file_name: The file name of the archive source.
        :parameter as_created_by: The user of the database inserting the archive source.

        :returns: The ID of the archive source.
        """

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveSource
            ).values(
                name=as_name,
                version=as_version,
                file_name=as_file_name,
                created_by=as_created_by
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveSource.name,
                    CaCSSQLiteDatabaseModelArchiveSource.version,
                    CaCSSQLiteDatabaseModelArchiveSource.file_name,
                ]
            )
        )

        return db_session.scalar(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveSource.id
            ).where(
                CaCSSQLiteDatabaseModelArchiveSource.name == as_name,
                CaCSSQLiteDatabaseModelArchiveSource.version == as_version,
                CaCSSQLiteDatabaseModelArchiveSource.file_name == as_file_name
            )
        )

    ####################################################################################################################
    # archive_compound AS ac
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_compounds(
            db_session: Session,
            ac_smiles_strings: Iterable[str],
            ac_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical compounds from the database.

        :parameter db_session: The session of the database.
        :parameter ac_smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter ac_created_by: The user of the database inserting the archive chemical compounds.

        :returns: The IDs of the archive chemical compounds.
        """

        acs = list()

        for ac_smiles in ac_smiles_strings:
            acs.append({
                "smiles": ac_smiles,
                "created_by": ac_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompound.id,
                    CaCSSQLiteDatabaseModelArchiveCompound.smiles,
                ]
            ),
            params=acs
        )

        acs = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveCompound.id
            ).where(
                CaCSSQLiteDatabaseModelArchiveCompound.smiles.in_(
                    ac_smiles_strings
                )
            )
        ).all()

        ac_ids = list()

        for ac in acs:
            ac_ids.append(
                ac.id
            )

        return ac_ids

    @staticmethod
    def _insert_archive_compound_sources(
            db_session: Session,
            ac_ids: Iterable[int],
            as_id: int
    ) -> None:
        """
        Insert the archive chemical compound sources into the database.

        :parameter db_session: The session of the database.
        :parameter ac_ids: The IDs of the archive chemical compounds.
        :parameter as_id: The ID of the archive source.
        """

        acss = list()

        for ac_id in ac_ids:
            acss.append({
                "archive_compound_id": ac_id,
                "archive_source_id": as_id,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompoundSource.archive_compound_id,
                    CaCSSQLiteDatabaseModelArchiveCompoundSource.archive_source_id,
                ]
            ),
            params=acss
        )

    @staticmethod
    def insert_archive_compounds(
            db_session: Session,
            ac_smiles_strings: Iterable[str],
            ac_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical compounds into the database.

        :parameter db_session: The session of the database.
        :parameter ac_smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter ac_created_by: The user of the database inserting the archive chemical compounds.
        :parameter as_id: The ID of the archive source.
        """

        ac_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_compounds(
            db_session=db_session,
            ac_smiles_strings=ac_smiles_strings,
            ac_created_by=ac_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_compound_sources(
            db_session=db_session,
            ac_ids=ac_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # archive_reaction AS ar
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_reactions(
            db_session: Session,
            ar_smiles_strings: Iterable[str],
            ar_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical reactions from the database.

        :parameter db_session: The session of the database.
        :parameter ar_smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter ar_created_by: The user of the database inserting the archive chemical reactions.

        :returns: The IDs of the archive chemical reactions.
        """

        ars = list()

        for ar_smiles in ar_smiles_strings:
            ars.append({
                "smiles": ar_smiles,
                "created_by": ar_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReaction
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReaction.id,
                    CaCSSQLiteDatabaseModelArchiveReaction.smiles,
                ]
            ),
            params=ars
        )

        ars = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveReaction.id
            ).where(
                CaCSSQLiteDatabaseModelArchiveReaction.smiles.in_(
                    ar_smiles_strings
                )
            )
        ).all()

        ar_ids = list()

        for ar in ars:
            ar_ids.append(
                ar.id
            )

        return ar_ids

    @staticmethod
    def _insert_archive_reaction_sources(
            db_session: Session,
            ar_ids: Iterable[int],
            as_id: int
    ) -> None:
        """
        Insert the archive chemical reaction sources into the database.

        :parameter db_session: The session of the database.
        :parameter ar_ids: The IDs of the archive chemical reactions.
        :parameter as_id: The ID of the archive source.
        """

        arss = list()

        for ar_id in ar_ids:
            arss.append({
                "archive_reaction_id": ar_id,
                "archive_source_id": as_id,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReactionSource.archive_reaction_id,
                    CaCSSQLiteDatabaseModelArchiveReactionSource.archive_source_id,
                ]
            ),
            params=arss
        )

    @staticmethod
    def insert_archive_reactions(
            db_session: Session,
            ar_smiles_strings: Iterable[str],
            ar_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical reactions into the database.

        :parameter db_session: The session of the database.
        :parameter ar_smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter ar_created_by: The user of the database inserting the archive chemical reactions.
        :parameter as_id: The ID of the archive source.
        """

        ar_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_reactions(
            db_session=db_session,
            ar_smiles_strings=ar_smiles_strings,
            ar_created_by=ar_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_reaction_sources(
            db_session=db_session,
            ar_ids=ar_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # archive_compound_pattern AS acp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_compound_patterns(
            db_session: Session,
            acp_smarts_strings: Iterable[str],
            acp_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical compound patterns from the database.

        :parameter db_session: The session of the database.
        :parameter acp_smarts_strings: The SMARTS strings of the archive chemical compound patterns.
        :parameter acp_created_by: The user of the database inserting the archive chemical compound patterns.

        :returns: The IDs of the archive chemical compound patterns.
        """

        acps = list()

        for acp_smarts in acp_smarts_strings:
            acps.append({
                "smarts": acp_smarts,
                "created_by": acp_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompoundPattern.id,
                    CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts,
                ]
            ),
            params=acps
        )

        acps = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.id
            ).where(
                CaCSSQLiteDatabaseModelArchiveCompoundPattern.smarts.in_(
                    acp_smarts_strings
                )
            )
        ).all()

        acp_ids = list()

        for acp in acps:
            acp_ids.append(
                acp.id
            )

        return acp_ids

    @staticmethod
    def _insert_archive_compound_pattern_sources(
            db_session: Session,
            acp_ids: Iterable[int],
            as_id: int
    ) -> None:
        """
        Insert the archive chemical compound pattern sources into the database.

        :parameter db_session: The session of the database.
        :parameter acp_ids: The IDs of the archive chemical compound patterns.
        :parameter as_id: The ID of the archive source.
        """

        acpss = list()

        for acp_id in acp_ids:
            acpss.append({
                "archive_compound_pattern_id": acp_id,
                "archive_source_id": as_id,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundPatternSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveCompoundPatternSource.archive_compound_pattern_id,
                    CaCSSQLiteDatabaseModelArchiveCompoundPatternSource.archive_source_id,
                ]
            ),
            params=acpss
        )

    @staticmethod
    def insert_archive_compound_patterns(
            db_session: Session,
            acp_smarts_strings: Iterable[str],
            acp_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter acp_smarts_strings: The SMARTS strings of the archive chemical compound patterns.
        :parameter acp_created_by: The user of the database inserting the archive chemical compound patterns.
        :parameter as_id: The ID of the archive source.
        """

        acp_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_compound_patterns(
            db_session=db_session,
            acp_smarts_strings=acp_smarts_strings,
            acp_created_by=acp_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_compound_pattern_sources(
            db_session=db_session,
            acp_ids=acp_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # archive_reaction_pattern AS arp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_reaction_patterns(
            db_session: Session,
            arp_smarts_strings: Iterable[str],
            arp_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical reaction patterns from the database.

        :parameter db_session: The session of the database.
        :parameter arp_smarts_strings: The SMARTS strings of the archive chemical reaction patterns.
        :parameter arp_created_by: The user of the database inserting the archive chemical reaction patterns.

        :returns: The IDs of the archive chemical reaction patterns.
        """

        arps = list()

        for arp_smarts in arp_smarts_strings:
            arps.append({
                "smarts": arp_smarts,
                "created_by": arp_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReactionPattern.id,
                    CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts,
                ]
            ),
            params=arps
        )

        arps = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelArchiveReactionPattern.id
            ).where(
                CaCSSQLiteDatabaseModelArchiveReactionPattern.smarts.in_(
                    arp_smarts_strings
                )
            )
        ).all()

        arp_ids = list()

        for arp in arps:
            arp_ids.append(
                arp.id
            )

        return arp_ids

    @staticmethod
    def _insert_archive_reaction_pattern_sources(
            db_session: Session,
            arp_ids: Iterable[int],
            as_id: int
    ) -> None:
        """
        Insert the archive chemical reaction pattern sources into the database.

        :parameter db_session: The session of the database.
        :parameter arp_ids: The IDs of the archive chemical reaction patterns.
        :parameter as_id: The ID of the archive source.
        """

        arpss = list()

        for arp_id in arp_ids:
            arpss.append({
                "archive_reaction_pattern_id": arp_id,
                "archive_source_id": as_id,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionPatternSource
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelArchiveReactionPatternSource.archive_source_id,
                ]
            ),
            params=arpss
        )

    @staticmethod
    def insert_archive_reaction_patterns(
            db_session: Session,
            arp_smarts_strings: Iterable[str],
            arp_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical reaction patterns into the database.

        :parameter db_session: The session of the database.
        :parameter arp_smarts_strings: The SMARTS strings of the archive chemical reaction patterns.
        :parameter arp_created_by: The user of the database inserting the archive chemical reaction patterns.
        :parameter as_id: The ID of the archive source.
        """

        arp_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_reaction_patterns(
            db_session=db_session,
            arp_smarts_strings=arp_smarts_strings,
            arp_created_by=arp_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_reaction_pattern_sources(
            db_session=db_session,
            arp_ids=arp_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # workbench_compound AS wc
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_compounds(
            db_session: Session,
            id_to_wc_smiles: Mapping[int, str],
            id_to_wc_is_building_block: Optional[Mapping[int, bool]],
            wc_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compounds from the database.

        :parameter db_session: The session of the database.
        :parameter id_to_wc_smiles: The ID to workbench chemical compound SMILES string mapping.
        :parameter id_to_wc_is_building_block: The ID to workbench chemical compound is building block indicator
            mapping.
        :parameter wc_created_by: The user of the database inserting the workbench chemical compounds.

        :returns: The workbench chemical compound SMILES string to ID dictionary.
        """

        wcs = list()

        for id_, wc_smiles in id_to_wc_smiles.items():
            wc = {
                "smiles": wc_smiles,
            }

            if id_to_wc_is_building_block is not None:
                wc["is_building_block"] = id_to_wc_is_building_block[id_]

            wc["created_by"] = wc_created_by

            wcs.append(
                wc
            )

        insert_statement = insert(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        ).values(
            wcs
        )

        if id_to_wc_is_building_block is None:
            insert_statement = insert_statement.on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles,
                ]
            )

        else:
            insert_statement = insert_statement.on_conflict_do_update(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles,
                ],
                set_={
                    "is_building_block": insert_statement.excluded.is_building_block
                },
                where=(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block !=
                    insert_statement.excluded.is_building_block
                )
            )

        db_session.execute(
            statement=insert_statement
        )

        wcs = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                CaCSSQLiteDatabaseModelWorkbenchCompound.smiles
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                    id_to_wc_smiles.values()
                )
            )
        ).all()

        wc_smiles_to_id = dict()

        for wc in wcs:
            wc_smiles_to_id[wc.smiles] = wc.id

        return wc_smiles_to_id

    @staticmethod
    def _insert_workbench_compound_archives(
            db_session: Session,
            ac_id_to_wc_smiles: Mapping[int, str],
            wc_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound archives into the database.

        :parameter db_session: The session of the database.
        :parameter ac_id_to_wc_smiles: The archive chemical compound ID to workbench chemical compound SMILES string
            mapping.
        :parameter wc_smiles_to_id: The workbench chemical compound SMILES string to ID mapping.
        """

        wcas = list()

        for ac_id, wc_smiles in ac_id_to_wc_smiles.items():
            wcas.append({
                "workbench_compound_id": wc_smiles_to_id[wc_smiles],
                "archive_compound_id": ac_id,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundArchive.workbench_compound_id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundArchive.archive_compound_id,
                ]
            ),
            params=wcas
        )

    @staticmethod
    def insert_workbench_compounds(
            db_session: Session,
            ac_id_to_wc_smiles: Mapping[int, str],
            ac_id_to_wc_is_building_block: Optional[Mapping[int, bool]],
            wc_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compounds into the database.

        :parameter db_session: The session of the database.
        :parameter ac_id_to_wc_smiles: The archive chemical compound ID to workbench chemical compound SMILES string
            mapping.
        :parameter ac_id_to_wc_is_building_block: The archive chemical compound ID to workbench chemical compound is
            building block indicator mapping.
        :parameter wc_created_by: The user of the database inserting the workbench chemical compounds.
        """

        wc_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            id_to_wc_smiles=ac_id_to_wc_smiles,
            id_to_wc_is_building_block=ac_id_to_wc_is_building_block,
            wc_created_by=wc_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_archives(
            db_session=db_session,
            ac_id_to_wc_smiles=ac_id_to_wc_smiles,
            wc_smiles_to_id=wc_smiles_to_id
        )

    ####################################################################################################################
    # workbench_reaction AS wr
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_reactions(
            db_session: Session,
            wr_smiles_strings: Iterable[str],
            wr_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical reactions from the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_strings: The SMILES strings of the workbench chemical reactions.
        :parameter wr_created_by: The user of the database inserting the workbench chemical reactions.

        :returns: The workbench chemical reaction SMILES string to ID dictionary.
        """

        wrs = list()

        for wr_smiles in wr_smiles_strings:
            wrs.append({
                "smiles": wr_smiles,
                "created_by": wr_created_by,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReaction
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                    CaCSSQLiteDatabaseModelWorkbenchReaction.smiles,
                ]
            ),
            params=wrs
        )

        wrs = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchReaction.id,
                CaCSSQLiteDatabaseModelWorkbenchReaction.smiles
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchReaction.smiles.in_(
                    wr_smiles_strings
                )
            )
        ).all()

        wr_smiles_to_id = dict()

        for wr in wrs:
            wr_smiles_to_id[wr.smiles] = wr.id

        return wr_smiles_to_id

    @staticmethod
    def _insert_workbench_reaction_archives(
            db_session: Session,
            ar_ids_and_wr_smiles_strings: Iterable[Tuple[int, str]],
            wr_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction archives into the database.

        :parameter db_session: The session of the database.
        :parameter ar_ids_and_wr_smiles_strings: The archive chemical reaction IDs and workbench chemical reaction
            SMILES strings.
        :parameter wr_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        """

        wras = list()

        for ar_id, wr_smiles in ar_ids_and_wr_smiles_strings:
            wras.append({
                "workbench_reaction_id": wr_smiles_to_id[wr_smiles],
                "archive_reaction_id": ar_id,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionArchive.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionArchive.archive_reaction_id,
                ]
            ),
            params=wras
        )

    @staticmethod
    def _insert_workbench_reaction_reactant_compounds(
            db_session: Session,
            wr_smiles_and_rc_smiles_strings: Iterable[Tuple[str, Iterable[str]]],
            wrrc_created_by: str,
            wr_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_and_rc_smiles_strings: The workbench chemical reaction SMILES strings and reactant compound
            SMILES strings.
        :parameter wrrc_created_by: The user of the database inserting the workbench chemical reaction reactant
            compounds.
        :parameter wr_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        """

        id_to_wrrc_smiles, id_ = dict(), 0

        for _, wrrc_smiles_strings in wr_smiles_and_rc_smiles_strings:
            for wrrc_smiles in wrrc_smiles_strings:
                id_to_wrrc_smiles[id_] = wrrc_smiles
                id_ += 1

        wrrc_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            id_to_wc_smiles=id_to_wrrc_smiles,
            id_to_wc_is_building_block=None,
            wc_created_by=wrrc_created_by
        )

        wrrcs = list()

        for wr_smiles, wrrc_smiles_strings in wr_smiles_and_rc_smiles_strings:
            for wrrc_smiles in wrrc_smiles_strings:
                wrrcs.append({
                    "workbench_reaction_id": wr_smiles_to_id[wr_smiles],
                    "workbench_compound_id": wrrc_smiles_to_id[wrrc_smiles],
                })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompound.workbench_compound_id,
                ]
            ),
            params=wrrcs
        )

    @staticmethod
    def _insert_workbench_reaction_spectator_compounds(
            db_session: Session,
            wr_smiles_and_sc_smiles_strings: Iterable[Tuple[str, Iterable[str]]],
            wrsc_created_by: str,
            wr_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_and_sc_smiles_strings: The workbench chemical reaction SMILES strings and spectator
            compound SMILES strings.
        :parameter wrsc_created_by: The user of the database inserting the workbench chemical reaction spectator
            compounds.
        :parameter wr_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        """

        id_to_wrsc_smiles, id_ = dict(), 0

        for _, wrsc_smiles_strings in wr_smiles_and_sc_smiles_strings:
            for wrsc_smiles in wrsc_smiles_strings:
                id_to_wrsc_smiles[id_] = wrsc_smiles
                id_ += 1

        wrsc_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            id_to_wc_smiles=id_to_wrsc_smiles,
            id_to_wc_is_building_block=None,
            wc_created_by=wrsc_created_by
        )

        wrscs = list()

        for wr_smiles, wrsc_smiles_strings in wr_smiles_and_sc_smiles_strings:
            for wrsc_smiles in wrsc_smiles_strings:
                wrscs.append({
                    "workbench_reaction_id": wr_smiles_to_id[wr_smiles],
                    "workbench_compound_id": wrsc_smiles_to_id[wrsc_smiles],
                })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompound.workbench_compound_id,
                ]
            ),
            params=wrscs
        )

    @staticmethod
    def _insert_workbench_reaction_product_compounds(
            db_session: Session,
            wr_smiles_and_pc_smiles_strings: Iterable[Tuple[str, Iterable[str]]],
            wrpc_created_by: str,
            wr_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction product compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_and_pc_smiles_strings: The workbench chemical reaction SMILES strings and product compound
            SMILES strings.
        :parameter wrpc_created_by: The user of the database inserting the workbench chemical reaction product
            compounds.
        :parameter wr_smiles_to_id: The workbench chemical reaction SMILES string to ID mapping.
        """

        id_to_wrpc_smiles, id_ = dict(), 0

        for _, wrpc_smiles_strings in wr_smiles_and_pc_smiles_strings:
            for wrpc_smiles in wrpc_smiles_strings:
                id_to_wrpc_smiles[id_] = wrpc_smiles
                id_ += 1

        wrpc_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            id_to_wc_smiles=id_to_wrpc_smiles,
            id_to_wc_is_building_block=None,
            wc_created_by=wrpc_created_by
        )

        wrpcs = list()

        for wr_smiles, wrpc_smiles_strings in wr_smiles_and_pc_smiles_strings:
            for wrpc_smiles in wrpc_smiles_strings:
                wrpcs.append({
                    "workbench_reaction_id": wr_smiles_to_id[wr_smiles],
                    "workbench_compound_id": wrpc_smiles_to_id[wrpc_smiles],
                })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound.workbench_compound_id,
                ]
            ),
            params=wrpcs
        )

    @staticmethod
    def insert_workbench_reactions(
            db_session: Session,
            wrs: Iterable[Tuple[int, str, Iterable[str], Iterable[str], Iterable[str]]],
            wr_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reactions into the database.

        :parameter db_session: The session of the database.
        :parameter wrs: The workbench chemical reactions.
        :parameter wr_created_by: The user of the database inserting the workbench chemical reactions.
        """

        wr_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reactions(
            db_session=db_session,
            wr_smiles_strings=[
                wr_smiles
                for _, wr_smiles, _, _, _ in wrs
            ],
            wr_created_by=wr_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_archives(
            db_session=db_session,
            ar_ids_and_wr_smiles_strings=[(
                ar_id,
                wr_smiles,
            ) for ar_id, wr_smiles, _, _, _ in wrs],
            wr_smiles_to_id=wr_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compounds(
            db_session=db_session,
            wr_smiles_and_rc_smiles_strings=[(
                wr_smiles,
                wrrc_smiles_strings,
            ) for _, wr_smiles, wrrc_smiles_strings, _, _ in wrs],
            wrrc_created_by=wr_created_by,
            wr_smiles_to_id=wr_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compounds(
            db_session=db_session,
            wr_smiles_and_sc_smiles_strings=[(
                wr_smiles,
                wrsc_smiles_strings,
            ) for _, wr_smiles, _, wrsc_smiles_strings, _ in wrs],
            wrsc_created_by=wr_created_by,
            wr_smiles_to_id=wr_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compounds(
            db_session=db_session,
            wr_smiles_and_pc_smiles_strings=[(
                wr_smiles,
                wrpc_smiles_strings,
            ) for _, wr_smiles, _, _, wrpc_smiles_strings in wrs],
            wrpc_created_by=wr_created_by,
            wr_smiles_to_id=wr_smiles_to_id
        )

    ####################################################################################################################
    # workbench_compound_pattern AS wcp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_compound_patterns(
            db_session: Session,
            wcp_smarts_strings: Iterable[str],
            wcp_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compound patterns from the database.

        :parameter db_session: The session of the database.
        :parameter wcp_smarts_strings: The SMARTS strings of the workbench chemical compound patterns.
        :parameter wcp_created_by: The user of the database inserting the workbench chemical compound patterns.

        :returns: The workbench chemical compound pattern SMARTS string to ID dictionary.
        """

        wcps = list()

        for wcp_smarts in wcp_smarts_strings:
            wcps.append({
                "smarts": wcp_smarts,
                "created_by": wcp_created_by,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts,
                ]
            ),
            params=wcps
        )

        wcps = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.id,
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern.smarts.in_(
                    wcp_smarts_strings
                )
            )
        ).all()

        wcp_smarts_to_id = dict()

        for wcp in wcps:
            wcp_smarts_to_id[wcp.smarts] = wcp.id

        return wcp_smarts_to_id

    @staticmethod
    def _insert_workbench_compound_pattern_archives(
            db_session: Session,
            acp_id_to_wcp_smarts: Mapping[int, str],
            wcp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound pattern archives into the database.

        :parameter db_session: The session of the database.
        :parameter acp_id_to_wcp_smarts: The archive chemical compound pattern ID to workbench chemical compound pattern
            SMARTS string mapping.
        :parameter wcp_smarts_to_id: The workbench chemical compound pattern SMARTS string to ID mapping.
        """

        wcpas = list()

        for acp_id, wcp_smarts in acp_id_to_wcp_smarts.items():
            wcpas.append({
                "workbench_compound_pattern_id": wcp_smarts_to_id[wcp_smarts],
                "archive_compound_pattern_id": acp_id,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive.workbench_compound_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive.archive_compound_pattern_id,
                ]
            ),
            params=wcpas
        )

    @staticmethod
    def _insert_workbench_compound_structure_patterns(
            db_session: Session,
            wc_id_to_wcp_smarts: Mapping[int, str],
            wcp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound structure patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wc_id_to_wcp_smarts: The workbench chemical compound ID to workbench chemical compound pattern SMARTS
            string mapping.
        :parameter wcp_smarts_to_id: The workbench chemical compound pattern SMARTS string to ID mapping.
        """

        wcsps = list()

        for wc_id, wcp_smarts in wc_id_to_wcp_smarts.items():
            wcsps.append({
                "workbench_compound_id": wc_id,
                "workbench_compound_pattern_id": wcp_smarts_to_id[wcp_smarts],
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundStructurePattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompoundStructurePattern.workbench_compound_id,
                    CaCSSQLiteDatabaseModelWorkbenchCompoundStructurePattern.workbench_compound_pattern_id,
                ]
            ),
            params=wcsps
        )

    @staticmethod
    def insert_workbench_compound_patterns(
            db_session: Session,
            acp_id_to_wcp_smarts: Mapping[int, str],
            wcp_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter acp_id_to_wcp_smarts: The archive chemical compound pattern ID to workbench chemical compound pattern
            SMARTS string mapping.
        :parameter wcp_created_by: The user of the database inserting the workbench chemical compound patterns.
        """

        wcp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=acp_id_to_wcp_smarts.values(),
            wcp_created_by=wcp_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_pattern_archives(
            db_session=db_session,
            acp_id_to_wcp_smarts=acp_id_to_wcp_smarts,
            wcp_smarts_to_id=wcp_smarts_to_id
        )

    @staticmethod
    def insert_workbench_compound_structure_patterns(
            db_session: Session,
            wc_id_to_wcp_smarts: Mapping[int, str],
            wcsp_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compound structure patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wc_id_to_wcp_smarts: The workbench chemical compound ID to workbench chemical compound pattern SMARTS
            string mapping.
        :parameter wcsp_created_by: The user of the database inserting the workbench chemical compound structure
            patterns.
        """

        wcp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wc_id_to_wcp_smarts.values(),
            wcp_created_by=wcsp_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_structure_patterns(
            db_session=db_session,
            wc_id_to_wcp_smarts=wc_id_to_wcp_smarts,
            wcp_smarts_to_id=wcp_smarts_to_id
        )

    ####################################################################################################################
    # workbench_reaction_pattern AS wrp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_reaction_patterns(
            db_session: Session,
            wrp_smarts_strings: Iterable[str],
            wrp_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical reaction patterns from the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_strings: The SMARTS strings of the workbench chemical reaction patterns.
        :parameter wrp_created_by: The user of the database inserting the workbench chemical reaction patterns.

        :returns: The workbench chemical reaction pattern SMARTS string to ID dictionary.
        """

        wrps = list()

        for wrp_smarts in wrp_smarts_strings:
            wrps.append({
                "smarts": wrp_smarts,
                "created_by": wrp_created_by,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionPattern.smarts,
                ]
            ),
            params=wrps
        )

        wrps = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.id,
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.smarts
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern.smarts.in_(
                    wrp_smarts_strings
                )
            )
        ).all()

        wrp_smarts_to_id = dict()

        for wrp in wrps:
            wrp_smarts_to_id[wrp.smarts] = wrp.id

        return wrp_smarts_to_id

    @staticmethod
    def _insert_workbench_reaction_pattern_archives(
            db_session: Session,
            arp_id_and_wrp_smarts: Iterable[Tuple[int, str]],
            wrp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction pattern archives into the database.

        :parameter db_session: The session of the database.
        :parameter arp_id_and_wrp_smarts: The archive chemical reaction pattern ID and workbench chemical reaction
        pattern SMARTS strings.
        :parameter wrp_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID mapping.
        """

        wrpas = list()

        for arp_id, wrp_smarts in arp_id_and_wrp_smarts:
            wrpas.append({
                "workbench_reaction_pattern_id": wrp_smarts_to_id[wrp_smarts],
                "archive_reaction_pattern_id": arp_id,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive.archive_reaction_pattern_id,
                ]
            ),
            params=wrpas
        )

    @staticmethod
    def _insert_workbench_reaction_transformation_patterns(
            db_session: Session,
            wr_id_and_wrp_smarts: Iterable[Tuple[int, str]],
            wrp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction transformation patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wr_id_and_wrp_smarts: The workbench chemical reaction ID and workbench chemical reaction pattern
            SMARTS string.
        :parameter wrp_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID mapping.
        """

        wrtps = list()

        for wr_id, wrp_smarts in wr_id_and_wrp_smarts:
            wrtps.append({
                "workbench_reaction_id": wr_id,
                "workbench_reaction_pattern_id": wrp_smarts_to_id[wrp_smarts],
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionTransformationPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionTransformationPattern.workbench_reaction_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionTransformationPattern.workbench_reaction_pattern_id,
                ]
            ),
            params=wrtps
        )

    @staticmethod
    def _insert_workbench_reaction_reactant_compound_patterns(
            db_session: Session,
            wrp_smarts_and_wrrcp_smarts_strings: Iterable[Tuple[str, Iterable[str]]],
            wrrcp_created_by: str,
            wrp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_and_wrrcp_smarts_strings: The workbench chemical reaction pattern SMARTS strings and
            reactant compound pattern SMARTS strings.
        :parameter wrrcp_created_by: The user of the database inserting the workbench chemical reaction reactant
            compound patterns.
        :parameter wrp_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID mapping.
        """

        wrrcp_smarts_strings_ = list()

        for _, wrrcp_smarts_strings in wrp_smarts_and_wrrcp_smarts_strings:
            for wrrcp_smarts in wrrcp_smarts_strings:
                wrrcp_smarts_strings_.append(
                    wrrcp_smarts
                )

        wrrcp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wrrcp_smarts_strings_,
            wcp_created_by=wrrcp_created_by
        )

        wrrcps = list()

        for wrp_smarts, wrrcp_smarts_strings in wrp_smarts_and_wrrcp_smarts_strings:
            for wrrcp_smarts in wrrcp_smarts_strings:
                wrrcps.append({
                    "workbench_reaction_pattern_id": wrp_smarts_to_id[wrp_smarts],
                    "workbench_compound_pattern_id": wrrcp_smarts_to_id[wrrcp_smarts],
                })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionReactantCompoundPattern.workbench_compound_pattern_id,
                ]
            ),
            params=wrrcps
        )

    @staticmethod
    def _insert_workbench_reaction_spectator_compound_patterns(
            db_session: Session,
            wrp_smarts_and_wrscp_smarts_strings: Iterable[Tuple[str, Iterable[str]]],
            wrscp_created_by: str,
            wrp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_and_wrscp_smarts_strings: The workbench chemical reaction pattern SMARTS strings and
            spectator compound pattern SMARTS strings.
        :parameter wrscp_created_by: The user of the database inserting the workbench chemical reaction spectator
            compound patterns.
        :parameter wrp_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID mapping.
        """

        wrscp_smarts_strings_ = list()

        for _, wrscp_smarts_strings in wrp_smarts_and_wrscp_smarts_strings:
            for wrscp_smarts in wrscp_smarts_strings:
                wrscp_smarts_strings_.append(
                    wrscp_smarts
                )

        wrscp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wrscp_smarts_strings_,
            wcp_created_by=wrscp_created_by
        )

        wrscps = list()

        for wrp_smarts, wrscp_smarts_strings in wrp_smarts_and_wrscp_smarts_strings:
            for wrscp_smarts in wrscp_smarts_strings:
                wrscps.append({
                    "workbench_reaction_pattern_id": wrp_smarts_to_id[wrp_smarts],
                    "workbench_compound_pattern_id": wrscp_smarts_to_id[wrscp_smarts],
                })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionSpectatorCompoundPattern.workbench_compound_pattern_id,
                ]
            ),
            params=wrscps
        )

    @staticmethod
    def _insert_workbench_reaction_product_compound_patterns(
            db_session: Session,
            wrp_smarts_and_wrpcp_smarts_strings: Iterable[Tuple[str, Iterable[str]]],
            wrpcp_created_by: str,
            wrp_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction product compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_and_wrpcp_smarts_strings: The workbench chemical reaction pattern SMARTS strings and
            product compound pattern SMARTS strings.
        :parameter wrpcp_created_by: The user of the database inserting the workbench chemical reaction product compound
            patterns.
        :parameter wrp_smarts_to_id: The workbench chemical reaction pattern SMARTS string to ID mapping.
        """

        wrpcp_smarts_strings_ = list()

        for _, wrpcp_smarts_strings in wrp_smarts_and_wrpcp_smarts_strings:
            for wrpcp_smarts in wrpcp_smarts_strings:
                wrpcp_smarts_strings_.append(
                    wrpcp_smarts
                )

        wrpcp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wrpcp_smarts_strings_,
            wcp_created_by=wrpcp_created_by
        )

        wrpcps = list()

        for wrp_smarts, wrpcp_smarts_strings in wrp_smarts_and_wrpcp_smarts_strings:
            for wrpcp_smarts in wrpcp_smarts_strings:
                wrpcps.append({
                    "workbench_reaction_pattern_id": wrp_smarts_to_id[wrp_smarts],
                    "workbench_compound_pattern_id": wrpcp_smarts_to_id[wrpcp_smarts],
                })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_reaction_pattern_id,
                    CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern.workbench_compound_pattern_id,
                ]
            ),
            params=wrpcps
        )

    @staticmethod
    def insert_workbench_reaction_patterns(
            db_session: Session,
            wrps: Iterable[Tuple[int, str, Iterable[str], Iterable[str], Iterable[str]]],
            wrp_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrps: The workbench chemical reaction patterns.
        :parameter wrp_created_by: The user of the database inserting the workbench chemical reaction patterns.
        """

        wrp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reaction_patterns(
            db_session=db_session,
            wrp_smarts_strings=[
                wrp_smarts
                for _, wrp_smarts, _, _, _ in wrps
            ],
            wrp_created_by=wrp_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_pattern_archives(
            db_session=db_session,
            arp_id_and_wrp_smarts=[(
                arp_id,
                wrp_smarts,
            ) for arp_id, wrp_smarts, _, _, _ in wrps],
            wrp_smarts_to_id=wrp_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compound_patterns(
            db_session=db_session,
            wrp_smarts_and_wrrcp_smarts_strings=[(
                wrp_smarts,
                wrrcp_smarts_strings,
            ) for _, wrp_smarts, wrrcp_smarts_strings, _, _ in wrps],
            wrrcp_created_by=wrp_created_by,
            wrp_smarts_to_id=wrp_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compound_patterns(
            db_session=db_session,
            wrp_smarts_and_wrscp_smarts_strings=[(
                wrp_smarts,
                wrscp_smarts_strings,
            ) for _, wrp_smarts, _, wrscp_smarts_strings, _ in wrps],
            wrscp_created_by=wrp_created_by,
            wrp_smarts_to_id=wrp_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compound_patterns(
            db_session=db_session,
            wrp_smarts_and_wrpcp_smarts_strings=[(
                wrp_smarts,
                wrpcp_smarts_strings,
            ) for _, wrp_smarts, _, _, wrpcp_smarts_strings in wrps],
            wrpcp_created_by=wrp_created_by,
            wrp_smarts_to_id=wrp_smarts_to_id
        )

    @staticmethod
    def insert_workbench_reaction_transformation_patterns(
            db_session: Session,
            wrtps: Iterable[Tuple[int, str, Iterable[str], Iterable[str], Iterable[str]]],
            wrp_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction transformation patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrtps: The workbench chemical reaction transformation patterns.
        :parameter wrp_created_by: The user of the database inserting the workbench chemical reaction patterns.
        """

        wrp_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reaction_patterns(
            db_session=db_session,
            wrp_smarts_strings=[
                wrp_smarts
                for _, wrp_smarts, _, _, _ in wrtps
            ],
            wrp_created_by=wrp_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_transformation_patterns(
            db_session=db_session,
            wr_id_and_wrp_smarts=[(
                wr_id,
                wrp_smarts,
            ) for wr_id, wrp_smarts, _, _, _ in wrtps],
            wrp_smarts_to_id=wrp_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compound_patterns(
            db_session=db_session,
            wrp_smarts_and_wrrcp_smarts_strings=[(
                wrp_smarts,
                wrrcp_smarts_strings,
            ) for _, wrp_smarts, wrrcp_smarts_strings, _, _ in wrtps],
            wrrcp_created_by=wrp_created_by,
            wrp_smarts_to_id=wrp_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compound_patterns(
            db_session=db_session,
            wrp_smarts_and_wrscp_smarts_strings=[(
                wrp_smarts,
                wrscp_smarts_strings,
            ) for _, wrp_smarts, _, wrscp_smarts_strings, _ in wrtps],
            wrscp_created_by=wrp_created_by,
            wrp_smarts_to_id=wrp_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compound_patterns(
            db_session=db_session,
            wrp_smarts_and_wrpcp_smarts_strings=[(
                wrp_smarts,
                wrpcp_smarts_strings,
            ) for _, wrp_smarts, _, _, wrpcp_smarts_strings in wrtps],
            wrpcp_created_by=wrp_created_by,
            wrp_smarts_to_id=wrp_smarts_to_id
        )

    ####################################################################################################################
    ####################################################################################################################
