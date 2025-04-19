""" The ``ncsw_data.storage.cacs.sqlite_.utility`` package ``typing_`` module. """

from typing import Tuple

from ncsw_data.storage.cacs.sqlite_.model.archive import *
from ncsw_data.storage.cacs.sqlite_.model.workbench import *


CaCSSQLiteDatabaseArchiveCompoundTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompound
]

CaCSSQLiteDatabaseArchiveCompoundFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompound,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseArchiveCompoundPatternTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompoundPattern
]

CaCSSQLiteDatabaseArchiveCompoundPatternFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseArchiveReactionTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReaction
]

CaCSSQLiteDatabaseArchiveReactionFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelArchiveReaction,
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

CaCSSQLiteDatabaseWorkbenchCompoundPatternTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern
]

CaCSSQLiteDatabaseWorkbenchCompoundPatternFromSourceTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveCompoundPattern,
    CaCSSQLiteDatabaseModelArchiveSource
]

CaCSSQLiteDatabaseWorkbenchReactionTuple = Tuple[
    CaCSSQLiteDatabaseModelWorkbenchReaction
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
