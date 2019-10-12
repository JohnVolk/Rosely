Rosely
======

Interactive wind roses simplified using Plotly and pandas


``Rosely`` leverages the polar bar char of `Plotly <https://plot.ly/python/>`__ and `pandas <https://pandas.pydata.org/>`__ to simplyfy the creation of beautiful and interactive wind rose diagrams. This package was inspired by the Plotly polar bar chart with hoverable tooltips, zoom, pan, and other interactive features. ``Rosely`` makes use of the Plotly polar bar chart for wind rose diagrams more accessable and efficient for custom workflows using pandas and a simple object-oriented implementation.

Documentation 
-------------

`ReadTheDocs <https://rosely.readthedocs.io/en/latest/index.html>`__


Installation
------------

``Rosely``'s dependencies are Python 3.4+, NumPy, pandas, and Plotly.

You may install the dependencies using the conda virtual environment (recommended), the environment file can be downloaded `here <https://raw.githubusercontent.com/JohnVolk/Rosely/master/environment.yml>`__ and installed and activated by

.. code-block:: bash

   conda env create -f environment.yml
   conda activate rosely

Once activated install with PIP:

.. code-block:: bash

   pip install rosely


Quick start
-----------

Given arbitrary time series data that contains wind speed and direction (degrees) ``Rosely`` can quickly produce wind statistics and interactive wind rose diagrams once the data is loaded into a `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__.

This example uses the `provided example CSV <https://raw.githubusercontent.com/JohnVolk/Rosely/master/example/test_data.csv>`_ containing meterological data.

.. code-block:: python

   import pandas as pd
   from rosely import WindRose
   df = pd.read_csv('path/to/example_data.csv')
   # make a WindRose object from the dataframe with "ws" and "wd" columns
   WR = WindRose(df)
   WR.plot(
       template='seaborn', colors='Plotly3', 
       title='Twitchell Island, California'
   )

The resulting wind rose diagram saved as a png (download `this file <https://raw.githubusercontent.com/JohnVolk/Rosely/master/docs/source/_static/quickstart.html>`_ for an interactive example):

.. image:: https://raw.githubusercontent.com/JohnVolk/Rosely/master/docs/source/_static/quickstart.png
   :align: center

Details and examples of plot customization, output options, and wind rose calculation options can be found in the online documentation. 

