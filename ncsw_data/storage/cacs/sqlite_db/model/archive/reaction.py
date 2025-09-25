""" The ``ncsw_data.storage.cacs.sqlite_db.model.archive`` package ``reaction`` module. """

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer, Text

from ncsw_data.storage.cacs.sqlite_db.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite_db.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelArchiveReaction(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model archive chemical reaction class. """

    __tablename__ = "archive_reaction"

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

    archive_sources = relationship(
        "CaCSSQLiteDatabaseModelArchiveSource",
        secondary="archive_reaction_source",
        back_populates="archive_reactions"
    )

    workbench_reactions = relationship(
        "CaCSSQLiteDatabaseModelWorkbenchReaction",
        secondary="workbench_reaction_archive",
        back_populates="archive_reactions"
    )
