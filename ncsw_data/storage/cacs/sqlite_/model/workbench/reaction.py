""" The ``ncsw_data.storage.cacs.sqlite_.model.workbench`` package ``reaction`` module. """

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer, Text

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite_.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelWorkbenchReaction(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction class. """

    __tablename__ = "workbench_reaction"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    smiles: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    archive_reactions = relationship(
        "CaCSSQLiteDatabaseModelArchiveReaction",
        secondary="workbench_reaction_archive",
        back_populates="workbench_reactions"
    )

    workbench_reactant_compounds = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompound",
        secondary="workbench_reaction_reactant_compound",
        back_populates="workbench_reactions_as_reactant"
    )

    workbench_spectator_compounds = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompound",
        secondary="workbench_reaction_spectator_compound",
        back_populates="workbench_reactions_as_spectator"
    )

    workbench_product_compounds = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompound",
        secondary="workbench_reaction_product_compound",
        back_populates="workbench_reactions_as_product"
    )

    workbench_reaction_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReactionPattern",
        secondary="workbench_reaction_transformation_pattern",
        back_populates="workbench_reactions"
    )
