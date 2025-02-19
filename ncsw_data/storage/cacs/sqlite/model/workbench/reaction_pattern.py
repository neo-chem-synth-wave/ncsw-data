""" The ``ncsw_data.storage.cacs.sqlite.model.workbench`` package ``reaction_pattern`` module. """

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import Integer, Text

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelWorkbenchReactionPattern(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction pattern class. """

    __tablename__ = "workbench_reaction_pattern"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    smarts: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True,
        unique=True
    )

    archive_reaction_patterns = relationship(
        "CaCSSQLiteDatabaseModelArchiveReactionPattern",
        secondary="workbench_reaction_pattern_archive",
        back_populates="workbench_reaction_patterns"
    )

    workbench_reactant_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompoundPattern",
        secondary="workbench_reaction_reactant_compound_pattern",
        back_populates="workbench_reaction_patterns_as_reactant"
    )

    workbench_spectator_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompoundPattern",
        secondary="workbench_reaction_spectator_compound_pattern",
        back_populates="workbench_reaction_patterns_as_spectator"
    )

    workbench_product_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompoundPattern",
        secondary="workbench_reaction_product_compound_pattern",
        back_populates="workbench_reaction_patterns_as_product"
    )

    workbench_reactions = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReaction",
        secondary="workbench_reaction_transformation_pattern",
        back_populates="workbench_reaction_patterns"
    )
