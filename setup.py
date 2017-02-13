# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name='word2vec_wikification_py'
version='0.15'
description='A package to run wikification'
author='Kensuke Mitsuzawa'
author_email='kensuke.mit@gmail.com'
url='https://github.com/Kensuke-Mitsuzawa/word2vec_wikification_py'
license_name='MIT'

install_requires = [
    'gensim',
    'mysqlclient',
    'pymysql',
    'typing'
]


dependency_links = [
]

short_description = ''

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Natural Language :: Japanese",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.5"
        ]

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email=author_email,
    url=url,
    license=license_name,
    packages=find_packages(),
    classifiers=classifiers,
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
