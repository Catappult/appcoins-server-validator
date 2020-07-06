import os
import logging
from enum import Enum


class Environments(Enum):
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"
    LOCAL = "LOCAL"


_ENV_VAR = "PURCHASE_CHECKER"

try:
    ENVIRONMENT = Environments(os.environ.get(_ENV_VAR))
except ValueError:
    ENVIRONMENT = Environments.LOCAL
    logging.warning("No valid value set for environment variable '{}'. "
                    "Assuming value '{}'".format(_ENV_VAR, ENVIRONMENT))
    from .local.validator import *

if ENVIRONMENT == Environments.PRODUCTION:
    from .production.validator import *
elif ENVIRONMENT == Environments.DEVELOPMENT:
    from .development.validator import *
