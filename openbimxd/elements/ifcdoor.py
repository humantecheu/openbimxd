import numpy as np
from ifcopenshell.api import run
from ifcopenshell import util


class IfcDoor:
    def __init__(self, ifc_model):
        """initialize IfcDoor object. Creates an empty IfcDoor in the IFC model
        given as input.

        Args:
            ifc_model (ifcfile): The IFC file the IfcWall will be added to
        """
        self.door = run("root.create_entity", ifc_model.model, ifc_class="IfcDoor")
        self.ifc_model = ifc_model

    def create_door(self, wall, bx):
        # Create a 4x4 identity matrix. This matrix is at the origin with no rotation.

        matrix = wall.matrix

        # yaw = np.arctan2(matrix[:, 0][1], matrix[:, 0][0])
        # print(f"Angle: {np.rad2deg(yaw)}")

        # transform = np.eye(4)
        # along_length = 0.5
        # z_diff = 1.0
        # transform[:, 3][0:3] = [
        #     along_length * np.cos(yaw),
        #     along_length * np.sin(yaw),
        #     z_diff,
        # ]

        # matrix = np.dot(transform, matrix)

        # print(matrix)

        # TODO: translate local placement, relative to wall
        # TODO: find the shortest vector between origin of wall placement
        # and door box corner points

        placement_door_vectors = bx.corner_points - np.tile(matrix[:, 3][0:3], (8, 1))
        lengths = np.linalg.norm(placement_door_vectors, axis=1)
        matrix[:, 3][0:3] += placement_door_vectors[np.argmin(lengths)]

        # Set our door's Object Placement using our matrix.
        # `is_si=True` states that we are using SI units instead of project units.
        run(
            "geometry.edit_object_placement",
            self.ifc_model.model,
            product=self.door,
            matrix=matrix,
            is_si=True,
        )

        # Add a new wall-like body geometry with bounding box dimensions
        # representation is used for opening and door
        representation = run(
            "geometry.add_wall_representation",
            self.ifc_model.model,
            context=self.ifc_model.body,
            length=float(bx.length()),
            height=float(bx.height()),
            thickness=float(bx.width()),
        )
        opening = run(
            "root.create_entity", self.ifc_model.model, ifc_class="IfcOpeningElement"
        )

        # Assign the opening to the model
        run(
            "geometry.assign_representation",
            self.ifc_model.model,
            product=opening,
            representation=representation,
        )
        run(
            "void.add_opening", self.ifc_model.model, opening=opening, element=wall.wall
        )
        run(
            "geometry.edit_object_placement",
            self.ifc_model.model,
            product=opening,
            matrix=matrix,
            is_si=True,
        )

        # # create relation to wall
        # run(
        #     "geometry.connect_element",
        #     self.ifc_model.model,
        #     relating_element=self.door,
        #     related_element=wall,
        #     description=None,
        # )

        # Place our wall in the ground floor
        run(
            "spatial.assign_container",
            self.ifc_model.model,
            relating_structure=self.ifc_model.storey,
            product=self.door,
        )

        pass
