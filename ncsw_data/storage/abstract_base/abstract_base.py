""" The ``ncsw_data.storage.abstract_base`` package ``abstract_base`` module. """

from abc import ABC
from logging import Logger
from typing import Optional


class AbstractBaseDataStorage(ABC):
    """ The abstract base data storage class. """

    def __init__(
            self,
            logger: Optional[Logger] = None
    ) -> None:
        """
        The constructor method of the class.

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
