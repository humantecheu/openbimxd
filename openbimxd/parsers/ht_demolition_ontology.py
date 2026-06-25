# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Extract IFC opening geometry parameters and serialize them to JSON."""

import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.placement
import numpy as np

from openbimxd.geometry import bbox_from_ifc_verts


class IfcConvertOpening:
    """Extract opening geometry parameters from an IFC model."""

    def __init__(self, ifc_file) -> None:
        """Open an IFC file and locate the first wall for opening extraction.

        Args:
            ifc_file: Path to the IFC file.
        """
        self.ifc_file = ifc_file
        self.ifc = ifcopenshell.open(ifc_file)
        self.ifc_walls = self.ifc.by_type("IfcWall")
        self.ifc_wall = self.ifc_walls[1]
        self.data_dict = {
            "IFC file": self.ifc_file,
            "Wall name": self.ifc_wall.Name,
            "Wall ID": self.ifc_wall.GlobalId,
        }

    def get_parameters(self):
        """Extract position and dimension parameters for each opening in the wall.

        Returns:
            IfcConvertOpening: ``self``, for method chaining.
        """
        wall_placement = ifcopenshell.util.placement.get_local_placement(
            self.ifc_wall.ObjectPlacement
        )[:, 3][:3]
        child_objects = ifcopenshell.util.element.get_decomposition(self.ifc_wall)

        # get the geometry of the opening
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        for child in child_objects:
            if child.is_a("IfcOpeningElement"):
                child_placement = ifcopenshell.util.placement.get_local_placement(
                    child.ObjectPlacement
                )[:, 3][:3]
                shape = ifcopenshell.geom.create_shape(settings, child)
                verts = np.asarray(shape.geometry.verts)  # ty: ignore[unresolved-attribute]
                bx = bbox_from_ifc_verts(verts)

                orig_distances = child_placement - wall_placement

                self.data_dict.update({
                    "Opening": {
                        "ID": child.GlobalId,
                        "X distance": orig_distances[0],
                        "Y distance": orig_distances[1],
                        "Z distance": orig_distances[2],
                        "Yaw orientation": 0,
                        "Length": bx.length(),
                        "Width": bx.width(),
                        "Height": bx.height(),
                    }
                })
        print(self.data_dict)
        return self

    def to_json(self):
        """Serialize the extracted parameters to a JSON file next to the IFC file.

        Returns:
            IfcConvertOpening: ``self``, for method chaining.
        """
        json_data = json.dumps(self.data_dict)

        with Path(f"{self.ifc_file[:-4]}.json").open("w") as json_file:
            json_file.write(json_data)

        return self


def main():
    """Run parameter extraction on the demo IFC file."""
    IfcConvertOpening("AC20-FZK-Haus.ifc").get_parameters().to_json()


if __name__ == "__main__":
    main()
