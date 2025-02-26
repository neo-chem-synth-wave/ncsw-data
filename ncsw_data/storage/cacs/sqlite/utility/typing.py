""" The ``ncsw_data.storage.cacs.sqlite.utility`` package ``typing`` module. """

from typing import Tuple

from ncsw_data.storage.cacs.sqlite.model.archive import *
from ncsw_data.storage.cacs.sqlite.model.workbench import *


ArchiveCompoundsTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompound
]

ArchiveCompoundsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompound,
    CaCSSQLiteDatabaseModelArchiveSource
]

ArchiveCompoundPatternsTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompoundPattern
]

ArchiveCompoundPatternsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

ArchiveReactionsTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReaction
]

ArchiveReactionsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReaction,
    CaCSSQLiteDatabaseModelArchiveSource
]

ArchiveReactionPatternsTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReactionPattern
]

ArchiveReactionPatternsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReactionPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

WorkbenchCompoundsTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompound
]

WorkbenchCompoundsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompound,
    CaCSSQLiteDatabaseModelArchiveCompound,
    CaCSSQLiteDatabaseModelArchiveSource
]

WorkbenchCompoundPatternsTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
]

WorkbenchCompoundPatternsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

WorkbenchReactionsTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReaction
]

WorkbenchReactionsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReaction,
    CaCSSQLiteDatabaseModelArchiveReaction,
    CaCSSQLiteDatabaseModelArchiveSource
]

WorkbenchReactionPatternsTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReactionPattern
]

WorkbenchReactionPatternsFromSourcesTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReactionPattern,
    CaCSSQLiteDatabaseModelArchiveReactionPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]
