#!/usr/bin/env python3

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

reqs = ["flashtext==2.7","Unidecode==1.1.1",
        "json5==0.8.5","jsonschema==3.0.2",
        "intervaltree==3.0.2", "pandas",
        "bioc==1.3.5", "psycopg2-binary","scp",
        "paramiko", "dataclasses","smart_open","requests","Deprecated==1.2.11"]


setup(name='pymedextcore',
      version='0.2',
      description='pymedext core toolkit for clinical NLP',
      packages=['pymedextcore'],
      install_requires=reqs,
      author='Antoine Neuraz, William Digan, Ivan Lerner, Alice Rogier, David Baudoin, Anita Burgun, Nicolas Garcelon, Bastien Rance ',
      author_email='william.digan@aphp.fr',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False,
      entry_points={
            'console_scripts': [
                'pymedext=pymedextcore.pymedext_cmdline:main'
            ]
        },

)
