import numpy as np

from openbimxd.ifctolabel import ifctolabel


def ifc_to_label(ifc_fname, pcd_fname, offset):
    """Opens IFC file and point cloud, gets labels from IFC geometry, saves
    point cloud as ascii with XYZ RGB SemanticLabel InstanceID

    Args:
        ifc_fname (string): IFC file name
        pcd_fname (string): Point cloud file name. Only open3d compatible formats work
        offset (float): offset for point to geometry assignment. The higher, the more coarse
        the labels
    """
    get_labels = ifctolabel.IfcToLabel(ifc_fname, pcd_fname, offset)
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


def main():
    # walls_test(30)
    # door_test()
    ifc_to_label("HT_DFKI_BA3_4thfloor.ifc", "DFKI_4th_floor.ply", 0.1)


if __name__ == "__main__":
    main()
