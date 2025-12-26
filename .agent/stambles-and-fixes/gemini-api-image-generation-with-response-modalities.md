## Stumbling Point

Calling the Gemini API only returned text responses, no images were generated.
The initial implementation didn't specify `responseModalities` in `generationConfig`, so the API defaulted to text-only responses.

## Solution

For Gemini 2.0+ models to generate images, the request payload must include:

```python
payload = {
    "contents": [{...}],
    "generationConfig": {
        "responseModalities": ["Text", "Image"]
    }
}
```

When extracting image data from responses, check these keys:
- `inlineData` or `inline_data` (varies by API version)
- Image data is base64-encoded in the `data` field

Reference: https://ai.google.dev/gemini-api/docs/image-generation
