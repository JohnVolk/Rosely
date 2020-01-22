# -*- coding: utf-8 -*-
"""
Tools for creating interactive wind rose diagrams and summary statistics using plotly and pandas.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio

class WindRose(object):
    """
    Manage data for calculating wind statistics and provide simple interface
    for creating customizable wind rose diagrams.

    Attributes:
        df (:obj:`pandas.DataFrame`): arbitrary :obj:`pandas.DataFrame` that
            is assigned to a :obj:`WindRose` object that must contain wind speed
            and direction columns before using other :obj:`WindRose` methods.
        theta_labels (list): 16 point compass labels for wind rose diagrams.
        theta_angles (:obj:`numpy.ndarray`): array of 11.25 degree intervals for
            16 point compass.
        wind_df (:obj:`pandas.DataFrame`): calculated wind statistics produced
            by :meth:`WindRose.calc_stats` and used by :meth:`WindRose.plot`.
    """

    # 16 point compass for now
    theta_labels = [
        'N','NNE','NNE','NE','NE','ENE','ENE','E','E','ESE','ESE','SE','SE',
        'SSE','SSE','S','S','SSW','SSW','SW','SW','WSW','WSW','W','W','WNW',
        'WNW','NW','NW','NNW','NNW','N'
    ]
    theta_angles = np.arange(0, 360.1, 11.25)

    def __init__(self, df=None):
        if df is not None and not isinstance(df, pd.DataFrame):
            raise TypeError("Must assign a pandas.DataFrame object")
        self._df = df
        self._plot_ready = False
        self.wind_df = None

    @property
    def df(self):
        """
        :obj:`pandas.DataFrame` containing input time series wind data
        needed to run :meth:`WindRose.plot`.
        """
        if isinstance(self._df, pd.DataFrame):
            return self._df

    @df.setter
    def df(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Must assign a pandas.DataFrame object")
        self._df = df

    def calc_stats(self, normed=True, bins=9, variable_names=None):
        """
        Calculate wind speed and direction bins needed for generating wind rose
        diagrams. 

        After running :meth:`WindRose.calc_stats` with different options a new
        instance attribute :attr:`WindRose.wind_df` is generated that contains
        the binned wind speed statistics. This attribute is in the form of a 
        :obj:`pandas.DataFrame` and can be used to create a histogram or saved
        to disk.

        Keyword Arguments:
            normed (bool): default True. If True compute wind speed/direction
                frequency bins that are normalized to sum to 100. If False
                frequency bins are counts of occurences of wind speed/direction.
            bins (int): default 9. Number of wind speed and direction bins to
                calculate. 9 is used because most :mod:`plotly` color sequences
                are lenght 9 or 10 which are later used by :meth:`WindRose.plot`
            variable_names (None or dict): default None. If none the wind speed
                and wind direction columns in :attr:`WindRose.df` should be 
                named 'ws' and 'wd' respectively. Otherwise a dictionary that
                maps the respective columns to 'ws' and 'wd' should be provided.
                
        Returns:
            None

        Example:

            Assuming you have a :obj:`pandas.DataFrame` loaded that has wind
            speed and direction columns titled 'wind_speed' and 'wind_direction'
            and the dataframe is named ``df``:

            >>> from rosely import WindRose
            >>> WR = WindRose(df) 
            >>> names = {'wind_speed':'ws', 'wind_direction':'wd'}
            >>> WR.calc_stats(normed=False, bins=8, variable_names=names)

            Now ``WR.wind_df`` should have the appropirate statistics and the
            :meth:`WindRose.plot` will use these statistics for the polar 
            stacked histogram (wind rose).

        """
        wind = self._df.copy()
        if not isinstance(wind, pd.DataFrame):
            print(
                'Must assign a pandas.DataFrame to the WindRose object with '
                'wind speed and direction before running calculations.'
            )
            return

        if variable_names:
            wind.rename(columns=variable_names, inplace=True)

        if not {'ws', 'wd'}.issubset(wind.columns):
            raise KeyError('ERROR: missing "ws" and "wd" columns, aborting.')

        spd_bins = pd.cut(wind.ws, bins=bins).dropna()
        spd_bins.name = 'spd_bins'
        wind = wind.join(spd_bins)

        dir_bins = pd.cut(wind.wd, bins=WindRose.theta_angles).dropna()
        dir_bins.name = 'dir_bins'
        wind = wind.join(dir_bins)

        def rename_bins(x):
            return '{:.2f}-{:.2f}'.format(x.left,x.right)

        wind.spd_bins = wind.spd_bins.apply(rename_bins)
        wind = wind.groupby(['dir_bins','spd_bins']).count().dropna()
        wind['direction'] = wind.index.get_level_values('dir_bins')
        wind['speed'] = wind.index.get_level_values('spd_bins')
        wind = wind[
            ['direction','speed', 'ws']
        ].droplevel(0).reset_index().drop('spd_bins',axis=1)
        wind.rename(columns={'ws':'frequency'}, inplace=True)
        # rename to compass directions
        tmp = wind.groupby('direction').count()
        tmp['labels'] = WindRose.theta_labels
        mapping_dict = tmp.labels.to_dict()
        wind.direction = wind.direction.map(mapping_dict)
        if normed:
            wind.frequency /= wind.frequency.sum()
            wind.frequency *= 100
            wind.frequency = wind.frequency.round(2)

        self.n_bins = bins
        self.wind_df = wind
        self._plot_ready = True

    def plot(self, output_type='save', out_file=None, colors='Plasma',
             template='plotly_dark', colors_reversed=True, **kwargs):
        """
        Create interactive wind rose diagrams with easily customizable options
        using Plotly's polar bar chart.

        Keyword Arguments:
            output_type (str): default 'save'. If 'save' save graph to 
                ``out_file``. Other options: 'show' will show in a new tab in
                web browser or within a Jupyter Notebook, and 'return' will
                return the plotly figure for further manual
                customization/modification or use in custom workflows like
                saving as a subplot with other plot figures.
            out_file (None or str): default None. If ``output_type='save'`` then
                save to specified path, if None save to current working 
                directory as "windrose.html".
            colors (str): default 'Plasma'. Name of Plotly color swatch or 
                sequence to use for coloring bins from center outward on
                wind rose. See :ref:`Tutorial` for examples and all options. Can
                also pass a list of hex or rgb colors of your own.
            template (str): default 'plotly_dark'. Name of Plotly template for 
                background theme/colors on wind rose.
            colors_reversed (bool): True. If True reverse the colors in 
                ``colors``. The first color in the sequence will be used for 
                the lightest wind speed bin.

            **kwargs: other keyword arguments are passed to the 
                ``plotly.express.bar_polar`` plot function, e.g. title or width.

        Returns (None or :obj:`plotly.graph_objects.Figure`)

        Example:

            Assuming a :obj:`pandas.DataFrame` object called "df" has been
            loaded and contains columns 'ws' and 'wd' with wind speed and
            direction,

            >>> from rosely import WindRose
            >>> WR = WindRose(df) # df already loaded pandas dataframe
            >>> # if you skip running WR.calc_stats the defaults will be used
            >>> WR.plot(output_type='show', colors='Greens', 
            >>>     colors_reversed=False)

            This will produced a normalized frequency wind rose (frequency 0-100
            percent) with 9 bins. To specify the to use count frequency or a
            different number of bins use the :meth:`WindRose.calc_stats` method
            before running :meth:`WindRose.plot`. 

        Tip:
            To see a list of all provided color sequences provided by Plotly,

            >>> import plotly.express as px
            >>> px.colors.sequential.swatches()

            All of the listed color schemes can be passed to the ``colors`` 
            arugment of :meth:`WindRose.plot`.

        """

        if template not in pio.templates.keys():
            print('ERROR: invalid plotly template use one of:\n{}'
                 .format(', '.join(pio.templates.keys())))
            return

        if not self._plot_ready:
            print(
                'Wind speed and direction statistics have not been calculated, '
                'Calculating them now using default parameters.'
            )
            self.calc_stats()

        if not hasattr(px.colors.sequential, colors) and not \
                isinstance(colors, list):
            print(
                'ERROR: {} is not a valid plotly color sequence, using default.'
            )
            colors = px.colors.sequential.Plasma

        elif isinstance(colors, str):
            colors = getattr(px.colors.sequential, colors)

        if self.n_bins > len(colors):
            print(
                'Warning: number of bins exceed number of colors, some '
                'colors may repeat.'
            )

        if colors_reversed:
            colors = colors[::-1]

        fig = px.bar_polar(
            self.wind_df, r="frequency", theta="direction", color="speed",
            template=template, color_discrete_sequence=colors, 
            category_orders={'direction': [
                'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 
                'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            }, **kwargs
        )

        # handle file save for accessing from instance variable
        if out_file is None and output_type == 'save':
            out_file = Path.cwd()/'windrose.html'
            out_dir = out_file.parent
            if not out_dir.is_dir():
                out_dir.mkdir(parents=True, exist_ok=True)
        # if out_file is to a non-existent directory create parents
        elif out_file is not None and output_type == 'save':
            out_dir = Path(out_file).parent
            if not out_dir.is_dir():
                out_dir.mkdir(parents=True, exist_ok=True)

        if output_type == 'save':
            pio.write_html(fig, str(out_file), auto_open=False)
            self.out_file = out_file
        elif output_type == 'show':
            fig.show()
        elif output_type == 'return':
            return fig

