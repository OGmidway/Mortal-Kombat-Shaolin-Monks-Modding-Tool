# Put a new character in Shaolin Monks

**Old game character = the slot you replace. New character = the body you want to play.**

Example: replace Reptile with Cyrax. Start with **Reptile's original MKSM export**. Put the new Cyrax body on **Reptile's game skeleton**.

Use **Blender Bridge 0.25.1** with **MKSM Studio 0.25.6 or later**. [Download the Bridge](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/download/v0.25.6/MKSM-Blender-Bridge-0.25.1.zip).

## First: install the Bridge

1. Download the Bridge ZIP. Extract it.
2. In Blender, open **Edit > Preferences > Add-ons**.
3. Use **Install from Disk** (in some versions: **Install**). Pick `io_mksm_studio.py`.
4. Enable **MKSM Studio Bridge**. Restart Blender if the old buttons remain.
5. In the 3D Viewport, press **N**. Click the **MKSM** tab.

The panel should say **MKSM Bridge 0.25.1 - Start here**. Studio's EXE updater does not install Blender add-ons. Install this download in Blender separately.

## 1. Get the ORIGINAL game character

In **MKSM Studio**:

1. Open your original game ISO.
2. Choose the character you want to replace.
3. Choose that character's textures. Check the preview.
4. Show every part you need, including extra parts. Liu Kang's dragon matters—keep it.
5. Click **Save for Blender…**. Use a new folder.
6. Keep **all files in that folder** together.

| File | What it is |
|---|---|
| `.glb` | Open this model in Blender. |
| `.original.pme2` | Untouched game model. Keep it as the reference. |
| `.original.pme2.textures.bin` | Original game textures. Keep beside the model. |
| `.mksm.json` | Extra information from Studio. Keep it too. |

Example pairs: **Liu Kang model 5888 / textures 5887**; **Reptile model 6732 / textures 6731**. These are examples, not IDs for every character.

## 2. Bring both characters into Blender

1. Start a clean Blender scene.
2. In the MKSM panel, click **Open original MKSM model (.glb)**. Choose the GLB from step 1.
3. Use Blender's **File > Import** menu to bring in your new character. Choose the importer for its file type.
4. Move, rotate and scale the **new body** until it fits the old body and bones.
5. Keep the new body as **separate mesh objects**. Do not join it into the original MKSM body.
6. Save a `.blend` working copy.

Keep the original MKSM skeleton. Keep its bone names and rest pose. The new character's own skeleton is not the game skeleton.

## 3. Copy the weights — make the new body follow the bones

**Weights tell each vertex which bones move it. The Bridge does not copy weights for you.**

For a basic transfer in Blender:

1. Select one new body mesh.
2. Add a **Data Transfer** modifier. Set its source to the matching original MKSM body mesh.
3. Enable **Vertex Data > Vertex Groups**. Use **Nearest Face Interpolated**. Generate destination data if Blender asks for it.
4. Apply the Data Transfer modifier. Repeat for the other new body meshes.
5. Add or update each new mesh's **Armature** modifier. Its object must be the **original MKSM armature**.
6. Pose a few game bones. Check the new body moves correctly. Fix bad weights by hand.
7. Return the rig to its original rest pose before export.

If the old body is split into several objects, transfer from the right part for each new mesh. One source object may not cover the whole body. Weight transfer is a starting point; it does not guarantee good results.

Apply the new mesh's Location, Rotation and Scale before material preparation. Keep its Armature modifier. **Do not apply transforms to or rebuild the original game armature.**

**Error: triangle uses more than three bones?** The three corners together must use at most three different bones. Remove tiny/unneeded weights, normalize, and check the pose again. “Three weights per vertex” alone may still leave four or more bones across a triangle.

### Reduced polygons or changed geometry?

Use **Bridge 0.25.1**. You can change topology and use **Import character** in Studio. **Import Blender edits** is for shape/UV edits that keep original topology.

1. Save a backup. Reduce the **new body** in Blender. Apply the Decimate modifier; keep the Armature modifier.
2. Finish texture setup. Select your new body and required skinned extras for export.
3. In step 5 of the MKSM panel, enable **Clean weights on export**.
4. Leave **Max weight removed (%) = 25** initially. This is the maximum total original influence the helper may remove from any vertex, not a polygon-reduction percentage.
5. Optional but useful: click **Preview cleaned weights on a copy**. Pose the original rig and check the selected copies around joints. The original meshes are hidden and kept.
6. Open **Weight cleanup report**. Check how many vertices lost influences and the largest removal.
7. Export using **Export selected character (.glb)**. Include the dragon and any other required extras; exclude old body meshes. Import that GLB through Studio's **Import character**.

With export cleanup enabled, the Bridge makes temporary export copies and cleans their weights automatically. It applies to selected-character GLB export, prepared-body export and native character package export. It does not change the source model or rig. Reports are kept in Blender's Text Editor and beside the exported file as `.weights.json`.

**If cleanup stops at the limit:** the repair needs a larger change than allowed. You may increase the limit and use the preview-copy button to inspect the result, or adjust that area manually. Higher limits can change movement noticeably. The helper never raises the limit automatically, adds new bone influences, transfers weights to an unweighted model, or ignores the game's three-bone restriction.

The cleanup checks the **union of bones across all three triangle corners**, not just weights per vertex. It removes selected influences, normalizes to native 1/4096 precision, and checks the result. Quads/ngons are triangulated on the copies so export uses the tested triangles. Material images and UVs remain unchanged. Preview copies should be exported with **Export selected character**, not a whole-scene export.

