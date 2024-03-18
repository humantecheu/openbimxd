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

"""
Update an IFC object. Updates the location, material or properties.

CLASSES
    UpdateIfcObject
        A class to update IFC objects. The updated objects are saved as a new file.

FUNCTIONS
    __init__(self, model, ifc_object) -> None
        Initializes an UpdateIfcObject object
    update_location(self, origin: np.ndarray, angle: float) -> None
        Update the location and angle of an the IfcLocalPlacement.
    update_material(self, ifc_material) -> None
        Update the IfcMaterial.
    update_property(self, pset_name: str, pset_dict: dict) -> None
        Updates the property set of an object. Either adds a new property
        set or updates the existing one, if one with same name as existing
        is given.
"""
