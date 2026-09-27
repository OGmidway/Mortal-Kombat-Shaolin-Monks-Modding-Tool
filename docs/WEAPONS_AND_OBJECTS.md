# Weapons and rigid objects

[Home](../README.md) · [Blender character guide](MODELS_AND_BLENDER.md) · [Projects and ISO building](PROJECTS_AND_TESTING.md)

Use **0.25.5 or later**. Version 0.25.4 introduced the rigid-object workshop but accidentally hid its toolbar button on rigid models; 0.25.5 fixes its visibility. A weapon with no skeleton does not need character weights or an armature. The first replacement compiler supports fully decoded, unskinned **type-0** native geometry. Other static layouts can still use the existing mapped shape/UV editing route where supported.

## 1. Copy another weapon already in the game

Example requested for this release: replace **0121 (kama)** with **0443 (tiger-hook sword)**.

1. Open your game ISO and select model **0121**.
2. Confirm its texture set is **0120** in the model preview.
3. Click **Import weapon / object…**.
4. Enter **0443** in **Copy game model ID**.
5. Leave **Include material textures** checked. The source texture field can stay `auto`; this example finds **0442**. You can enter a texture ID explicitly if the suggestion is wrong.
6. Click **Review game-model copy**. The status should say model **0443 → 0121** and texture **0442 → 0120**. Inspect the preview.
7. Click **Add to project**, close the workshop, then **Build ISO**. Save the project if you want to reopen these edits later.

This copies the native donor model/texture bytes into the destination archive slots, even when their file sizes differ. It keeps the donor's model origin, scale and materials. The destination slot still determines its attacks/game behavior. It does not turn a kama attack into a newly authored sword attack. Models sharing texture set 0120 will also see the changed set.

The tool/project/ISO path for this pair has been checked. Grip, orientation, culling and weapon use still need a gameplay test. Boot the new ISO fresh instead of relying on a save state containing the old resource.

## 2. Export the original to Blender

Select the destination weapon and its texture set, then choose **Save for Blender…**. Keep the exported GLB, `.original.pme2`, mapping JSON and texture sidecar together. The native PME2 is the untouched source snapshot for that export.

Install the separately downloaded **MKSM-Blender-Bridge-0.23.zip** add-on, then use **MKSM → Open Studio GLB** in Blender. The character/animation operators remain available; use the new weapon/object operator for rigid models.

## 3. Replace or edit the mesh

1. Keep one destination Studio model per Blender scene.
2. Retain its source properties and original material slots. For a simple one-part weapon, you can edit its vertices freely or put a new mesh in the scene and assign those original materials. Keep the original object as an unselected reference until export if the new object has no source properties yet.
3. Align the new mesh to the original grip/origin and intended size. No armature or weight transfer is needed for this rigid workflow.
4. Supply UV0 and normals. Apply modifiers and shape keys. Do not include animation tracks.
5. To change textures, put embedded images on the original material slots. Bake each image to that native slot's existing width/height. Arbitrary resizing is not introduced by this update.
6. Select **only** the replacement mesh objects. Choose **MKSM → Save Weapon / Object for Studio**.
7. In Studio, select the same destination → **Import weapon / object… → Import Blender object…**. Keep **Include material textures** on if the images should be imported.
8. Review the rebuilt preview and counts. Click **Add to project**, save the project, and build a separate ISO.

For a model with multiple original native chunks, retain each mesh's original `mksm_chunk` assignment. Every original rigid chunk needs replacement geometry. A replacement may change vertices and triangles within those chunks; this version does not invent new attachment/chunk structures.

## Current boundaries

- Rebuilt rigid parts currently allow up to 16,384 vertices and 60,000 triangles per native chunk. These are encoding/tool guards, not safe gameplay budgets. Use modest PS2-scale models.
- The compiler retains original attachment/transform/material records and rebuilds vertex/index buffers, counts, local bounding boxes and spheres.
- Original materials and texture-slot identities are required. Native palette/dimension restrictions still apply to Blender material images.
- Skinned characters use **Import character**. Other rigid/level encodings, unknown geometry and varying auxiliary vertex records can be rejected.
- Collision, hitboxes, pickup behavior, damage and attacks are not edited by replacing visual geometry.
- Existing **Import Blender edits…** remains the route for mapped shape/UV changes that preserve original topology.

Validation included 18 decoded rigid resources and a real Blender 4.2.22 export with increased topology and an edited material image. See [Validation](VALIDATION.md) for the difference between tool checks and gameplay confirmation.
