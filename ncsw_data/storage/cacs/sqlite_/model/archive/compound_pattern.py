""" The ``ncsw_data.storage.cacs.sqlite_.model.archive`` package ``compound_pattern`` module. """

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import Integer, Text

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite_.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelArchiveCompoundPattern(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model archive chemical compound pattern class.
    """

    __tablename__ = "archive_compound_pattern"

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

    archive_sources = relationship(
        "CaCSSQLiteDatabaseModelArchiveSource",
        secondary="archive_compound_pattern_source",
        back_populates="archive_compound_patterns"
    )

    workbench_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchCompoundPattern",
        secondary="workbench_compound_pattern_archive",
        back_populates="archive_compound_patterns"
    )
