#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2020 by Jussi Vatjus-Anttila
:license: MIT, see LICENSE for more details.
"""
from setuptools import setup


setup(
    name="robot-opentmi",
    use_scm_version=True,
    description="robot-framework plugin for publish results to opentmi",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Jussi Vatjus-Anttila",
    author_email="jussiva@gmail.com",
    url="https://github.com/opentmi/robot-opentmi",
    packages=["robot_opentmi"],
    setup_requires=["setuptools_scm"],
    install_requires=["robotframework", "opentmi-client>=0.6.2", "joblib"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install .[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        'dev': ['coverage', 'coveralls', 'mock', 'pylint', 'nose', 'pyinstaller']
    },
    license="MIT",
    keywords="robot-framework opentmi report",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Framework :: Robot Framework :: Library",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
