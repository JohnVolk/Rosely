Tutorial
========

This tutorial covers basic usage of the ``Rosely`` package including
loading of data, calculatiion of wind statistics, and wind rose plotting
customizations.

    >>> import pandas as pd
    >>> import plotly.express as px
    >>> from rosely import WindRose

Read input data
---------------

:mod:`rosely` requires wind data to first be loaded into a
:obj:`pandas.DataFrame` object, also wind direction should be in degrees,
i.e. in [0, 360].

The example data used in this tutorial is a modified version of 30
minute data that was originally from the “Twitchell Alfalfa” AmeriFlux
eddy covariance flux tower site in the Sacramento–San Joaquin River
Delta in California. The site is located in alfalfa fields and exhibits
a mild Mediterranean climate with dry and hot summers, for more
information on this site click
`here <https://ameriflux.lbl.gov/sites/siteinfo/US-Tw3>`__.

The data used for this example can be downloaded on the Rosely GitHub repositor `here <https://raw.githubusercontent.com/JohnVolk/Rosely/master/example/test_data.csv>`__. And a Jupyter Notebook of this tutorial is available `here <https://github.com/JohnVolk/Rosely/blob/master/example/tutorial.ipynb>`_.

    >>> df = pd.read_csv('test_data.csv', index_col='date', parse_dates=True)
    >>> df[['ws','wd']].head()


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>ws</th>
          <th>wd</th>
        </tr>
        <tr>
          <th>date</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2013-05-24 12:30:00</td>
          <td>3.352754</td>
          <td>236.625093</td>
        </tr>
        <tr>
          <td>2013-05-24 13:00:00</td>
          <td>3.882154</td>
          <td>243.971055</td>
        </tr>
        <tr>
          <td>2013-05-24 13:30:00</td>
          <td>4.646089</td>
          <td>238.620934</td>
        </tr>
        <tr>
          <td>2013-05-24 14:00:00</td>
          <td>5.048825</td>
          <td>247.868815</td>
        </tr>
        <tr>
          <td>2013-05-24 14:30:00</td>
          <td>5.302946</td>
          <td>250.930258</td>
        </tr>
      </tbody>
    </table>
    </div>
    <br>



Or another view of the summary statistics of wind data

    >>> df[['ws','wd']].describe()


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>ws</th>
          <th>wd</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>count</td>
          <td>84988.000000</td>
          <td>84988.000000</td>
        </tr>
        <tr>
          <td>mean</td>
          <td>3.118813</td>
          <td>233.210960</td>
        </tr>
        <tr>
          <td>std</td>
          <td>2.032425</td>
          <td>84.893918</td>
        </tr>
        <tr>
          <td>min</td>
          <td>0.010876</td>
          <td>0.003150</td>
        </tr>
        <tr>
          <td>25%</td>
          <td>1.442373</td>
          <td>220.401528</td>
        </tr>
        <tr>
          <td>50%</td>
          <td>2.731378</td>
          <td>255.568402</td>
        </tr>
        <tr>
          <td>75%</td>
          <td>4.517145</td>
          <td>272.190239</td>
        </tr>
        <tr>
          <td>max</td>
          <td>14.733296</td>
          <td>359.997582</td>
        </tr>
      </tbody>
    </table>
    </div>



Create a :obj:`.WindRose` instance
----------------------------------

Using the loaded wind speed and direction data within a
:obj:`pandas.DataFrame` we can initialize a :obj:`rosely.WindRose` object
which provides simple methods for generating interactive wind rose
diagrams.

    >>> WR = WindRose(df)

Alternatively the dataframe can be later assigned to a :obj:`.WindRose`
object,

    >>> WR = WindRose()
    >>> WR.df = df

Calculate wind statistics
-------------------------

A wind rose diagram is essentially a stacked histogram that is binned by
wind speed and freqeuncy for a set of wind directions. These
calculations are accomplished by the :meth:`.WindRose.calc_stats` method
which allows for changing the number of default wind speed bins (equally
spaced) and whether or not the frequency is normalized to sum to 100 or
it is just the actual frequency of wind occurences (counts) in a certain
direction and speed bin.

By default the freqeuncy is normalized and the number of wind speed bins
is 9:

    >>> WR.calc_stats()

