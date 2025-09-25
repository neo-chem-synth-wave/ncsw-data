""" The ``ncsw_data.storage.cacs.sqlite_db.model.workbench`` package ``reaction_product_compound`` module. """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite_db.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite_db.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchReactionProductCompound(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical reaction product compound
    class.
    """

    __tablename__ = "workbench_reaction_product_compound"

    workbench_reaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_reaction.id"
        ),
        primary_key=True
    )

    workbench_compound_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_compound.id"
        ),
        primary_key=True
    )
