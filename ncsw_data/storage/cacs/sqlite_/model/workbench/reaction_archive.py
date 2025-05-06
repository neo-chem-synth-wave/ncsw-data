""" The ``ncsw_data.storage.cacs.sqlite_.model.workbench`` package ``reaction_archive`` module. """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite_.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchReactionArchive(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction archive class.
    """

    __tablename__ = "workbench_reaction_archive"

    workbench_reaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_reaction.id"
        ),
        primary_key=True
    )

    archive_reaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_reaction.id"
        ),
        primary_key=True
    )
