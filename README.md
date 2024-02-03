# OpenBIMxD

## Summary
OpenBIMxD offers methods to 
- Set up and create an IFC file with basic hierarchty, 
- Create IFC objects from reconstructed semantics and geometry
- Filter IFC objects
- assign semantic labels to a point cloud based on IFC objects' geometry
- Update IFC objects' location, rotation, material and properties

All methods in OpenBIMxD use https://github.com/IfcOpenShell/IfcOpenShell to interact with IFC files. All credits to Thomas Krijnen and all contributors for this great library. We recommend to use https://blenderbim.org/ from the same ecosystem to visualize whatever you have created using OpenBIMxD. 

OpenBIMxD is still under development, thus you might have to play with the code yourself to achieve the results you need. Or you take it as an inspiration to write your own stuff. 

OpenBIMxD is part of the HumanTech project. The development was funded by the European Union under grant agreement No. 101058236. 

## Installation

It is recommended to us a python virtual environment. First, set one up using

`python3 -m venv /path/to/new/virtual/environment`

and activate your environment. 

Then, from the active environment and /some/path/to/openbimxd, clone this repo and 

`python3 -m pip install -e`

Use the -e flag in case you want to change some contents of the package to your needs. 


## Dependencies 

### General

| **Name**      | **version**       |
|---------------|-------------------|
| ifcopenshell  | 0.7.0             |
| numpy         | 1.25.2            |
| scipy         | 1.11.2            |

### For Ifc to Label module

| **Name**      | **version**       |
|---------------|-------------------|
| pystruct3d    | 0.1               |

For installation instructions, see: https://github.com/humantecheu/pystruct3d

# Usage

In all modules the main function can be used to test the functionality. Download the sample files before: https://seafile.rlp.net/d/d944c03d4d444dfb9e60/ and place the files in /some/path/to/openbimxd. 

