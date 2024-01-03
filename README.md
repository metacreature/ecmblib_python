> [!WARNING]
> This project is still under developement, so please don't use it atm

# *.ecmb - The new Comic-Manga-eBook
**Benefits:**
- right to left reading in page-mode for Mangas, while scroll-mode is still top-down
- of course left to right and top-down reading for (western) Comics
- advanced support for double-pages
- content-warnings for using safe-guard
- a bunch of possible meta-data like genres and even the homepage of the publisher ([go to example >](https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/example_full.xml))
- support for sub-chapters and many possibilities for navigation with headlines and page-links ([go to example >](https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/advanced_book/advanced_book.ecmb_unpacked/ecmb.xml))
- validateable via XSD
- published under [MIT License](https://choosealicense.com/licenses/mit/)

## The project ([https://metacreature.github.io/ecmb](https://metacreature.github.io/ecmb))
**It contains:**
- the [definition](https://github.com/metacreature/ecmb_definition) of the file-format and a file-validator
- a [library](https://github.com/metacreature/ecmblib_python) for packing the eBooks
- a simple-to-use [builder](https://github.com/metacreature/ecmb_builder) for building the eBooks from your source-images
- a mobile-app for reading the eBooks is under developement
- unfortunately there is no web-scraper to download source-images, coz I guess that would be illegal in my country to publish something like that. Maybe you'll find some here: [https://github.com/topics/manga-scraper](https://github.com/topics/manga-scraper)

**If you like it I would be happy if you  [donate on checkya](https://checkya.com/1hhp2cpit9eha/payme)**


## About this repository:

This is the python-library you can use for your project to build `*`.ecmb - files without caring about the internals of the file-format.
You can't do anything wrong with this, coz if you do a mistake (eg. passing a boolean to set_description()) an ecmbException will be raised. After the creation the file will be automatic validated. 

Published under [MIT License](https://choosealicense.com/licenses/mit/)

# Using the library

### Installation
- download and install Python3 (>=3.11) [https://www.python.org/downloads/](https://www.python.org/downloads/)
- open the console and then
    - run `pip install ecmblib`
 
### Trying out examples
- download and install Python3 (>=3.11) [https://www.python.org/downloads/](https://www.python.org/downloads/)
- download and install Git [https://git-scm.com/downloads](https://git-scm.com/downloads)´
- open the git-console and then
    - clone this repositiory `git clone git@github.com:metacreature/ecmblib_python.git`
    - go to the project-folder `cd ecmblib_python/`
    - run `pip install -r requirements.txt`
    - go to the example-folder `cd examples/advanced_book/`
    - run `python advanced_book.py`
The examples are working even if you didn't install the library via pip, but coz of the relative import type-hinting is not working.
If you want to use type-hinting you have to install the library first and then change the import of ecmblib at the top of the examples.

### Documentation:
[https://metacreature.github.io/ecmb/ecmblib_python.html](https://metacreature.github.io/ecmb/ecmblib_python.html)
