# -*- coding: utf-8 -*-
import sys
from setuptools import (
    setup,
    find_packages
    )
from SOGcommand.__version__ import (
    version,
    release,
    dev_status,
    )

python_classifiers = [
    'Programming Language :: Python :: {0}'.format(py_version)
    for py_version in ['2', '2.6', '2.7']]
other_classifiers = [
    'Development Status :: ' + dev_status,
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: Implementation :: CPython',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    ]

with open('SOGcommand/README', 'rt') as file_obj:
    detailed_description = file_obj.read()
with open('SOGcommand/CHANGELOG', 'rt') as file_obj:
    detailed_description += '\n\n' + file_obj.read()
with open('SOGcommand/requirements.txt', 'rt') as file_obj:
    requirements = file_obj.read()
install_requires = [line for line in requirements.split('\n')
                    if line and not line.startswith('#')]
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.extend([
        'argparse',
        'unittest2',
    ])

setup(
    name='SOGcommand',
    version=version + release,
    description='Command processor for SOG.',
    long_description=detailed_description,
    author='Doug Latornell',
    author_email='djl@douglatornell.ca',
    url='http://bjossa.eos.ubc.ca:9000/SOG/',
    license="New BSD License",
    classifiers=python_classifiers + other_classifiers,
    install_requires=install_requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['SOG = SOGcommand.command_processor:run']},
)
