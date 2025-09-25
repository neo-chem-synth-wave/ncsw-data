""" The ``ncsw_data.storage.cacs.sqlite_db.model.workbench`` package ``compound_archive`` module. """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite_db.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite_db.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchCompoundArchive(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical compound archive class.
    """

    __tablename__ = "workbench_compound_archive"

    workbench_compound_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_compound.id"
        ),
        primary_key=True
    )

    archive_compound_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_compound.id"
        ),
        primary_key=True
    )
