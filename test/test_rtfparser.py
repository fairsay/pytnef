from __future__ import with_statement
import sys, unittest, os
from tnef import *
import util

#s = """{\\*\\htmltag84 <img src="http://www.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">}\\htmlrtf  {\\field{\\*\\fldinst{HYPERLINK "http://www.org.uk/email/imin/spacer.gif"}}{\\fldrslt\\cf1\\ul }}\\htmlrtf0 The """
   
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

#test_color = "\\red0\\green4\\blue9;"
test_color = "{\colortbl\red0\green0\blue0;\red0\green0\blue255;\red153\green204\blue0;\red137\green137\blue82;}"
test_controlcode = "\\jfdjfd84444\\sdsd\\*\\html343\\keer99"
test_html = """<a href=\"http://fgfg.oo/a%20b?a=349&b=sk\" id=\"kk\">some&nbsp;</a>"""
test_content = "\\htmlrtf0 Dear Whoever,"
test_brackets = "{}"

#test_basic = "".join((test_color, test_ctrlcode+test_html + test_content + test_brackets))
#test_complex = """{\*\htmltag84 <img src="http://www.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">}\htmlrtf  {\field{\*\fldinst{HYPERLINK "http://www.org.uk/email/imin/spacer.gif"}}{\fldrslt\cf1\ul }}\htmlrtf0 The """

test_both = """{\*\htmltag84 <img src="http://www.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">}\htmlrtf  {\field{\*\fldinst{HYPERLINK "http://www.org.uk/email/imin/spacer.gif"}}{\fldrslt\cf1\ul }}\htmlrtf0 The """


class TestParserFunctions(unittest.TestCase):
          
   def testColor(self):
      #self.assertEqual("\\red0\\green4\\blue9;", "".join(OneOrMore(BASE_CTRL).parseString(test_color)))
      self.assertEqual(extract_html_line(test_color), "")
      
   def testControlCode(self):
      # TODO: should really return [""], not empty?
      self.assertEqual(extract_html_line(test_controlcode), "")
      
   def testContent(self):
      self.assertEqual(extract_html_line(test_content), "Dear Whoever,")


   def testBoth(self):
      #tag = """ The <img src="http://www.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">"""      
      correct = """<img src="http://www.org.uk/email/imin/spacer.gif" width="1" height="8" border="0" alt="">"""
      self.assertEqual(correct, extract_html_line(test_both))

   def testKeepWhitespace(self):
      correct = "   "
      self.assertEqual(correct, extract_html_line(correct))

   def testKeepWhitesAndTabs(self):
      correct = "  \t  "
      self.assertEqual(correct, extract_html_line(correct))

   def testKeepWhitesAndTabsAndNewLine(self):
      correct = "  \t  \n"
      self.assertEqual(correct, extract_html_line(correct))

   def testKeepNewLine(self):
      correct = "\n\n"
      self.assertEqual(correct, extract_html_line(correct))

   def testKeepNewLineTimesTwo(self):
      correct = "\n\n"
      self.assertEqual(correct, extract_html_line(correct))

   def testKeepNewLine2(self):
      correct = "\r\n"
      self.assertEqual(correct, extract_html_line(correct))

   def testKeepNewLine2(self):
      correct = "\n\r"
      self.assertEqual(correct, extract_html_line(correct))

   """
   def testExample1ByLine(self):
      with util.files_reader(util.getpath("example1.rtf"), util.getpath("example1.html")) as reader:
         for rtf_line, html_line in reader:
            parsed = extract_html_line(rtf_line)
            original = html_line
            print "ORIGINAL: %s" % original
            print "PARSED: %s" % parsed
            self.assertEqual(parsed, original)

   def testExample1ByLines(self):
      original_html = open(util.getpath("example1.html"))
      for i, parsed in enumerate(extract_html_lines(open(util.getpath("example1.rtf")))):
         original = original_html.readline()[:-1]
         parsed = parsed.rstrip("\n")
         print "LINE %i -----------------------------"  % i
         print " -> ORIGINAL: %s..." % original[:30]
         print " -> PARSED: %s..." % parsed[:30]
         self.assertEqual(parsed, original)

   #def testExample1WriteHTML(self):
   #   write_html_document(util.getpath("example1.rtf"), util.getpath("example1_test.html"))
   """

if __name__=="__main__":
   unittest.main()