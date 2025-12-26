## Stumbling Point

Attempted to install the `google-generativeai` library from a Blender addon, but failed due to:
1. `subprocess.check_call([sys.executable, "-m", "pip", "install", "package"])` failed with permission errors
2. `pip install` after `ensurepip.bootstrap()` failed with temporary directory errors
3. Import errors persisted even after Blender restart

## Solution

Completely remove external library dependencies and call the Gemini API using only Python standard library:

```python
import urllib.request
import json
import base64

def call_gemini_api(api_key, model, prompt, image_path):
    # Base64 encode the image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # REST API request
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {
                    "mime_type": "image/png",
                    "data": image_data
                }}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    req = urllib.request.Request(url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))
```

Benefits:
- No installation required, works immediately
- No permission issues
- Cross-platform compatible

References:
- https://ai.google.dev/gemini-api/docs/image-generation
- Blender official: https://blender.stackexchange.com/questions/168448/bundling-python-library-with-addon
