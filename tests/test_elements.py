import numpy as np
import pytest
from pystruct3d.bbox.bbox import BBox

from openbimxd.elements.ifccolumn import IfcColumn
from openbimxd.elements.ifcdoor import IfcDoor
from openbimxd.elements.ifcwall import IfcWall
from openbimxd.ifcfile.ifcfile import IfcModelBuilder


def _make_bbox(x, y, z, dx, dy, dz) -> BBox:
    pts = np.array(
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
    bx = BBox()
    bx.fit_horizontal_aligned(pts)
    return bx


@pytest.fixture
def ifc_model():
    return IfcModelBuilder(filename="test_elements.ifc")


def test_wall_created(ifc_model):
    bx = _make_bbox(0, 0, 0, 3.0, 0.3, 2.5)
    wall = IfcWall(ifc_model)
    wall.create_wall(bx)
    assert len(ifc_model.model.by_type("IfcWall")) == 1


def test_wall_get_verts(ifc_model):
    bx = _make_bbox(0, 0, 0, 3.0, 0.3, 2.5)
    wall = IfcWall(ifc_model)
    wall.create_wall(bx)
    verts = wall.get_verts()
    assert isinstance(verts, np.ndarray)
    assert verts.ndim == 1
    assert len(verts) % 3 == 0


def test_column_square_created(ifc_model):
    bx = _make_bbox(0, 0, 0, 0.5, 0.5, 3.0)
    col = IfcColumn(ifc_model)
    col.create(bx, shape="square")
    assert len(ifc_model.model.by_type("IfcColumn")) == 1


def test_door_in_wall(ifc_model):
    wall_bx = _make_bbox(0, 0, 0, 3.0, 0.3, 2.5)
    wall = IfcWall(ifc_model)
    wall.create_wall(wall_bx)

    door_bx = _make_bbox(1.0, 0, 0, 0.9, 0.3, 2.1)
    door = IfcDoor(ifc_model)
    door.create_door(wall, door_bx)
    assert len(ifc_model.model.by_type("IfcDoor")) == 1
    assert len(ifc_model.model.by_type("IfcOpeningElement")) >= 1
