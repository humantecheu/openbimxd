"""
Inherit semantic point labels from IFC classes and geometry.

CLASSES
    IfcToLabel
        Class objects retrieve semantic labels from a point cloud from 
        IFC objects' geometry. 
        The labeled point cloud can be visualized. 

FUNCTIONS
    __init__(self, ifc_file, pcd_file, offset) -> None
        Initialize an IfcToLabel object
    get_inliers(self, ifc_element) -> tuple(np.ndarray, np.ndarray)
        Creates a bounding box from the IFC geometry, return all inliers
    get_inliers_conv_hull(self, ifc_element) -> tuple(np.ndarray, np.ndarray)
        Create a convex hull around the geometry of an IFC element, get all inliers.
        Typically used for more complex non-box shapes e.g., slabs.
    edit_labels(self, ifc_objects, semantic_label, use_conv_hull=False) -> None:
        Edits the labels array given a list of objects of the same class and 
        the respective semantic label.
    parse_doors(self) -> None
        Parse doors, edit the label array.
    parse_windows(self) -> None
        Parse windows, edit the label array.
    parse_slabs(self) -> None
        Parse slabs, edit the label array.
    parse_walls(self) -> None
        Parse walls, edit the label array.
    visualize(self) -> None
        Opens the visualization window.
    
"""
