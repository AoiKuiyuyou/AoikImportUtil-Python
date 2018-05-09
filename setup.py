# coding: utf-8
from __future__ import absolute_import

from setuptools import find_packages
from setuptools import setup


setup(
    name='AoikImportUtil',

    version='0.3.0',

    description="""Import module by code, name, path, and import object.""",

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikImportUtil-Python>`_""",

    url='https://github.com/AoiKuiyuyou/AoikImportUtil-Python',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    python_requires='>=2.5',

    keywords='import',

    package_dir={'': 'src'},

    packages=find_packages('src'),
)
