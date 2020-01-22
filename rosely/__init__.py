"""
A small package for efficiently generating customizable and interactive wind rose diagrams. Once wind speed and direction is loaded into a ``pandas.DataFrame`` the package can create wind speed and direction statistics which are used to create windrose diagrams via ``Plotly``'s polar bar chart function with multiple tools for easy plot customization.
"""

__name__ = 'rosely'
__author__ = 'John Volk'
__version__ = '0.0.2.post1'


from rosely.windrose import WindRose
