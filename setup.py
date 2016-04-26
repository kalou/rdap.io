import sys
import os
import re

from setuptools import setup, find_packages

requires = [
    'flask',
    'requests',
]

setup(
    name="rdapio",
    version='0.0.1',
    packages=find_packages(),
    description="rdap.io website",
    install_requires=requires,
)
