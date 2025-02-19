""" The ``ncsw_data.storage.cacs.sqlite.model.workbench`` package ``reaction_pattern_archive`` module. """

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchReactionPatternArchive(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction pattern archive
    class.
    """

    __tablename__ = "workbench_reaction_pattern_archive"

    workbench_reaction_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_reaction_pattern.id"
        ),
        primary_key=True
    )

    archive_reaction_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_reaction_pattern.id"
        ),
        primary_key=True
    )
