"""
This module implements a low-level wrapper to the 'tnef' command. There should
be no need to use it directly; the higher-level API implemented in tnef.tnef
and imported to the top-level package namespace should be used instead.
"""

import logging
from subprocess import Popen, PIPE

# package
import errors, util

__all__ = ("listContents", "extractContents")

# wrapped core tnef shell command API; listing & extraction;
# see above argument table & tnef man page for an overview

# If 'body' is set, the message body is always extracted, and if 
# 'contents' or 'mimeinfo' is additionally set, the body will be 
# included in contents listing as well

# If 'contents' is set, a list of contained files; alternatively,
# if 'mimeinfo' is set, a list of filename:mimetype dictionaries is
# returned

logger = logging.getLogger("tnef-command")

def listContents(sourcefile, **kwargs):
   "wrapper for using tnef command body/attachment listing functionality"

   kwargs.update({"contents":True})

   output =  _tnef(sourcefile, kwargs)
   
   if output:
      output = util.process_tnef_output(output, kwargs)
   else:
      output = []
   logger.debug("listContents of %s: %s" % (sourcefile.name, ", ".join(output)))
   return output


def extractContents(sourcefile, **kwargs):
   "wrapper for using tnef command body/attachment extraction functionality"

   _tnef(sourcefile, kwargs)


# actual command invocation

def _tnef(sourcefile, kwargs):
   "shell command runner"

   args = util.process_args(kwargs)
   args = ["tnef"] + args
   process = Popen(args, stdin=sourcefile, stdout=PIPE, stderr=PIPE)
   out, err = process.communicate()
   sourcefile.seek(0)
   
   problem = (process.returncode != 1 and process.returncode) or err
   if problem:
      raise errors.TNEFRunnerError("command failed: %s" % problem)

   return out
