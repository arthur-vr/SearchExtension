"""Async texture generation management."""

import bpy
import os
import threading
from .api_client import call_gemini_api
from .image_utils import save_image_to_blender, set_image_active_in_editor, build_texture_name
from .material_utils import create_material_with_texture

# Global state for async generation
_generation_state = {
    'running': False,
    'result': None,
    'error': None,
    'source_obj': None,
    'temp_files': [],
    'texture_prefix': "nanobanana_texture",
    'append_timestamp': True,
    'progress_count': 0,
    'model': '',
}


def async_generate_texture(api_key, model, prompt, image_references):
    """Run texture generation in a background thread.

    Args:
        api_key: Google Gemini API key
        model: Model name to use
        prompt: Text prompt for generation
        image_references: List of reference dicts
    """
    global _generation_state

    try:
        response = call_gemini_api(api_key, model, prompt, image_references)
        _generation_state['result'] = response
        _generation_state['error'] = None
    except Exception as e:
        _generation_state['result'] = None
        _generation_state['error'] = str(e)
    finally:
        _generation_state['running'] = False


def _update_progress():
    """Update progress bar animation."""
    global _generation_state
    
    if not _generation_state['running']:
        return None  # Stop timer
    
    # Increment progress continuously (will be modulo'd by Blender internally)
    _generation_state['progress_count'] += 1
    
    try:
        wm = bpy.context.window_manager
        # Large max value so progress keeps incrementing
        wm.progress_update(_generation_state['progress_count'])
    except:
        pass
    
    return 0.1  # Update every 100ms


