bl_info = {"name": "Export Decentraland", "category": "Development"}

import bpy
import os
import shutil
from bpy.types import Operator


def export_to_dcl():
    
    # export to blend file location
    basedir = os.path.dirname(bpy.data.filepath)

    if not basedir:
        raise Exception("Blend file is not saved")

    #create directories
    export_path = os.path.join(basedir, "export")
    
    if os.path.exists(export_path):
        shutil.rmtree(export_path)
        
    os.makedirs(export_path)

    models_path = os.path.join(export_path, "models")
    

    
    
    if not os.path.exists(models_path):
        os.makedirs(models_path)


    scene = bpy.context.scene
    obj_active = scene.objects.active
    selection = bpy.context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    xml = "<a-scene>\n"


    for o in bpy.data.objects:
        
        if o.hide == False:
            o.select = True
            # some exporters only use the active object
            scene.objects.active = o

            name = bpy.path.clean_name(o.name)
            fn = os.path.join(models_path, name)

            bpy.ops.export_scene.obj(filepath=fn + ".obj", use_selection=True)
            o.select = False

            model = "  <a-obj-model"
            model += " position=\"{0} {1} {2}\" ".format(*[5,0,5]) #(*o.location)
            model += " scale=\"{0} {1} {2}\" ".format(*[0.5,0.5,0.5]) #(*o.scale)
            model += " rotation=\"{0} {1} {2}\" ".format(*[0,0,0]) #(*o.rotation_euler)
            model += " obj-model=\"obj:models/{0}.obj; mtl:models/{0}.mtl\">".format(name)
            model += "</a-obj-model>\n"
            xml += model

    xml += "</a-scene>\n"

    fn = os.path.join(export_path, "scene.xml")
    f = open(fn, 'w', encoding='utf-8')
    f.write(xml)
    f.close()

    scene.objects.active = obj_active

    for o in selection:
        o.select = True

    return {'FINISHED'}


class ExportDecentraland(Operator):
    """This will generate and export folder next to your blend file with a whole deentraland scene"""
    bl_idname = "diegodorado.export_decentraland"
    bl_label = "Export Decentraland"

    def execute(self, context):
        return export_to_dcl()


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportDecentraland.bl_idname, text="Export to Decentraland")


def register():
    bpy.utils.register_class(ExportDecentraland)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportDecentraland)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()







