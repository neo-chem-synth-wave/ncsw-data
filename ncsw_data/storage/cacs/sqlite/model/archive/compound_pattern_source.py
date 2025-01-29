""" The ``ncsw_data.storage.cacs.sqlite.model.archive`` package ``compound_pattern_source`` module. """

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelArchiveCompoundPatternSource(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model archive chemical compound pattern source
    class.
    """

    __tablename__ = "archive_compound_pattern_source"

    archive_compound_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_compound_pattern.id"
        ),
        primary_key=True
    )

    archive_source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_source.id"
        ),
        primary_key=True
    )
