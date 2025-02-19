""" The ``ncsw_data.storage.cacs.sqlite.model.workbench`` package ``reaction_product_compound_pattern`` module. """

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchReactionProductCompoundPattern(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction product compound
    pattern class.
    """

    __tablename__ = "workbench_reaction_product_compound_pattern"

    workbench_reaction_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_reaction_pattern.id"
        ),
        primary_key=True
    )

    workbench_compound_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_compound_pattern.id"
        ),
        primary_key=True
    )
