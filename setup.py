#!/usr/bin/env python
#
# Copyright 2021-2022 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The setup script."""

import os
import re

from setuptools import find_packages, setup

VERSION = "2.1.3"

with open("README.md") as readme_file:
    readme = readme_file.read()


def is_ubuntu() -> bool:
    """Verify if running on Ubuntu."""
    try:
        with open("/etc/os-release") as release_file:
            os_release = release_file.read()
        if re.search(r"^ID(?:_LIKE)?=.*\bubuntu\b.*$", os_release, re.MULTILINE):
            return True
    except FileNotFoundError:
        return False
    else:
        return False


def is_rtd() -> bool:
    """Verify if running on ReadTheDocs."""
    return "READTHEDOCS" in os.environ


install_requires = [
    # see https://github.com/mkorpela/overrides/issues/121
    "overrides!=7.6.0",
    "PyYAML",
    "pydantic>=2.0.0",
    "pyxdg",
    "requests>=2.32,<3.0",
    "requests-unixsocket2>=0.4.0",
]

dev_requires = [
    "autoflake",
    "twine",
]

docs_require = [
    "sphinx",
    "sphinx-autodoc-typehints",
    "sphinx-lint",
    "sphinx-pydantic",
    "sphinx-rtd-theme",
    "sphinxcontrib-details-directive==0.1.0",
]

types_requires = [
    "mypy[reports]>=1.4.1,<2.0",
    "types-colorama",
    "types-docutils",
    "types-jsonschema",
    "types-Pillow",
    "types-Pygments",
    "types-pytz",
    "types-PyYAML",
    "types-requests",
    "types-setuptools",
]

test_requires = [
    "black",
    "codespell",
    "coverage",
    "hypothesis",
    "jsonschema",
    "pydocstyle",
    "pyright==1.1.385",
    "pytest",
    "pytest-check",
    "pytest-cov",
    "pytest-mock",
    "pytest-subprocess",
    "requests-mock",
    "tox",
    "yamllint==1.35.1",
]

extras_requires = {
    "dev": dev_requires + docs_require + test_requires + types_requires,
    "docs": docs_require,
    "test": test_requires + types_requires,
    "types": types_requires,
    # Generic "apt" extra for handling any apt-based platforms (e.g. Debian, Ubuntu)
    "apt": ["python-apt>=2.0.0"],
}


setup(
    name="craft-parts",
    version=VERSION,
    description="Craft parts tooling",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Canonical Ltd.",
    author_email="snapcraft@lists.snapcraft.io",
    url="https://github.com/canonical/craft-parts",
    license="GNU General Public License v3",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "craftctl=craft_parts.ctl:main",
        ],
    },
    install_requires=install_requires,
    extras_require=extras_requires,
    packages=[
        *find_packages(include=["craft_parts", "craft_parts.*"]),
        "craft_parts_docs",
    ],
    # todo: can we make the docs optional?
    package_dir={"craft_parts_docs": "docs/common"},
    package_data={
        "craft_parts": ["py.typed"],
        "craft_parts_docs": ["**"],
    },
    include_package_data=True,
    zip_safe=False,
)
