"""
module to extend the email.Message of python stdlib with TNEF parsing
and extraction of HTML from TNEF RTF attachments
"""

import email

class Message2(email.Message):
   "a message with added tnef functionality"
   
   
