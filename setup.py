__version__ = '0.8-py3k'

import os
import sys

if sys.version_info[:2] < (3, 1):
    msg = ("Py65-py3k requires Python 3.1 or better, you are attempting to "
           "install it using version %s.  Please install with a "
           "supported version\n" % sys.version)
    sys.stderr.write(msg)
    sys.exit(1)

from distutils.core import setup
here = os.path.abspath(os.path.dirname(__file__))

DESC = """\
Simulate 6502-based microcomputer systems in Python 3."""

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Assembly',
    'Topic :: Software Development :: Assemblers',
    'Topic :: Software Development :: Disassemblers',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Embedded Systems',
    'Topic :: Software Development :: Interpreters',
    'Topic :: System :: Emulators',
    'Topic :: System :: Hardware'
    ]

setup(
    name = 'py65',
    version = __version__,
    license = 'License :: OSI Approved :: BSD License',
    url = 'http://github.com/dabeaz/py65',
    description = '6502 microprocessor simulation package (Python3 port)',
    long_description= DESC,
    classifiers = CLASSIFIERS,
    author = "Mike Naberezny",
    author_email = "mike@naberezny.com",
    maintainer = "David Beazley",
    maintainer_email = "dave@dabeaz.com",
    package_dir = {'py65':'src/py65'},
    packages = [ 'py65','py65.devices','py65.utils','py65.tests','py65.tests.devices','py65.tests.utils'],
    # put data files in egg 'doc' dir
    data_files=[ ('doc', [
        'CHANGES.txt',
        'LICENSE.txt',
        'README.markdown',
        'TODO.txt',
        ]
    )],
)
