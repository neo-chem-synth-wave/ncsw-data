""" The ``ncsw_data.storage.cacs.sqlite_.model.workbench`` package ``reaction_transformation_pattern`` module. """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite_.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite_.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchReactionTransformationPattern(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction transformation
    pattern class.
    """

    __tablename__ = "workbench_reaction_transformation_pattern"

    workbench_reaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_reaction.id"
        ),
        primary_key=True
    )

    workbench_reaction_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_reaction_pattern.id"
        ),
        primary_key=True
    )
