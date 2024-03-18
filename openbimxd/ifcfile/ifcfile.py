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
from ifcopenshell.api import run


class IfcModelBuilder:
    """
    A class to create an IFC model with a basic hierarchy.

    Attributes:
        filename (str): Path to write the file to
        project_name (str): optional, name of the IfcProject
        site_name (str): optional, name of the IfcSite
        building_name (str): optional, name of the IfcBuilding
        storey_name (str): optional, name of the IfcBuildingStorey
        schema (str): optional, identifies the IFC schema. Typically IFC2X3 or IFC4

    """

    def __init__(
        self,
        filename,
        project_name="awesome project",
        site_name="nice site",
        building_name="building A",
        storey_name="Level 0",
        schema="IFC4",
    ) -> None:
        """
        Constructs an IfcModelBuilder object

        Attributes:
            filename (str): Path to write the file to
            project_name (str): optional, name of the IfcProject
            site_name (str): optional, name of the IfcSite
            building_name (str): optional, name of the IfcBuilding
            storey_name (str): optional, name of the IfcBuildingStorey
            schema (str): optional, identifies the IFC schema. Typically IFC2X3 or IFC4

        """

        self.filename = filename
        self.project_name = project_name
        self.site_name = site_name
        self.building_name = building_name
        self.storey_name = storey_name
        self.schema = schema

        self.model = ifcopenshell.file(schema=self.schema)

        self.project = run(
            "root.create_entity",
            self.model,
            ifc_class="IfcProject",
            name="self.project_name",
        )

        # Specify units: millimeters, square meters, and cubic meters
        run("unit.assign_unit", self.model)

        # Let's create a modeling geometry context, so we can store 3D geometry
        self.context = run("context.add_context", self.model, context_type="Model")

        # In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
        self.body = run(
            "context.add_context",
            self.model,
            context_type="self.model",
            context_identifier="Body",
            target_view="MODEL_VIEW",
            parent=self.context,
        )

        # Create a site, building, and storey. Many hierarchies are possible.
        self.site = run(
            "root.create_entity", self.model, ifc_class="IfcSite", name=self.site_name
        )
        self.building = run(
            "root.create_entity",
            self.model,
            ifc_class="IfcBuilding",
            name=self.building_name,
        )
        self.storey = run(
            "root.create_entity",
            self.model,
            ifc_class="IfcBuildingStorey",
            name=self.storey_name,
        )

        # Since the site is our top level location, assign it to the project
        # Then place our building on the site, and our storey in the building
        run(
            "aggregate.assign_object",
            self.model,
            relating_object=self.project,
            product=self.site,
        )
        run(
            "aggregate.assign_object",
            self.model,
            relating_object=self.site,
            product=self.building,
        )
        run(
            "aggregate.assign_object",
            self.model,
            relating_object=self.building,
            product=self.storey,
        )

    def write(self):
        """Write the IFC model to file."""
        self.model.write(self.filename)
