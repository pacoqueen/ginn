#!/usr/bin/env python

# Setup script for the libgmail package
# Usage: 
# To create a source package; python setup.py sdist
# To install to your system; python setup.py install
import libgmail
from distutils.core import setup
mods = ['libgmail','lgconstants','gmail_transport']
setup (name = "libgmail",
       version = "%s" % libgmail.Version,
       description = "python bindings to access Gmail",
       author = "wdaher@mit.edu,stas@linux.isbeter.nl,follower@myrealbox.com",
       author_email = "libgmail-developer@lists.sf.net",
       url = "http://libgmail.sourceforge.net/",
       license = "GPL",
       py_modules = mods,
      )

