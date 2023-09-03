import ifcopenshell
from ifcopenshell.api import run


class IfcModelBuilder:
    def __init__(
        self,
        filename,
        project_name="awesome project",
        site_name="nice site",
        building_name="building A",
        storey_name="Level 0",
        schema="IFC4",
    ) -> None:
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
        self.model.write(self.filename)
