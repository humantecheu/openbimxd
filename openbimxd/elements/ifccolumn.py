import numpy as np
import ifcopenshell
from ifcopenshell.api import run
from ifcopenshell import util


class IfcColumn:
    def __init__(self, ifc_model) -> None:
        self.ifc_model = ifc_model
        self.column = run("root.create_entity", ifc_model.model, ifc_class="IfcColumn")

        pass

    def create(self, bx, shape="square", **kwargs):
        """Creates round and square columns

        Kwargs:
            radius (float): Radius of round column, in mms

        Args:
            bx (bbox): Bounding box. Should be presented for either shape of column
            shape (str, optional): "round" or "square". Defaults to "square".
        """
        matrix = np.eye(4)
        matrix = util.placement.rotation(bx.angle(), "Z") @ matrix
        # apply transformation
        matrix[:, 3][0:3] = np.mean(bx.corner_points[:4], axis=0)
        print("Column centroid:", np.mean(bx.corner_points[:4], axis=0))
        run(
            "geometry.edit_object_placement",
            self.ifc_model.model,
            product=self.column,
            matrix=matrix,
            is_si=True,
        )
        if shape == "square":
            profile = self.ifc_model.model.create_entity(
                "IfcRectangleProfileDef",
                ProfileName="AwesomeProfile",
                ProfileType="AREA",
                XDim=1000 * bx.length(),
                YDim=1000 * bx.width(),
            )
        elif shape == "round":
            profile = self.ifc_model.model.create_entity(
                "IfcCircleProfileDef",
                ProfileName="AwesomeProfile",
                ProfileType="AREA",
                Radius=1000 * kwargs.get("radius", 0.3),
            )
        else:
            print("Unknown column shape, passing ...")

        # Add a new wall-like body geometry with bounding box dimensions
        representation = run(
            "geometry.add_profile_representation",
            self.ifc_model.model,
            context=self.ifc_model.body,
            profile=profile,
            depth=bx.height(),
        )
        # Assign our new body geometry back to our wall
        run(
            "geometry.assign_representation",
            self.ifc_model.model,
            product=self.column,
            representation=representation,
        )

        # Place our wall in the ground floor
        run(
            "spatial.assign_container",
            self.ifc_model.model,
            relating_structure=self.ifc_model.storey,
            product=self.column,
        )
