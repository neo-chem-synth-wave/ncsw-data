""" The ``ncsw_data.storage.cacs.sqlite_db.utility`` package ``typing`` module. """

from typing import Tuple

from ncsw_data.storage.cacs.sqlite_db.model.archive import *
from ncsw_data.storage.cacs.sqlite_db.model.workbench import *


CaCSSQLiteDatabaseArchiveCompoundTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompound
]

CaCSSQLiteDatabaseArchiveCompoundFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompound,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseArchiveReactionTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReaction
]

CaCSSQLiteDatabaseArchiveReactionFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReaction,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseArchiveCompoundPatternTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompoundPattern
]

CaCSSQLiteDatabaseArchiveCompoundPatternFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseArchiveReactionPatternTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReactionPattern
]

CaCSSQLiteDatabaseArchiveReactionPatternFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReactionPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseWorkbenchCompoundTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompound
]

CaCSSQLiteDatabaseWorkbenchCompoundFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompound,
    CaCSSQLiteDatabaseModelArchiveCompound,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseWorkbenchReactionTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReaction
]

CaCSSQLiteDatabaseWorkbenchCompoundPatternTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
]

CaCSSQLiteDatabaseWorkbenchCompoundPatternFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseWorkbenchReactionFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReaction,
    CaCSSQLiteDatabaseModelArchiveReaction,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseWorkbenchReactionPatternTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReactionPattern
]

CaCSSQLiteDatabaseWorkbenchReactionPatternFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReactionPattern,
    CaCSSQLiteDatabaseModelArchiveReactionPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]
