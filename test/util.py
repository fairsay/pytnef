import sys, unittest, os
from contextlib import contextmanager
from cStringIO import StringIO

datadir = "data"

def getpath(filename):
   return sys.path[0] + os.sep + datadir + os.sep + filename

def getFiles(filename):
   f = open(getpath(filename))
   s = StringIO(f.read())
   f.seek(0)
   return f, s


@contextmanager
def files_reader(file1, file2):
   
   def iterfiles(file1, file2):
      file1=open(file1)
      file2=open(file2)
      while 1:
         try:
            yield file1.readline(), file2.readline()
         except:
            raise StopIteration
            
   yield iterfiles(file1, file2)


def convertRtfTestFiles(testdir=os.curdir):
   "convert all test rtf files that come with the package"
   testfiles = ("rtfparse_testoxfam",) 
   #RTF.setDebug()
   
   testfiles = [fn for fn in os.listdir(testdir) if fn.endswith(".rtf")]
   
   for tf in testfiles:
      #print "\n### parsing %s ###\n" % tf
      testdata = open(os.sep.join((testdir, tf))).read()
      output = open(os.sep.join((testdir, "%s.html" % tf[:-4])), "w")

      for n, l in enumerate(testdata.split("\n")):
         if l:
            try:
               r = RTF.parseString(l)
               if r: 
                  #print l
                  #print "%s\n" % "".join(r)
                  output.write("".join(r))
            except Exception, e:
               print e, l
               sys.exit()
         else:
            pass #print "\n -> ignored newline\n"



if __name__=="__main__":
   convertRtfTestFiles()
