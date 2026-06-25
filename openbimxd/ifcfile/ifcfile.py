# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Build IFC models with a project/site/building/storey hierarchy."""

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.root
import ifcopenshell.api.unit
from ifcopenshell.util.schema import IFC_SCHEMA


class IfcModelBuilder:
    """Build an IFC model with project/site/building/storey hierarchy."""

    def __init__(
        self,
        filename: str,
        project_name: str = "awesome project",
        site_name: str = "nice site",
        building_name: str = "building A",
        storey_name: str = "Level 0",
        schema: IFC_SCHEMA = "IFC4",
    ) -> None:
        """Create an IFC model with a full spatial hierarchy.

        Args:
            filename: Path the IFC file will be written to.
            project_name: Name of the IfcProject entity.
            site_name: Name of the IfcSite entity.
            building_name: Name of the IfcBuilding entity.
            storey_name: Name of the IfcBuildingStorey entity.
            schema: IFC schema version, typically ``"IFC2X3"`` or ``"IFC4"``.
        """
        self.filename = filename
        self.project_name = project_name
        self.site_name = site_name
        self.building_name = building_name
        self.storey_name = storey_name
        self.schema = schema

        # self.model = ifcopenshell.file(schema=self.schema)
        self.model = ifcopenshell.api.project.create_file(version=self.schema)
        self.project = ifcopenshell.api.root.create_entity(
            self.model,
            ifc_class="IfcProject",
            name=self.project_name,
        )

        # Specify units: millimeters, square meters, and cubic meters
        ifcopenshell.api.unit.assign_unit(self.model)

        # Let's create a modeling geometry context, so we can store 3D geometry
        self.context = ifcopenshell.api.context.add_context(
            self.model,
            context_type="Model",
        )

        # In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
        self.body = ifcopenshell.api.context.add_context(
            self.model,
            context_type="Model",
            context_identifier="Body",
            target_view="MODEL_VIEW",
            parent=self.context,
        )

        # Create a site, building, and storey. Many hierarchies are possible.
        self.site = ifcopenshell.api.root.create_entity(
            self.model,
            ifc_class="IfcSite",
            name=self.site_name,
        )
        self.building = ifcopenshell.api.root.create_entity(
            self.model,
            ifc_class="IfcBuilding",
            name=self.building_name,
        )
        self.storey = ifcopenshell.api.root.create_entity(
            self.model,
            ifc_class="IfcBuildingStorey",
            name=self.storey_name,
        )

        # Since the site is our top level location, assign it to the project
        # Then place our building on the site, and our storey in the building
        ifcopenshell.api.aggregate.assign_object(
            self.model,
            relating_object=self.project,
            products=[self.site],
        )
        ifcopenshell.api.aggregate.assign_object(
            self.model,
            relating_object=self.site,
            products=[self.building],
        )
        ifcopenshell.api.aggregate.assign_object(
            self.model,
            relating_object=self.building,
            products=[self.storey],
        )

    def write(self) -> None:
        """Write the IFC model to file."""
        self.model.write(self.filename)
