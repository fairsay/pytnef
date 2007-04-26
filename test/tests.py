# First install the package (python setup.py install),
# then run these tests from within the test directory

from __future__ import with_statement
import unittest, os, sys
from StringIO import StringIO
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

   def testHasContent(self):
      self.failUnless(tnef.hasContent(open(getpath("two-files.tnef"))))
      self.failIf(tnef.hasContent(open(getpath("multi-name-property.tnef"))))
      self.failUnless(tnef.hasContent(open(getpath("body.tnef"))))


   def testlistContents_Body_NoMimeTypes(self):
      correct = {
         "AUTOEXEC.BAT": "",
         "CONFIG.SYS": "",
         "boot.ini": "",
         "%s.rtf" % TNEF_BODYFILENAME: "",
      }
      sourcefile = open(getpath("data-before-name.tnef"))
      tested = tnef.listContents(sourcefile, body=TNEF_BODYFILENAME, mimeinfo=True)
      self.assertEqual(correct, tested)

      
   def testListContents_NoBody_MimeTypes(self):
      correct = {
         "AUTHORS": "application/octet-stream",
         "README": "application/octet-stream",
      }
      tested = tnef.listContents(open(getpath("two-files.tnef")), mimeinfo=True)
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

   def testListBodyTypes_OneBodyNoFiles(self):
      "get list of body types (html,rtf,text) in TNEF file"
      self.assertEqual("html", tnef.listBodyTypes(open(getpath("body.tnef")))[0])
      
   def testListBodyTypes_OneBodyManyFiles(self):
      "get body type when there are many attached files"
      self.assertEqual("rtf", tnef.listBodyTypes(open(getpath("data-before-name.tnef")))[0])

if __name__=="__main__":   
   unittest.main()
   
