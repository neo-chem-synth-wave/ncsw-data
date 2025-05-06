""" The ``ncsw_data.storage.cacs.sqlite_.utility`` package ``insert_`` module. """

from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from ncsw_data.storage.cacs.sqlite_.model.archive import *
from ncsw_data.storage.cacs.sqlite_.model.workbench import *


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
            acs_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical compounds from the database.

        :parameter db_session: The session of the database.
        :parameter ac_smiles_strings: The SMILES strings of the archive chemical compounds.
        :parameter acs_created_by: The user of the database inserting the archive chemical compounds.

        :returns: The IDs of the archive chemical compounds.
        """

        acs = list()

        for ac_smiles in ac_smiles_strings:
            acs.append({
                "smiles": ac_smiles,
                "created_by": acs_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompound
            ).on_conflict_do_nothing(
                index_elements=[
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
            acs: Iterable[str],
            acs_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical compounds into the database.

        :parameter db_session: The session of the database.
        :parameter acs: The archive chemical compounds: [ `ac_smiles`, ... ].
        :parameter acs_created_by: The user of the database inserting the archive chemical compounds.
        :parameter as_id: The ID of the archive source.
        """

        ac_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_compounds(
            db_session=db_session,
            ac_smiles_strings=acs,
            acs_created_by=acs_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_compound_sources(
            db_session=db_session,
            ac_ids=ac_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # archive_compound_pattern AS acp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_compound_patterns(
            db_session: Session,
            acp_smarts_strings: Iterable[str],
            acps_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical compound patterns from the database.

        :parameter db_session: The session of the database.
        :parameter acp_smarts_strings: The SMARTS strings of the archive chemical compound patterns.
        :parameter acps_created_by: The user of the database inserting the archive chemical compound patterns.

        :returns: The IDs of the archive chemical compound patterns.
        """

        acps = list()

        for acp_smarts in acp_smarts_strings:
            acps.append({
                "smarts": acp_smarts,
                "created_by": acps_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
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
            acps: Iterable[str],
            acps_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter acps: The archive chemical compound patterns: [ `acp_smarts`, ... ].
        :parameter acps_created_by: The user of the database inserting the archive chemical compound patterns.
        :parameter as_id: The ID of the archive source.
        """

        acp_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_compound_patterns(
            db_session=db_session,
            acp_smarts_strings=acps,
            acps_created_by=acps_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_compound_pattern_sources(
            db_session=db_session,
            acp_ids=acp_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # archive_reaction AS ar
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_reactions(
            db_session: Session,
            ar_smiles_strings: Iterable[str],
            ars_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical reactions from the database.

        :parameter db_session: The session of the database.
        :parameter ar_smiles_strings: The SMILES strings of the archive chemical reactions.
        :parameter ars_created_by: The user of the database inserting the archive chemical reactions.

        :returns: The IDs of the archive chemical reactions.
        """

        ars = list()

        for ar_smiles in ar_smiles_strings:
            ars.append({
                "smiles": ar_smiles,
                "created_by": ars_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReaction
            ).on_conflict_do_nothing(
                index_elements=[
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
            ars: Iterable[str],
            ars_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical reactions into the database.

        :parameter db_session: The session of the database.
        :parameter ars: The archive chemical reactions: [ `ar_smiles`, ... ].
        :parameter ars_created_by: The user of the database inserting the archive chemical reactions.
        :parameter as_id: The ID of the archive source.
        """

        ar_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_reactions(
            db_session=db_session,
            ar_smiles_strings=ars,
            ars_created_by=ars_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_archive_reaction_sources(
            db_session=db_session,
            ar_ids=ar_ids,
            as_id=as_id
        )

    ####################################################################################################################
    # archive_reaction_pattern AS arp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_archive_reaction_patterns(
            db_session: Session,
            arp_smarts_strings: Iterable[str],
            arps_created_by: str
    ) -> List[int]:
        """
        Insert and select the archive chemical reaction patterns from the database.

        :parameter db_session: The session of the database.
        :parameter arp_smarts_strings: The SMARTS strings of the archive chemical reaction patterns.
        :parameter arps_created_by: The user of the database inserting the archive chemical reaction patterns.

        :returns: The IDs of the archive chemical reaction patterns.
        """

        arps = list()

        for arp_smarts in arp_smarts_strings:
            arps.append({
                "smarts": arp_smarts,
                "created_by": arps_created_by,
            })

        db_session.execute(
            statement=insert(
                table=CaCSSQLiteDatabaseModelArchiveReactionPattern
            ).on_conflict_do_nothing(
                index_elements=[
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
            arps: Iterable[str],
            arps_created_by: str,
            as_id: int
    ) -> None:
        """
        Insert the archive chemical reaction patterns into the database.

        :parameter db_session: The session of the database.
        :parameter arps: The archive chemical reaction patterns: [ `arp_smarts`, ... ].
        :parameter arps_created_by: The user of the database inserting the archive chemical reaction patterns.
        :parameter as_id: The ID of the archive source.
        """

        arp_ids = CaCSSQLiteDatabaseInsertUtility._insert_and_select_archive_reaction_patterns(
            db_session=db_session,
            arp_smarts_strings=arps,
            arps_created_by=arps_created_by
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
            wc_smiles_strings: Iterable[str],
            wcs_are_building_blocks: Optional[bool],
            wcs_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compounds from the database.

        :parameter db_session: The session of the database.
        :parameter wc_smiles_strings: The SMILES strings of the workbench chemical compounds.
        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.
        :parameter wcs_created_by: The user of the database inserting the workbench chemical compounds.

        :returns: The SMILES string to ID dictionary of the workbench chemical compounds.
        """

        wcs = list()

        for wc_smiles in wc_smiles_strings:
            wc = {
                "smiles": wc_smiles,
            }

            if wcs_are_building_blocks is not None:
                wc["is_building_block"] = wcs_are_building_blocks

            wc["created_by"] = wcs_created_by

            wcs.append(
                wc
            )

        wcs_insert_statement = insert(
            CaCSSQLiteDatabaseModelWorkbenchCompound
        ).values(
            wcs
        )

        if wcs_are_building_blocks is None:
            wcs_insert_statement = wcs_insert_statement.on_conflict_do_nothing(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles,
                ]
            )

        else:
            wcs_insert_statement = wcs_insert_statement.on_conflict_do_update(
                index_elements=[
                    CaCSSQLiteDatabaseModelWorkbenchCompound.smiles,
                ],
                set_={
                    "is_building_block": wcs_insert_statement.excluded.is_building_block
                },
                where=(
                    CaCSSQLiteDatabaseModelWorkbenchCompound.is_building_block !=
                    wcs_insert_statement.excluded.is_building_block
                )
            )

        db_session.execute(
            statement=wcs_insert_statement
        )

        wcs = db_session.execute(
            statement=select(
                CaCSSQLiteDatabaseModelWorkbenchCompound.id,
                CaCSSQLiteDatabaseModelWorkbenchCompound.smiles
            ).where(
                CaCSSQLiteDatabaseModelWorkbenchCompound.smiles.in_(
                    wc_smiles_strings
                )
            )
        ).all()

        wcs_smiles_to_id = dict()

        for wc in wcs:
            wcs_smiles_to_id[wc.smiles] = wc.id

        return wcs_smiles_to_id

    @staticmethod
    def _insert_workbench_compound_archives(
            db_session: Session,
            ac_ids_and_wc_smiles_strings: Iterable[Tuple[int, str]],
            wcs_smiles_to_id: Dict[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound archives into the database.

        :parameter db_session: The session of the database.
        :parameter ac_ids_and_wc_smiles_strings: The IDs of the archive chemical compounds and SMILES strings of the
            workbench chemical compounds.
        :parameter wcs_smiles_to_id: The SMILES string to ID dictionary of the workbench chemical compounds.
        """

        wcas = list()

        for ac_id, wc_smiles in ac_ids_and_wc_smiles_strings:
            wcas.append({
                "workbench_compound_id": wcs_smiles_to_id[wc_smiles],
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
            wcs: Iterable[Tuple[int, str]],
            wcs_are_building_blocks: Optional[bool],
            wcs_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wcs: The workbench chemical compounds: [ ( `ac_id`, `wc_smiles`, ), ... ].
        :parameter wcs_are_building_blocks: The indicator of whether the workbench chemical compounds are building
            blocks.
        :parameter wcs_created_by: The user of the database inserting the workbench chemical compounds.
        """

        wcs_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            wc_smiles_strings=[
                wc_smiles
                for _, wc_smiles in wcs
            ],
            wcs_are_building_blocks=wcs_are_building_blocks,
            wcs_created_by=wcs_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_archives(
            db_session=db_session,
            ac_ids_and_wc_smiles_strings=wcs,
            wcs_smiles_to_id=wcs_smiles_to_id
        )

    ####################################################################################################################
    # workbench_compound_pattern AS wcp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_compound_patterns(
            db_session: Session,
            wcp_smarts_strings: Iterable[str],
            wcps_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical compound patterns from the database.

        :parameter db_session: The session of the database.
        :parameter wcp_smarts_strings: The SMARTS strings of the workbench chemical compound patterns.
        :parameter wcps_created_by: The user of the database inserting the workbench chemical compound patterns.

        :returns: The SMARTS string to ID dictionary of the workbench chemical compound patterns.
        """

        wcps = list()

        for wcp_smarts in wcp_smarts_strings:
            wcps.append({
                "smarts": wcp_smarts,
                "created_by": wcps_created_by,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
            ).on_conflict_do_nothing(
                index_elements=[
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

        wcps_smarts_to_id = dict()

        for wcp in wcps:
            wcps_smarts_to_id[wcp.smarts] = wcp.id

        return wcps_smarts_to_id

    @staticmethod
    def _insert_workbench_compound_pattern_archives(
            db_session: Session,
            acp_ids_and_wcp_smarts_strings: Iterable[Tuple[int, str]],
            wcps_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical compound pattern archives into the database.

        :parameter db_session: The session of the database.
        :parameter acp_ids_and_wcp_smarts_strings: The IDs of the archive chemical compound patterns and SMARTS strings
            of the workbench chemical compound patterns.
        :parameter wcps_smarts_to_id: The SMARTS string to ID dictionary of the workbench chemical compound patterns.
        """

        wcpas = list()

        for acp_id, wcp_smarts in acp_ids_and_wcp_smarts_strings:
            wcpas.append({
                "workbench_compound_pattern_id": wcps_smarts_to_id[wcp_smarts],
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
    def insert_workbench_compound_patterns(
            db_session: Session,
            wcps: Iterable[Tuple[int, str]],
            wcps_created_by: str
    ) -> None:
        """
        Insert the workbench chemical compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wcps: The workbench chemical compound patterns: [ ( `acp_id`, `wcp_smarts`, ), ... ].
        :parameter wcps_created_by: The user of the database inserting the workbench chemical compound patterns.
        """

        wcps_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=[
                wcp_smarts
                for _, wcp_smarts in wcps
            ],
            wcps_created_by=wcps_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_compound_pattern_archives(
            db_session=db_session,
            acp_ids_and_wcp_smarts_strings=wcps,
            wcps_smarts_to_id=wcps_smarts_to_id
        )

    ####################################################################################################################
    # workbench_reaction AS wr
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_reactions(
            db_session: Session,
            wr_smiles_strings: Iterable[str],
            wrs_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical reactions from the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_strings: The SMILES strings of the workbench chemical reactions.
        :parameter wrs_created_by: The user of the database inserting the workbench chemical reactions.

        :returns: The workbench chemical reaction SMILES string to ID dictionary.
        """

        wrs = list()

        for wr_smiles in wr_smiles_strings:
            wrs.append({
                "smiles": wr_smiles,
                "created_by": wrs_created_by,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReaction
            ).on_conflict_do_nothing(
                index_elements=[
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

        wrs_smiles_to_id = dict()

        for wr in wrs:
            wrs_smiles_to_id[wr.smiles] = wr.id

        return wrs_smiles_to_id

    @staticmethod
    def _insert_workbench_reaction_archives(
            db_session: Session,
            ar_ids_and_wr_smiles_strings: Iterable[Tuple[int, str]],
            wrs_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction archives into the database.

        :parameter db_session: The session of the database.
        :parameter ar_ids_and_wr_smiles_strings: The IDs of the archive chemical reactions and SMILES strings of the
            workbench chemical reactions.
        :parameter wrs_smiles_to_id: The SMILES string to ID mapping of the workbench chemical reactions.
        """

        wras = list()

        for ar_id, wr_smiles in ar_ids_and_wr_smiles_strings:
            wras.append({
                "workbench_reaction_id": wrs_smiles_to_id[wr_smiles],
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
            wr_smiles_strings_and_wrrc_smiles_strings: Iterable[Tuple[str, str]],
            wrrcs_created_by: str,
            wrs_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_strings_and_wrrc_smiles_strings: The SMILES strings of the workbench chemical reactions and
            SMILES strings of the workbench chemical reaction reactant compounds.
        :parameter wrrcs_created_by: The user of the database inserting the workbench chemical reaction reactant
            compounds.
        :parameter wrs_smiles_to_id: The SMILES string to ID mapping of the workbench chemical reactions.
        """

        wrrc_smiles_strings = list()

        for _, wrrc_smiles in wr_smiles_strings_and_wrrc_smiles_strings:
            wrrc_smiles_strings.append(
                wrrc_smiles
            )

        if len(wrrc_smiles_strings) == 0:
            return

        wrrcs_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            wc_smiles_strings=wrrc_smiles_strings,
            wcs_are_building_blocks=None,
            wcs_created_by=wrrcs_created_by
        )

        wrrcs = list()

        for wr_smiles, wrrc_smiles in wr_smiles_strings_and_wrrc_smiles_strings:
            wrrcs.append({
                "workbench_reaction_id": wrs_smiles_to_id[wr_smiles],
                "workbench_compound_id": wrrcs_smiles_to_id[wrrc_smiles],
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
            wr_smiles_strings_and_wrsc_smiles_strings: Iterable[Tuple[str, str]],
            wrscs_created_by: str,
            wrs_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_strings_and_wrsc_smiles_strings: The SMILES strings of the workbench chemical reactions and
            SMILES strings of the workbench chemical reaction spectator compounds.
        :parameter wrscs_created_by: The user of the database inserting the workbench chemical reaction spectator
            compounds.
        :parameter wrs_smiles_to_id: The SMILES string to ID mapping of the workbench chemical reactions.
        """

        wrsc_smiles_strings = list()

        for _, wrsc_smiles in wr_smiles_strings_and_wrsc_smiles_strings:
            wrsc_smiles_strings.append(
                wrsc_smiles
            )

        if len(wrsc_smiles_strings) == 0:
            return

        wrscs_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            wc_smiles_strings=wrsc_smiles_strings,
            wcs_are_building_blocks=None,
            wcs_created_by=wrscs_created_by
        )

        wrscs = list()

        for wr_smiles, wrsc_smiles in wr_smiles_strings_and_wrsc_smiles_strings:
            wrscs.append({
                "workbench_reaction_id": wrs_smiles_to_id[wr_smiles],
                "workbench_compound_id": wrscs_smiles_to_id[wrsc_smiles],
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
            wr_smiles_strings_and_wrpc_smiles_strings: Iterable[Tuple[str, str]],
            wrpcs_created_by: str,
            wrs_smiles_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction product compounds into the database.

        :parameter db_session: The session of the database.
        :parameter wr_smiles_strings_and_wrpc_smiles_strings: The SMILES strings of the workbench chemical reactions and
            SMILES strings of the workbench chemical reaction product compounds.
        :parameter wrpcs_created_by: The user of the database inserting the workbench chemical reaction product
            compounds.
        :parameter wrs_smiles_to_id: The SMILES string to ID mapping of the workbench chemical reactions.
        """

        wrpc_smiles_strings = list()

        for _, wrpc_smiles in wr_smiles_strings_and_wrpc_smiles_strings:
            wrpc_smiles_strings.append(
                wrpc_smiles
            )

        if len(wrpc_smiles_strings) == 0:
            return

        wrpcs_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compounds(
            db_session=db_session,
            wc_smiles_strings=wrpc_smiles_strings,
            wcs_are_building_blocks=None,
            wcs_created_by=wrpcs_created_by
        )

        wrpcs = list()

        for wr_smiles, wrpc_smiles in wr_smiles_strings_and_wrpc_smiles_strings:
            wrpcs.append({
                "workbench_reaction_id": wrs_smiles_to_id[wr_smiles],
                "workbench_compound_id": wrpcs_smiles_to_id[wrpc_smiles],
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
            wrs_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reactions into the database.

        :parameter db_session: The session of the database.
        :parameter wrs: The workbench chemical reactions: [ ( `ar_id`, `wr_smiles`, `wrrc_smiles_strings`,
            `wrsc_smiles_strings`, `wrpc_smiles_strings`, ), ... ].
        :parameter wrs_created_by: The user of the database inserting the workbench chemical reactions.
        """

        wrs_smiles_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reactions(
            db_session=db_session,
            wr_smiles_strings=[
                wr_smiles
                for _, wr_smiles, _, _, _ in wrs
            ],
            wrs_created_by=wrs_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_archives(
            db_session=db_session,
            ar_ids_and_wr_smiles_strings=[
                (ar_id, wr_smiles, )
                for ar_id, wr_smiles, _, _, _ in wrs
            ],
            wrs_smiles_to_id=wrs_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compounds(
            db_session=db_session,
            wr_smiles_strings_and_wrrc_smiles_strings=[
                (wr_smiles, wrrc_smiles, )
                for _, wr_smiles, wrrc_smiles_strings, _, _ in wrs
                for wrrc_smiles in wrrc_smiles_strings
            ],
            wrrcs_created_by=wrs_created_by,
            wrs_smiles_to_id=wrs_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compounds(
            db_session=db_session,
            wr_smiles_strings_and_wrsc_smiles_strings=[
                (wr_smiles, wrsc_smiles, )
                for _, wr_smiles, _, wrsc_smiles_strings, _ in wrs
                for wrsc_smiles in wrsc_smiles_strings
            ],
            wrscs_created_by=wrs_created_by,
            wrs_smiles_to_id=wrs_smiles_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compounds(
            db_session=db_session,
            wr_smiles_strings_and_wrpc_smiles_strings=[
                (wr_smiles, wrpc_smiles, )
                for _, wr_smiles, _, _, wrpc_smiles_strings in wrs
                for wrpc_smiles in wrpc_smiles_strings
            ],
            wrpcs_created_by=wrs_created_by,
            wrs_smiles_to_id=wrs_smiles_to_id
        )

    ####################################################################################################################
    # workbench_reaction_pattern AS wrp
    ####################################################################################################################

    @staticmethod
    def _insert_and_select_workbench_reaction_patterns(
            db_session: Session,
            wrp_smarts_strings: Iterable[str],
            wrps_created_by: str
    ) -> Dict[str, int]:
        """
        Insert and select the workbench chemical reaction patterns from the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_strings: The SMARTS strings of the workbench chemical reaction patterns.
        :parameter wrps_created_by: The user of the database inserting the workbench chemical reaction patterns.

        :returns: The SMARTS string to ID dictionary of the workbench chemical reaction patterns.
        """

        wrps = list()

        for wrp_smarts in wrp_smarts_strings:
            wrps.append({
                "smarts": wrp_smarts,
                "created_by": wrps_created_by,
            })

        db_session.execute(
            statement=insert(
                CaCSSQLiteDatabaseModelWorkbenchReactionPattern
            ).on_conflict_do_nothing(
                index_elements=[
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

        wrps_smarts_to_id = dict()

        for wrp in wrps:
            wrps_smarts_to_id[wrp.smarts] = wrp.id

        return wrps_smarts_to_id

    @staticmethod
    def _insert_workbench_reaction_pattern_archives(
            db_session: Session,
            arp_ids_and_wrp_smarts_strings: Iterable[Tuple[int, str]],
            wrps_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction pattern archives into the database.

        :parameter db_session: The session of the database.
        :parameter arp_ids_and_wrp_smarts_strings: The IDs of the archive chemical reaction patterns and SMARTS strings
            of the workbench chemical reaction patterns.
        :parameter wrps_smarts_to_id: The SMARTS string to ID dictionary of the workbench chemical reaction patterns.
        """

        wrpas = list()

        for arp_id, wrp_smarts in arp_ids_and_wrp_smarts_strings:
            wrpas.append({
                "workbench_reaction_pattern_id": wrps_smarts_to_id[wrp_smarts],
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
    def _insert_workbench_reaction_reactant_compound_patterns(
            db_session: Session,
            wrp_smarts_strings_and_wrrcp_smarts_strings: Iterable[Tuple[str, str]],
            wrrcps_created_by: str,
            wrps_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction reactant compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_strings_and_wrrcp_smarts_strings: The SMARTS strings of the workbench chemical reaction
            patterns and SMARTS strings of the workbench chemical reaction reactant compound patterns.
        :parameter wrrcps_created_by: The user of the database inserting the workbench chemical reaction reactant
            compound patterns.
        :parameter wrps_smarts_to_id: The SMARTS string to ID dictionary of the workbench chemical reaction patterns.
        """

        wrrcp_smarts_strings = list()

        for _, wrrcp_smarts in wrp_smarts_strings_and_wrrcp_smarts_strings:
            wrrcp_smarts_strings.append(
                wrrcp_smarts
            )

        if len(wrrcp_smarts_strings) == 0:
            return

        wrrcps_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wrrcp_smarts_strings,
            wcps_created_by=wrrcps_created_by
        )

        wrrcps = list()

        for wrp_smarts, wrrcp_smarts in wrp_smarts_strings_and_wrrcp_smarts_strings:
            wrrcps.append({
                "workbench_reaction_pattern_id": wrps_smarts_to_id[wrp_smarts],
                "workbench_compound_pattern_id": wrrcps_smarts_to_id[wrrcp_smarts],
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
            wrp_smarts_strings_and_wrscp_smarts_strings: Iterable[Tuple[str, str]],
            wrscps_created_by: str,
            wrps_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction spectator compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_strings_and_wrscp_smarts_strings: The SMARTS strings of the workbench chemical reaction
            patterns and SMARTS strings of the workbench chemical reaction spectator compound patterns.
        :parameter wrscps_created_by: The user of the database inserting the workbench chemical reaction spectator
            compound patterns.
        :parameter wrps_smarts_to_id: The SMARTS string to ID dictionary of the workbench chemical reaction patterns.
        """

        wrscp_smarts_strings = list()

        for _, wrscp_smarts in wrp_smarts_strings_and_wrscp_smarts_strings:
            wrscp_smarts_strings.append(
                wrscp_smarts
            )

        if len(wrscp_smarts_strings) == 0:
            return

        wrscps_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wrscp_smarts_strings,
            wcps_created_by=wrscps_created_by
        )

        wrscps = list()

        for wrp_smarts, wrscp_smarts in wrp_smarts_strings_and_wrscp_smarts_strings:
            wrscps.append({
                "workbench_reaction_pattern_id": wrps_smarts_to_id[wrp_smarts],
                "workbench_compound_pattern_id": wrscps_smarts_to_id[wrscp_smarts],
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
            wrp_smarts_strings_and_wrpcp_smarts_strings: Iterable[Tuple[str, str]],
            wrpcps_created_by: str,
            wrps_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction product compound patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrp_smarts_strings_and_wrpcp_smarts_strings: The SMARTS strings of the workbench chemical reaction
            patterns and SMARTS strings of the workbench chemical reaction product compound patterns.
        :parameter wrpcps_created_by: The user of the database inserting the workbench chemical reaction product
            compound patterns.
        :parameter wrps_smarts_to_id: The SMARTS string to ID dictionary of the workbench chemical reaction patterns.
        """

        wrpcp_smarts_strings = list()

        for _, wrpcp_smarts in wrp_smarts_strings_and_wrpcp_smarts_strings:
            wrpcp_smarts_strings.append(
                wrpcp_smarts
            )

        if len(wrpcp_smarts_strings) == 0:
            return

        wrpcps_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_compound_patterns(
            db_session=db_session,
            wcp_smarts_strings=wrpcp_smarts_strings,
            wcps_created_by=wrpcps_created_by
        )

        wrpcps = list()

        for wrp_smarts, wrpcp_smarts in wrp_smarts_strings_and_wrpcp_smarts_strings:
            wrpcps.append({
                "workbench_reaction_pattern_id": wrps_smarts_to_id[wrp_smarts],
                "workbench_compound_pattern_id": wrpcps_smarts_to_id[wrpcp_smarts],
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
            wrps_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrps: The workbench chemical reaction patterns: [ ( `arp_id`, `wrp_smarts`, `wrrcp_smarts_strings`,
            `wrscp_smarts_strings`, `wrpcp_smarts_strings`, ), ... ].
        :parameter wrps_created_by: The user of the database inserting the workbench chemical reaction patterns.
        """

        wrps_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reaction_patterns(
            db_session=db_session,
            wrp_smarts_strings=[
                wrp_smarts
                for _, wrp_smarts, _, _, _ in wrps
            ],
            wrps_created_by=wrps_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_pattern_archives(
            db_session=db_session,
            arp_ids_and_wrp_smarts_strings=[
                (arp_id, wrp_smarts, )
                for arp_id, wrp_smarts, _, _, _ in wrps
            ],
            wrps_smarts_to_id=wrps_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compound_patterns(
            db_session=db_session,
            wrp_smarts_strings_and_wrrcp_smarts_strings=[
                (wrp_smarts, wrrcp_smarts, )
                for _, wrp_smarts, wrrcp_smarts_strings, _, _ in wrps
                for wrrcp_smarts in wrrcp_smarts_strings
            ],
            wrrcps_created_by=wrps_created_by,
            wrps_smarts_to_id=wrps_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compound_patterns(
            db_session=db_session,
            wrp_smarts_strings_and_wrscp_smarts_strings=[
                (wrp_smarts, wrscp_smarts, )
                for _, wrp_smarts, _, wrscp_smarts_strings, _ in wrps
                for wrscp_smarts in wrscp_smarts_strings
            ],
            wrscps_created_by=wrps_created_by,
            wrps_smarts_to_id=wrps_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compound_patterns(
            db_session=db_session,
            wrp_smarts_strings_and_wrpcp_smarts_strings=[
                (wrp_smarts, wrpcp_smarts, )
                for _, wrp_smarts, _, _, wrpcp_smarts_strings in wrps
                for wrpcp_smarts in wrpcp_smarts_strings
            ],
            wrpcps_created_by=wrps_created_by,
            wrps_smarts_to_id=wrps_smarts_to_id
        )

    ####################################################################################################################
    # workbench_reaction_transformation_pattern AS wrtp
    ####################################################################################################################

    @staticmethod
    def _insert_workbench_reaction_transformation_patterns(
            db_session: Session,
            wr_ids_and_wrp_smarts_strings: Iterable[Tuple[int, str]],
            wrps_smarts_to_id: Mapping[str, int]
    ) -> None:
        """
        Insert the workbench chemical reaction transformation patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wr_ids_and_wrp_smarts_strings: The IDs of the workbench chemical reactions and SMARTS strings of the
            workbench chemical reaction patterns.
        :parameter wrps_smarts_to_id: The SMARTS string to ID dictionary of the workbench chemical reaction patterns.
        """

        wrtps = list()

        for wr_id, wrp_smarts in wr_ids_and_wrp_smarts_strings:
            wrtps.append({
                "workbench_reaction_id": wr_id,
                "workbench_reaction_pattern_id": wrps_smarts_to_id[wrp_smarts],
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
    def insert_workbench_reaction_transformation_patterns(
            db_session: Session,
            wrtps: Iterable[Tuple[int, str, Iterable[str], Iterable[str], Iterable[str]]],
            wrtps_created_by: str
    ) -> None:
        """
        Insert the workbench chemical reaction transformation patterns into the database.

        :parameter db_session: The session of the database.
        :parameter wrtps: The workbench chemical reaction transformation patterns: [ ( `wr_id`, `wrp_smarts`,
            `wrrcp_smarts_strings`, `wrscp_smarts_strings`, `wrpcp_smarts_strings`, ), ... ].
        :parameter wrtps_created_by: The user of the database inserting the workbench chemical reaction transformation
            patterns.
        """

        wrps_smarts_to_id = CaCSSQLiteDatabaseInsertUtility._insert_and_select_workbench_reaction_patterns(
            db_session=db_session,
            wrp_smarts_strings=[
                wrp_smarts
                for _, wrp_smarts, _, _, _ in wrtps
            ],
            wrps_created_by=wrtps_created_by
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_transformation_patterns(
            db_session=db_session,
            wr_ids_and_wrp_smarts_strings=[
                (wr_id, wrp_smarts, )
                for wr_id, wrp_smarts, _, _, _ in wrtps
            ],
            wrps_smarts_to_id=wrps_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_reactant_compound_patterns(
            db_session=db_session,
            wrp_smarts_strings_and_wrrcp_smarts_strings=[
                (wrp_smarts, wrrcp_smarts, )
                for _, wrp_smarts, wrrcp_smarts_strings, _, _ in wrtps
                for wrrcp_smarts in wrrcp_smarts_strings
            ],
            wrrcps_created_by=wrtps_created_by,
            wrps_smarts_to_id=wrps_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_spectator_compound_patterns(
            db_session=db_session,
            wrp_smarts_strings_and_wrscp_smarts_strings=[
                (wrp_smarts, wrscp_smarts, )
                for _, wrp_smarts, _, wrscp_smarts_strings, _ in wrtps
                for wrscp_smarts in wrscp_smarts_strings
            ],
            wrscps_created_by=wrtps_created_by,
            wrps_smarts_to_id=wrps_smarts_to_id
        )

        CaCSSQLiteDatabaseInsertUtility._insert_workbench_reaction_product_compound_patterns(
            db_session=db_session,
            wrp_smarts_strings_and_wrpcp_smarts_strings=[
                (wrp_smarts, wrpcp_smarts, )
                for _, wrp_smarts, _, _, wrpcp_smarts_strings in wrtps
                for wrpcp_smarts in wrpcp_smarts_strings
            ],
            wrpcps_created_by=wrtps_created_by,
            wrps_smarts_to_id=wrps_smarts_to_id
        )
