""" The ``ncsw_data.storage.cacs.sqlite_`` package ``typing_`` module. """

from typing import Callable, Optional, Sequence, Tuple


CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[str]]
]

CaCSSQLiteDatabaseArchiveReactionStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[Sequence[Tuple[str, Sequence[str], Sequence[str], Sequence[str]]]]]
]

CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable

CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable

CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable
