"""Atlas texture preset prompts for texture generation."""

# Preset prompts for Atlas mode
# Each preset has a name, description, and prompt text
ATLAS_PRESETS = [
    {
        "id": "tileable_stone",
        "name": "Tileable Stone",
        "description": "Seamless stone texture",
        "prompt": "Create a seamless tileable stone texture. Natural rock surface with realistic cracks and variations. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "tileable_wood",
        "name": "Tileable Wood",
        "description": "Seamless wood plank texture",
        "prompt": "Create a seamless tileable wood plank texture. Natural wood grain with realistic knots and color variation. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "tileable_brick",
        "name": "Tileable Brick",
        "description": "Seamless brick wall texture",
        "prompt": "Create a seamless tileable red brick wall texture with mortar joints. Realistic weathering and color variation. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "tileable_metal",
        "name": "Tileable Metal",
        "description": "Seamless metal plate texture",
        "prompt": "Create a seamless tileable brushed metal plate texture. Industrial steel with subtle scratches and wear. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "tileable_fabric",
        "name": "Tileable Fabric",
        "description": "Seamless fabric texture",
        "prompt": "Create a seamless tileable fabric texture. Woven cloth material with realistic thread detail. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "tileable_grass",
        "name": "Tileable Grass",
        "description": "Seamless grass ground texture",
        "prompt": "Create a seamless tileable grass ground texture from top-down view. Lush green grass with realistic variation. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "tileable_concrete",
        "name": "Tileable Concrete",
        "description": "Seamless concrete texture",
        "prompt": "Create a seamless tileable concrete texture. Smooth cement surface with subtle cracks and stains. High detail, photorealistic, suitable for 3D game textures. Edges must tile perfectly.",
    },
    {
        "id": "character_skin",
        "name": "Character Skin Atlas",
        "description": "Character skin texture atlas",
        "prompt": "Create a character skin texture atlas for a humanoid 3D model. Include face, body, and limb regions. Realistic human skin tones with subtle detail. Suitable for UV unwrapped character mesh.",
    },
    {
        "id": "stylized_toon",
        "name": "Stylized Toon",
        "description": "Cartoon style texture",
        "prompt": "Create a stylized cartoon texture atlas. Flat colors with cel-shading style. Bold outlines and vibrant colors. Suitable for anime/toon style 3D models.",
    },
    {
        "id": "scifi_panel",
        "name": "Sci-Fi Panel",
        "description": "Futuristic panel texture",
        "prompt": "Create a seamless tileable sci-fi metal panel texture. Futuristic design with glowing elements, rivets, and tech details. Cyberpunk aesthetic. High detail, suitable for 3D game textures.",
    },
]


def get_preset_by_id(preset_id):
    """Get a preset by its ID.
    
    Args:
        preset_id: Preset identifier string
        
    Returns:
        dict: Preset data or None if not found
    """
    for preset in ATLAS_PRESETS:
        if preset["id"] == preset_id:
            return preset
    return None


def get_preset_enum_items():
    """Get presets as Blender EnumProperty items.
    
    Returns:
        list: List of (id, name, description) tuples
    """
    items = [("NONE", "Select Preset...", "Choose a preset prompt")]
    for preset in ATLAS_PRESETS:
        items.append((preset["id"], preset["name"], preset["description"]))
    return items
