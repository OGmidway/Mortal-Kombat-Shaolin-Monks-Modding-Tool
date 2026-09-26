# Characters, skeletons and Blender

[Home](../README.md) · [Animations](ANIMATIONS.md) · [Build an ISO](PROJECTS_AND_TESTING.md)

## Export a character

1. Open your ISO and select a character resource.
2. Check the texture set and preview. Use Show bones to see the original rig.
3. Show all surfaces you need; decide whether to include Extra meshes.
4. Click **Save for Blender…** and choose a new export folder.
5. Keep the GLB and native companion files together. They identify the original resource for editing/rebuilding.

Use the **rigged GLB** for skeletons, skin weights and animation. OBJ is useful for simple static geometry but cannot carry this rigged workflow.

## Install the optional bridge

Download **MKSM-Blender-Bridge-0.22.zip** from Releases and extract `io_mksm_studio.py`. Install it through Blender's add-on preferences and enable MKSM Studio. The exact menu varies by Blender version; the bridge was tested with Blender 4.2. Open the 3D Viewport sidebar's **MKSM** panel.

Use **Open Studio GLB** there. The bridge retains mappings/companions needed for native return. Keep a `.blend` working copy alongside the original export.

## Why the character is grouped this way

Objects such as `Body_texture_00` combine body pieces using the same native texture and exported skeleton. Legs, clothes and a mask can share one texture atlas and UV layer. Existing UVs are retained; atlases are not repacked and vertices are not welded.

Different native materials may remain as material slots even when they use the same image. Keep those identities. `Attachments_texture_*` contains rigid bone attachments; `Extras_texture_*` contains optional geometry. Different skeletons stay separate. Level objects follow a different structure.

The grouping applies across supported character exports, not only Scorpion. It does not establish support for every character in every game revision.

## Returning a character to the game

### A. Adjust existing shape or UVs

Use this for proportion corrections, moving existing vertices or UV adjustments without rebuilding topology.

1. Start from a fresh Studio export and its original rig.
2. Keep vertex/triangle structure, materials, rig and weights intact.
3. Preserve `_MKSM_PART`, `_MKSM_VERTEX` and `_MKSM_COPY` mapping attributes.
4. Choose **Save Shape Edits for Studio** in the bridge.
5. Select the original resource in Studio and choose **Import Blender edits…**.
6. Inspect the returned preview, save the project, and build a separate ISO.

### B. Replace a body or change topology — experimental

1. Export the original character as a reference.
2. Build/import your replacement in Blender. Align it and bind it to the original armature.
3. Transfer and clean up weights. Keep original bone names, hierarchy and bind/rest skeleton.
4. Use supported original material identities and native texture dimensions/layouts.
5. Choose **Save Replacement for Studio** in the bridge.
6. Select the original character in Studio and choose **Import character…**, then **1. Choose character…**.
7. Review the rebuilt native preview and reported limits. Use **3. Add to project** to stage the character and textures together; **Save native copies…** is available for standalone output.
8. Save the project and **Build & play…**. Test the actual character in gameplay.

The compiler creates native skin batches and quantizes weights/positions. It supports up to four influences per vertex and four distinct bones per triangle in this workflow. Different topology can work within supported constraints. Unsupported material, coordinate or rig layouts are rejected with an explanation.

Original rigid attachments are preserved by character rebuilding; use the shape path for their supported position/UV changes. Triangles in a mapped grouped object cannot cross distinct original native rig groups.

A good Studio preview is necessary but not sufficient: test movement, attacks, attachments and transitions in-game. Increase complexity gradually.

## Common problems

- **Wrong texture:** check the original texture set and preserve native material slots.
- **Missing surfaces:** check Surfaces and Extra meshes before exporting.
- **Collapse/twisting:** check rest pose and transferred weights. Matching names alone do not make skeletons equivalent.
- **Shape import rejects topology:** choose the replacement workflow for intentional topology changes.
- **Valid rebuild fails in-game:** record the resource ID and failure point; reduce complexity and compare against an unmodified baseline.
