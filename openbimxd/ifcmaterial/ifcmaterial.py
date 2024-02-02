import ifcopenshell


class IfcMaterials:
    def __init__(self, ifc_model) -> None:
        self.concrete = ifcopenshell.api.run(
            "material.add_material", ifc_model, name="CON01", category="concrete"
        )
        self.clt = ifcopenshell.api.run(
            "material.add_material", ifc_model, name="CLT", category="wood"
        )
