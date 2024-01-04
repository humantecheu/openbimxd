import numpy as np
import open3d as o3d

import ifcopenshell
import ifcopenshell.geom

from openbimxd.ifcfile import ifcfile
from openbimxd.elements import ifcwall, ifcdoor, ifccolumn

from pystruct3d.bbox import bbox
from pystruct3d.visualization import visualization


def walls_test(test_angle):
    sample_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
            [5.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 3.0],
            [5.0, 0.0, 3.0],
            [5.0, 1.0, 3.0],
            [0.0, 1.0, 3.0],
        ]
    )
    sample_points += np.array([-10, -10, 0])
    bx = bbox.BBox(sample_points)

    print(f"Test angle: {test_angle}")
    bx.rotate(test_angle)
    bx.translate(np.array([1.0, 2.0, 0.0]))
    bx.order_points()
    print(f"Box angle: {bx.angle()}")

    ifc_model = ifcfile.IfcModelBuilder("my_file.ifc", "my_project")

    wall = ifcwall.IfcWall(ifc_model)
    wall.create_wall(bx)

    ifc_model.write()
    # extract the shape and vertices of the wall
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    shape = ifcopenshell.geom.create_shape(settings, wall.wall)
    verts = np.asarray(shape.geometry.verts)
    # generate a bbox from the vertices
    ifc_bx = bbox.BBox()
    ifc_bx.bbox_from_verts(verts)

    print(f"Ifc Box angle: {ifc_bx.angle()}")

    # print(bx.corner_points)
    # print(ifc_bx.corner_points)

    visu = visualization.Visualization()
    visu.bbox_geometry(bx)
    visu.bbox_geometry(ifc_bx, color=[1, 0.75, 0])
    visu.visualize()

    print("------------------------")


def door_test(ang):
    # rotation matrix
    angle = np.deg2rad(ang)  # problem at 180
    axis = np.array([0, 0, 1])
    c = np.cos(angle)
    s = np.sin(angle)
    t = 1 - c
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    # fmt:off
    rot_mat = np.array(
        [
            [t * x**2 + c, t * x * y - s * z, t * x * z + s * y],
            [t * x * y + s * z, t * y**2 + c, t * y * z - s * x],
            [t * x * z - s * y, t * y * z + s * x, t * z**2 + c],
        ]
    )
    # fmt:on

    wall_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
            [5.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 3.0],
            [5.0, 0.0, 3.0],
            [5.0, 1.0, 3.0],
            [0.0, 1.0, 3.0],
        ]
    )
    wall_points += np.array([-10, -10, 0])
    wall_points = np.dot(wall_points, rot_mat.T)
    wall_bx = bbox.BBox(wall_points)
    # wall_bx.rotate(180)
    wall_bx.order_points()

    door_points = np.array(
        [
            [1.0, 0.0, 1.0],
            [2.0, 0.0, 1.0],
            [2.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 0.0, 2.0],
            [2.0, 0.0, 2.0],
            [2.0, 1.0, 2.0],
            [1.0, 1.0, 2.0],
        ]
    )
    door_points += np.array([-10, -10, 0])
    door_points = np.dot(door_points, rot_mat.T)
    door_box = bbox.BBox(door_points)
    door_box.order_points()
    # door_box.rotate(180)
    # door_box.project_into_parent(wall_bx)
    door_box.order_points()

    visu = visualization.Visualization()
    visu.bbox_geometry(wall_bx)
    visu.bbox_geometry(door_box, color=[1, 0.75, 0])
    visu.visualize()

    ifc_model = ifcfile.IfcModelBuilder("my_file.ifc", "my_project")

    wall = ifcwall.IfcWall(ifc_model)
    wall.create_wall(wall_bx)
    door = ifcdoor.IfcDoor(ifc_model)
    door.create_door(wall, door_box)

    ifc_model.write()


def column_test():
    ifc_model = ifcfile.IfcModelBuilder("my_file.ifc", "my_project")
    col_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0],
            [0.5, 0.5, 0.0],
            [0.0, 0.5, 0.0],
            [0.0, 0.0, 3.0],
            [0.5, 0.0, 3.0],
            [0.5, 0.5, 3.0],
            [0.0, 0.5, 3.0],
        ]
    )
    col_box = bbox.BBox(col_points)
    ifc_col = ifccolumn.IfcColumn(ifc_model)
    ifc_col.create(col_box, shape="round")
    ifc_model.write()


def main():
    # walls_test(90.0002257895)
    for i in range(0, 185, 5):
        door_test(i)
    # column_test()


if __name__ == "__main__":
    main()
