import numpy as np
from pystruct3d.bbox.bbox import BBox

from openbimxd.geometry import bbox_from_ifc_verts


def _box_verts(x, y, z, dx, dy, dz) -> np.ndarray:
    """Return flat IFC-style vertex array for an axis-aligned box."""
    corners = np.array(
        [
            [x, y, z],
            [x + dx, y, z],
            [x + dx, y + dy, z],
            [x, y + dy, z],
            [x, y, z + dz],
            [x + dx, y, z + dz],
            [x + dx, y + dy, z + dz],
            [x, y + dy, z + dz],
        ],
        dtype=float,
    )
    return corners.flatten()


def test_returns_bbox_instance():
    flat = _box_verts(0, 0, 0, 3.0, 0.3, 2.5)
    bx = bbox_from_ifc_verts(flat, force_cuboid=True)
    assert isinstance(bx, BBox)


def test_corner_points_shape():
    flat = _box_verts(0, 0, 0, 3.0, 0.3, 2.5)
    bx = bbox_from_ifc_verts(flat, force_cuboid=True)
    assert bx.corner_points is not None
    assert bx.corner_points.shape == (8, 3)


def test_force_cuboid_false():
    flat = _box_verts(1.0, 2.0, 0.5, 2.0, 0.5, 3.0)
    bx = bbox_from_ifc_verts(flat, force_cuboid=False)
    assert isinstance(bx, BBox)
    assert bx.corner_points is not None
    assert bx.corner_points.shape == (8, 3)


def test_translated_box():
    flat = _box_verts(5.0, 3.0, 1.0, 1.0, 0.2, 2.8)
    bx = bbox_from_ifc_verts(flat, force_cuboid=True)
    assert bx.corner_points is not None
    assert bx.corner_points.shape == (8, 3)
