# OpenBIMxD

![Python 3.10–3.12](https://img.shields.io/badge/python-3.10--3.12-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

OpenBIMxD is an open-source Python library for interacting with IFC BIM models as part of scan-to-BIM workflows. It provides tools for building IFC file structures from scratch, creating IFC elements from reconstructed geometry, filtering models, assigning semantic labels to point clouds from IFC geometry, and updating existing IFC objects.

OpenBIMxD is built on [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell). We recommend [BlenderBIM](https://blenderbim.org/) from the same ecosystem for visualization.

> **Work in progress.** The API is not yet stable and may change between releases.

## Features

- **ifcfile** — Build an IFC model with a full project/site/building/storey hierarchy
- **elements** — Create `IfcWall`, `IfcColumn`, and `IfcDoor` objects from bounding boxes
- **ifcmaterial** — Create and assign IFC materials to elements
- **filtering** — Filter IFC objects by class, attributes, and spatial relationships; export the result as a new IFC file
- **geometry** — Utility for fitting bounding boxes to IfcOpenShell vertex arrays
- **ifctolabel** — Assign semantic labels to a point cloud using IFC element geometry
- **ifcupdate** — Update an IFC object's placement, material, and property sets
- **parsers** — Extract opening geometry parameters and serialize to JSON

## Installation

```shell
pip install git+https://github.com/humantecheu/openbimxd.git
```

For development (editable install from a local clone):

```shell
git clone https://github.com/humantecheu/openbimxd.git
cd openbimxd
pip install -e .
```

> **Python 3.10–3.12 only.** Inherited from the [pystruct3d](https://github.com/humantecheu/pystruct3d) dependency (Open3D does not yet ship wheels for Python 3.13+).

## Acknowledgement

This research was funded by the European Union as part of the HumanTech project (Grant Agreement 101058236).

## License

MIT License. See [LICENSE](LICENSE) for details.
