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
# openbimxd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openbimxd.  If not, see <http://www.gnu.org/licenses/>.
#
# This project uses IfcOpenShell <https://blenderbim.org/>, all credits to
# Dion Moult for his great work

"""
Create IFC objects based on bouding box bbox objects from pystruct3d. Pystruct3d offers
basic geometric reconstruction algorithms to build your own scan to BIM pipeline. Refer to 
https://github.com/humantecheu/pystruct3d for more information. 

To create the IFC objects, you need an IFC file. Use ifcfile / IfcModelBuilder class to 
create it. 

MODULES / ClASSES
    ifcolumn / IfcColumn
        Create IfcColumn objects with round or square profile
    ifcdoor / IfcDoor
        Create IfcDoor objects with basic box-style geometry
    ifcwall / IfcWall
        Create IfcWall objects with box-style geometry
"""
