"""
A few utility functions used by other modules.
"""

import os, logging, sys
from contextlib import contextmanager

# package
from config import *

logger = logging.getLogger("pytnef")


@contextmanager
def data2file(datastr):
   "utility to factor away the write/open4read functionality"
   tmp_name = os.tempnam()
   tnef_file = open(tmp_name, "wb")
   tnef_file.write(datastr)
   tnef_file.flush()
   tnef_file.close()
   # mode needs to be rb
   tnef_file = open(tmp_name, "rb")
   yield tnef_file
   tnef_file.close()
   os.remove(tmp_name)   


@contextmanager
def temporary():
   "make tmpdir at begin, move it, move out & remove it and files in it at the end"
   os.mkdir(TNEF_DIRECTORY)
   os.chdir(TNEF_DIRECTORY)
   yield
   for filename in os.listdir('.'):
      os.remove(filename)
   os.chdir("..")
   os.rmdir(TNEF_DIRECTORY)


def process_tnef_output(output, kwargs):
   "process file contents or contents + mimeinfo"
   
   output = output.strip().split('\n')
   if "mimeinfo" in kwargs:  
      output = dict([line.split('|') for line in output])

   return output


def process_args(args, argtable=TNEF_ARGUMENTS):
   """
   transmogrify python keyword args (passed as dict)
   to shell command args, using a mapping table
   """

   # set value if a real value (ie. not 'True') is given
   postprocess = lambda arg, value: arg if value==True else arg + '=' + value
      
   # filter out 'False' values
   args = [(arg, value) for arg, value in args.items() if value is not False]

   # process args
   return [postprocess(argtable[arg], value) for arg, value in args]
   
