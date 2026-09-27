# Textures, audio and advanced tools

[Home](../README.md) · [Projects and ISO building](PROJECTS_AND_TESTING.md)

## Replace a supported texture

1. Select the texture resource/pack.
2. Export its images as dimensions/reference.
3. Edit a PNG with the same width and height.
4. Choose **Replace image…** for the specific image.
5. Review the converted preview, palette/error information and limitations.
6. Click **Use this image**, save the project, and build a separate ISO.

Paletted images are converted into available native palette capacity. Supported smaller texture levels are regenerated. PS2 alpha representation can reduce precision. A colorful modern image can look different after palette conversion; inspect the converted result.

**General texture resizing is not implemented.** Changing an image to 4096 × 4096 does not make native storage, the renderer or PS2 memory support it. Archive relocation does not remove format/runtime limits.

Some materials use alpha for effects. Compare with Transparency disabled if opacity looks wrong. In-game materials can behave differently from the simplified viewer.

## Audio and voices

Select **Music & voices**, choose a supported resource, and use its audio controls. **Save audio…** exports supported decoded audio. Formats, sample rates and compression vary; unknown entries may need more research.

Choose **Replace audio & set loop points…** to import WAV/ADX, convert to the original game sample rate and channels, and choose a specific section to loop. **Apply to project** repacks the mapped containing bank and includes it in the next ISO build. Longer and shorter sounds are supported. See the [complete audio workshop guide](AUDIO.md) for exact loop placement, preview, supported formats and recovered-bank limitations.

## Exported files versus stored bytes

- **Export:** supported interchange images, decoded audio or 3D models.
- **Extract game files:** native resource data for research.
- **Save stored bytes:** the archive representation, potentially compressed or packaged.
- **Save index:** the discovered resource list.

An editor-compatible file is not automatically a valid game replacement. Use the supported native build/import route.

## Hex, strings and details

Enable **Advanced tools** for native metadata, hexadecimal bytes and readable strings. These help investigate headers, offsets and names. Not every number is a size or a safe field to change. Validated import support does not mean arbitrary binary edits will load.

Animation Lab has its own Advanced tools switch, clip/bank scope, hex search and strings view. Use the bank directory for clip names.
