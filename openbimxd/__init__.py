"""Openbimxd is a module that allows you to setup a basic IFC file structure, create 
IFCs from reconstructed semantics and geometry, to filter IFC objects, to inherit
labels for point clouds from IFC objects and to update IFC objects

MODULES
    ifcfile
        Creates an IFC file with a specified schema and structure. 
    elements
        Create IFC objects from bounding boxes. By now, IfcWall, IfcDoor and IfcColumn 
        are implemented
    ifcmaterial
        Create a set of IFC materials to be assigned to objects
    ifctolabel
        Converts the geometry representatio of IFC objects into bounding boxes and 
        assigns the IfcClass to all points inside the respective bounding box. 
    ifcupdate
        Update attributes, properties and geometry of IFC objects. Preserves the GUID
        of the initial object
"""
