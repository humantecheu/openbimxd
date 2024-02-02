import ifcopenshell
from ifcopenshell import file
import ifcopenshell.util as util
from ifcopenshell.api import run
from ifcopenshell.api import material
import ifcopenshell.util.selector
import time


class objectFilter:
    def __init__(self, ifc_model_path: str, filtered_model_path: str) -> None:
        self.ifc_model = ifcopenshell.open(ifc_model_path)
        self.filtered_model_path = filtered_model_path
        self.objects = []
        self.materials = self.ifc_model.by_type("IfcMaterial")
        self.material_sets = self.ifc_model.by_type("IfcMaterialLayerSet")
        self.filtered_model = file(schema=self.ifc_model.schema)
        print(f"Set up filtered model with schema: {self.ifc_model.schema}")
        if self.ifc_model.schema == "IFC2X3":
            print(f"Schema version: {self.ifc_model.schema}, no context ...")
        else:
            self.filtered_model.add(self.ifc_model.by_type("IfcContext")[0])
        prj = self.filtered_model.add(self.ifc_model.by_type("IfcProject")[0])

        for site in self.ifc_model.by_type("IfcSite"):
            new_site = self.filtered_model.add(site)
            run(
                "aggregate.assign_object",
                self.filtered_model,
                relating_object=prj,
                product=new_site,
            )
            for building in self.ifc_model.by_type("IfcBuilding"):
                new_building = self.filtered_model.add(building)
                run(
                    "aggregate.assign_object",
                    self.filtered_model,
                    relating_object=new_site,
                    product=new_building,
                )

                for st in self.ifc_model.by_type("IfcBuildingStorey"):
                    new_st = self.filtered_model.add(st)
                    run(
                        "aggregate.assign_object",
                        self.filtered_model,
                        relating_object=new_building,
                        product=new_st,
                    )

    def filter_objects(self, search_str: str):
        """Filter objects of a specific class and other attributes and properties.
        Uses the IfcOpenShell selector class.
        Typical search_str: "IfcWall", ore more advanced: "IfcWall, Name=FOO"
        Options for search strings:
        https://blenderbim.org/docs-python/ifcopenshell-python/selector_syntax.html

        Args:
            search_str (str): string with search parameters: IFC Class, name, ...
        """
        self.objects = util.selector.filter_elements(self.ifc_model, search_str)
        print(f"{len(self.objects)} objects filtered")

        # TODO: useful for getting child elements

    def create_materials(self):
        new_mats = {}
        for m in self.materials:
            new = self.filtered_model.add(m)
            new_mats[new.Name] = new
        new_mat_sets = {}
        for mset in self.material_sets:
            new_set = self.filtered_model.add(mset)
            new_mat_sets[new_set.LayerSetName] = new_set
        return new_mats, new_mat_sets

    def assign_container(self, obj, new_obj):
        container_info = util.element.get_container(obj).get_info()
        new_container = list(
            util.selector.filter_elements(
                self.filtered_model,
                f"{container_info.get('type')}, Name={container_info.get('Name')}",
            )
        )
        run(
            "spatial.assign_container",
            self.filtered_model,
            relating_structure=new_container[0],
            product=new_obj,
        )

    def assign_opening(self, obj, new_obj):
        child_objects = util.element.get_decomposition(obj)
        for child in child_objects:
            if child.is_a("IfcOpeningElement"):
                new_opening = self.filtered_model.add(child)
                run(
                    "void.add_opening",
                    self.filtered_model,
                    opening=new_opening,
                    element=new_obj,
                )

    def assign_material(self, obj, new_obj, new_mats, new_mat_sets):
        # BUG: get material layer sets
        material = util.element.get_material(obj)
        try:
            if material.is_a("IfcMaterial"):
                # print(f"Assign new material {new_mats.get(material.Name)}")
                run(
                    "material.assign_material",
                    self.filtered_model,
                    product=new_obj,
                    material=new_mats.get(material.Name),
                )

            elif material.is_a("IfcMaterialLayerSetUsage"):
                # print(
                #     f"IfcMaterialLayerSetUsage, assign new material layer set {new_mat_sets.get(material[0].LayerSetName)}"
                # )
                run(
                    "material.assign_material",
                    self.filtered_model,
                    product=new_obj,
                    material=new_mat_sets.get(material[0].LayerSetName),
                )
            elif material.is_a("IfcMaterialLayerSet"):
                # print(
                #     f"IfcMaterialLayerSet, assign new material layer set {new_mat_sets.get(material.LayerSetName)}"
                # )
                run(
                    "material.assign_material",
                    self.filtered_model,
                    product=new_obj,
                    material=new_mat_sets.get(material.LayerSetName),
                )
        except TypeError:
            print("Material is NoneType, passing")
        except AttributeError:
            print("Material is NoneType, passing")

    def assign_psets(self, obj, new_obj):
        # get property set from old
        psets = util.element.get_psets(obj)
        for k in list(psets.keys()):
            # assign property set
            # if k == "AllplanAttributes":

            pset = run(
                "pset.add_pset",
                self.filtered_model,
                product=new_obj,
                name=k,
            )
            p_dict = psets.get(k)
            # fix ThermalTransmittance in IFC2X3 breaking
            if (
                self.filtered_model.schema == "IFC2X3"
                and "ThermalTransmittance" in p_dict.keys()
            ):
                print(
                    "Set ThermalTransmittance value to None in IFC2X3 to avoid errors"
                )
                # workaround: set to None to avoid errors
                p_dict["ThermalTransmittance"] = None
                run(
                    "pset.edit_pset",
                    self.filtered_model,
                    pset=pset,
                    properties=p_dict,
                )

            else:
                run(
                    "pset.edit_pset",
                    self.filtered_model,
                    pset=pset,
                    properties=p_dict,
                )

    def export_model(self):
        new_mats, new_mat_sets = self.create_materials()
        for i, obj in enumerate(self.objects):
            # if obj.is_a("IfcElementAssembly"):
            #     print(util.element.get_decomposition(obj))
            new_obj = self.filtered_model.add(obj)
            self.assign_material(obj, new_obj, new_mats, new_mat_sets)
            self.assign_psets(obj, new_obj)
            self.assign_opening(obj, new_obj)
            if util.element.get_container(obj) is not None:
                self.assign_container(obj, new_obj)

            if i % 100 == 0:
                print(f"{i} / {len(self.objects)} processed")

        print(f"Write filtered IFC file: {self.filtered_model_path}")
        self.filtered_model.write(self.filtered_model_path)


def main():
    start = time.perf_counter()
    # /home/kaufmann/Desktop/ifcs_from_hell/SCE-ZBG-BI-9-M211-A0-XXX-00-00-P-0.ifc
    # HT_DFKI_BA3_4thfloor.ifc
    # AC20-FZK-Haus.ifc
    # scene = "AC20-FZK-Haus.ifc"
    # scene = "slab_test.ifc"
    scene = (
        "/home/kaufmann/Desktop/ifcs_from_hell/SCE-ZBG-BI-9-M211-A0-XXX-00-00-P-0.ifc"
    )
    of = objectFilter(scene, f"{scene[:-4]}_filtered.ifc")
    of.filter_objects("IfcSlab, IfcBeam")
    of.export_model()
    execution_time = time.perf_counter() - start
    execution_mins = execution_time / 60
    print(f"Finished processing in {execution_time:.2f} s ~ {execution_mins:.2f} min")


if __name__ == "__main__":
    main()
