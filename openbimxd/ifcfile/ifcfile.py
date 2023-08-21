import ifcopenshell
from ifcopenshell.api import run


class IfcTemplate:
    def __init__(self, filename, project_name) -> None:
        self.filename = filename
        self.project_name = project_name

        self.model = ifcopenshell.file()

        self.project = run(
            "root.create_entity",
            self.model,
            ifc_class="IfcProject",
            name="self.project_name",
        )

        # Specify units: millimeters, square meters, and cubic meters
        run("unit.assign_unit", self.ifcfile)

        # Let's create a modeling geometry context, so we can store 3D geometry
        self.context = run("context.add_context", self.model, context_type="Model")

        # https://blenderbim.org/docs-python/ifcopenshell-python/code_examples.html
