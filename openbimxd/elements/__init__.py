"""
Create IFC objects based on bouding box bbox objects from pystruct3d. Pystruct3d offers
basic geometric reconstruction algorithms to build your own scan to BIM pipeline. Refer to 
https://github.com/humantecheu/pystruct3d for more information. 

To create the IFC objects, you need an IFC file. Use ifcfile / IfcModelBuilder class to 
create it. 

MODULES / ClASSES
    ifcolumn / IfcColumn
        Create IfcColumn objects with round or square profile
    ifcdoor / IfcDoor
        Create IfcDoor objects with basic box-style geometry
    ifcwall / IfcWall
        Create IfcWall objects with box-style geometry
"""
