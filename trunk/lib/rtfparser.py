"""
The module implements a pyparsing - based special-purpose RTF parser
specifically for extracting HTML from RTF contained within a TNEF
attachment.
"""

import sys
from logging import critical

from pyparsing import Optional, Literal, Word, Group
from pyparsing import Suppress, Combine, replaceWith
from pyparsing import alphas, nums, printables, alphanums
from pyparsing import restOfLine, oneOf, OneOrMore, ZeroOrMore
from pyparsing import ParseException

__all__ = ("extractHTML", "RTFParserException")

class RTFParserException(Exception):
   "indicate failed RTF parsing"

htmchars = printables.replace("<","").replace(">","").replace("\\","").replace("{","").replace("}","") + " " + "\t"

SEP = Literal(';')

BRCKT_L = Literal('{')
BRCKT_R = Literal('}')
BRCKT = BRCKT_L | BRCKT_R
BRCKT.setName("Bracket")

# basic RTF control codes, ie. "\labelname3434"
CTRL_LABEL = Combine(Word(alphas + "'") + Optional(Word(nums)))
BASE_CTRL = Combine(Literal('\\') + CTRL_LABEL)

# in some rare cases (color table declarations), control has ' ;' suffix
BASE_CTRL = Combine(BASE_CTRL + SEP) | BASE_CTRL
BASE_CTRL.setName("BaseControl")

#\*\html93394
HTM_CTRL = Combine(Literal('\\*\\') + CTRL_LABEL)
HTM_CTRL.setName("HtmlControl")

RTF_CTRL = BASE_CTRL | HTM_CTRL
RTF_CTRL.setName("Control")

RTFCODE = OneOrMore(RTF_CTRL | BRCKT)

# handle "{\*\htmltag4 \par }""
HTM_CTRL_NEWLINE = HTM_CTRL.suppress() + Literal("\\par").setParseAction(replaceWith("\n"))
HTM_CTRL_NEWLINE.suppress()

# handle "{\*\htmltag84       }"
HTM_CTRL_EMPTY = HTM_CTRL.suppress() + Word(" ").leaveWhitespace()

HTM_TXT =  OneOrMore(Word(htmchars))
HTM_CTRL_CONTENT = HTM_CTRL.suppress() + Optional(BRCKT_R).suppress() + HTM_TXT

# Both opening and closing tags and their contents
HTM_TAG = Combine(Literal("<") + Word(htmchars) + Literal(">"))
HTM_TAG.leaveWhitespace()
HTM_TAG.setName("HtmlTag")
     
#HTM_TAG_EMPTYCONTENT = Word(" ") + BRCKT_R.suppress()
HTM_TAG_PLUS_CONTENT = HTM_TAG + Optional(BRCKT_R.suppress() + HTM_TXT)
HTM_TAG_PLUS_CONTENT.leaveWhitespace()

# Text content inside HTML
HTM_CONTENT_IND = Suppress("\\htmlrtf0 ")
HTM_CONTENT = HTM_CONTENT_IND + OneOrMore(Word(htmchars))

HTM_CONTENT.setName("Html content")
HTM_CONTENT.leaveWhitespace()

RTFLINK = Suppress("HYPERLINK \"") + Word(htmchars.replace('"','')) + Literal('"').suppress()

RTF = OneOrMore(
   HTM_CTRL_CONTENT | \
   HTM_TAG_PLUS_CONTENT | \
   HTM_CONTENT |  \
   HTM_CTRL_NEWLINE | \
   #HTM_CTRL_EMPTY | \
   RTFLINK.suppress() | \
   RTF_CTRL.suppress() | \
   BRCKT.suppress()
)  


def extractHTML(rtfsource):
   "parse a file-like RTF source & return extracted HTML"
   html = []

   for i, l in enumerate(rtfsource.read().split("\n")):
      l = l.strip()
      if l:
         try:
            r = RTF.parseString(l)
         except ParseException, e:
            raise RTFParserException("failed at line %i: %s..." % (i, l[:30]))
            # print "rtfparser error: %s" % e
            #r = None
            #if r: 
         html.append("".join(r))

   return "\n".join(html)

   
