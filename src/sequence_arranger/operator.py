import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX


def is_prime(n):
    """Check if n is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def get_fibonacci_set(limit):
    """Get set of Fibonacci numbers up to limit."""
    fib_set = set()
    a, b = 0, 1
    while a <= limit:
        fib_set.add(a)
        a, b = b, a + b
    return fib_set


class SEARCHEXT_OT_sequence_arranger(bpy.types.Operator):
    """Arrange two objects based on a sequence (Prime or Fibonacci)"""
    bl_idname = "search_extension.sequence_arranger"
    bl_label = "Sequence Arranger" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    sequence_type: bpy.props.EnumProperty(
        name="Sequence Type",
        items=[
            ('PRIME', "Prime Numbers", "Object A at prime positions"),
            ('FIBONACCI', "Fibonacci Sequence", "Object A at Fibonacci positions"),
        ],
        default='PRIME'
    )

    count: bpy.props.IntProperty(
        name="Count",
        default=20,
        min=1,
        max=1000,
        description="Number of positions (1 to Count)"
    )

    spacing: bpy.props.FloatProperty(
        name="Spacing",
        default=2.0,
        min=0.1,
        description="Distance between positions"
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 2

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "sequence_type")
        layout.prop(self, "count")
        layout.prop(self, "spacing")

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'ERROR'}, "Please select at least 2 objects")
            return {'CANCELLED'}

        # Object A = sequence positions, Object B = non-sequence positions
        obj_a = selected[0]
        obj_b = selected[1]

        # Prepare sequence check function
        if self.sequence_type == 'PRIME':
            def is_in_sequence(n):
                return is_prime(n)
        else:
            fib_set = get_fibonacci_set(self.count + 1)
            def is_in_sequence(n):
                return n in fib_set

        # Create collection for arranged objects
        collection_name = f"SequenceArrangement_{self.sequence_type}"
        if collection_name in bpy.data.collections:
            # Remove existing collection
            old_collection = bpy.data.collections[collection_name]
            for obj in old_collection.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(old_collection)

        new_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(new_collection)

        # Place objects at each position
        created_objects = []
        for i in range(1, self.count + 1):
            x_pos = (i - 1) * self.spacing

            if is_in_sequence(i):
                source_obj = obj_a
            else:
                source_obj = obj_b

            # Create linked duplicate
            new_obj = source_obj.copy()
            new_obj.location = (x_pos, 0, 0)
            new_collection.objects.link(new_obj)
            created_objects.append(new_obj)

        # Select created objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in created_objects:
            obj.select_set(True)
        if created_objects:
            context.view_layer.objects.active = created_objects[0]

        self.report({'INFO'}, f"Created {len(created_objects)} instances")
        return {'FINISHED'}
