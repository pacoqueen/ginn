from distutils.core import setup
import warnings
warnings.filterwarnings("ignore", "Unknown distribution option")

subpackages = ['firebird', 'include', 'mysql', 'postgres',
               'sqlite', 'sybase', 'maxdb']

import sys
# patch distutils if it can't cope with the "classifiers" keyword
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name="SQLObject",
      version="0.6.1",
      description="Object-Relational Manager, aka database wrapper",
      long_description="""\
Classes created using SQLObject wrap database rows, presenting a
friendly-looking Python object instead of a database/SQL interface.
Emphasizes convenience.  Works with MySQL, Postgres, SQLite, Firebird.
Requires Python 2.2+.
""",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Programming Language :: Python",
                   "Topic :: Database",
                   "Topic :: Database :: Front-Ends",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      author="Ian Bicking",
      author_email="ianb@colorstudy.com",
      url="http://sqlobject.org",
      license="LGPL",
      packages=["sqlobject"] + ['sqlobject.%s' % package for package in subpackages],
      download_url="http://prdownloads.sourceforge.net/sqlobject/SQLObject-0.6.1.tar.gz?download")

# Send announce to:
#   sqlobject-discuss@lists.sourceforge.net
#   db-sig@python.org
#   python-announce@python.org
#   python-list@python.org

# Email tempate:
"""
@@ INTRO

What is SQLObject
=================

SQLObject is an object-relational mapper.  Your database tables are described as classes, and rows are instances of those classes.  SQLObject is meant to be easy to use and quick to get started with.

SQLObject supports a number of backends: MySQL, PostgreSQL, SQLite, and Firebird.  It also has newly added support for Sybase and MaxDB (also known as SAPDB).


Where is SQLObject
==================

Site:
http://sqlobject.org

Mailing list:
https://lists.sourceforge.net/mailman/listinfo/sqlobject-discuss

Archives:
http://news.gmane.org/gmane.comp.python.sqlobject

Download:
http://prdownloads.sourceforge.net/sqlobject/SQLObject-@@.tar.gz?download

News and changes:
http://sqlobject.org/docs/News.html


What's New
==========

@@ CHANGES

For a more complete list, please see the news: http://sqlobject.org/docs/News.html

-- 
Ian Bicking  /  ianb@colorstudy.com  / http://blog.ianbicking.org
"""