To view the results of the wind statistics that will be used for the
wind rose later, view the ``WindRose.wind_df`` which is created after
running :meth:`.WindRose.calc_stats`:

    >>> # view all statistics for winds coming from the North
    >>> WR.wind_df.loc[WR.wind_df.direction=='N']


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>direction</th>
          <th>speed</th>
          <th>frequency</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>0</td>
          <td>N</td>
          <td>-0.00-1.65</td>
          <td>1.36</td>
        </tr>
        <tr>
          <td>1</td>
          <td>N</td>
          <td>1.65-3.28</td>
          <td>0.66</td>
        </tr>
        <tr>
          <td>2</td>
          <td>N</td>
          <td>3.28-4.92</td>
          <td>0.24</td>
        </tr>
        <tr>
          <td>3</td>
          <td>N</td>
          <td>4.92-6.55</td>
          <td>0.07</td>
        </tr>
        <tr>
          <td>4</td>
          <td>N</td>
          <td>6.55-8.19</td>
          <td>0.01</td>
        </tr>
        <tr>
          <td>5</td>
          <td>N</td>
          <td>8.19-9.83</td>
          <td>0.01</td>
        </tr>
        <tr>
          <td>6</td>
          <td>N</td>
          <td>9.83-11.46</td>
          <td>0.00</td>
        </tr>
        <tr>
          <td>184</td>
          <td>N</td>
          <td>-0.00-1.65</td>
          <td>1.32</td>
        </tr>
        <tr>
          <td>185</td>
          <td>N</td>
          <td>1.65-3.28</td>
          <td>1.19</td>
        </tr>
        <tr>
          <td>186</td>
          <td>N</td>
          <td>3.28-4.92</td>
          <td>0.59</td>
        </tr>
        <tr>
          <td>187</td>
          <td>N</td>
          <td>4.92-6.55</td>
          <td>0.27</td>
        </tr>
        <tr>
          <td>188</td>
          <td>N</td>
          <td>6.55-8.19</td>
          <td>0.15</td>
        </tr>
        <tr>
          <td>189</td>
          <td>N</td>
          <td>8.19-9.83</td>
          <td>0.06</td>
        </tr>
        <tr>
          <td>190</td>
          <td>N</td>
          <td>9.83-11.46</td>
          <td>0.04</td>
        </tr>
        <tr>
          <td>191</td>
          <td>N</td>
          <td>11.46-13.10</td>
          <td>0.01</td>
        </tr>
      </tbody>
    </table>
    </div>



.. note:: 
   The winds speed bins in a certain direction may appear to be duplicated
   above but they are not, what is happening is that
   :meth:`.WindRose.calc_stats` bins each direction on a 16 point compass twice
   for 11.25 degrees sections on both sides of the compass azimuth. So for
   North there are two internal azimuth bins: from 348.75-360 degrees and from
   0-11.25 degrees. If you wanted to see the summed Northerly winds frequencies
   within the 9 speed bins you could run:

    >>> WR.wind_df.groupby(['direction','speed']).sum().loc['N']


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>frequency</th>
        </tr>
        <tr>
          <th>speed</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>-0.00-1.65</td>
          <td>2.68</td>
        </tr>
        <tr>
          <td>1.65-3.28</td>
          <td>1.85</td>
        </tr>
        <tr>
          <td>3.28-4.92</td>
          <td>0.83</td>
        </tr>
        <tr>
          <td>4.92-6.55</td>
          <td>0.34</td>
        </tr>
        <tr>
          <td>6.55-8.19</td>
          <td>0.16</td>
        </tr>
        <tr>
          <td>8.19-9.83</td>
          <td>0.07</td>
        </tr>
        <tr>
          <td>9.83-11.46</td>
          <td>0.04</td>
        </tr>
        <tr>
          <td>11.46-13.10</td>
          <td>0.01</td>
        </tr>
        <tr>
          <td>13.10-14.73</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



Here is an example of not normalizing the freqeuncy (using raw counts
instead) and using 6 instead of 9 bins for speed. This example shows the
same grouped output for Northerly winds,

    >>> WR.calc_stats(normed=False, bins=6)
    >>> WR.wind_df.groupby(['direction','speed']).sum().loc['N']


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>frequency</th>
        </tr>
        <tr>
          <th>speed</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>-0.00-2.46</td>
          <td>3318.0</td>
        </tr>
        <tr>
          <td>2.46-4.92</td>
          <td>1232.0</td>
        </tr>
        <tr>
          <td>4.92-7.37</td>
          <td>366.0</td>
        </tr>
        <tr>
          <td>7.37-9.83</td>
          <td>121.0</td>
        </tr>
        <tr>
          <td>9.83-12.28</td>
          <td>38.0</td>
        </tr>
        <tr>
          <td>12.28-14.73</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



