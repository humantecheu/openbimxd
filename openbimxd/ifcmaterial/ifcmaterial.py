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


import ifcopenshell


class IfcMaterials:
    """
    A class to create and represent IFC materials.

    Attributes:
        ifc_model : IfcModelBuilder object
    """

    def __init__(self, ifc_model) -> None:
        self.concrete = ifcopenshell.api.run(
            "material.add_material", ifc_model, name="CON01", category="concrete"
        )
        self.clt = ifcopenshell.api.run(
            "material.add_material", ifc_model, name="CLT", category="wood"
        )
