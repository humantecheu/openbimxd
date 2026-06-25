# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Create IfcDoor elements in an IFC model."""

import ifcopenshell.api.feature
import ifcopenshell.api.geometry
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.geom
import numpy as np


class IfcDoor:
    """Create an IfcDoor in an IFC model from a bounding box."""

    def __init__(self, ifc_model) -> None:
        """Create an empty IfcDoor entity in the IFC model.

        Args:
            ifc_model: IfcModelBuilder instance the door will be added to.
        """
        self.door = ifcopenshell.api.root.create_entity(
            ifc_model.model,
            ifc_class="IfcDoor",
        )
        self.ifc_model = ifc_model

    def create_door(self, wall, bx, uid=None) -> None:
        """Create door placement, representation, and opening; assign to building storey.

        Args:
            wall: IfcWall instance that is the parent object.
            bx: Bounding box defining the door geometry.
            uid: Optional GUID to use instead of generating a new one.
        """
        print("-- creating IFC door")
        # set uid if given
        if uid is not None:
            self.door.GlobalId = uid

        door_matrix = wall.matrix.copy()
        # points are ordered, try to use 1st corner vector
        door_matrix[:, 3][0:3] += bx.corner_points[0] - wall.matrix[:, 3][0:3]
        # Set our door's Object Placement using our matrix.
        # `is_si=True` states that we are using SI units instead of project units.
        ifcopenshell.api.geometry.edit_object_placement(
            self.ifc_model.model,
            product=self.door,
            matrix=door_matrix,
            is_si=True,
        )

        # Add a new wall-like body geometry with bounding box dimensions
        # representation is used for opening and door
        opening_representation = ifcopenshell.api.geometry.add_wall_representation(
            self.ifc_model.model,
            context=self.ifc_model.body,
            length=float(bx.length()),
            height=float(bx.height()),
            thickness=float(bx.width()),
        )
        # TODO: fix door representation, add generic door-style one
        # door_representation = run(
        #     "geometry.add_door_representation",
        #     self.ifc_model.model,
        #     context=self.ifc_model.body,
        #     door_type="DOUBLE_SWING_RIGHT",
        # )
        opening = ifcopenshell.api.root.create_entity(
            self.ifc_model.model,
            ifc_class="IfcOpeningElement",
        )

        # Assign the opening to the model
        ifcopenshell.api.geometry.assign_representation(
            self.ifc_model.model,
            product=opening,
            representation=opening_representation,
        )

        # using box-style opening representation
        ifcopenshell.api.geometry.assign_representation(
            self.ifc_model.model,
            product=self.door,
            representation=opening_representation,
        )
        ifcopenshell.api.feature.add_feature(
            self.ifc_model.model,
            feature=opening,
            element=wall.wall,
        )
        ifcopenshell.api.geometry.edit_object_placement(
            self.ifc_model.model,
            product=opening,
            matrix=door_matrix,
            is_si=True,
        )

        # Place our wall in the ground floor
        ifcopenshell.api.spatial.assign_container(
            self.ifc_model.model,
            products=[self.door],
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
        shape = ifcopenshell.geom.create_shape(settings, self.door)
        return np.asarray(shape.geometry.verts)  # ty: ignore[unresolved-attribute]
