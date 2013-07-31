# -*- coding: utf-8 -*-
"""
SOG command processor

:Author: Doug Latornell <djl@douglatornell.ca>
:License: Apache License, Version 2.0

Copyright 2010-2013 Doug Latornell and The University of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import (
    setup,
    find_packages
)

python_classifiers = [
    'Programming Language :: Python :: {0}'.format(py_version)
    for py_version in ['2', '2.7', '3', '3.3']]
other_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: Implementation :: CPython',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
]

with open('README.rst', 'rt') as file_obj:
    detailed_description = file_obj.read()
with open('SOGcommand/CHANGELOG', 'rt') as file_obj:
    detailed_description += '\n\n' + file_obj.read()
install_requires = [
    # see requirements/production.txt for versions most recently used
    # in development
    'colander',
    'PyYAML',
    'six',
]

setup(
    name='SOGcommand',
    version='1.2.1',
    description='Command processor for SOG.',
    long_description=detailed_description,
    author='Doug Latornell',
    author_email='djl@douglatornell.ca',
    url='http://bjossa.eos.ubc.ca:9000/SOG/',
    license="Apache License, Version 2.0",
    classifiers=python_classifiers + other_classifiers,
    install_requires=install_requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['SOG = SOGcommand.command_processor:run']},
)
