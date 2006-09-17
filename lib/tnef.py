#!/usr/local/bin/python2.4
import os
from subprocess import Popen, PIPE
from copy import copy
from logging import debug
from StringIO import StringIO

__all__ = (
   "TNEFError", "hasBody", "hasFiles", "listFilesAndTypes", 
   "extractAll", "hasContent", "getBody", "getBodyTypes", 
   "TNEFBodyNotFoundException", "DEFAULTBODY"
)

DEFAULTBODY = "tnfbdyname"
TMPDIR = "tneftmpdir"
TNEFBODYTYPES = ("html", "rtf", "txt")

class TNEFError(Exception):
   "raised whenever something goes wrong invoking the command-line"


class TNEFBodyNotFoundException(TNEFError):
   "no body of the requested type"
   
def runTnef(sourcefile, args):
   "feed cmdline an open fileobj & args"
   args = ("tnef",) + args
   TNEF = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
   out, err = TNEF.communicate(sourcefile.read())
   sourcefile.close()   
   if TNEF.returncode:
      raise TNEFError("Problem running tnef command: %s" % err)

   return out
   

def getBodyTypes(sourcefile):
   "get a list of body types found"
   files = listFilesAndTypes(sourcefile, bodyname=DEFAULTBODY).keys()
   types = []
   for fn in files:
      for tt in TNEFBODYTYPES:
         if fn == '.'.join((DEFAULTBODY, tt)): 
            types.append(tt)
   return types
   
   
def getBody(sourcefile, bodytype="html"):
   "return body text or raise TNEFBodyNotFoundException if the file has no body of the type"

   srccopy = StringIO(sourcefile.read())
   sourcefile.seek(0)

   files = listFilesAndTypes(srccopy, bodyname=DEFAULTBODY).keys()
   filename = '.'.join((DEFAULTBODY, bodytype))

   # desired body type is available

   if  filename in files:
      os.mkdir(TMPDIR)
      extracted = extractAll(sourcefile, targetdir=TMPDIR, bodyname=DEFAULTBODY)
      body = None
      for extracted_file_path in extracted:
         if filename in extracted_file_path:
            bodyfp = open(extracted_file_path)
            body = bodyfp.read()
            bodyfp.close()
            del bodyfp
         os.remove(extracted_file_path)
      os.rmdir(TMPDIR)
      return body
      
   else:
      raise TNEFBodyNotFoundException("no %s body found" % bodytype)
  
   
def hasBody(sourcefile):
   "true if the TNEF file contains a content body"
   files = listFilesAndTypes(sourcefile, bodyname=DEFAULTBODY).keys()
   if DEFAULTBODY in "".join(files):
      return True
   return False

   
def hasFiles(sourcefile):
   "true if the TNEF file contains embedded files; ignores body"
   filenames = listFilesAndTypes(sourcefile, bodyname=DEFAULTBODY).keys()
   if not filenames or DEFAULTBODY in filenames[0]:
      return False
   return True


def hasContent(sourcefile):
   "true of the file contains body OR files"
   if listFilesAndTypes(sourcefile):
      return True
   return False


def parseListing(listing):
   "return a dict of file names as keys & types as values"
   listing = listing.strip().split("\n")
   files = {}
   for l in listing:
      if l:
         fname, ftype = l.split('|')
         files[fname] = ftype
   return files

   
def listFilesAndTypes(sourcefile, bodyname=None):
   "list files, including body"
   args = ("--list-with-mime-types",)   

   if bodyname:
      args += ("--save-body=%s" % bodyname,)
   else:
      args += ("--save-body",)

   output = runTnef(sourcefile, args)
   return parseListing(output)


def extractAll(sourcefile, targetdir=None, bodyname=None):
   "return {fullpath: contenttype} list of extracted stuff"

   args = ("--overwrite",)

   if bodyname:
      args += ("--save-body=%s" % bodyname,)
   else:
      args += ("--save-body",)

   if targetdir:
      args += ("--directory=%s" % targetdir,)
   else:
      targetdir = os.curdir
   files = []
   runTnef(sourcefile, args) #gives no output
   return [targetdir + os.sep + fn for fn in os.listdir(targetdir)]
