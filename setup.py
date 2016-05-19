import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name="revscoring",
    version="1.2.6",  # change in revscoring/__init__.py
    author="Aaron Halfaker",
    author_email="ahalfaker@wikimedia.org",
    description=("A set of utilities for generating quality scores for " + \
                 "MediaWiki revisions"),
    license="MIT",
    entry_points={
        'console_scripts': [
            'revscoring = revscoring.revscoring:main',
        ],
    },
    url="https://github.com/halfak/Revision-Scores",
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=requirements("requirements.txt"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
