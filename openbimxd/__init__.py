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

"""Openbimxd is a module that allows you to setup a basic IFC file structure, create 
IFCs from reconstructed semantics and geometry, to filter IFC objects, to inherit
labels for point clouds from IFC objects and to update IFC objects

MODULES
    ifcfile
        Creates an IFC file with a specified schema and structure. 
    elements
        Create IFC objects from bounding boxes. By now, IfcWall, IfcDoor and IfcColumn 
        are implemented
    ifcmaterial
        Create a set of IFC materials to be assigned to objects
    ifctolabel
        Converts the geometry representatio of IFC objects into bounding boxes and 
        assigns the IfcClass to all points inside the respective bounding box. 
    ifcupdate
        Update attributes, properties and geometry of IFC objects. Preserves the GUID
        of the initial object
"""
