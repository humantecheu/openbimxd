# openbimxd - open source tools to interact with IFC files
# Copyright (C) 2024, 2024 the HumanTech project
# Main contributors: Fabian Kaufmann fabian.kaufmann@rptu.de
#           Marius Schellen marius.schellen@rptu.de
#           Mahdi Chamseddine mahdi.chamseddine@dfki.de
#
# This file is part of openbimxd
#
# openbimxd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.
#
# This project uses IfcOpenShell <https://blenderbim.org/>, all credits to
# Dion Moult for his great work

from os import path

from setuptools import Extension, find_packages, setup

# Add Native Extensions
# See https://docs.python.org/3/extending/building.html on details
ext_modules = []
# ext_modules.append(Extension('demo', sources = ['demo.c']))

# Parse requirements.txt
# with open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')
# install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
# dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

# Call the setup.py
setup(
    name="openbimxd",
    version="0.00",
    author="Mahdi Chamseddine, Fabian Kaufmann",
    author_email="mahdi.chamseddine@dfki.de, kaufmann@rptu.de",
    license="MIT",
    # packages=find_packages(exclude=["docs", "libs", "test*", "examples"]),
    packages=find_packages(),
    # Alternative if you prefer to have a package as a sub-folder of src, instead of sub-folder of root.
    # package_dir={'': 'src'},
    # packages=find_packages(where='src'),
    # install_requires=install_requires,
    # dependency_links=dependency_links,
    ext_modules=ext_modules,
    # entry_points={
    #     "console_scripts": [
    #         "datapipefs = datapipefs.cli.__main__:main",
    #     ]
    # },
)
