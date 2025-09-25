""" The ``ncsw_data.storage.cacs.sqlite_db.model.archive`` package ``source`` module. """

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import Index
from sqlalchemy.sql.sqltypes import Integer, String

from ncsw_data.storage.cacs.sqlite_db.model.base.base import CaCSSQLiteDatabaseModelBase

from ncsw_data.storage.cacs.sqlite_db.model.base.mixin import (
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin,
)


class CaCSSQLiteDatabaseModelArchiveSource(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin,
    CaCSSQLiteDatabaseModelTimestampColumnsMixin
):
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model archive source class. """

    __tablename__ = "archive_source"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(
            length=100
        ),
        nullable=False
    )

    version: Mapped[str] = mapped_column(
        String(
            length=100
        ),
        nullable=False
    )

    file_name: Mapped[str] = mapped_column(
        String(
            length=100
        ),
        nullable=False
    )

    archive_compounds = relationship(
        "CaCSSQLiteDatabaseModelArchiveCompound",
        secondary="archive_compound_source",
        back_populates="archive_sources"
    )

    archive_compound_patterns = relationship(
        "CaCSSQLiteDatabaseModelArchiveCompoundPattern",
        secondary="archive_compound_pattern_source",
        back_populates="archive_sources"
    )

    archive_reactions = relationship(
        "CaCSSQLiteDatabaseModelArchiveReaction",
        secondary="archive_reaction_source",
        back_populates="archive_sources"
    )

    archive_reaction_patterns = relationship(
        "CaCSSQLiteDatabaseModelArchiveReactionPattern",
        secondary="archive_reaction_pattern_source",
        back_populates="archive_sources"
    )

    __table_args__ = (
        Index(
            "idx_archive_source_name_version_file_name",
            "name",
            "version",
            "file_name",
            unique=True
        ),
    )
