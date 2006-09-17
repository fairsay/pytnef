import sys, unittest, os
from tnef.rtfparser import RTF

#s = """{\\*\\htmltag84 <img src="http://www.oxfam.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">}\\htmlrtf  {\\field{\\*\\fldinst{HYPERLINK "http://www.oxfam.org.uk/email/imin/spacer.gif"}}{\\fldrslt\\cf1\\ul }}\\htmlrtf0 The """
   
#s = "{\\*\\htmltag84 &rsquo;}\\htmlrtf \\'92\\htmlrtf0  fdfdf around. Because "
#s = "{\\*\\htmltag92 </a>} entering the name of the person you "
   
#s="{\\*\\htmltag4 \\par }  {\\*\\htmltag84       }"

# Sometimes content appears after a HTM_CTRL
# {\*\htmltag244 Untitled Document}"
# Sometimes AFTER the bracket.
# {\*\htmltag84       }here to view this email online

# Should handle these cases:
# {\\*\\htmltag84 &rsquo;}\\htmlrtf \\'92\\htmlrtf0 re attempting the biggest
#HTM_DATA = HTM_CTRL.suppress() + OneOrMore(HTM_TAG | HTM_TXT) + OneOrMore(BRCKT.suppress() | BASE_CTRL.suppress()) + ZeroOrMore(HTM_TXT)

# A tricky case
# {\*\htmltag84 &rsquo;}\htmlrtf \'92\htmlrtf0 re attempting the biggest

test_color = "\\red0\\green4\\blue9;"
test_ctrlcode = "\\jfdjfd84444\\sdsd\\*\\html343\\keer99"
test_html = "<a href=\"http://fgfg.oo/a%20b?a=349&b=sk\" id=\"kk\">some&nbsp;</a>"
test_content = "\\htmlrtf0 Dear Whoever,"
test_brackets = "{}"

testdata = "".join((test_color, test_ctrlcode+test_html + test_content + test_brackets))

test_complex = """{\*\htmltag84 <img src="http://www.oxfam.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">}\htmlrtf  {\field{\*\fldinst{HYPERLINK "http://www.oxfam.org.uk/email/imin/spacer.gif"}}{\fldrslt\cf1\ul }}\htmlrtf0 The """

test_complex = """{\*\htmltag84 <img src="http://www.oxfam.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">}\htmlrtf  {\field{\*\fldinst{HYPERLINK "http://www.oxfam.org.uk/email/imin/spacer.gif"}}{\fldrslt\cf1\ul }}\htmlrtf0 The """


class TestParserFunctions(unittest.TestCase):
    
   def setUp(self):
      pass
      
   def tearDown(self):
      pass
      
   def testColor(self):
      pass #self.assertEqual("\\red0\\green4\\blue9;", "".join(OneOrMore(BASE_CTRL).parseString(test_color)))
   
   def testComplex(self):
      tag = """ The <img src="http://www.oxfam.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">"""
      print RTF.parseString(test_complex)
      self.assertEqual(tag, "".join(RTF.parseString(test_complex)))


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
   unittest.main()