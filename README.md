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
* Command Line fitsfile I/O using `click`
* Add \_\_main\_\_s to scripts
* An actual config file
* A database to store fitsfiles and cache results of processing
* Logging
* Visualization
* Generating documentation with Sphinx/readthedocs
* Optimization of M31 Amsterdam lookup
* Optimization of source transformation
* misc: run `git grep -E 'TODO|FIXME`
