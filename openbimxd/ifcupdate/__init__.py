"""
Update an IFC object. Updates the location, material or properties.

CLASSES
    UpdateIfcObject
        A class to update IFC objects. The updated objects are saved as a new file.

FUNCTIONS
    __init__(self, model, ifc_object) -> None
        Initializes an UpdateIfcObject object
    update_location(self, origin: np.ndarray, angle: float) -> None
        Update the location and angle of an the IfcLocalPlacement.
    update_material(self, ifc_material) -> None
        Update the IfcMaterial.
    update_property(self, pset_name: str, pset_dict: dict) -> None
        Updates the property set of an object. Either adds a new property
        set or updates the existing one, if one with same name as existing
        is given.
"""
