""" The ``ncsw_data.storage.cacs.sqlite_db.model.archive`` package ``reaction_pattern`` module. """

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer, Text

from ncsw_data.storage.cacs.sqlite_db.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite_db.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelArchiveReactionPattern(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model archive chemical reaction pattern class.
    """

    __tablename__ = "archive_reaction_pattern"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    smarts: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    archive_sources = relationship(
        "CaCSSQLiteDatabaseModelArchiveSource",
        secondary="archive_reaction_pattern_source",
        back_populates="archive_reaction_patterns"
    )

    workbench_reaction_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReactionPattern",
        secondary="workbench_reaction_pattern_archive",
        back_populates="archive_reaction_patterns"
    )
