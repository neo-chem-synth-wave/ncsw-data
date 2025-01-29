""" The ``ncsw_data.storage.base`` package ``base`` module. """

from abc import ABC
from logging import Logger
from typing import Optional


class DataStorageBase(ABC):
    """ The data storage base class. """

    def __init__(
            self,
            logger: Optional[Logger] = None
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        """

        self.logger = logger

    @property
    def logger(
            self
    ) -> Optional[Logger]:
        """
        Get the logger.

        :returns: The logger.
        """

        return self.__logger

    @logger.setter
    def logger(
            self,
            value: Optional[Logger]
    ) -> None:
        """
        Set the logger.

        :parameter value: The logger. The value `None` indicates that the logger should not be utilized.
        """

        self.__logger = value
