# -*- coding: utf8 -*-

from focusbackup.settings.base import *

# Import local settings like DB passwords and SECRET_KEY
try:
    from focusbackup.settings.local import *
except ImportError, e:
    raise ImportError("Couldn't load local settings uno.settings.local")

if 'debug_toolbar' in INSTALLED_APPS:
    from focusbackup.settings.debug_toolbar import *