Lastly, if the wind speed and wind direction columns in the dataframe
assigned to the :obj:`.WindRose` object are not named ‘ws’ and ‘wd’
respectively, instead of renaming them ahead of time or inplace, you may
pass a dictionary that maps their names to the :meth:`.WindRose.calc_stats`
method. For example, lets purposely change the names in our input
dataframe to ‘wind_speed’ and ‘direction’:

    >>> tmp_df = df[['ws','wd']]
    >>> tmp_df.columns = ['wind_speed', 'direction']
    >>> tmp_df.head()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wind_speed</th>
          <th>direction</th>
        </tr>
        <tr>
          <th>date</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2013-05-24 12:30:00</td>
          <td>3.352754</td>
          <td>236.625093</td>
        </tr>
        <tr>
          <td>2013-05-24 13:00:00</td>
          <td>3.882154</td>
          <td>243.971055</td>
        </tr>
        <tr>
          <td>2013-05-24 13:30:00</td>
          <td>4.646089</td>
          <td>238.620934</td>
        </tr>
        <tr>
          <td>2013-05-24 14:00:00</td>
          <td>5.048825</td>
          <td>247.868815</td>
        </tr>
        <tr>
          <td>2013-05-24 14:30:00</td>
          <td>5.302946</td>
          <td>250.930258</td>
        </tr>
      </tbody>
    </table>
    </div>
    <br>



Now reassign this differently named dataframe to a :obj:`.WindRose` instance to demonstrate

    >>> WR.df = tmp_df
    >>> # create renaming dictionary
    >>> names = {
    >>>     'wind_speed':'ws',
    >>>     'direction': 'wd'
    >>> }
    >>> WR.calc_stats(normed=False, bins=6, variable_names=names)
    >>> WR.wind_df.groupby(['direction','speed']).sum().loc['N']




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>frequency</th>
        </tr>
        <tr>
          <th>speed</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>-0.00-2.46</td>
          <td>3318.0</td>
        </tr>
        <tr>
          <td>2.46-4.92</td>
          <td>1232.0</td>
        </tr>
        <tr>
          <td>4.92-7.37</td>
          <td>366.0</td>
        </tr>
        <tr>
          <td>7.37-9.83</td>
          <td>121.0</td>
        </tr>
        <tr>
          <td>9.83-12.28</td>
          <td>38.0</td>
        </tr>
        <tr>
          <td>12.28-14.73</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



The same results were achieved as above, however the column names used
for initial assignment are retained by the :attr:`.WindRose.df` property:

    >>> WR.df.head()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wind_speed</th>
          <th>direction</th>
        </tr>
        <tr>
          <th>date</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2013-05-24 12:30:00</td>
          <td>3.352754</td>
          <td>236.625093</td>
        </tr>
        <tr>
          <td>2013-05-24 13:00:00</td>
          <td>3.882154</td>
          <td>243.971055</td>
        </tr>
        <tr>
          <td>2013-05-24 13:30:00</td>
          <td>4.646089</td>
          <td>238.620934</td>
        </tr>
        <tr>
          <td>2013-05-24 14:00:00</td>
          <td>5.048825</td>
          <td>247.868815</td>
        </tr>
        <tr>
          <td>2013-05-24 14:30:00</td>
          <td>5.302946</td>
          <td>250.930258</td>
        </tr>
      </tbody>
    </table>
    </div>



.. tip:: 
   In this tutorial the full dataset of 30 minute windspeed was used to create
   the statistics (above) and the diagrams (below), in practice it may be
   important to view wind speed / direction during certain time periods like
   day or night, or summer/winter seasons. This is one of the main reasons for
   using :obj:`pandas.DataFrame` objects- they have many tools for time series
   analysis, particularly temporal aggregation and resampling. If you wanted to
   view the wind statistics/plot for this site during day times defined (not
   quite accurately) as 8:00 AM to 8:00 PM it is as simple as this:

    >>> # reassign the wind data but sliced just for day hours we want
    >>> WR.df = df[['ws','wd']].between_time('8:00', '16:00')
    >>> # calculate the wind statistics again
    >>> WR.calc_stats(normed=False, bins=6)
    >>> WR.wind_df.groupby(['direction','speed']).sum().loc['N']


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>frequency</th>
        </tr>
        <tr>
          <th>speed</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>0.03-2.49</td>
          <td>1234.0</td>
        </tr>
        <tr>
          <td>2.49-4.94</td>
          <td>966.0</td>
        </tr>
        <tr>
          <td>4.94-7.39</td>
          <td>308.0</td>
        </tr>
        <tr>
          <td>7.39-9.84</td>
          <td>103.0</td>
        </tr>
        <tr>
          <td>9.84-12.29</td>
          <td>35.0</td>
        </tr>
        <tr>
          <td>12.29-14.73</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



Generate wind rose diagrams
---------------------------

The main purpose of :mod:`rosely` is to simplyfy the generation of
beautiful, interactive wind rose diagrams by using
``plotly.express.bar_polar`` charts and ``pandas``. Once a :obj:`.WindRose`
object has been created and has been assigned a :obj:`pandas.DataFrame`
with wind speed and wind direction you can skip calculating statistics
(falls back on default parameters for statistics) and jump right to
creating a wind rose diagram. For example:

    >>> # create a new WindRose object from our example data with 'ws' and 'wd' columns
    >>> WR = WindRose(df)
    >>> WR.plot()
        Wind speed and direction statistics have not been calculated, Calculating them now using default parameters.


