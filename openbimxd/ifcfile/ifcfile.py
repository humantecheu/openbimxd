import ifcopenshell
from ifcopenshell.api import run

import time
import tempfile

# see: https://blenderbim.org/docs-python/ifcopenshell-python/geometry_creation.html


class IfcTemplate:
    def __init__(self, filename, project_name) -> None:
        self.filename = filename
        self.project_name = project_name

        self.ifcfile = ifcopenshell.file()

        project = run(
            "root.create_entity",
            self.ifcfile,
            ifc_class="IfcProject",
            name="self.project_name",
        )
