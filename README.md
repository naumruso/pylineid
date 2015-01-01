Line identification plots using Matplotlib
==========================================

The python module `pylineid` is used for automatic placement of labels
of spectral features (lines) without the labels overlapping each other
in a spectrum.

The use case of this module can be found in spectroscopy, where it is 
common to task to create plots of a spectrum with lines identified with
labels.

An example illustrating the features of `pylineid` is in included
with the repository.

Installation
============

To install the code run

```
python setup.py install
```
  
If you want to install the code in your local user directory run

```
python setup.py install --user
```

To download the entire repository either clone the repository or use
the *Download* button. To download just the `pylineid.py` file,
click on the file and then download the *raw* version.

Example
=======

A basic plot can be created by calling the function `put_lines()` and
passing the required parameters. It is important the the user first
plots the spectrum and lets matplotlib draw the figure.

![Example plot](https://github.com/naumruso/pylineid/blob/master/pylineid_example.png)

Notes
=====

In OS X it is required that the user calls `Figure.show()` after plotting
the spectrum and before calling the function `put_lines()`. `Figure.show()`
creates the necessary renderers that define the size of different elements
of the plot. In Linux, usually `Figure.canvas.draw()` is enough.

In the opposite case one will get a matplotlib `RuntimeError: Cannot get window extent w/o renderer`

License
=======

Released under BSD; see http://www.opensource.org/licenses/bsd-license.php.

Credits
=======

The module `pyidline` uses code taken from [lineid_plot](https://github.com/phn/lineid_plot), originally
written by Prasanth Nair and released used the BSD license.
