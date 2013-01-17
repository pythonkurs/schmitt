from setuptools import setup, find_packages
import sys, os

version = '0.1dev'

setup(name='schmitt',
      version=version,
      description="SciLifeLab python course 2013",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='scilifelab bioinformatics',
      author='Thomas Schmitt',
      author_email='Thomas.Schmitt@scilifelab.se',
      url='http://github.com/pythonkurs/schmitt',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
