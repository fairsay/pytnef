# First install the package (python setup.py install),
# then run these tests from within the test directory

import unittest, os
from cStringIO import StringIO
from logging import root, DEBUG
import tnef

root.setLevel(DEBUG)

tmpdir = "tmptestdir"


def getFiles(filename):
   f = open(filename)
   s = StringIO(f.read())
   f.seek(0)
   return f, s

class TestTnefFunctions(unittest.TestCase):
    
   def setUp(self):
      os.chdir("data")
      os.mkdir(tmpdir)
      
   def tearDown(self):
      os.rmdir(tmpdir)
      os.chdir("..")

   def testHasBody(self):
      f, s = getFiles("body.tnef")
      self.failUnless(tnef.hasBody(f))

      self.failUnless(tnef.hasBody(s))
      f, s = getFiles("multi-name-property.tnef")
      self.failIf(tnef.hasBody(f))
      self.failIf(tnef.hasBody(s))

   def testHasFiles(self):
      f, s = getFiles("multi-name-property.tnef")
      self.failIf(tnef.hasFiles(f))

      self.failIf(tnef.hasFiles(s))
      self.failUnless(tnef.hasFiles(open("two-files.tnef")))
      self.failIf(tnef.hasFiles(open("body.tnef")))

   def testHasContent(self):
      self.failUnless(tnef.hasContent(open("two-files.tnef")))
      self.failIf(tnef.hasContent(open("multi-name-property.tnef")))
      self.failUnless(tnef.hasContent(open("body.tnef")))

   def testlistFilesAndTypes_Body_NoMimeTypes(self):
      correct = {
         "AUTOEXEC.BAT": "",
         "CONFIG.SYS": "",
         "boot.ini": "",
         "%s.rtf" % tnef.DEFAULTBODY: "",
      }
      tested = tnef.listFilesAndTypes(open("data-before-name.tnef"), bodyname=tnef.DEFAULTBODY)
      self.assertEqual(correct, tested)
      
   def testlistFilesAndTypes_NoBody_MimeTypes(self):
      correct = {
         "AUTHORS": "application/octet-stream",
         "README": "application/octet-stream",
      }
      tested = tnef.listFilesAndTypes(open("two-files.tnef"))
      self.assertEqual(correct, tested)
      
   def testExtractAll_Body_NoMimeTypes(self):
      "use StringIO to make sure filelike objects are ok"
      pth = tmpdir + os.sep
      correct = [
         "%sAUTOEXEC.BAT" % pth,
         "%sCONFIG.SYS" % pth,
         "%sboot.ini" % pth,
         "%s%s.rtf" % (pth, tnef.DEFAULTBODY)
      ]
      tfile = open("data-before-name.tnef")
      files = tnef.listFilesAndTypes(tfile, bodyname=tnef.DEFAULTBODY).keys()
      tfile = StringIO(open("data-before-name.tnef").read())
      listing = tnef.extractAll(tfile, targetdir=tmpdir, bodyname=tnef.DEFAULTBODY)
      for fn in files:
         pth = tmpdir + os.sep + fn
         self.failUnless(os.path.isfile(pth))
         os.remove(pth)
      self.assertEqual(correct, listing)

   def testGetBody_TypeIsAvailable(self):
      "when the desired body type is available"
      f, s = getFiles("body.tnef")
      retrieved = tnef.getBody(f, bodytype="html")
      content = open("message.html").read()
      self.assertEqual(content, retrieved)

      #retrieved = tnef.getBody(s, bodytype="html")
      #self.assertEqual(content, retrieved)

   def testGetBody_TypeIsNotAvailable(self):
      "when the desired body type is NOT available"
      def raiser():
         retrieved = tnef.getBody(open("body.tnef"), bodytype="rtf")
      self.assertRaises(tnef.TNEFBodyNotFoundException, raiser)

   def testGetBodyTypes_OneBodyNoFiles(self):
      "get list of body types (html,rtf,text) in TNEF file"

      self.assertEqual("html", tnef.getBodyTypes(open("body.tnef"))[0])
      
   def testGetBodyTypes_OneBodyManyFiles(self):
      "get body type when there are many attached files"
      self.assertEqual("rtf", tnef.getBodyTypes(open("data-before-name.tnef"))[0])

if __name__=="__main__":   
   unittest.main()
   
