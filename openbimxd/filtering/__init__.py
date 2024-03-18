# openbimxd - open source tools to interact with IFC files
# Copyright (C) 2024, 2024 the HumanTech project
# Main contributors: Fabian Kaufmann fabian.kaufmann@rptu.de
#           Marius Schellen marius.schellen@rptu.de
#           Mahdi Chamseddine mahdi.chamseddine@dfki.de
#
# This file is part of openbimxd
#
# openbimxd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# openbimxd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openbimxd.  If not, see <http://www.gnu.org/licenses/>.
#
# This project uses IfcOpenShell <https://blenderbim.org/>, all credits to
# Dion Moult for his great work

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
