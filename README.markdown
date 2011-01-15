# Py65 for Python 3

Note: This is a Python 3 port of Py65 created by David Beazley
(http://www.dabeaz.com) for his own diabolical amusement and personal
projects.  Important differences from the standard version:

- Py65 is only installed as a library.  If you want to run the
  monitor, use 'python3 -m py65.monitor'.

- Installation is based on distutils, not setuptools.

- Installation should not conflict with an existing Python-2
  installation of py65.

- Includes a 'superboard' demo where you can run an emulated
  1979 OSI Superboard II system and write little Microsoft 
  Basic 1.0 programs.   It's fun.

So far as I know, this version passes all of the tests contained 
in src/py65/tests. However, I have not done any testing beyond
my own use of the library (e.g., "it works for me.")

Note: I do not intend to maintain this branch except as needed for my
own projects under Python 3.  Use at your own risk. - Dave.

# Py65

Py65 provides tools for simulating hardware based on 6502-like
microprocessors.  It has the following goals:

 - Focus on ease of use and modularity rather than performance.  Py65 is
   written in the Python programming language for productivity, while
   similar programs are written in C for performance.

 - Enable simulations to be created for systems where it might have 
   otherwise not been practical, such as homebuilt computers. 

 - Rigorously unit test all of the components.  While the tools provided
   by Py65 may not always be perfect, their behavior is verified through 
   tests so unexpected results are minimized.
   
## Installation

Obtain the source from Github (http://github.com/dabeaz/py65).  Please
note that the original location of the Py65 project is at
http://github.com/mnaberez/py65/downloads.   Use the following to install
after you've obtained the source:

    $ python3 setup.py install

## Devices

The following devices are simulated at this time:

 - `mpu6502` simulates the original NMOS 6502 microprocessor from MOS
    Technology, later known as Commodore Semiconductor Group (CSG). At this
    time, all of the documented opcodes are supported.  Support for the
    illegal opcodes is planned for the future.

 - `mpu65c02` simulates a generic CMOS 65C02 microprocessor. There were
    several 65C02 versions from various manufacturers, some with more opcodes
    than others. This simulation is based on the W65C02S from the Western
    Design Center (WDC).

## Monitor

Py65 includes a console-based machine language monitor (sometimes also
called a debugger).  This program, launched using 'python3 -m
py65.monitor' allows you to interact with the simulations that you
build.  Its features include:

 - Commands that are largely compatible with those used in the monitor of
   the popular VICE emulator for Commodore computers.

 - Ability to load, dump, and fill memory.

 - Simple assemble and disassemble capability, including support for labels 
   and labels with offsets.

## Documentation

Py65 documentation is written using [Sphinx](http://sphinx.pocoo.org/) and is
periodically published to 
[http://6502.org/projects/py65/](http://6502.org/projects/py65/).

## Contributors

These people are responsible for Py65:

 - [Mike Naberezny](http://github.com/mnaberez) is the original author of 
   Py65 and is the primary maintainer.
 
 - [Oscar Lindberg](http://github.com/offe) started the 65C02 simulation 
   module and contributed greatly to its implementation. 

 - [Ed Spittles](http://github.com/biged) helped with testing and provided 
   many useful issue reports and patches.

 - [Dave Beazley](http://github.com/dabeaz) is the guilty party responsible
   for this Python 3 port.
