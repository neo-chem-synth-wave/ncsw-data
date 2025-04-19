""" The ``ncsw_data.storage.cacs.sqlite_.model.base`` package ``mixin`` module. """

from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime, String


class CaCSSQLiteDatabaseModelReprMethodMixin:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model `__repr__` method mixin class. """

    def __repr__(
            self
    ) -> str:
        """
        The `__repr__` method of the class.

        :returns: The string representation of a database model instance.
        """

        return "{table_name:s}({table_column_names_and_values:s})".format(
            table_name=self.__class__.__tablename__,
            table_column_names_and_values=", ".join(
                "{table_column_name:s}={table_column_value}".format(
                    table_column_name=table_column.name,
                    table_column_value=getattr(self, table_column.name)
                ) for table_column in self.__table__.columns
            )
        )


class CaCSSQLiteDatabaseModelTimestampColumnsMixin:
    """ The computer-assisted chemical synthesis (CaCS) SQLite database model timestamp columns mixin class. """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        nullable=False,
        server_default=func.now()
    )

    created_by: Mapped[str] = mapped_column(
        String(
            length=100
        ),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        nullable=True,
        server_onupdate=func.now()
    )

    updated_by: Mapped[str] = mapped_column(
        String(
            length=100
        ),
        nullable=True
    )
