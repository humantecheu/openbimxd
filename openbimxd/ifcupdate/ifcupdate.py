import numpy as np

import ifcopenshell
from ifcopenshell.util import placement, element
from ifcopenshell.api import run


from openbimxd.elements import ifcwall, ifccolumn, ifcdoor
from openbimxd.ifcmaterial import ifcmaterial


class UpdateElement:
    def __init__(self, model, ifc_element) -> None:
        self.model = model
        self.ifc_element = ifc_element
        pass

    def __str__(self):
        strg = "I will update the model"
        return strg

    def update_location(self, origin: np.ndarray, angle: float):
        # new placement unit matrix at (0, 0, 0)
        matrix = np.eye(4)
        matrix = placement.rotation(angle, "Z") @ matrix
        matrix[:, 3][0:3] = origin

        run(
            "geometry.edit_object_placement",
            self.model,
            product=self.ifc_element,
            matrix=matrix,
            is_si=True,
        )
        pass

    def update_material(self, ifc_material):
        run(
            "material.assign_material",
            self.model,
            product=self.ifc_element,
            type="IfcMaterial",
            material=ifc_material,
        )
        pass

    def update_property(self, pset_name, pset_dict):
        psets = element.get_psets(self.ifc_element)
        print(f"Ifc Class of element: {self.ifc_element.get_info().get('type')}")
        print(f"Type of property sets: {list(psets.keys())}")
        # manage update depending on property set
        if len(list(psets.keys())) == 0 or len(list(psets.keys())) == 1:
            pset = run(
                "pset.add_pset",
                self.model,
                product=self.ifc_element,
                name=pset_name,
            )
            run("pset.edit_pset", self.model, pset=pset, properties=pset_dict)
        else:
            print(
                f"Object of class {self.ifc_element.get_info().get('type')} has more than one PSet, check manually"
            )
        pass

    def write(self):
        self.model.write("baubot_demo_update.ifc")


def main():
    ifc_mdl = ifcopenshell.open("baubot_demo.ifc")
    # get the first wall in the model
    ifc_robot = ifc_mdl.by_guid("34tooC1TvAbQnDhok8tUWM")
    ifc_mats = ifcmaterial.IfcMaterials(ifc_mdl)

    update = UpdateElement(ifc_mdl, ifc_robot)
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
