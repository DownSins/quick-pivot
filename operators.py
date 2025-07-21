import bpy
from bpy.types import Operator
from bpy.props import EnumProperty

class CustomPivotOperator(Operator):
    bl_idname = "view3d.custom_pivot"
    bl_label = "Custom Pivot"
    bl_options = {'REGISTER', 'UNDO'}

    pivot_action: EnumProperty(
        name="Pivot Action",
        items=[
            ('SET_CUSTOM', "Set Custom Pivot", "Use selected object/element to set pivot & orientation"),
            ('RESET_TO_ORIGIN', "Reset Orientation", "Switch back to global orientation"),
            ('CURSOR_TO_ACTIVE', "Cursor to Active", "Move 3D cursor to active object or element"),
            ('ORIGIN_TO_CURSOR', "Origin to Cursor", "Move object origin to 3D cursor"),
        ],
        default='SET_CUSTOM'
    )

    def draw(self, context):
        self.layout.prop(self, "pivot_action", expand=True)

    def execute(self, context):
        if self.pivot_action == 'SET_CUSTOM':
            return self.set_custom_pivot(context)
        elif self.pivot_action == 'RESET_TO_ORIGIN':
            return self.reset_orientation(context)
        elif self.pivot_action == 'CURSOR_TO_ACTIVE':
            return self.cursor_to_active(context)
        elif self.pivot_action == 'ORIGIN_TO_CURSOR':
            return self.origin_to_cursor(context)
        return {'CANCELLED'}

    def set_custom_pivot(self, context):
        import bmesh

        sel = context.selected_objects
        act = context.active_object
        if not sel or not act:
            self.report({'ERROR'}, "No selection.")
            return {'CANCELLED'}

        context.scene.transform_orientation_slots[0].type = 'GLOBAL'
        try:
            bpy.ops.transform.create_orientation(name="Custom", use=True, overwrite=True)
            context.scene.transform_orientation_slots[0].type = 'Custom'
        except RuntimeError:
            self.report({'ERROR'}, "Could not create custom orientation.")
            return {'CANCELLED'}

        self.report({'INFO'}, "Custom orientation set.")
        return {'FINISHED'}

    def reset_orientation(self, context):
        context.scene.transform_orientation_slots[0].type = 'GLOBAL'
        self.report({'INFO'}, "Orientation reset to Global.")
        return {'FINISHED'}

    def cursor_to_active(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object.")
            return {'CANCELLED'}

        try:
            bpy.ops.view3d.snap_cursor_to_active()
        except RuntimeError:
            self.report({'ERROR'}, "Failed to snap cursor.")
            return {'CANCELLED'}

        self.report({'INFO'}, "Cursor moved to active.")
        return {'FINISHED'}

    def origin_to_cursor(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object.")
            return {'CANCELLED'}

        prev_mode = obj.mode
        if prev_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        try:
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        except RuntimeError as e:
            self.report({'ERROR'}, str(e))
            if prev_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=prev_mode)
            return {'CANCELLED'}

        if prev_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=prev_mode)

        self.report({'INFO'}, "Origin moved to 3D cursor.")
        return {'FINISHED'}


class ToggleGizmoOperator(Operator):
    bl_idname = "view3d.toggle_gizmo"
    bl_label = "Toggle Gizmo"
    bl_options = {'REGISTER', 'UNDO'}

    gizmo_type: EnumProperty(
        name="Gizmo Type",
        items=[
            ('TRANSLATE', "Move", "Show Move Gizmo"),
            ('ROTATE', "Rotate", "Show Rotate Gizmo"),
            ('SCALE', "Scale", "Show Scale Gizmo"),
            ('ALL', "All", "Show all transform gizmos"),
        ],
        default='TRANSLATE',
    )

    def draw(self, context):
        self.layout.prop(self, "gizmo_type", expand=True)

    def invoke(self, context, event):
        last_type = context.scene.get("last_gizmo_type", "TRANSLATE")
        self.gizmo_type = last_type

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space:
                    any_on = (
                        space.show_gizmo_object_translate or
                        space.show_gizmo_object_rotate or
                        space.show_gizmo_object_scale
                    )

                    space.show_gizmo_object_translate = False
                    space.show_gizmo_object_rotate = False
                    space.show_gizmo_object_scale = False

                    if not any_on:
                        if last_type == 'TRANSLATE':
                            space.show_gizmo_object_translate = True
                        elif last_type == 'ROTATE':
                            space.show_gizmo_object_rotate = True
                        elif last_type == 'SCALE':
                            space.show_gizmo_object_scale = True
                        elif last_type == 'ALL':
                            space.show_gizmo_object_translate = True
                            space.show_gizmo_object_rotate = True
                            space.show_gizmo_object_scale = True
                break
        else:
            self.report({'WARNING'}, "No 3D View found.")

        return {'FINISHED'}

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space:
                    space.show_gizmo_object_translate = False
                    space.show_gizmo_object_rotate = False
                    space.show_gizmo_object_scale = False

                    if self.gizmo_type == 'TRANSLATE':
                        space.show_gizmo_object_translate = True
                    elif self.gizmo_type == 'ROTATE':
                        space.show_gizmo_object_rotate = True
                    elif self.gizmo_type == 'SCALE':
                        space.show_gizmo_object_scale = True
                    elif self.gizmo_type == 'ALL':
                        space.show_gizmo_object_translate = True
                        space.show_gizmo_object_rotate = True
                        space.show_gizmo_object_scale = True
                break
        else:
            self.report({'WARNING'}, "No 3D View found.")

        context.scene["last_gizmo_type"] = self.gizmo_type
        self.report({'INFO'}, f"Gizmo set to {self.gizmo_type}")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CustomPivotOperator)
    bpy.utils.register_class(ToggleGizmoOperator)

def unregister():
    bpy.utils.unregister_class(CustomPivotOperator)
    bpy.utils.unregister_class(ToggleGizmoOperator)
