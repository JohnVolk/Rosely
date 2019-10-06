"""
A small package for efficiently generating customizable and interactive windrose diagrams. Once wind speed and direction is loaded into a ``pandas.DataFrame`` the package can create wind speed and direction statistics which are used to create windrose diagrams via ``Plotly``'s polar bar chart function.
"""

__name__ = 'rosely'
__author__ = 'John Volk'
__version__ = '0.0.1'


from rosely.windrose import WindRose
