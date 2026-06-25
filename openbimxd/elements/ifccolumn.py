# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Create IfcColumn elements in an IFC model."""

import ifcopenshell.api.geometry
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.geom
import ifcopenshell.util.placement
import numpy as np


class IfcColumn:
    """Create an IfcColumn in an IFC model from a bounding box."""

    def __init__(self, ifc_model) -> None:
        """Create an empty IfcColumn entity in the IFC model.

        Args:
            ifc_model: IfcModelBuilder instance to add the column to.
        """
        self.ifc_model = ifc_model
        self.column = ifcopenshell.api.root.create_entity(
            ifc_model.model,
            ifc_class="IfcColumn",
        )

    def create(self, bx, shape="square", **kwargs) -> None:
        """Create round or square column geometry and assign it to the building storey.

        Args:
            bx: Bounding box defining the column extent.
            shape: Profile shape — ``"square"`` (default) or ``"round"``.
            **kwargs: Additional profile parameters.  For ``shape="round"``,
                ``radius`` (float, metres) sets the circle radius (default 0.3).
        """
        matrix = np.eye(4)
        matrix = ifcopenshell.util.placement.rotation(bx.angle(), "Z") @ matrix
        # apply transformation
        matrix[:, 3][0:3] = np.mean(bx.corner_points[:4], axis=0)
        print("Column centroid:", np.mean(bx.corner_points[:4], axis=0))
        ifcopenshell.api.geometry.edit_object_placement(
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
            return

        # Add a new wall-like body geometry with bounding box dimensions
        representation = ifcopenshell.api.geometry.add_profile_representation(
            self.ifc_model.model,
            context=self.ifc_model.body,
            profile=profile,
            depth=bx.height(),
        )
        # Assign our new body geometry back to our wall
        ifcopenshell.api.geometry.assign_representation(
            self.ifc_model.model,
            product=self.column,
            representation=representation,
        )

        # Place our wall in the ground floor
        ifcopenshell.api.spatial.assign_container(
            self.ifc_model.model,
            products=[self.column],
            relating_structure=self.ifc_model.storey,
        )

    def get_verts(self) -> np.ndarray:
        """Return all corner vertices of the geometry representation.

        Returns:
            Flat vertex array of shape ``(n,)``.
        """
        # ifc geom settings for ifc box visualization
        settings = ifcopenshell.geom.settings()
        settings.set("use-world-coords", True)
        # retrieve shape
        shape = ifcopenshell.geom.create_shape(settings, self.column)
        return np.asarray(shape.geometry.verts)  # ty: ignore[unresolved-attribute]
