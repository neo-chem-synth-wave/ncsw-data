""" The ``ncsw_data.storage.cacs.sqlite_.model.workbench`` package ``compound_pattern`` module. """

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import Integer, Text

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite_.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelWorkbenchCompoundPattern(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical compound pattern class.
    """

    __tablename__ = "workbench_compound_pattern"

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

    archive_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelArchiveCompoundPattern",
        secondary="workbench_compound_pattern_archive",
        back_populates="workbench_compound_patterns"
    )

    workbench_reaction_patterns_as_reactant = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReactionPattern",
        secondary="workbench_reaction_reactant_compound_pattern",
        back_populates="workbench_reactant_compound_patterns"
    )

    workbench_reaction_patterns_as_spectator = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReactionPattern",
        secondary="workbench_reaction_spectator_compound_pattern",
        back_populates="workbench_spectator_compound_patterns"
    )

    workbench_reaction_patterns_as_product = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReactionPattern",
        secondary="workbench_reaction_product_compound_pattern",
        back_populates="workbench_product_compound_patterns"
    )
