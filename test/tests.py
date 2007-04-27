# First install the package (python setup.py install),
# then run these tests from within the test directory

from __future__ import with_statement
from contextlib import closing
import unittest, os, sys
from cStringIO import StringIO
from logging import root, DEBUG

import tnef
from tnef.config import *
from tnef.errors import *
from tnef.util import temporary

root.setLevel(DEBUG)

datadir = "data"
tmpdir = "tmptestdir"


def getFiles(filename):
   f = open(getpath(filename))
   s = StringIO(f.read())
   f.seek(0)
   return f, s


def getpath(filename):
   return sys.path[0] + os.sep + datadir + os.sep + filename
   
class TestTnefFunctions(unittest.TestCase):
    
   def testHasBody(self):
      f, s = getFiles("body.tnef")
      self.failUnless(tnef.hasBody(f))
      #self.failUnless(tnef.hasBody(s))
      
      f, s = getFiles("multi-name-property.tnef")
      self.failIf(tnef.hasBody(f))
      #self.failIf(tnef.hasBody(s))

   def testHasFiles(self):
      f, s = getFiles("multi-name-property.tnef")
      self.failIf(tnef.hasFiles(f))
      #self.failIf(tnef.hasFiles(s))
      
      self.failUnless(tnef.hasFiles(open(getpath("two-files.tnef"))))
      self.failIf(tnef.hasFiles(open(getpath("body.tnef"))))


   def testlistBodies(self):
      correct = ["rtf"]
      sourcefile = open(getpath("data-before-name.tnef"))
      tested = tnef.listBodies(sourcefile)
      self.assertEqual(correct, tested)

      
   def testListFiles_MimeTypes(self):
      correct = {
         "AUTHORS": "application/octet-stream",
         "README": "application/octet-stream",
      }
      tested = tnef.listFiles(open(getpath("two-files.tnef")), mimeinfo=True)
      self.assertEqual(correct, tested)

      
   def testExtractContents_Body_NoMimeTypes(self):
      "are files & bodies listed ok by listContents?"
      
      correct = [
         "AUTOEXEC.BAT", "CONFIG.SYS", "boot.ini", TNEF_BODYFILENAME + ".rtf"
      ]
      
      sourcefile = open(getpath("data-before-name.tnef"))
      filenames = tnef.listContents(sourcefile, body=TNEF_BODYFILENAME)
      with temporary():
         tnef.extractContents(sourcefile, body=TNEF_BODYFILENAME)
         for filename in filenames:
            self.failUnless(os.path.isfile(filename))
      self.assertEqual(correct, filenames)


   def testGetFiles(self):
      "getFiles extracts attached files?"
      
      correct = {}
      with closing(open(getpath("README"))) as rfp:
         correct["README"] = rfp.read()
      with closing(open(getpath("AUTHORS"))) as afp:
         correct["AUTHORS"] = afp.read()            

      with closing(open(getpath("two-files.tnef"))) as source:
         for name, content in tnef.getFiles(source):
            assert content == correct[name]
               
      
   def testGetBody_TypeIsAvailable(self):
      "getBody returns existing desired body type?"
      f, s = getFiles("body.tnef")
      retrieved = tnef.getBody(f, preference=("html",))
      content = open(getpath("message.html")).read()
      self.assertEqual(content, retrieved)

      #retrieved = tnef.getBody(s, bodytype="html")
      #self.assertEqual(content, retrieved)


   def testGetBody_TypeIsNotAvailable(self):
      "getBody raises exception when desired body type is not available?"
      def raiser():
         retrieved = tnef.getBody(open(getpath("body.tnef")), preference=("rtf",))
      self.assertRaises(TNEFProcessingException, raiser)


   def testListBodies_OneBodyNoFiles(self):
      "get list of body types (html,rtf,text) in TNEF file"
      sourcefile = open(getpath("body.tnef"))
      bodytype = tnef.listBodies(sourcefile, preference=("html",))[0]
      self.assertEqual("html", bodytype)
      
      
   def testListBodies_OneBodyManyFiles(self):
      "get body type when there are many attached files"
      sourcefile = open(getpath("data-before-name.tnef"))
      bodytype = tnef.listBodies(sourcefile)[0]
      self.assertEqual("rtf", bodytype)


if __name__=="__main__":   
   unittest.main()
   
