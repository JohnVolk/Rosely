Rosely
======

Interactive windroses using pandas and plotly


``Rosely`` leverages the polar bar char of `Plotly <https://plot.ly/python/>`__ and `pandas <https://pandas.pydata.org/>`__ to simplyfy the creation of beautiful and interactive windrose diagrams. This package was inspired by the Plotly polar bar chart with hoverable tooltips, zoom, pan, and other interactive features.``Rosely``'s main purpose is to make use of the Plotly polar bar chart more accessable and efficient for custom workflows using pandas and a simple object-oriented implementation.

Documentation 
-------------

Coming soon.


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

Given arbitrary time series data that contains wind speed and direction (degrees) ``Rosely`` can quickly produce wind statistics and interactive windrose diagrams once the data is loaded into a `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__.

This example uses the `provided example CSV <https://raw.githubusercontent.com/JohnVolk/Rosely/master/example/test_data.csv>`_ containing meterological data.

    >>> import pandas as pd
    >>> from rosely import WindRose
    >>> df = pd.read_csv('path/to/example_data.csv')
    >>> # make a WindRose object from the dataframe with "ws" and "wd" columns
    >>> WR = WindRose(df)
    >>> WR.plot(
    >>>     template='seaborn', colors='Plotly3', 
    >>>     title='Twitchell Island, California'
    >>> )

The resulting windrose diagram:

.. image:: https://raw.githubusercontent.com/JohnVolk/Rosely/master/docs/source/_static/quickstart.html

Details and examples of plot customization, output options, and windrose calculation options can be found in the online documentation. 

