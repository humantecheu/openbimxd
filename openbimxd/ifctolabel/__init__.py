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
