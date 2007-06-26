"""
The tnef module provides high-level access to tnef decoding; namely,
listing contents of TNEF attachments and extracting and retrieving
TNEF body/bodies and embedded files.

@group content checking: has*
@group content retrieval: get*
@group content listing: list*
@group utilities: listBodyTypes, getInfo
"""

from __future__ import with_statement
from contextlib import closing

import os, logging
from copy import copy
from cStringIO import StringIO

# package
import cmd
from errors import TNEFProcessingException
from config import TNEF_DIRECTORY, TNEF_BODYFILENAME, TNEF_BODYPREFERENCE
from util import temporary


__author__ = "Petri Savolainen"
__all__ = (
   "hasBody", "hasFiles",
   "getBody", "getFiles",
   "listFiles", "listBodies",
)

TNEFBODYTYPES = ("rtf", "html", "txt")


# RETRIEVING CONTENTS

def getBody(sourcefile, preference=None, extract=True):
   """
   By default, looks up body types in default order (rtf > html > txt).

   @type sourcefile: open file (in mode 'rb')
   @type preference: tuple
   @param preference: The lookup preference can be altered by giving a tuple consisting
   one or more out of "rtf", "html" and "txt".
   @param extract: return html extracted from inside rtf instead of returning rtf?
   @rtype string   
      
   If no body is found, an exception is raised.
   """

   if preference:
      shortpref = "".join([item[0] for item in preference])
   else:
      shortpref = TNEF_BODYPREFERENCE

   # acceptable body type exists in the TNEF file?
   bodytypes = listBodies(sourcefile)
   if not set(preference).intersection(bodytypes):
      errmsg = "%s contains %s bodies, no %s"
      errdata = (sourcefile.name, ", ".join(bodytypes), ", ".join(preference))
      raise TNEFProcessingException(errmsg % errdata)

   body = None
      
   with temporary():
      cmd.extractContents(sourcefile, body=TNEF_BODYFILENAME, preference=shortpref)
      logging.debug("getBody extracted files: %s" % ", ".join(os.listdir('.')))
      for suffix in preference:
         bodyfilename = TNEF_BODYFILENAME + "." + suffix
         try:
            bodyfile = open(bodyfilename)
         except:
            logging.debug("getBody could not open %s" % bodyfilename)
            continue
            
         body = bodyfile.read()
         bodyfile.close()
         
         # extract RTF contents?
         if suffix == "rtf" and extract:
            body = body
         break

   if body:
      return body
   else:
      errdata = (", ".join(preference), sourcefile.name)
      raise TNEFProcessingException("%s bodies not found in %s" % errdata)
      

def getFiles(sourcefile, names=[]):
   "get all attached files, or a subset id'd by file names"
   with temporary():
      cmd.extractContents(sourcefile)
      for filename in os.listdir('.'):
         with closing(open(filename)) as attachment:
            yield filename, attachment.read()
      
# LISTING TNEF CONTENTS


def listFiles(sourcefile, mimeinfo=False):
   "return list of attached file names and optionally their mime types"
   return cmd.listContents(sourcefile, mimeinfo=mimeinfo)


def listBodies(sourcefile, preference=None):
   "return list of contained message bodies (body types rtf/html/text)"
   
   if preference:
      shortpref = "".join([item[0] for item in preference])
   else:
      shortpref = "all"
   
   files = cmd.listContents(sourcefile, body=TNEF_BODYFILENAME, preference=shortpref)

   bodies = []
   for fn in files:
      for tt in TNEFBODYTYPES:
         if fn == '.'.join((TNEF_BODYFILENAME, tt)):
            bodies.append(tt)
            
   logging.debug("%s contains following bodies: %s" % (sourcefile.name, ", ".join(bodies)))
   return bodies
   
   
   
# CHECKING CONTENTS

def hasBody(sourcefile, preference=None):
   "return true if the TNEF file contains a content body within preference list"
   
   if preference:
      shortpref = "".join([item[0] for item in preference])
   else:
      shortpref = "all"
   
   filenames = cmd.listContents(sourcefile, body=TNEF_BODYFILENAME, preference=shortpref)
   
   for filename in filenames:
      if TNEF_BODYFILENAME in filename:
         return True
   return False

   
def hasFiles(sourcefile):
   "return true if the TNEF file contains embedded files; ignores body"
   if cmd.listContents(sourcefile):
      return True
   return False




   
   
   

