""" The ``ncsw_data.storage.cacs.sqlite.model.workbench`` package ``compound`` module. """

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import Boolean, Integer, Text

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelWorkbenchCompound(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical compound class. """

    __tablename__ = "workbench_compound"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    smiles: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True,
        unique=True
    )

    is_building_block: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    archive_compounds = relationship(
        "CaCSSQLiteDatabaseModelArchiveCompound",
        secondary="workbench_compound_archive",
        back_populates="workbench_compounds"
    )

    workbench_reactions_as_reactant = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReaction",
        secondary="workbench_reaction_reactant_compound",
        back_populates="workbench_reactant_compounds"
    )

    workbench_reactions_as_spectator = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReaction",
        secondary="workbench_reaction_spectator_compound",
        back_populates="workbench_spectator_compounds"
    )

    workbench_reactions_as_product = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReaction",
        secondary="workbench_reaction_product_compound",
        back_populates="workbench_product_compounds"
    )

    workbench_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompoundPattern",
        secondary="workbench_compound_structure_pattern",
        back_populates="workbench_compounds"
    )
