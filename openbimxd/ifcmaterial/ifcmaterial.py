# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project


import ifcopenshell.api.material


class IfcMaterials:
    """
    A class to create and represent IFC materials.

    Attributes:
        ifc_model : IfcModelBuilder object
    """

    def __init__(self, ifc_model) -> None:
        self.concrete = ifcopenshell.api.material.add_material(
            ifc_model,
            name="CON01",
            category="concrete",
        )
        self.clt = ifcopenshell.api.material.add_material(
            ifc_model,
            name="CLT",
            category="wood",
        )
