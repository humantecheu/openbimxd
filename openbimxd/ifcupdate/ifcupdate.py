import numpy as np

import ifcopenshell
from ifcopenshell.util import placement, element
from ifcopenshell.api import run

from openbimxd.ifcmaterial import ifcmaterial


class UpdateIfcObject:
    """
    A class to update IFC objects. The updated objects are saved as a new file.

    Attributes:
        model: IFC model, open it using ifcopenshell.open()
        ifc_object: specific IFC object. Use IfcOpenShell to select an object.
    """

    def __init__(
        self,
        model: ifcopenshell.file,
        ifc_object: ifcopenshell.main.ifcopenshell_wrapper.Element,
    ) -> None:
        """Initialize UpdateIfcObject object

        Args:
            model (ifcopenshell.file): IFC model
            ifc_object (ifcopenshell.main.ifcopenshell_wrapper.Element): subclass of IfcElement
        """
        self.model = model
        self.ifc_object = ifc_object
        pass

    def __str__(self) -> str:
        """Print string

        Returns:
            string: String to be printed when print()
        """
        strg = f"I will update the model {self.model}"
        return strg

    def update_location(self, origin: np.ndarray, angle: float) -> None:
        """Update the location and angle of an the IfcLocalPlacement.

        Args:
            origin (np.ndarray): New origin, shape (3,)
            angle (float): Angle for rotation in degrees. Counter-clockwise
                            is positive
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
        """Update the IfcMaterial.

        Args:
            ifc_material (IfcMaterial): Ifc Material
        """
        run(
            "material.assign_material",
            self.model,
            product=self.ifc_object,
            type="IfcMaterial",
            material=ifc_material,
        )

    def update_property(self, pset_name: str, pset_dict: dict) -> None:
        """Updates the property set of an object. Either adds a new property
        set or updates the existing one, if one with same name as existing
        is given.

        Args:
            pset_name (str): Name of the property set. Note, that Pset_ is reserved for
            property sets in the IFC standard, so name yours differently.
            pset_dict (dict): Dictionary with new properties. Key is name of
            property, value is value of property. Note, that python data types
            are transferred into IFC data types, but this could be ambiguous.
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
        """Write the updated model"""
        self.model.write("baubot_demo_update.ifc")


def main():
    ifc_mdl = ifcopenshell.open("baubot_demo.ifc")
    # get the first wall in the model
    ifc_robot = ifc_mdl.by_guid("34tooC1TvAbQnDhok8tUWM")
    ifc_mats = ifcmaterial.IfcMaterials(ifc_mdl)

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
