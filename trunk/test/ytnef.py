import os, logging
logging.basicConfig()
from tnef.errors import *
from tnef.ytnef import *
from tnef.mapiproperties import properties as mapiproperties

props = [list(pair) for pair in mapiproperties]
for pair in props:
   pair.reverse()
mapiproperties = dict(props)

logger = logging.getLogger("ytnef")

def parse_tnef(filepath):
   if not os.path.isfile(tneffiledir + os.sep + filename):
      raise IOError("file not found: %s" % filename)
   result = None
   try:
      result = parseFile(filepath)
   except Exception,e:
      raise TNEFProcessingError("error parsing %s: %s" % (filename,e))
   if result in (-1, -3):
      raise TNEFProcessingError("error parsing %s: error code: %i" % (filename, result))
   return result


if __name__=="__main__":
   tneffiledir = os.path.dirname(os.path.abspath(__file__))+ os.sep + "data"
   tneffilenames = [fn for fn in os.listdir(tneffiledir) if fn.split('.')[-1] in ("dat", "tnef")]
   for filename in tneffilenames:
      try:
         t = parse_tnef(tneffiledir + os.sep + filename)
      except IOError:
         logger.error("file not found: %s" % filename)
         continue
      except TNEFProcessingError:
         logger.error("could not parse %s" % filename)
         continue

      print "\n--------------------------------"
      print "     %s " % filename
      print "--------------------------------"

      if t.messageClass:
         print t.messageClass
      if t.body.size:
         print "body size: %i" % t.body.size
      for i in range(t.MapiProperties.count)[:4]:
         print getMAPIProperty(t.MapiProperties,i).namedproperty

      print "--------------------------------\n"

