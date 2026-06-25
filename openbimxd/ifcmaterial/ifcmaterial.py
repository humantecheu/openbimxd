# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Create and assign IFC materials (concrete, CLT)."""

import ifcopenshell.api.material


class IfcMaterials:
    """Create and represent a set of IFC materials (concrete, CLT)."""

    def __init__(self, ifc_model) -> None:
        """Create concrete and CLT materials in the given IFC model.

        Args:
            ifc_model: The IfcOpenShell file object to add materials to.
        """
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
