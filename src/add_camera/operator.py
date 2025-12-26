import bpy
import math
from mathutils import Vector
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_add_camera(bpy.types.Operator):
    """Add a camera with preset resolution and frame selected object"""
    bl_idname = "search_extension.add_camera"
    bl_label = "Add Camera" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    resolution_preset: bpy.props.EnumProperty(
        name="Resolution",
        description="Select a resolution preset",
        items=[
            ('1024x1024', "1024×1024", "Square (Default)"),
            ('1920x1080', "1920×1080", "Full HD 16:9"),
            ('1080x1920', "1080×1920", "Portrait 9:16"),
            ('2048x2048', "2048×2048", "Square 2K"),
            ('3840x2160', "3840×2160", "4K 16:9"),
            ('1024x1792', "1024×1792", "Portrait ~9:16 (AI)"),
            ('1792x1024', "1792×1024", "Landscape ~16:9 (AI)"),
        ],
        default='1024x1024'
    )

    rotation_x: bpy.props.FloatProperty(
        name="Rotation X",
        description="Camera rotation around X axis",
        default=math.radians(90),
        min=math.radians(-180),
        max=math.radians(180),
        subtype='ANGLE'
    )

    rotation_y: bpy.props.FloatProperty(
        name="Rotation Y",
        description="Camera rotation around Y axis",
        default=0.0,
        min=math.radians(-180),
        max=math.radians(180),
        subtype='ANGLE'
    )

    rotation_z: bpy.props.FloatProperty(
        name="Rotation Z",
        description="Camera rotation around Z axis",
        default=0.0,
        min=math.radians(-180),
        max=math.radians(180),
        subtype='ANGLE'
    )

    location_x: bpy.props.FloatProperty(
        name="Location X",
        description="Camera location X coordinate",
        default=0.0,
        subtype='DISTANCE'
    )

    location_y: bpy.props.FloatProperty(
        name="Location Y",
        description="Camera location Y coordinate",
        default=-4.0,
        subtype='DISTANCE'
    )

    location_z: bpy.props.FloatProperty(
        name="Location Z",
        description="Camera location Z coordinate",
        default=0.0,
        subtype='DISTANCE'
    )

    def draw(self, context):
        layout = self.layout
        
        # Resolution presets section
        layout.label(text="Resolution Presets:")
        
        # Create grid layout for resolution buttons
        grid = layout.grid_flow(row_major=True, columns=2, align=True)
        
        # Display each resolution preset as a button
        grid.prop_enum(self, "resolution_preset", '1024x1024')
        grid.prop_enum(self, "resolution_preset", '1920x1080')
        grid.prop_enum(self, "resolution_preset", '1080x1920')
        grid.prop_enum(self, "resolution_preset", '2048x2048')
        grid.prop_enum(self, "resolution_preset", '3840x2160')
        grid.prop_enum(self, "resolution_preset", '1024x1792')
        grid.prop_enum(self, "resolution_preset", '1792x1024')
        
        layout.separator()
        
        # Rotation controls
        layout.label(text="Camera Rotation:")
        col = layout.column(align=True)
        col.prop(self, "rotation_x")
        col.prop(self, "rotation_y")
        col.prop(self, "rotation_z")

        layout.separator()

        # Location controls
        layout.label(text="Camera Location:")
        col = layout.column(align=True)
        col.prop(self, "location_x")
        col.prop(self, "location_y")
        col.prop(self, "location_z")

    def execute(self, context):
        # Parse resolution
        width, height = map(int, self.resolution_preset.split('x'))
        
        # Set render resolution
        context.scene.render.resolution_x = width
        context.scene.render.resolution_y = height
        
        # Add camera
        bpy.ops.object.camera_add()
        camera = context.active_object
        
        # Set rotation
        camera.rotation_euler = (self.rotation_x, self.rotation_y, self.rotation_z)
        
        # Get selected objects (excluding the newly created camera)
        selected_objects = [obj for obj in context.selected_objects if obj != camera]
        
        if selected_objects:
            # Calculate bounding box of all selected objects
            min_coord = Vector((float('inf'), float('inf'), float('inf')))
            max_coord = Vector((float('-inf'), float('-inf'), float('-inf')))
            
            for obj in selected_objects:
                # Get world space bounding box corners
                bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                
                for corner in bbox_corners:
                    min_coord.x = min(min_coord.x, corner.x)
                    min_coord.y = min(min_coord.y, corner.y)
                    min_coord.z = min(min_coord.z, corner.z)
                    max_coord.x = max(max_coord.x, corner.x)
                    max_coord.y = max(max_coord.y, corner.y)
                    max_coord.z = max(max_coord.z, corner.z)
            
            # Calculate center and size
            center = (min_coord + max_coord) / 2
            size = (max_coord - min_coord).length
            
            # Calculate camera distance based on object size and FOV
            camera_data = camera.data
            fov = camera_data.angle
            distance = (size / 2) / math.tan(fov / 2) * 1.5  # 1.5 for some padding
            
            # Calculate camera position based on rotation
            # Create a direction vector pointing forward from the camera
            direction = Vector((0, 0, -1))
            direction.rotate(camera.rotation_euler)
            
            # Position camera at distance from center, opposite to direction
            camera.location = center - (direction * distance)
            
            # Point camera at center
            direction_to_target = center - camera.location
            rot_quat = direction_to_target.to_track_quat('-Z', 'Y')
            camera.rotation_euler = rot_quat.to_euler()
            
            # Apply the user's rotation on top
            camera.rotation_euler.x += self.rotation_x
            camera.rotation_euler.y += self.rotation_y
            camera.rotation_euler.z += self.rotation_z
            
            self.report({'INFO'}, f"Camera added at {width}×{height}, framing selected object(s)")
        else:
            # No object selected, use specified location
            camera.location = (self.location_x, self.location_y, self.location_z)
            self.report({'INFO'}, f"Camera added at {width}×{height} at ({self.location_x:.2f}, {self.location_y:.2f}, {self.location_z:.2f})")
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
