import logging
from enum import StrEnum

"""
This file is for configuring our global logging system for this entire backend. Per-file logging is handled very simply inside each module.
As for global logging, once we call basicConfig one time, we can call our configured logger from anywhere in any module within this entire project. 

At the initial startup, we simply call the configure_logging function using "INFO" or "DEBUG" or something
which configures the logging system to give us extended insights into each log as per the LOG_FORMAT_DEBUG format if in debug mode
or just info if in INFO mode so like normal logging without timestamps and all the above. 
"""

LOG_FORMAT_DEBUG = (
    "%(asctime)s %(levelname)s %(message)s "
    "[%(pathname)s:%(funcName)s:%(lineno)d]"
)

class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str = LogLevels.error):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]       # Make a list of all possible log level values

    # if the user passed in an invalid log_level, then configure an error which immediately just logs an error to console
    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    # if the user passed in "DEBUG" then we start it up in debug mode and use the format we specified above
    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    # otherwise just instantiate it with whatever other log level (Info or Warn)
    logging.basicConfig(level=log_level)


"""
In other files, to use this configured logging system, do the following:

import logging

logger = logging.getLogger(__name__)        # __name__ organized the loggers by module path

# Then in the code you can just do this and it will handle the rest
logger.debug("...")
logger.info("...")
logger.error("DB connection failed...")
"""