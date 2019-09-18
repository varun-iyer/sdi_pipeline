# SDI Pipeline
UCSB’s astronomical data processing pipeline

## Installation
Currently only prepared for use on `starmaker`

## Usage
```
$ python3 -m /path/to/sdi /path/to/*.fz
```
Outputs a `srcs.pkl` file representing a catalog of transient candidates.

## TODO
* EASY: small fixes that can be done without special python knowledge, mostly modifying existing code or some tinkering
    * Pylinting files
    * Logging
* MEDIUM: new features that require a little bit of python experience and reading through some library documentation
    * Command Line fitsfile I/O using `click`
        * Add \_\_main\_\_s to scripts (easy after the above is completed)
    * Generating documentation with Sphinx/readthedocs
    *  An actual config file
	* Package with `setup.py` for distribution/installation
* DIFFICULT: features and modifications that requires experience with Python, more complex libraries, or computer algorithms
    * A SQLite database to store fitsfiles and cache results of processing
    * optimization of M31 Amsterdam lookup with local databases and k-vectors or knn
    * Numpy or Cython optimization of source transformation
	* Unit testing
* Miscellaneous: run `git grep -E 'TODO|FIXME'`
