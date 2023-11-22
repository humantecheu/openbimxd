import numpy as np
from ifcopenshell.api import run
from ifcopenshell import util


class IfcWall:
    def __init__(self, ifc_model) -> None:
        """initialize IfcWall object. Creates an empty IfcWall in the IFC model
        given as input.

        Args:
            ifc_model (ifcfile): The IFC file the IfcWall will be added to
        """
        self.wall = run("root.create_entity", ifc_model.model, ifc_class="IfcWall")
        self.ifc_model = ifc_model
        self.matrix = None

    def create_wall(self, bx):
        """Creates IfcWalls from a bounding box

        Args:
            bx (bbox): bounding box that holds the wall's geometry
        """
        # Create a 4x4 identity matrix. This matrix is at the origin with no rotation.
        matrix = np.eye(4)

        # Rotate anti-clockwise around the Z axis (i.e. in plan).
        # Anti-clockwise is positive. Clockwise is negative.
        if bx.angle() % 180 == 0:
            matrix = util.placement.rotation(0.0, "Z") @ matrix
        elif bx.angle() % 90 == 0:
            matrix = util.placement.rotation(90, "Z") @ matrix
        else:
            matrix = util.placement.rotation(bx.angle(), "Z") @ matrix
        # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
        # This is because the rotation origin is always at 0, 0, 0.
        if bx.angle() % 180 == 0:
            # find the point with min x and y of the lower points
            lower_points = bx.corner_points[:3]
            idx = np.where(
                (lower_points[:, 0] == np.min(lower_points[:, 0]))
                & (lower_points[:, 1] == np.min(lower_points[:, 1]))
            )
            print(f"Minimum point index: {idx[0].size}")
            if idx[0].size != 0:
                print("pick index with min x and min y")
                matrix[:, 3][0:3] = bx.corner_points[idx]
            else:
                print("use index 0")
                matrix[:, 3][0:3] = bx.corner_points[0]
        elif bx.angle() % 90 == 0:
            # in this case, the origin of the local placement needs to
            # be at max x and min y
            lower_points = bx.corner_points[:3]
            idx = np.where(
                (lower_points[:, 0] == np.max(lower_points[:, 0]))
                & (lower_points[:, 1] == np.min(lower_points[:, 1]))
            )
            print(f"Minimum point index: {idx[0].size}")
            if idx[0].size != 0:
                print("pick index with min x and min y")
                matrix[:, 3][0:3] = bx.corner_points[idx]
            else:
                print("use index 1")
                matrix[:, 3][0:3] = bx.corner_points[1]
        # in any other cases the origin of the local placement can be found
        # using the minimum of x or y
        # Note, that numpy argmin and argmax return the first item found
        # so this returns the lower point with the condition met
        elif bx.angle() < 90:
            idx = np.argmin(bx.corner_points[:, 1])
            matrix[:, 3][0:3] = bx.corner_points[idx]
        elif bx.angle() < 180:
            idx = np.argmax(bx.corner_points[:, 0])
            matrix[:, 3][0:3] = bx.corner_points[idx]
        elif bx.angle() < 270:
            idx = np.argmax(bx.corner_points[:, 1])
            matrix[:, 3][0:3] = bx.corner_points[idx]
        else:
            idx = np.argmin(bx.corner_points[:, 0])
            matrix[:, 3][0:3] = bx.corner_points[idx]

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
