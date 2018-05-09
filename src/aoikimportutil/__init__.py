# coding: utf-8
from __future__ import absolute_import  # Require Python 2.5+

import aoikimportutil.aoikimportutil as _aoikimportutil


__version__ = _aoikimportutil.__version__


# Support usage like:
# `from aoikimportutil import load_obj`
# instead of:
# `from aoikimportutil.aoikimportutil import load_obj`
#
for key in getattr(_aoikimportutil, '__all__'):
    globals()[key] = getattr(_aoikimportutil, key)

del _aoikimportutil
