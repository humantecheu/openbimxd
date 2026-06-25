# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Update an IFC object's placement, material, or property sets."""

import ifcopenshell
import numpy as np
from ifcopenshell import entity_instance
from ifcopenshell.api import run
from ifcopenshell.util import element, placement


class UpdateIfcObject:
    """Update an IFC object's placement, material, or property sets."""

    def __init__(
        self,
        model: ifcopenshell.file,
        ifc_object: entity_instance,
    ) -> None:
        """Initialise with an open IFC model and the object to update.

        Args:
            model: Open IFC model (``ifcopenshell.open()``).
            ifc_object: The specific IFC element to update.
        """
        self.model = model
        self.ifc_object = ifc_object

    def __str__(self) -> str:
        """Return a human-readable description of this updater.

        Returns:
            String identifying the model being updated.
        """
        return f"I will update the model {self.model}"

    def update_location(self, origin: np.ndarray, angle: float) -> None:
        """Update the IfcLocalPlacement of the object.

        Args:
            origin: New origin coordinates, shape ``(3,)``.
            angle: Rotation angle in degrees (counter-clockwise is positive).
        """
        # new placement unit matrix at (0, 0, 0)
        matrix = np.eye(4)
        matrix = placement.rotation(angle, "Z") @ matrix
        matrix[:, 3][0:3] = origin

        run(
            "geometry.edit_object_placement",
            self.model,
            product=self.ifc_object,
            matrix=matrix,
            is_si=True,
        )

    def update_material(self, ifc_material) -> None:
        """Replace the material assigned to the object.

        Args:
            ifc_material: New IfcMaterial to assign.
        """
        run(
            "material.assign_material",
            self.model,
            product=self.ifc_object,
            type="IfcMaterial",
            material=ifc_material,
        )

    def update_property(self, pset_name: str, pset_dict: dict) -> None:
        """Add or update a property set on the object.

        If the object already has one property set it is updated; if it has more
        than one, a message is printed and no change is made.

        Args:
            pset_name: Name of the property set.  Avoid the ``Pset_`` prefix
                (reserved by the IFC standard for standard property sets).
            pset_dict: Property name-to-value mapping.  Python types are
                converted to IFC types automatically, though this may be
                ambiguous in edge cases.
        """
        psets = element.get_psets(self.ifc_object)
        print(f"Ifc Class of element: {self.ifc_object.get_info().get('type')}")
        print(f"Type of property sets: {list(psets.keys())}")
        # manage update depending on property set
        if len(list(psets.keys())) == 0 or len(list(psets.keys())) == 1:
            pset = run(
                "pset.add_pset",
                self.model,
                product=self.ifc_object,
                name=pset_name,
            )
            run("pset.edit_pset", self.model, pset=pset, properties=pset_dict)
        else:
            print(
                f"Object of class {self.ifc_object.get_info().get('type')} has more than one PSet, check manually"
            )

    def write(self) -> None:
        """Write the updated model to a file."""
        self.model.write("baubot_demo_update.ifc")


def main():
    """Load a demo IFC file, apply a location update, and write the result."""
    ifc_mdl = ifcopenshell.open("baubot_demo.ifc")
    # get the first wall in the model
    ifc_robot = ifc_mdl.by_guid("34tooC1TvAbQnDhok8tUWM")
    update = UpdateIfcObject(ifc_mdl, ifc_robot)
    update.update_location(np.asarray([5.0, 2.0, 0.0]), 90.0)
    # update.update_material(ifc_mats.clt)
    update.update_property(
        "PSet_Robot",
        {
            "is_active": True,
            "battery": 0.82,
            "current_task": "moving to opening",
            "is_moving": False,
        },
    )
    update.write()
    # TODO: visualize update


if __name__ == "__main__":
    main()
