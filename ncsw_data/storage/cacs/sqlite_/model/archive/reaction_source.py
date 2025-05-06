""" The ``ncsw_data.storage.cacs.sqlite_.model.archive`` package ``reaction_source`` module. """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite_.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelArchiveReactionSource(CaCSSQLiteDatabaseModelBase, CaCSSQLiteDatabaseModelReprMethodMixin):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model archive chemical reaction source class.
    """

    __tablename__ = "archive_reaction_source"

    archive_reaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_reaction.id"
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
