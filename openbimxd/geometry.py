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
# openbimxd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openbimxd.  If not, see <http://www.gnu.org/licenses/>.
#
# This project uses IfcOpenShell <https://blenderbim.org/>, all credits to
# Dion Moult for his great work

from __future__ import annotations

import numpy as np

from pystruct3d.bbox.bbox import BBox


def bbox_from_ifc_verts(verts: np.ndarray, force_cuboid: bool = True) -> BBox:
    """Create a BBox from an IfcOpenShell flat vertex array.

    IfcOpenShell geometry shapes expose vertices as a flat ``(n,)`` array of
    XYZ triplets.  This function reshapes that array and fits a bounding box.

    Typical usage::

        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        shape = ifcopenshell.geom.create_shape(settings, ifc_element)
        bx = bbox_from_ifc_verts(np.asarray(shape.geometry.verts))

    Args:
        verts: flat vertex array of shape ``(n,)`` as returned by
            ``ifcopenshell.geom``; ``n`` must be a multiple of 3.
        force_cuboid: when ``True`` (default) fit a minimum-volume
            Z-aligned bounding box via ``fit_horizontal_aligned``, which
            enforces a proper cuboid.  When ``False``, select the 8 points
            furthest from the centroid as corner candidates — fast but may
            produce a non-cuboid result for complex IFC shapes.

    Returns:
        Fitted BBox.
    """
    bx = BBox()
    pts = verts.reshape((-1, 3))
    if force_cuboid:
        bx.fit_horizontal_aligned(pts)
    else:
        corner_pts = pts[pts[:, 2].argsort()]
        centrd = np.array([
            (np.amin(corner_pts[:, 0]) + np.amax(corner_pts[:, 0])) / 2,
            (np.amin(corner_pts[:, 1]) + np.amax(corner_pts[:, 1])) / 2,
            (np.amin(corner_pts[:, 2]) + np.amax(corner_pts[:, 2])) / 2,
        ])
        dists = np.linalg.norm(corner_pts - centrd, axis=1)
        bx.corner_points = corner_pts[(-dists).argsort()[:8]]
        bx.order_points()
    return bx
