# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name='wiki_node_disambiguation'
version='0.1'
description=''
author='Kensuke Mitsuzawa'
author_email='kensuke.mit@gmail.com'
url=''
license_name=''

install_requires = [
    'gensim',
    'JapaneseTokenizer',
    'mysqlclient',
    'pymysql'
]


dependency_links = [
]


setup(
    name=name,
    version=version,
    description=description,
    author=author,
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email=author_email,
    url=url,
    license=license_name,
    packages=find_packages(),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)