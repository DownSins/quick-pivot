bl_info = {
    "name": "Quick Pivot",
    "blender": (4, 3, 0),
    "category": "3D View",
    "author": "Down Sins",
    "version": (1, 0, 0),
    "location": "Hotkeys: D (Pivot), Shift+Q (Toggle Gizmo)",
    "description": "Control pivot orientation and gizmos with hotkeys and Redo Panel.",
    "wiki_url": "",
    "tracker_url": "",
}

import bpy
from . import operators

addon_keymaps = []

def register():
    operators.register()

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi_1 = km.keymap_items.new(operators.CustomPivotOperator.bl_idname, 'D', 'PRESS')
        kmi_2 = km.keymap_items.new(operators.ToggleGizmoOperator.bl_idname, 'Q', 'PRESS', shift=True)
        addon_keymaps.extend([(km, kmi_1), (km, kmi_2)])

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    operators.unregister()

if __name__ == "__main__":
    register()
