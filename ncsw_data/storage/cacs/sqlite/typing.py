""" The ``ncsw_data.storage.cacs.sqlite`` package ``typing`` module. """

from typing import Callable, Optional, Sequence, Tuple

CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[str]]
]

CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable

CaCSSQLiteDatabaseArchiveReactionStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[Sequence[Tuple[str, Sequence[str], Sequence[str], Sequence[str]]]]]
]

CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable

CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable
