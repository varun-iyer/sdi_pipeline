# TODO
*Sorted in order of priority with a E/M/H difficulty*
*Key:* 

**E** Requires little coding knowledge, just some googling. 

**M** requires a decent understanding of Python and some documentation-reading but nothing special

**H** requires a good understanding of Python and CS principles and a command of an external library or three

* **M** output as fitsfile + sources text file
* **E** Documentation with Sphinx and readthedocs
* **M** Use js9 to make clicky-click UI to view stuff
* **M** Implement Alard-Lupton in memory through [OIS](https://github.com/toros-astro/ois)
* **M** Configuration files: figure out how hotpants/OIS/sep are configured and create a YAML config file
* **M** Normalize image brightness by applying a gain and bias based on relative brightness of known stars
* **M** Command line interface with `click` to run parts of the pipeline, incl. help text and man page
* **H** Extract point spread functions for DIA from known sources
* **H** Collect light curves for transient candidates over all images and use them to filter candidates
	* Use integration of PSF instead of peak pixel
* **M** Add filtration techniques; e.g. checking if a source appears as a transient candidate in x% of images, etc.
* **H** Make a database to store science/processed/results and acces+view easily
* **E** Logging -- print more information about what the pipeline is doing with a way to filter it
	* `--log-level=STARWARS`
* **E** PyLinting: clean up existing code with `pylint`
* **H** Optimize reference star lookup with a wider cone query
	* Identify the 'same' stars between images with RA/DEC
* **M** Clean up the way sources are handled throughout the pipeline
* **M** Create unit tests
* **E** Test detection of known transient objects
Miscellaneous: run `git grep -E 'TODO|FIXME'`

* short exposure stacking
