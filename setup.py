import os
import platform
import sys

from setuptools import find_packages, setup

about_path = os.path.join(os.path.dirname(__file__), "revscoring/about.py")
exec(compile(open(about_path).read(), about_path, "exec"))


if sys.version_info <= (3, 0):
    print("Revscoring needs Python 3 to run properly. Your version is " +
          platform.python_version())
    sys.exit(1)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]


setup(
    python_requires=">=3",
    name=__name__,  # noqa
    version=__version__,  # noqa
    author=__author__,  # noqa
    author_email=__author_email__,  # noqa
    description=__description__,  # noqa
    url=__url__,  # noqa
    license=__license__,  # noqa
    entry_points={
        'console_scripts': [
            'revscoring = revscoring.revscoring:main',
        ],
    },
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=requirements("requirements.txt"),
    include_package_data=True,
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
