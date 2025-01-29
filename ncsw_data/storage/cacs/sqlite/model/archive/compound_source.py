""" The ``ncsw_data.storage.cacs.sqlite.model.archive`` package ``compound_source`` module. """

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelArchiveCompoundSource(CaCSSQLiteDatabaseModelBase, CaCSSQLiteDatabaseModelReprMethodMixin):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model archive chemical compound source class.
    """

    __tablename__ = "archive_compound_source"

    archive_compound_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_compound.id"
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
