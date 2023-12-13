import ifcopenshell
import numpy as np
import open3d as o3d
from pystruct3d.bbox import bbox
from pystruct3d.visualization import visualization


class IfcToLabel:
    def __init__(self, ifc_file, pcd_file, offset) -> None:
        self.offset = offset
        self.ifc_model = ifcopenshell.open(ifc_file)
        self.pcd = o3d.io.read_point_cloud(pcd_file)
        num_points = np.shape(np.asarray(self.pcd.points))[0]
        self.labels = np.zeros((num_points, 2))
        self.visu = visualization.Visualization()

    def get_inliers(self, ifc_element):
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        shape = ifcopenshell.geom.create_shape(settings, ifc_element)
        verts = np.asarray(shape.geometry.verts)
        # generate a bbox from the vertices
        ifc_bx = bbox.BBox()
        ifc_bx.bbox_from_verts(verts)
        ifc_bx.expand(self.offset)
        element_pts, indices = ifc_bx.points_in_BBox(np.asarray(self.pcd.points))
        self.visu.bbox_geometry(ifc_bx)
        return element_pts, indices

    def parse_doors(self):
        print("Parse doors ...")
        doors = self.ifc_model.by_type("IfcDoor")

        for door in doors:
            door_pts, indices = self.get_inliers(door)
            self.labels[indices, 0] = 8
            self.labels[indices, 1] = door.id()

            self.visu.point_cloud_geometry(door_pts)

    def parse_windows(self):
        print("Parse windows ...")
        windows = self.ifc_model.by_type("IfcWindow")

        for window in windows:
            window_pts, indices = self.get_inliers(window)
            self.labels[indices, 0] = 11
            self.labels[indices, 1] = window.id()

            self.visu.point_cloud_geometry(window_pts)

    def parse_curtain(self):
        print("Parse curtain walls")
        curtws = self.ifc_model.by_type("IfcCurtainWall")

        for curt in curtws:
            curt_pts, indices = self.get_inliers(curt)
            self.labels[indices, 0] = 27
            self.labels[indices, 1] = curt.id()

            self.visu.point_cloud_geometry(curt_pts)

    def parse_walls(self):
        print("Parse walls ...")
        walls = self.ifc_model.by_type("IfcWall")

        for wall in walls:
            wall_pts, indices = self.get_inliers(wall)
            self.labels[indices, 0] = 4
            self.labels[indices, 1] = wall.id()

            self.visu.point_cloud_geometry(wall_pts)

        print(np.unique(self.labels))

    def visualize(self):
        self.visu.visualize()
