"""Gemini API client for texture generation."""

import base64
import json
import os
import urllib.request
import urllib.parse
import urllib.error


def _get_mime_type(image_path):
    """Get MIME type from file extension.

    Args:
        image_path: Path to image file

    Returns:
        str: MIME type string
    """
    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.heic': 'image/heic',
        '.heif': 'image/heif'
    }
    return mime_types.get(ext, 'image/png')


def call_gemini_api(api_key, model, prompt, image_references):
    """Call Gemini API with image generation support.

    Args:
        api_key: Google Gemini API key
        model: Model name to use
        prompt: Text prompt for generation
        image_references: List of reference dicts ({'path': ..., 'type': ...})

    Returns:
        dict: API response

    Raises:
        Exception: If API call fails
    """
    # Validate image count
    if len(image_references) > 14:
        raise Exception("Maximum 14 reference images allowed")

    if len(image_references) == 0:
        raise Exception("At least one reference image is required")

    # Build parts list - SIMPLIFIED
    parts = []

    # 1. Simple instruction if images exist
    parts.append({
        "text": "Use the following reference images for generation:"
    })

    # 2. Add images (no extra instructions per image)
    for ref in image_references:
        # Backward compatibility
        if isinstance(ref, str):
            image_path = ref
        else:
            image_path = ref.get('path')

        if not image_path:
            continue

        # Image Part only
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        mime_type = _get_mime_type(image_path)
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": image_data
            }
        })

    # 3. User's prompt directly
    parts.append({
        "text": prompt
    })

    # Build request payload with image generation config
    payload = {
        "contents": [{
            "parts": parts
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }

    # Log payload (text only to avoid spamming console with base64)
    debug_parts = []
    for p in parts:
        if 'text' in p:
            debug_parts.append(p)
        else:
            debug_parts.append({'inline_data': '<IMAGE DATA HIDDEN>'})
    print(f"[NanoBanana] API payload: {json.dumps({'contents': [{'parts': debug_parts}]}, ensure_ascii=False)}")

    # API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    # Make request
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise Exception(f"Connection error: {str(e)}")
