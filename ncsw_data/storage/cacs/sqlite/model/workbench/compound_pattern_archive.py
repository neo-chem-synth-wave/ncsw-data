""" The ``ncsw_data.storage.cacs.sqlite.model.workbench`` package ``compound_pattern_archive`` module. """

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ncsw_data.storage.cacs.sqlite.model.base.base import CaCSSQLiteDatabaseModelBase
from ncsw_data.storage.cacs.sqlite.model.base.mixin import CaCSSQLiteDatabaseModelReprMethodMixin


class CaCSSQLiteDatabaseModelWorkbenchCompoundPatternArchive(
    CaCSSQLiteDatabaseModelBase,
    CaCSSQLiteDatabaseModelReprMethodMixin
):
    """
    The computer-assisted chemical synthesis (CaCS) SQLite database model workbench chemical compound pattern archive
    class.
    """

    __tablename__ = "workbench_compound_pattern_archive"

    workbench_compound_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="workbench_compound_pattern.id"
        ),
        primary_key=True
    )

    archive_compound_pattern_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="archive_compound_pattern.id"
        ),
        primary_key=True
    )
