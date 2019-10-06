# -*- coding: utf-8 -*-
"""
Tools for creating interactive windrose diagrams and summary statistics using pandas and plotly.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio

class WindRose(object):

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
        needed to run :meth:`WindRose.windrose`.
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
             template='plotly_dark', **kwargs):

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
            colors = px.colors.sequential.Plasma[::-1]

        elif isinstance(colors, str):
            colors = getattr(px.colors.sequential, colors)[::-1]

        if self.n_bins > len(colors):
            print(
                'Warning: number of bins exceed number of colors, some '
                'colors may repeat.'
            )

        fig = px.bar_polar(
            self.wind_df, r="frequency", theta="direction", color="speed",
            template=template, color_discrete_sequence=colors, **kwargs
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
            plot(fig, filename=str(out_file))
            self.out_file = out_file
        elif output_type == 'show':
            fig.show()
        elif output_type == 'return':
            return fig

