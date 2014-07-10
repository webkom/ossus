# -*- coding: utf8 -*-

from focusbackup.settings.base import *

# Import local settings like DB passwords and SECRET_KEY
try:
    from focusbackup.settings.local import *
except ImportError, e:
    raise ImportError("Couldn't load local settings focusbackup.settings.local")