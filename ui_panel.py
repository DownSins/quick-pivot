import bpy

class QUICKPIVOT_PT_Panel(bpy.types.Panel):
    bl_label = "Quick Pivot"
    bl_idname = "QUICKPIVOT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pivot"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set Pivot Mode:")
        layout.operator("view3d.quick_pivot", text="Bounding Box").pivot_mode = 'BOUNDING_BOX_CENTER'
        layout.operator("view3d.quick_pivot", text="Cursor").pivot_mode = 'CURSOR'
        layout.operator("view3d.quick_pivot", text="Individual Origins").pivot_mode = 'INDIVIDUAL_ORIGINS'
        layout.operator("view3d.quick_pivot", text="Median Point").pivot_mode = 'MEDIAN_POINT'
        layout.operator("view3d.quick_pivot", text="Active Element").pivot_mode = 'ACTIVE_ELEMENT'

        layout.separator()
        layout.operator("view3d.toggle_gizmo", text="Toggle Gizmo")

def register():
    bpy.utils.register_class(QUICKPIVOT_PT_Panel)

def unregister():
    bpy.utils.unregister_class(QUICKPIVOT_PT_Panel)
