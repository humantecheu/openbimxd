import numpy as np
from ifcopenshell.api import run
from ifcopenshell import util
import ifcopenshell.geom


class IfcWall:
    def __init__(self, ifc_model) -> None:
        """initialize IfcWall object. Creates an empty IfcWall in the IFC model
        given as input.

        Args:
            ifc_model (ifcfile): The IFC file the IfcWall will be added to
        """
        self.wall = run("root.create_entity", ifc_model.model, ifc_class="IfcWall")
        self.ifc_model = ifc_model
        self.matrix = np.eye(4)

    def create_wall(self, bx, uid=None):
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
        matrix = util.placement.rotation(bx.angle(), "Z") @ matrix
        # points ordered, set placement to 1st corner point
        matrix[:, 3][0:3] = bx.corner_points[0]

        # Set our wall's Object Placement using our matrix.
        # `is_si=True` states that we are using SI units instead of project units.
        run(
            "geometry.edit_object_placement",
            self.ifc_model.model,
            product=self.wall,
            matrix=matrix,
            is_si=True,
        )
        self.matrix = matrix

        # Add a new wall-like body geometry with bounding box dimensions
        representation = run(
            "geometry.add_wall_representation",
            self.ifc_model.model,
            context=self.ifc_model.body,
            length=float(bx.length()),
            height=float(bx.height()),
            thickness=float(bx.width()),
        )
        # Assign our new body geometry back to our wall
        run(
            "geometry.assign_representation",
            self.ifc_model.model,
            product=self.wall,
            representation=representation,
        )

        # Place our wall in the ground floor
        run(
            "spatial.assign_container",
            self.ifc_model.model,
            relating_structure=self.ifc_model.storey,
            product=self.wall,
        )

    def get_verts(self):
        # ifc geom settings for ifc box visualization
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        # retrieve shape
        shape = ifcopenshell.geom.create_shape(settings, self.wall)
        verts = np.asarray(shape.geometry.verts)

        return verts
