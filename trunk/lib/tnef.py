"""
high-level access to tnef decoding
"""
from __future__ import with_statement
import os, logging
from copy import copy
from StringIO import StringIO

# package
import cmd
from errors import TNEFProcessingException
from config import TNEF_DIRECTORY, TNEF_BODYFILENAME, TNEF_BODYPREFERENCE
from util import temporary


__all__ = ("hasBody", "hasFiles", "hasContent", "getBody", "listBodyTypes")

TNEFBODYTYPES = ("rtf", "html", "txt")


class TNEFAttachment:
   pass

   def __init__(self, sourcefile):
      self.source = sourcefile
      filenames = cmd.listContents(body=TNEF_BODYFILENAME, preference="all")

      self.rtf = self.html = self.text = None

      for filename in filenames:
         if TNEF_BODYFILENAME in filename:
            pass


   def getRTF(self):
      return self.rtf or getBody(preference="rtf")

   def getHTML(self):
      return self.html

   def getText(self):
      return self.text

   def getAttachments(self):
      return self.attachments



# TNEF CONTENT RETRIEVAL

def getBody(sourcefile, preference=None):
   """
   By default, looks up body types in default order (rtf > html > txt).

   The lookup preference can be altered by giving a tuple with maximum
   three items out of "rtf", "html" and "txt".
   string made of first chars of types. So 'r' looks for rtf only, 'ht'
   for html first and then text, and so on.

   If no body is found, an exception is raised.
   """

   if preference:
      shortpref = "".join([item[0] for item in preference])
   else:
      shortpref = TNEF_BODYPREFERENCE

   # acceptable body type exists in the TNEF file?
   bodytypes = listBodyTypes(sourcefile)
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
         break

   if body:
      return body
   else:
      errdata = (", ".join(preference), sourcefile.name)
      raise TNEFProcessingException("%s bodies not found in %s" % errdata)
      

def getAttachments(sourcefile, name=None):
   "get attached files, or just one id'd by 'name'"


# TOOLS FOR CHECKING TNEF CONTENTS

def listBodyTypes(sourcefile, preference=None):
   "get a list of body types found"

   pref = preference or "all"
   files = cmd.listContents(sourcefile, body=TNEF_BODYFILENAME, preference=pref)

   types = []
   for fn in files:
      for tt in TNEFBODYTYPES:
         if fn == '.'.join((TNEF_BODYFILENAME, tt)):
            types.append(tt)
   logging.debug("%s contains following bodies: %s" % (sourcefile.name, ", ".join(types)))
   return types


def hasBody(sourcefile, preference=None):
   "true if the TNEF file contains a content body within preference list"
   pref = preference or "all"
   filenames = cmd.listContents(sourcefile, body=TNEF_BODYFILENAME, preference=pref)
   for filename in filenames:
      if TNEF_BODYFILENAME in filename:
         return True
   return False

   
def hasFiles(sourcefile):
   "true if the TNEF file contains embedded files; ignores body"
   if cmd.listContents(sourcefile):
      return True
   return False


def hasContent(sourcefile):
   "true of the file contains body OR files"
   if cmd.listContents(sourcefile, body=True):
      return True
   return False


def parseInfo(sourcefile):
   "retrieve the info into a datadict"
   filelist = cmd.listContents(sourcefile, body=True, preference="all")
   data = {}
   
   
