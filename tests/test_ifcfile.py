import tempfile
from pathlib import Path

import ifcopenshell

from openbimxd.ifcfile.ifcfile import IfcModelBuilder


def test_model_created():
    model = IfcModelBuilder(filename="test.ifc")
    assert model.model is not None


def test_project_exists():
    model = IfcModelBuilder(filename="test.ifc")
    assert len(model.model.by_type("IfcProject")) == 1


def test_site_building_storey_hierarchy():
    model = IfcModelBuilder(filename="test.ifc")
    assert len(model.model.by_type("IfcSite")) == 1
    assert len(model.model.by_type("IfcBuilding")) == 1
    assert len(model.model.by_type("IfcBuildingStorey")) == 1


def test_custom_project_name():
    model = IfcModelBuilder(filename="test.ifc", project_name="Test Project")
    project = model.model.by_type("IfcProject")[0]
    assert project.Name == "Test Project"


def test_write_and_reload():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_output.ifc"
        model = IfcModelBuilder(filename=str(path))
        model.write()
        assert path.exists()
        reloaded = ifcopenshell.open(str(path))
        assert len(reloaded.by_type("IfcProject")) == 1
        assert len(reloaded.by_type("IfcBuildingStorey")) == 1


def test_ifc4_schema():
    model = IfcModelBuilder(filename="test.ifc", schema="IFC4")
    assert model.model.schema == "IFC4"
