# Changelog

All notable changes to openbimxd are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.5.1] - 2026-06-25

### Added
- pdoc added to dev dependencies for documentation generation
- GitHub Actions CI workflow: ruff check, ruff format, ty check, pytest on push/PR to main
- GitHub Actions docs workflow: build pdoc site and deploy to GitHub Pages on push to main
- `openbimxd.__version__` exposed via `importlib.metadata` (required by the docs workflow)

### Changed
- Project description updated in `pyproject.toml`
- Google docstring convention enforced via `[tool.ruff.lint.pydocstyle] convention = "google"`; `"D"` removed from the global ignore list
- All class, method, and module docstrings rewritten in Google style (one-liner class descriptions, `Args:`/`Returns:` sections with punctuation)

### Fixed
- Missing MIT SPDX header in `debug.py`
- Missing SPDX header and docstrings in `parsers/ht_demolition_ontology.py`

## [0.5.0] - 2026-06-25

### Added
- Test suite: `test_geometry`, `test_ifcfile`, `test_elements` (14 tests covering core modules)

### Changed
- License changed from GPL-3 to MIT (matching pystruct3d)
- GPL headers replaced with `SPDX-License-Identifier: MIT` in all source files
- ruff lint expanded to `select = ["ALL"]` with targeted ignores documented in `pyproject.toml`
- `requires-python` set to `>=3.10,<3.13` (matching pystruct3d / open3d cap)
- README rewritten with badges, clean install instructions, and module features list
- `tool.uv.sources` workspace override removed — dependency resolves from git URL for all users
- `tool.ty.environment` removed — ty auto-detects the active Python
- `.python-version` removed from version control

### Fixed
- `objectFilter` renamed to `ObjectFilter` (N801 — PEP 8 class naming)
- Deprecated `BBox.points_in_bbox_probability` replaced with `BBox.points_in_bbox` in `IfcToLabel`
- Bare `except Exception` replaced with `except (QhullError, ValueError)` in `IfcToLabel.get_inliers_conv_hull`
- Unnecessary `pass` statements removed in `IfcColumn.__init__` and `UpdateIfcObject.__init__`
- Trivial assignments before `return` inlined (RET504)
- `key in dict.keys()` simplified to `key in dict` in `ObjectFilter.assign_psets` (SIM118)
- `open()` replaced with `Path.open()` in `IfcConvertOpening.to_json` (PTH123)
- Imports sorted in `geometry.py` (I001)

## [0.4.0] - 2026-06-03

### Added
- `geometry.bbox_from_ifc_verts`: fit a `BBox` from an IfcOpenShell flat vertex array;
  replaces `pystruct3d.BBox.bbox_from_verts` which was removed in pystruct3d 0.13

### Changed
- `IfcToLabel.get_inliers` updated to use `geometry.bbox_from_ifc_verts`

## [0.3.0] - 2026-05-28

### Changed
- `IfcToLabel`: dropped `open3d` dependency; point cloud I/O now uses `pystruct3d.io.readers.read_point_cloud`
- `IfcToLabel`: visualization updated to the `pystruct3d.visualization.Visualizer` fluent API
- ruff lint and format pass added; codebase reformatted to black-compatible style

## [0.2.0] - 2025-11-25

### Added
- `pyproject.toml` with `setuptools-scm` dynamic versioning and declared dependencies

### Fixed
- Code compatibility with IfcOpenShell 0.8 API changes

## [0.1.0] - 2024-09-20

### Added
- `ifcfile.IfcModelBuilder`: create an IFC model with project/site/building/storey hierarchy
- `elements.IfcWall`, `elements.IfcColumn`, `elements.IfcDoor`: create IFC elements from `BBox` objects
- `ifcmaterial.IfcMaterials`: create and assign concrete and CLT materials
- `filtering.ObjectFilter`: filter IFC objects by class, attributes, and spatial relationships; export filtered model
- `ifctolabel.IfcToLabel`: assign semantic labels to a point cloud from IFC element geometry
- `ifcupdate.UpdateIfcObject`: update IFC object placement, material, and property sets
- `parsers.IfcConvertOpening`: extract opening geometry parameters and serialize to JSON
