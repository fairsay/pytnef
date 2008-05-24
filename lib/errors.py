"""
This module contains exception & error definitions
"""

class TNEFRunnerError(Exception):
   "raised whenever something goes wrong invoking the command-line"


class TNEFProcessingException(Exception):
   "no body of the requested type, whatever etc."

class TNEFProcessingError(Exception):
   "could not successfully process TNEF"
