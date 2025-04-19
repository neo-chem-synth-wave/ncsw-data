""" The ``ncsw_data.storage.cacs.sqlite_`` package ``typing_`` module. """

from typing import Callable, Iterable, Optional, Sequence, Tuple


CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[str]]
]

CaCSSQLiteDatabaseArchiveReactionStandardizationCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[Iterable[Tuple[str, Iterable[str], Iterable[str], Iterable[str]]]]]
]

CaCSSQLiteDatabaseArchiveCompoundPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveCompoundStandardizationCallable

CaCSSQLiteDatabaseArchiveReactionPatternStandardizationCallable = \
    CaCSSQLiteDatabaseArchiveReactionStandardizationCallable

CaCSSQLiteDatabaseWorkbenchReactionPatternExtractionCallable = Callable[
    [Sequence[str]],
    Sequence[Optional[
        Iterable[Tuple[str, Iterable[Tuple[str, str]], Iterable[Tuple[str, str]], Iterable[Tuple[str, str]]]]
    ]]
]
