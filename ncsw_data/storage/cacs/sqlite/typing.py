""" The ``ncsw_data.storage.cacs.sqlite`` package ``typing`` module. """

from typing import Callable, Iterable, Optional, Sequence, Tuple


CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[str]]
]

CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable

CaCSSQLiteDatabaseArchiveReactionStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[Iterable[Tuple[str, Iterable[str], Iterable[str], Iterable[str]]]]]
]

CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable

CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable
