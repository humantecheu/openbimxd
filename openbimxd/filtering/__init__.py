"""
Filter objects based on their IFC class, attributes, semantic and spatial relationships. 

CLASSES
    objectFilter
        class objects are used to open an IFC file, filter objects and export the IFC file
FUNCTIONS
    __init__(self, ifc_model_path: str, filtered_model_path: str) -> None
        Initialize the objectFilter object
    filter_objects(self, search_str: str)
        Filter objects with a given search string. Uses the IfcOpenShell selector 
        syntax: https://blenderbim.org/docs-python/ifcopenshell-python/selector_syntax.html
    create_materials(self):
        Gets all materials from original file and adds them to the filtered file
    assign_container(self, obj, new_obj)
        Assigns the spatioal container e.g., the building storey of an object
    assign_opening(self, obj, new_obj)
        Gets and assigns all openings of a parent object. Only the openings, no elements 
        inside the opening such as windows, doors, etc.
    assign_material(self, obj, new_obj, new_mats, new_mat_sets)
        Assigns the materials created in create_materials() to the filtered objects
    assign_psets(self, obj, new_obj)
        Gets and assigns property sets. This is sensitive to IFC schema versions, so be 
        careful!
    export_model(self)
        Executes the filtering and assignments and saves the filtered model. 
"""