This resolves the weight-compatibility import error. A successful import still does not establish that a replacement loads in-game or fix the separate loading-freeze investigation.

## 4. Make the textures ready

Choose one route.

### A. Automatic textures — keep more detail

**Already using the right game materials and image sizes? Skip this step.** Do not squeeze a working multi-texture character into one image.

1. Save a backup `.blend`. Finish weight transfer and remove the **old body meshes** from this working scene. Keep the original skeleton, dragon and other needed extras.
2. Select **only your NEW body meshes**. Leave the dragon and other kept parts unselected.
3. Leave **Game textures = 0**. This means automatic: use the available game texture slots for better detail.
4. Click **Set up game textures (keep more detail)**.
5. Click **Check texture result**. Look at the copied body in Material Preview.
6. Select that prepared body **AND the dragon/other needed extras**. Continue to the export step below.

**Want two or three atlases?** Set **Game textures** to **2** or **3** before setup. The helper combines source images only when needed. It adjusts the copied UVs to match; it does not unwrap the body again or change bone weights.

Automatic is usually the better choice for quality. For the saved Liu Kang test scene, automatic kept **five body textures**, with the dragon's separate texture protected. All five body images were already 128 × 128, so they needed no reduction. Other characters can have different slot counts and dimensions.

**What stays safe:** original source meshes are kept and hidden; working copies are selected. Game textures used by unselected original meshes, including hidden extras, are reserved. A repeated setup recognizes its own previous backup meshes. If all slots are reserved, remove only the old reference body after saving a backup; do not delete the skeleton or required extras.

**Supported:** opaque sRGB image textures connected directly to Principled Base Color, with Image Texture extension **Repeat**, and solid base colors. Negative/repeating UV coordinates are handled during packing. Mixed/procedural colors and Mapping nodes need to be baked/applied first. Normal maps and other modern shader effects are not included.

This uses the original game's slots and image dimensions. It does not create unlimited slots or raise texture resolution. Fewer atlases can still lose detail. Studio also converts images to the game's palette format. Review the result and test the rebuilt ISO.

### B. Manual materials — keep separate game texture slots

1. Assign the original MKSM materials to the new meshes.
2. Put your new texture images into those materials.
3. Match each image's width and height to its original game texture slot.
4. Adjust the new character's UV map so the textures line up.
5. If two materials share one game texture slot, use the same image for both.

Renaming a new material does not give it the original game's material information. Use the exported game materials. Do not overwrite a texture still needed by the dragon or another extra part without checking that part too.

## 5. Export from Blender — choose ONE button

### Normal route: GLB

**Used the texture helper, and only need its prepared body?** Click **Export prepared body (.glb)**. This exports the latest prepared body and game skeleton.

**Used manual materials, or need extra skinned parts?**

1. Select your **new body meshes** (or the prepared copies).
2. Also select every needed extra skinned part, such as the dragon.
3. Do not select the old human body as well.
4. Click **Export selected character (.glb)**. Leave **Export selected meshes only** checked.
5. Save a new GLB file.

The original game skeleton is included automatically. No need to select it separately. Hiding an object does not delete it, and exporting the whole scene can include hidden old bodies. Use the selected-only button above.

**Do not rename GLB to BIN.** Studio converts the GLB to the game's format when you import it.

### Optional route: `.mksmcharacter` package

Use this instead if you want Blender to ask Studio to create the game-format package directly.

1. Select the new body and required extra skinned parts, as above.
2. Open **Optional: game-format export (.mksmcharacter)**.
3. **Studio .exe:** choose your current `MKSM Studio.exe`.
4. **Original .pme2:** choose the **untouched `.original.pme2` from step 1**. Not your new character. Not your `.blend` file.
5. Keep its `.textures.bin` companion beside it.
6. Click **Export game character (.mksmcharacter)**. Save to a new filename.

This packages the character; it does not bypass weight, texture or game limits.

## 6. Put it back into Studio

1. Open the original ISO in Studio.
2. Choose the **same character and texture set** you exported in step 1.
3. Click **Import character… > 1. Choose character…**.
4. Choose your new `.glb` or `.mksmcharacter`.
5. For GLB, keep **Import GLB material images** enabled if you changed textures.
6. Check the model, textures and required extra parts. Confirm the edits are staged in your project.
7. Click **Build ISO…**. Save to a **new ISO filename**.
8. Boot that ISO fresh in PCSX2. Select the character. Test movement and attacks.

Save the Studio project if you want to keep working later. A good editor preview does not prove the game can load the character. A loading freeze is still a failure: keep the model files and, if possible, save a PCSX2 save state while frozen for diagnosis.

## Wrong button? Use this table

| Your job | Blender button | Studio button |
|---|---|---|
| Completely new character | **Export selected character (.glb)** | **Import character…** |
| Body made by the texture helper | **Export prepared body (.glb)** | **Import character…** |
| New character as a native package | **Export game character (.mksmcharacter)** | **Import character…** |
| Only move existing vertices / UVs | **Save shape / UV edits (.glb)** | **Import Blender edits…** |
| Replace a rigid weapon | **Export selected weapon / object (.glb)** | **Import weapon / object…** |
| Change an animation | **Export edited animation (.glb)** | Animation Lab: **Import edited clip…**, then **Add animation to project** |

**Short version: old game bones + new body + correct weights + game materials → export → Import character → Build ISO → test.**

[Full technical guide](MODELS_AND_BLENDER.md) · [Home](../README.md)
