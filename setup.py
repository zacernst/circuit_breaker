# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

setup(
    name='circuit_breaker',
    version='0.1.1',
    description='Timeout decorator for functions with backup',
    long_description=('Allows you to decorate a function, provide '
                      'a timeout and a backup function if it is '
                      'not complete within the timeout specified.'),
    author='Zachary Ernst',
    author_email='zac.ernst@gmail.com',
    url='https://github.com/zacernst/circuit_breaker',
    include_package_data=True,
    package_data={},
    scripts=[],
    packages=['circuit_breaker'],
    package_dir={'circuit_breaker': 'circuit_breaker'},
    install_requires=[]
)

# os.system("cd docs && make html")
# os.system("cp -rfv ./docs/_build/html/* ./htmldocs/")
# os.system("behave tests")