def check_generation_progress():
    """Timer callback to check if generation is complete.

    Returns:
        float or None: Seconds until next check, or None to stop timer
    """
    global _generation_state

    if not _generation_state['running']:
        # Generation complete - end progress bar
        def end_progress():
            try:
                wm = bpy.context.window_manager
                wm.progress_end()
            except:
                pass
            
            # Clear status text
            try:
                bpy.context.workspace.status_text_set(None)
            except:
                pass
        
        bpy.app.timers.register(end_progress, first_interval=0.0)
        
        # Process result
        if _generation_state['error']:
            # Show error
            def show_error():
                bpy.ops.nanobanana.show_message(
                    'INVOKE_DEFAULT',
                    message_type='ERROR',
                    message=f"API Error: {_generation_state['error']}"
                )
            bpy.app.timers.register(show_error, first_interval=0.0)
        elif _generation_state['result']:
            # Process successful result
            def process_result():
                try:
                    response = _generation_state['result']
                    source_obj = _generation_state['source_obj']
                    temp_files = _generation_state.get('temp_files', [])

                    # Extract generated image
                    generated_image = None
                    text_description = None

                    if 'candidates' in response and len(response['candidates']) > 0:
                        candidate = response['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            for part in candidate['content']['parts']:
                                if 'inlineData' in part or 'inline_data' in part:
                                    inline_data = part.get('inlineData') or part.get('inline_data')
                                    if inline_data and 'data' in inline_data:
                                        image_data = inline_data['data']
                                        texture_prefix = _generation_state.get('texture_prefix') or "nanobanana_texture"
                                        append_ts = bool(_generation_state.get('append_timestamp', True))
                                        image_name = build_texture_name(texture_prefix, append_timestamp=append_ts)
                                        generated_image = save_image_to_blender(image_data, image_name)

                                if 'text' in part:
                                    text_description = part['text']

                    if generated_image:
                        # Add to history on successful generation
                        if _generation_state.get('history_info'):
                            # Use singleton storage for consistency
                            from .operator import _get_persistent_storage
                            storage = _get_persistent_storage()
                            hist_info = _generation_state['history_info']
                            prompt_to_save = hist_info.get('prompt', '')
                            print(f"[NanoBanana] Saving to history - prompt length: {len(prompt_to_save)}")
                            storage.add_prompt_to_history(
                                prompt=prompt_to_save,
                                negative_prompt="",
                                model_version=hist_info['model_version'],
                                seed=hist_info['seed'],
                                reference_info=hist_info['reference_info']
                            )
                            _generation_state['history_info'] = None

                        set_image_active_in_editor(generated_image)

                        # Apply texture to source object if it still exists
                        if source_obj:
                            # Check if object still exists in scene
                            try:
                                # Verify object is still valid
                                obj_name = source_obj.name
                                print(f"[NanoBanana] Attempting to apply texture to: {obj_name}")

                                if obj_name in bpy.data.objects:
                                    obj = bpy.data.objects[obj_name]
                                    print(f"[NanoBanana] Object found, type: {obj.type}")

                                    if obj.type == 'MESH':
                                        print(f"[NanoBanana] Creating material with texture...")
                                        mat = create_material_with_texture(obj, generated_image)
                                        print(f"[NanoBanana] Material created: {mat.name}")
                                        print(f"[NanoBanana] Texture successfully applied to {obj_name}")
                                    else:
                                        print(f"[NanoBanana] Object {obj_name} is no longer a mesh")
                                else:
                                    print(f"[NanoBanana] Object {obj_name} was deleted")
                            except Exception as e:
                                print(f"[NanoBanana] ERROR: Could not apply texture to object: {str(e)}")
                                import traceback
                                traceback.print_exc()
                        else:
                            print("[NanoBanana] No source object stored - texture will not be applied to object")

                        if text_description:
                            print(f"\n=== NanoBanana Generation Notes ===")
                            print(text_description)
                            print(f"===================================\n")

                        bpy.ops.nanobanana.show_message(
                            'INVOKE_DEFAULT',
                            message_type='INFO',
                            message="Texture generation complete!"
                        )
                    else:
                        bpy.ops.nanobanana.show_message(
                            'INVOKE_DEFAULT',
                            message_type='ERROR',
                            message="No image was generated by the API"
                        )

                    # Cleanup temp files
                    for temp_file in temp_files:
                        if temp_file and os.path.exists(temp_file):
                            try:
                                os.remove(temp_file)
                            except OSError:
                                pass

                    # Reset state
                    _generation_state['result'] = None
                    _generation_state['source_obj'] = None
                    _generation_state['temp_files'] = []

                except Exception as e:
                    print(f"Error processing result: {str(e)}")
                    import traceback
                    traceback.print_exc()

            bpy.app.timers.register(process_result, first_interval=0.0)

        # Don't repeat this timer
        return None

    # Check again in 0.5 seconds
    return 0.5


def start_generation(api_key, model, prompt, image_references, source_obj, temp_files, texture_prefix, append_timestamp, history_info):
    """Start async texture generation.

    Args:
        api_key: Google Gemini API key
        model: Model name to use
        prompt: Text prompt for generation
        image_references: List of reference dicts ({'path': ..., 'type': ...})
        source_obj: Source Blender object
        temp_files: List of temporary files to cleanup
        texture_prefix: Prefix for generated texture
        append_timestamp: Whether to append timestamp to texture name
        history_info: History information to save

    Raises:
        RuntimeError: If generation already running
    """
    global _generation_state

    if _generation_state['running']:
        raise RuntimeError("Generation already in progress. Please wait...")

    _generation_state['running'] = True
    _generation_state['result'] = None
    _generation_state['error'] = None
    _generation_state['source_obj'] = source_obj
    _generation_state['temp_files'] = temp_files or []
    _generation_state['texture_prefix'] = (texture_prefix or "nanobanana_texture").strip() or "nanobanana_texture"
    _generation_state['append_timestamp'] = bool(append_timestamp)
    _generation_state['history_info'] = history_info
    _generation_state['progress_count'] = 0
    _generation_state['model'] = model

    try:
        wm = bpy.context.window_manager
        wm.progress_begin(0, 10000)
        wm.progress_update(0)
    except Exception as e:
        print(f"[NanoBanana] Could not start progress bar: {e}")

    # Set status text
    try:
        bpy.context.workspace.status_text_set(f"NanoBanana: Generating texture with {model}...")
    except:
        pass

    print(f"[NanoBanana] Starting generation with {model}...")

    # Start progress animation timer
    bpy.app.timers.register(_update_progress, first_interval=0.1)

    # Start background thread
    thread = threading.Thread(
        target=async_generate_texture,
        args=(api_key, model, prompt, image_references)
    )
    thread.daemon = True
    thread.start()

    # Start timer to check progress
    bpy.app.timers.register(check_generation_progress, first_interval=0.5)


def is_generation_running():
    """Check if generation is currently running.

    Returns:
        bool: True if generation is running
    """
    return _generation_state['running']
