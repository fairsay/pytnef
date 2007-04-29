"""pytnef library: wrapper to access MS TNEF-coded files (winmail.dat)
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Libraries
Topic :: Communications :: Email
Operating System :: Unix
Operating System :: POSIX
"""

import sys, os
from distutils.core import setup, Extension

#from ez_setup import use_setuptools
#use_setuptools()

if os.name == "posix":
   PLATFORM_INCLUDES = ['/usr/include','/usr/include/python%i.%i' % sys.version_info[:2]]
   PLATFORM_LIBRARIES = ["/usr/lib","/usr/local/lib"]
if sys.version_info < (2, 3):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

doclines = __doc__.split("\n")

setup(name="pytnef",
      version="0.4",
      maintainer="Petri Savolainen",
      maintainer_email="petri.savolainen@iki.fi",
      license = "http://www.fsf.org/licensing/licenses/lgpl.txt",
      platforms = ["unix"],
      packages = ["tnef"],
      package_dir = {"tnef": "lib"},
      ext_modules=[Extension(
         "ytnef",
         [os.path.join("src","ytnef.c")],
         include_dirs=PLATFORM_INCLUDES,
         libraries = ["ytnef"],
         library_dirs = PLATFORM_LIBRARIES,
      )],
      description = doclines[0],
      classifiers = filter(None, classifiers.split("\n")),
      long_description = "\n".join(doclines[2:]),
)

