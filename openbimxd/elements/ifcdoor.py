import numpy as np
from ifcopenshell.api import run
from ifcopenshell import util
import ifcopenshell.geom


class IfcDoor:
    def __init__(self, ifc_model):
        """initialize IfcDoor object. Creates an empty IfcDoor in the IFC model
        given as input.

        Args:
            ifc_model (ifcfile): The IFC file the IfcWall will be added to
        """
        self.door = run("root.create_entity", ifc_model.model, ifc_class="IfcDoor")
        self.ifc_model = ifc_model

    def create_door(self, wall, bx, uid=None):
        print("-- creating IFC door")
        # set uid if given
        if uid is not None:
            self.door.GlobalId = uid

        door_matrix = wall.matrix.copy()
        # points are ordered, try to use 1st corner vector
        door_matrix[:, 3][0:3] += bx.corner_points[0] - wall.matrix[:, 3][0:3]
        # Set our door's Object Placement using our matrix.
        # `is_si=True` states that we are using SI units instead of project units.
        run(
            "geometry.edit_object_placement",
            self.ifc_model.model,
            product=self.door,
            matrix=door_matrix,
            is_si=True,
        )

        # Add a new wall-like body geometry with bounding box dimensions
        # representation is used for opening and door
        opening_representation = run(
            "geometry.add_wall_representation",
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
        opening = run(
            "root.create_entity", self.ifc_model.model, ifc_class="IfcOpeningElement"
        )

        # Assign the opening to the model
        run(
            "geometry.assign_representation",
            self.ifc_model.model,
            product=opening,
            representation=opening_representation,
        )
        # using box-style opening representation
        run(
            "geometry.assign_representation",
            self.ifc_model.model,
            product=self.door,
            representation=opening_representation,
        )
        run(
            "void.add_opening", self.ifc_model.model, opening=opening, element=wall.wall
        )
        run(
            "geometry.edit_object_placement",
            self.ifc_model.model,
            product=opening,
            matrix=door_matrix,
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

    def get_verts(self):
        # ifc geom settings for ifc box visualization
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        # retrieve shape
        shape = ifcopenshell.geom.create_shape(settings, self.door)
        verts = np.asarray(shape.geometry.verts)

        return verts
