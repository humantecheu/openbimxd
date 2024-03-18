# openbimxd - open source tools to interact with IFC files
# Copyright (C) 2024, 2024 the HumanTech project
# Main contributors: Fabian Kaufmann fabian.kaufmann@rptu.de
#           Marius Schellen marius.schellen@rptu.de
#           Mahdi Chamseddine mahdi.chamseddine@dfki.de
#
# This file is part of openbimxd
#
# openbimxd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.
#
# This project uses IfcOpenShell <https://blenderbim.org/>, all credits to
# Dion Moult for his great work

import numpy as np
import open3d as o3d

import ifcopenshell
import ifcopenshell.geom

from openbimxd.ifcfile import ifcfile
from openbimxd.elements import ifcwall, ifcdoor, ifccolumn
from openbimxd.ifcmaterial import ifcmaterial

from pystruct3d.bbox import bbox
from pystruct3d.visualization import visualization


def walls_test(test_angle):
    # rotation matrix
    print(f"Test angle: {test_angle}")
    angle = np.deg2rad(test_angle)
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
    sample_points = np.dot(sample_points, rot_mat.T)
    sample_points += np.array([0, -10, 0])
    
    gen = np.random.Generator(np.random.PCG64())
    gen.shuffle(sample_points)
    print(sample_points)
    bx = bbox.BBox(sample_points)
    bx.order_points()
    print(f"Box angle: {bx.angle()}")
    print(bx.corner_points)

    ifc_model = ifcfile.IfcModelBuilder("my_file.ifc", "my_project")
    mats = ifcmaterial.IfcMaterials(ifc_model.model)

    wall = ifcwall.IfcWall(ifc_model, ifc_material=mats.concrete)
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
    visu.points_geometry(bx.corner_points[0].reshape(1, 3))
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
    # wall_points += np.array([-2, -2, 0])
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
    # door_points += np.array([-10, -10, 0])
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
    door_test(0)
    # for i in range(10):
    #     walls_test(0.0)
    #     walls_test(180.0)
    # walls_test(180.0 - np.random.random() / 1e6)
    # walls_test(0.0)
    #     # door_test(i)
    # walls_test(np.random.random() * 180)
    # column_test()
    # for i in range(10):
    #     walls_test(89.999999999999999999999)


if __name__ == "__main__":
    main()
