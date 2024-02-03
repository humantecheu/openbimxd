import ifcopenshell


class IfcMaterials:
    """
    A class to create and represent IFC materials.

    Attributes:
        ifc_model : IfcModelBuilder object
    """

    def __init__(self, ifc_model) -> None:
        self.concrete = ifcopenshell.api.run(
            "material.add_material", ifc_model, name="CON01", category="concrete"
        )
        self.clt = ifcopenshell.api.run(
            "material.add_material", ifc_model, name="CLT", category="wood"
        )
