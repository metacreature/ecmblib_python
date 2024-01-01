.. ecmblib documentation master file, created by
   sphinx-quickstart on Fri Dec 29 21:16:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ecmblib's documentation!
===================================

"ecmblib" is the python-library you can use for your project to build `*`.ecmb - files without caring about the internals of the file-format.
You can't do anything wrong with this, coz if you do a mistake (eg. passing a boolean to set_description()) an ecmbException will be raised and after the creation the file will be automatic validated.

Published under: `MIT License <https://choosealicense.com/licenses/mit/>`_

Go to source-code: `https://github.com/metacreature/ecmblib_python <https://github.com/metacreature/ecmblib_python>`_

`*`.ecmb - The new Comic-Manga-eBook
------------------------------------
**Benefits:**

* right to left reading in page-mode for Mangas, while scroll-mode is still top-down
* of course left to right and top-down reading for (western) Comics
* advanced support for double-pages
* content-warnings for using safe-guard
* a bunch of possible meta-data like genres and even the homepage of the publisher (`go to example <https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/example_full.xml>`_)
* support for sub-chapters and many possibilities for navigation with headlines and page-links (`go to example <https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/advanced_book/advanced_book.ecmb_unpacked/ecmb.xml>`_)
* validateable via XSD
* published under `MIT License <https://choosealicense.com/licenses/mit/>`_

The project
-----------
**It contains:**

* the `definition <https://github.com/metacreature/ecmb_definition>`_ of the file-format and a file-validator
* a `library <https://github.com/metacreature/ecmblib_python>`_ for packing the eBooks
* a simple-to-use `builder <https://github.com/metacreature/ecmb_builder>`_ for building the eBooks from your source-images
* a mobile-app for reading the eBooks is under developement
* unfortunately there is no web-scraper to download source-images, coz I guess that would be illegal in my country to publish something like that. Maybe you'll find some here: `https://github.com/topics/manga-scraper <https://github.com/topics/manga-scraper>`_

**If you like it I would be happy if you** `donate on checkya <https://checkya.com/1hhp2cpit9eha/payme>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
