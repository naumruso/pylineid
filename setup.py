from distutils.core import setup

import pylineid


version = pylineid.__version__

short_descr = "Automatic placement of labels for spectral lines"

classifiers = ['Development Status :: 4 - Beta',
               'Programming Language :: Python',
               'Intended Audience :: Science/Research',
               'Topic :: Scientific/Engineering :: Astronomy',
               'Topic :: Scientific/Engineering :: Physics',
               'License :: OSI Approved :: BSD License']


setup(
    name="pylineid",
    version=version,
    description=short_descr,
    license='BSD',
    author="Naum Rusomarov",
    author_email="naum.rusomarov@gmail.com",
    url='https://github.com/naumruso/pylineid',
    classifiers=classifiers,
    py_modules=["pylineid"]
    )
