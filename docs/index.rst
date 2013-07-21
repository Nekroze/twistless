.. Twistless documentation master file, created by
   sphinx-quickstart on Mon Jul 22 00:10:51 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Twistless's documentation!
=====================================

A simple to use bridge between stackless python (available in pypy) and the
twisted networking library.

The underlying implementation is based off of the excelent article by Stephen
Coursen found here
http://www.stevecoursen.com/209/stackless-python-meets-twisted-matrix/ and
was a huge help when writing twistless.

*Twistless* is designed to give a quick and easy start to using stackless
python and twisted together. The following shows an overly brief example of a
twisted reactor being started with stackless support.

.. literalinclude:: ../quickdemo.py
    :language: python
    :linenos:

Contents:

.. toctree::
   :maxdepth: 4

   usage

Feedback
========

If you have any suggestions or questions about *Twistless* feel free to
email me at nekroze@eturnilnetwork.com.

You can check out more of what I am doing at http://nekroze.eturnilnetwork.com
my blog.

If you encounter any errors or problems with *Twistless*, please let me know!
Open an Issue at the GitHub http://github.com/Nekroze/twistless main repository.
