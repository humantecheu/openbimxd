# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Utilities for fitting bounding boxes to IfcOpenShell vertex arrays."""

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
