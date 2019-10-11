import io, re
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("rosely/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

requires = [
    'numpy',
    'pandas>=0.24',
    'plotly'
]

tests_require = ['pytest']

classifiers = [
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.7',
    'Environment :: Console',
    'Development Status :: 4 - Beta',
    'Topic :: Scientific/Engineering',
    'Intended Audience :: Science/Research'
]

setup(
    name='Rosely',
    description='Interactive wind rose diagrams simplified',
    long_description=readme,
    author='John Volk',
    author_email='john.volk@dri.edu',
    license='BSD3',
    python_requires='>=3.7',
    version=version,
    url='https://github.com/JohnVolk/Rosely',
    platforms=['Windows','Linux','Mac OS X'],
    classifiers=classifiers,
    packages=['rosely'],
    install_requires=requires,
    tests_require=tests_require,
    include_package_data=True,
)
