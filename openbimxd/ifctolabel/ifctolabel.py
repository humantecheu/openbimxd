import ifcopenshell
import ifcopenshell.geom
import numpy as np
import open3d as o3d
from scipy.spatial import ConvexHull
from pystruct3d.bbox import bbox
from pystruct3d.visualization import visualization


class IfcToLabel:
    """
    A class to assign semantic labels from IFC objects to a point cloud.

    Attributes:
        ifc_file (string): path/to/IfcFile
        pcd_file (string): path to point cloud
        offset (flaot): controls the extension of the search volume (bounding box)
        in either direction.
    """

    def __init__(self, ifc_file, pcd_file, offset) -> None:
        """Constructor for IfcToLabel. Reads the IFC an point cloud file, initializes
        the label array of shape (number of points, 2), creates visualization object

        Args:
            ifc_file (string): path/to/IfcFile
            pcd_file (string): path to point cloud
            offset (flaot): controls the extension of the search volume (bounding box)
            in either direction.
        """
        self.offset = offset
        self.ifc_model = ifcopenshell.open(ifc_file)
        self.pcd = o3d.io.read_point_cloud(pcd_file)
        num_points = np.shape(np.asarray(self.pcd.points))[0]
        self.labels = np.zeros((num_points, 2))
        self.visu = visualization.Visualization()

    def get_inliers(self, ifc_element) -> tuple([np.ndarray, np.ndarray]):
        """Creates a bounding box from the IFC geometry, return all inliers

        Args:
            ifc_element (IFC element): IFC element such as wall, door, window. The
            element needs to hold a geometry representation

        Returns:
            np.ndarray : inlier points (n, 3)
            np.ndarray : indices of inlier points (n, )
        """
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        shape = ifcopenshell.geom.create_shape(settings, ifc_element)
        verts = np.asarray(shape.geometry.verts)
        # generate a bbox from the vertices
        ifc_bx = bbox.BBox()
        ifc_bx.bbox_from_verts(verts)
        ifc_bx.expand(self.offset)
        element_pts, indices = ifc_bx.points_in_bbox_probability(
            np.asarray(self.pcd.points)
        )
        # visualize vertices
        orig_shape = verts.shape[0]
        verts_reshape = verts.reshape((int(orig_shape / 3), 3))
        self.visu.points_geometry(verts_reshape)
        # create visualizer object of ifc bounding box
        self.visu.bbox_geometry(ifc_bx)

        return element_pts, indices

    def get_inliers_conv_hull(self, ifc_element) -> tuple([np.ndarray, np.ndarray]):
        """Create a convex hull around the geometry of an IFC element, get all inliers.
        Typically used for more complex non-box shapes e.g., slabs.

        Args:
            ifc_element (Ifc Element): IfcSlab, needs to have geometry

        Returns:
            np.ndarray: points in convex hull, shape (n, 3)
            np.ndarray: indices of inlier points, shape (n, )
        """
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        shape = ifcopenshell.geom.create_shape(settings, ifc_element)
        verts = np.asarray(shape.geometry.verts)
        orig_shape = verts.shape[0]
        verts = verts.reshape((int(orig_shape / 3), 3))
        try:
            # convex hull
            hull = ConvexHull(verts)

            # Get array of boolean values indicating in hull if True
            in_hull = np.all(
                np.add(
                    np.dot(np.asarray(self.pcd.points), hull.equations[:, :-1].T),
                    hull.equations[:, -1],
                )
                <= self.offset,
                axis=1,
            )  # tolerance could be set to zero, not tested

            # Get the actual points inside the box
            points_in_conv_hull = np.asarray(self.pcd.points)[in_hull]
            indices = np.where(in_hull == True)[0]

            return points_in_conv_hull, indices
        except:
            print("-- trying to construct empty convex hull, passing ...")
            return np.empty((0,)), np.empty((0,))

    def edit_labels(self, ifc_objects, semantic_label, use_conv_hull=False) -> None:
        """Edits the labels array given a list of objects of the same class and the respective
        semantic label.

        Args:
            ifc_objects (list): List of IFC elements with geometry
            semantic_label (int): label
        """
        for obj in ifc_objects:
            if use_conv_hull:
                print("Using convec hull to find inliers ...")
                obj_pts, indices = self.get_inliers_conv_hull(obj)
            else:
                obj_pts, indices = self.get_inliers(obj)

            label_mask = (
                self.labels[indices, np.zeros(indices.shape[0], dtype=int)] == 0
            )
            id_mask = self.labels[indices, np.ones(indices.shape[0], dtype=int)] == 0
            print(np.unique(label_mask))

            self.labels[indices[label_mask], 0] = semantic_label
            self.labels[indices[id_mask], 1] = obj.id()
            print("labels unique:", np.unique(self.labels))

            self.visu.point_cloud_geometry(obj_pts)

    def parse_doors(self) -> None:
        """Parse doors, edit the label array."""
        print("Parse doors ...")
        doors = self.ifc_model.by_type("IfcDoor")
        self.edit_labels(doors, 8)

    def parse_windows(self) -> None:
        """Parse windows, edit the label array."""
        print("Parse windows ...")
        windows = self.ifc_model.by_type("IfcWindow")
        self.edit_labels(windows, 11)

    def parse_slabs(self) -> None:
        """Parse slabs, edit the label array."""
        print("Parse slabs ...")
        slabs = self.ifc_model.by_type("IfcSlab")
        self.edit_labels(slabs, 1, use_conv_hull=True)

    def parse_walls(self) -> None:
        """Parse walls, edit the label array."""
        print("Parse walls ...")
        walls = self.ifc_model.by_type("IfcWall")
        self.edit_labels(walls, 4)

    def visualize(self) -> None:
        """Opens the visualization window."""
        self.visu.visualize()


def main():
    """Opens IFC file and point cloud, gets labels from IFC geometry, saves
    point cloud as ascii with XYZ RGB SemanticLabel InstanceID

    Args:
        ifc_fname (string): IFC file name
        pcd_fname (string): Point cloud file name. Only open3d compatible formats work
        offset (float): offset for point to geometry assignment. The higher, the more coarse
        the labels
    """
    ifc_fname = "HT_DFKI_BA3_4thfloor.ifc"
    pcd_fname = "DFKI_4th_floor.ply"
    offset = 0.1
    get_labels = IfcToLabel(ifc_fname, pcd_fname, offset)
    get_labels.parse_doors()
    get_labels.parse_windows()
    get_labels.parse_slabs()
    get_labels.parse_walls()
    # get_labels.visualize()
    print(np.unique(get_labels.labels))
    point_cloud_array = np.hstack(
        (
            np.asarray(get_labels.pcd.points),
            np.asarray(get_labels.pcd.colors),
            get_labels.labels,
        )
    )
    print(point_cloud_array.shape)
    get_labels.visualize()
    np.savetxt(f"{pcd_fname[:-4]}_labeled.asc", point_cloud_array)


if __name__ == "__main__":
    main()
