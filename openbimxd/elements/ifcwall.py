# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

import ifcopenshell.api.geometry
import ifcopenshell.api.material
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.geom
import ifcopenshell.util.placement
import numpy as np


class IfcWall:
    """
    A class to create an IfcWall

    Attributes:
        ifc_model : IfcModelBuilder object

    Methods:
        create_wall
            Create the wall geometry representation, assign the wall to a building
            storey.
        get_verts
            Get the vertices of the geometry representation.
    """

    def __init__(self, ifc_model, ifc_material=None) -> None:
        """Initialize IfcWall object. Creates an empty IfcWall in the IFC model
        given as input.

        Args:
            ifc_model (ifcfile): The IFC file the IfcWall will be added to
        """

        self.wall = ifcopenshell.api.root.create_entity(
            ifc_model.model,
            ifc_class="IfcWall",
        )
        self.ifc_model = ifc_model
        self.ifc_material = ifc_material
        self.matrix = np.eye(4)

    def create_wall(self, bx, uid=None) -> None:
        """Creates IfcWalls from a bounding box

        Args:
            bx (bbox): bounding box that holds the wall's geometry
            uid (string): optional, to set uid according to reference data
        """
        # set uid if given
        if uid is not None:
            self.wall.GlobalId = uid
        # Create a 4x4 identity matrix. This matrix is at the origin with no rotation.
        matrix = np.eye(4)
        # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
        # This is because the rotation origin is always at 0, 0, 0.
        # Rotate anti-clockwise around the Z axis (i.e. in plan).
        # Anti-clockwise is positive. Clockwise is negative.
        matrix = ifcopenshell.util.placement.rotation(bx.angle(), "Z") @ matrix
        # points ordered, set placement to 1st corner point
        matrix[:, 3][0:3] = bx.corner_points[0]

        # Set our wall's Object Placement using our matrix.
        # `is_si=True` states that we are using SI units instead of project units.
        ifcopenshell.api.geometry.edit_object_placement(
            self.ifc_model.model,
            product=self.wall,
            matrix=matrix,
            is_si=True,
        )
        self.matrix = matrix

        # Add a new wall-like body geometry with bounding box dimensions
        representation = ifcopenshell.api.geometry.add_wall_representation(
            self.ifc_model.model,
            context=self.ifc_model.body,
            length=float(bx.length()),
            height=float(bx.height()),
            thickness=float(bx.width()),
        )

        # Assign our new body geometry back to our wall
        ifcopenshell.api.geometry.assign_representation(
            self.ifc_model.model,
            product=self.wall,
            representation=representation,
        )

        # assign material
        if self.ifc_material is not None:
            ifcopenshell.api.material.assign_material(
                self.ifc_model.model,
                products=[self.wall],
                type="IfcMaterial",
                material=self.ifc_material,
            )
        # assign property set
        pset = ifcopenshell.api.pset.add_pset(
            self.ifc_model.model,
            product=self.wall,
            name="Pset_WallCommon",
        )
        ifcopenshell.api.pset.edit_pset(
            self.ifc_model.model,
            pset=pset,
            properties={"FireRating": "F60", "LoadBearing": True},
        )

        # Place our wall in the ground floor
        ifcopenshell.api.spatial.assign_container(
            self.ifc_model.model,
            relating_structure=self.ifc_model.storey,
            products=[self.wall],
        )

    def get_verts(self) -> np.ndarray:
        """Get the vertices i.e., all corner points of the geometry representation

        Returns:
            verts: np.ndarray
        """
        # ifc geom settings for ifc box visualization
        settings = ifcopenshell.geom.settings()
        settings.set("use-world-coords", True)
        # retrieve shape
        shape = ifcopenshell.geom.create_shape(settings, self.wall)
        return np.asarray(shape.geometry.verts)  # ty: ignore[unresolved-attribute]
