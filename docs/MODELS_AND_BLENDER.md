# Characters, skeletons and Blender

[Home](../README.md) · [Animations](ANIMATIONS.md) · [Build an ISO](PROJECTS_AND_TESTING.md)

## Export a character

1. Open your ISO and select a character resource.
2. Check the texture set and preview. Use Show bones to see the original rig.
3. Show all surfaces you need; decide whether to include Extra meshes.
4. Click **Save for Blender…** and choose a new export folder.
5. Keep the GLB and native companion files together. They identify the original resource for editing/rebuilding.

Use the **rigged GLB** for skeletons, skin weights and animation. OBJ is useful for simple static geometry but cannot carry this rigged workflow.

### Getting the untouched native original

Start from the original ISO with no model replacement staged (or restore that resource first). **Save for Blender…** writes the editable `.glb`, a `.original.pme2` native snapshot and `.mksm.json` mapping. When available, `.original.pme2.textures.bin` preserves the selected native texture set. Keep them together. A snapshot exported after staging edits represents that current model, so keep a separate untouched source export.

GLB carries the editable rig, mesh, weights and UVs. The native companion is the game-format reference; a GLB or OBJ cannot simply be renamed to BIN and installed.

## Install the optional bridge

Download **MKSM-Blender-Bridge-0.24.zip** from Releases and extract `io_mksm_studio.py`. Install it through Blender's add-on preferences and enable MKSM Studio. The exact menu varies by Blender version; the bridge was tested with Blender 4.2. Open the 3D Viewport sidebar's **MKSM** panel.

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
4. Use **Prepare Character for MKSM** for supported opaque materials (see [automatic preparation](#automatic-material-preparation)), or manually use original material identities and native texture dimensions/layouts.
5. Choose **Save Prepared Character for Studio** for automatically prepared copies, or **Save Replacement for Studio** for the manual path. The manual button includes hidden bound skin meshes; remove unwanted meshes or select only replacements and enable its selected-only export option.
6. Select the original character in Studio and choose **Import character…**, then **1. Choose character…**.
7. Review the rebuilt native preview and reported limits. Successful imports automatically stage the character and textures together; **Save native copies…** is available for standalone output.
8. Choose **Build ISO…**, then **Build ISO only** or **Build & boot in PCSX2**. Save the project if you want to keep the edits for a later session. Test the actual character in gameplay.

The compiler creates native skin batches and quantizes weights/positions. **Each triangle may reference at most three different bones across all three corners.** Studio automatically groups compatible triangles into three-bone batches without changing their weights. For example, a triangle whose corners collectively use pelvis, thigh and calf is supported; adding a foot bone makes four, even if no individual vertex has four influences.

If a triangle exceeds this limit, Studio reports the mesh name and triangle number. Review the triangle's vertex groups in Blender, remove unnecessary influences deliberately, normalize the remaining weights, and export again. Limiting each vertex to three influences alone does not guarantee that a whole triangle uses only three bones. Keep an untouched Blender copy before adjusting weights.

Earlier versions treated four storage slots as four-bone rendering support. The researched USA character draw routine skips that batch type, causing replacement bodies to disappear even with a correct Studio preview. Update to **0.25.2 or later**, then re-import the replacement GLB against the original character source and build a new ISO. Existing incompatible native packages must be rebuilt. Native imports and ISO preflight now check for this problem, while retaining unchanged original records. Updating Studio does not modify ISOs already built.

Different topology can work within supported constraints. Unsupported material, coordinate or rig layouts are rejected with an explanation. If using the Blender bridge's native-package export, point its Studio executable setting to the updated EXE.

Original rigid attachments are preserved by character rebuilding; use the shape path for their supported position/UV changes. Triangles in a mapped grouped object cannot cross distinct original native rig groups.

**In-game milestone:** Kratos replacing Reptile model **6732**, with texture set **6731**, was reported fully visible and running in-game after this fix. These IDs describe that test, not every character's pairing. The compiler fix applies generally to supported replacements; CJ or another character still needs its own weight/material preparation and game test.

A good Studio preview is necessary but not sufficient: test movement, attacks, attachments and transitions in-game. Increase complexity gradually.

## Automatic material preparation

Use **Studio 0.25.6** with the separate **Blender Bridge 0.24** download. This replaces the manual material-count/image-size/UV-layout work for supported **opaque base-color** character meshes. Weight transfer and alignment still happen first.

1. In Studio, select the destination character, load the correct texture set, then **Save for Blender…**. Keep the GLB and native companions together.
2. In Blender's MKSM sidebar, use **Open Studio GLB**. Import your replacement, align it, and transfer/clean up weights onto the original armature. Keep the original bones and rest pose.
3. Apply the donor's object transforms and non-armature modifiers. Keep its original textured materials and UVs. The donor needs one Armature modifier targeting the Studio rig.
4. Select **only your replacement meshes**. Click **Prepare Character for MKSM**. Baking can take time on large meshes; wait for completion.
5. Inspect the selected objects in **MKSM Prepared Character**, using Material Preview. If the original reference body overlaps, hide that body in the Outliner or use Blender's Local View on the selected prepared meshes. Source meshes remain in the scene; preparation hides the selected donors in the viewport without changing their geometry, materials or UVs.
6. Open **Preparation Report**. It shows the native atlas size/material and warns if the texture is shared with attachments. The full report is also saved as a Blender text data-block. Save a `.blend` working file to keep the packed atlas and prepared copies.
7. Click **Save Prepared Character for Studio**. This exports only the latest prepared copies plus the original rig; it does not include other hidden character bodies.
8. In Studio, select the same destination, choose **Import character… → 1. Choose character…**, and load that GLB with **Import GLB material images** enabled. Review the rebuilt native colors/model, then build a separate ISO and test it in-game.

### What the automatic step does

- Finds the largest textured body slot in the original destination GLB and retains its native material ID and image dimensions. You do not need to create the original number of textures manually.
- Packs new UV islands across the selected meshes and bakes their base colors into one atlas. Image textures and solid base colors are supported; base-color node inputs are evaluated by Blender's bake engine.
- Keeps source image sampling on its original UV layer during the bake. Prepared copies get the atlas as their export UV0, with the image packed into the GLB.
- Keeps the original skeleton and prepared vertex positions, topology and weights. Does not silently remove bone influences. The existing three-bone-per-triangle check still applies.
- Leaves original source geometry/materials intact. If preparation fails, temporary copies/images/materials are removed and render settings are restored. Repeating preparation creates another set; the dedicated export button uses the newest set.

### Limits to review

- This first version uses **one existing native-size atlas**, so a detailed donor can lose texture detail. It does not increase native texture resolution or remove PS2 limits. Studio still performs native palette conversion; review its preview after import.
- Only opaque materials with a Principled BSDF directly connected to Material Output are accepted. A linked Alpha input or Alpha below 1 is rejected. Normal maps, metallic/roughness, emission and other modern shader effects are not recreated as native game materials.
- **Attachments or extra meshes sharing the chosen native texture keep their original UVs.** The report flags texture sharing found in the template export. Those parts can need manual texture/material work; inspect them in Studio, including hidden/extra surfaces. Export omitted surfaces cannot be checked by the Blender helper.
- Preparation does not fit the donor to the rig, transfer weights, repair animation or certify a game-ready character. Test the rebuilt ISO. The original manual replacement path remains available for special materials or multiple carefully authored native textures.
- This preparation button handles skinned characters; use the separate weapon/object workflow for rigid models.

## Textures and UVs on a replacement

Replacement GLB UV0 and supported embedded base-color images can accompany the mesh. Map materials to the chosen original character's native texture slots and use the destination image dimensions. Different materials sharing one native texture slot must use the same image. Bake unsupported material effects and texture transforms into the image/UVs first.

This workflow imports new texture artwork and UV mapping; it does not provide general native texture resizing or arbitrary modern shader materials. See [texture editing](ASSETS_AND_INSPECTION.md).

## Common problems

- **Wrong texture:** check the original texture set and preserve native material slots.
- **Missing surfaces:** check Surfaces and Extra meshes before exporting.
- **Body appears in Studio but disappears in-game:** update to 0.25.2 or later, rebuild the replacement from its GLB with compatible weights, and build a fresh ISO. Old four-bone packages are not repaired by previewing them.
- **Collapse/twisting:** check rest pose and transferred weights. Matching names alone do not make skeletons equivalent.
- **Shape import rejects topology:** choose the replacement workflow for intentional topology changes.
- **Valid rebuild fails in-game:** record the resource ID and failure point; reduce complexity and compare against an unmodified baseline.

## Weapons and rigid objects

Use **Import weapon / object…** for supported unskinned type-0 models. Blender Bridge **0.23 and later** has **Save Weapon / Object for Studio**. This path can rebuild topology without a character armature, or copy an existing game model and its textures. See [Weapons and objects](WEAPONS_AND_OBJECTS.md) for the 0443-over-0121 workflow and current limits.