The two lines above saved the plot with default parameters (9 speed
bins) normalized frequency, and default :mod:`rosely` color schemes to the
current working directory named ‘windrose.html’.

To view the default plot without saving,

    >>> # try zooming, clicking on legend, etc.
    >>> WR.plot(output_type='show')


.. raw:: html
    :file: _static/tutorial/fig1.html


Notice that these plots used the default statistics parameters, to use
other options be sure to call :meth:`.WindRose.calc_stats` before
:meth:`.WindRose.plot`. E.g. if we wanted 6 equally spaced bins with
freqeuncies represented as counts as opposed to percentages,

    >>> WR.calc_stats(normed=False, bins=6)
    >>> WR.plot(output_type='show')



.. raw:: html
    :file: _static/tutorial/fig2.html


.. hint:: 
   Assign the path to save the output file if ``output_type`` = ‘save’ using
   the ``out_file`` keyword argument.

The third option that can be assigned to ``output_type`` other than
‘save’ and ‘show’ is ‘return’. When ``output_type='return`` the
:meth:`.WindRose.plot` method returns the plot figure for further
modification or integration in other workflows like adding it into a
group of subplots.

Here is an example use of the ‘return’ option that modifies the wind
rose after it’s creation by :mod:`rosely` by changing the background color
and margins:

.. code:: ipython3

    fig = WR.plot(output_type='return')
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="grey",
    )
    fig.show()



.. raw:: html
    :file: _static/tutorial/fig3.html



Easy wind rose customizations
-----------------------------

:mod:`rosely` makes it simple to experiment with different wind rose
statistcs options but also plot color schemes, this section of the
tutorial highlights some useful options to the :meth:`.WindRose.plot` method
for doing the latter.

First off there are three important keyword arguments to
:meth:`.WindRose.plot` that control the color schemes (``colors``,
``template``, and ``colors_reversed``):

1. ``colors`` is the name of the ``Plotly`` sequential color swatch or a
   list of your own RGB or Hex colors to passfor the stacked histograms
   (the first color in the list will be the most inner color on the
   diagram and them moving outwards towards higher wind speeds).
2. ``template``, this is the name of the ``Plotly`` template that
   defines the background color and other visual appearences. You may
   also pass a custom ``Plotly.py`` template object.
3. ``colors_reversed`` simply allows for the automatic reversal of color
   sequences which may be useful because some color swatches range from
   light to dark while others range from dark to light tones.

A list of all provided colors (hint hover over them to view the Hex or
RGB values themselves):

.. code:: ipython3

    px.colors.sequential.swatches()



.. raw:: html
    :file: _static/tutorial/swatches.html


As for templates they are easily listed by the following:

    >>> import plotly.io as pio
    >>> pio.templates
        Templates configuration
        -----------------------
            Default template: 'plotly'
            Available templates:
                ['ggplot2', 'seaborn', 'plotly', 'plotly_white', 'plotly_dark',
                 'presentation', 'xgridoff', 'none']



Now, let’s try out some of these colors and templates!

    >>> WR.plot(output_type='show', template='seaborn', colors='Plotly3', width=600, height=600)


.. raw:: html
    :file: _static/tutorial/fig4.html


Some color swatches may look better without colors reversed,

    >>> WR.plot(output_type='show', template='xgridoff', colors='turbid', colors_reversed=False)


.. raw:: html
    :file: _static/tutorial/fig5.html


This final example not only shows different color schemes but that you can
pass additional useful keyword arguments that are accepted by
``plotly.express.bar_polar`` such as ``title``, and ``width`` to
:meth:`.WindRose.plot`. It also demonstrates that HTML can be embedded into
the plot title and an example of prefiltering the wind time series to
before calculating wind statistics, in this case to create a wind rose
for the winter months only.

    >>> # reassign the wind data but sliced just for Dec-Mar
    >>> WR.df = df[['ws','wd']].loc[df.index.month.isin([12,1,2,3])]
    >>> # calculate the wind statistics (only necessary because not using default n bins)
    >>> WR.calc_stats(normed=True, bins=6)
    >>> WR.plot(
    >>>     output_type='show', 
    >>>     colors='Greens', 
    >>>     template='plotly_dark', 
    >>>     colors_reversed=False,
    >>>     width=600,
    >>>     height=600,
    >>>     title='Eddy Flux Site on Twitchell Island, CA <br>Wind measured Dec-Mar<br><a href="https://ameriflux.lbl.gov/sites/siteinfo/US-Tw3">Visit site</a>'
    >>> )


.. raw:: html
    :file: _static/tutorial/fig6.html

As we can see the winter wind system is substantially different from the
average long-term wind which may be expected due to seasonal storm
systems or temporally varying larger scale atmospheric circulations.
