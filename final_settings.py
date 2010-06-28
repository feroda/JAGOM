# Configuration options that depend on others
# which can be overridden by user

import os
from settings import *

TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = DEBUG

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "media"),
    os.path.join(PINAX_ROOT, "media", PINAX_THEME),
]

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
]
