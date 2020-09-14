import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="configutils",
    version="0.0.1",
    author="Patrick Cauthorn",
    author_email="patrick.cauthorn@gmail.com",
    description="Tools to dynamically build config files",
    license="BSD",
    url="https://github.com/pcauthorn/python-configutils",
    packages=['configutils', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
