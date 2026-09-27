# Put a new character in Shaolin Monks

**Old game character = the slot you replace. New character = the body you want to play.**

Example: replace Reptile with Cyrax. Start with **Reptile's original MKSM export**. Put the new Cyrax body on **Reptile's game skeleton**.

Use **Blender Bridge 0.24.1** with **MKSM Studio 0.25.6 or later**. [Download the Bridge](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/download/v0.25.6/MKSM-Blender-Bridge-0.24.1.zip).

## First: install the Bridge

1. Download the Bridge ZIP. Extract it.
2. In Blender, open **Edit > Preferences > Add-ons**.
3. Use **Install from Disk** (in some versions: **Install**). Pick `io_mksm_studio.py`.
4. Enable **MKSM Studio Bridge**. Restart Blender if the old buttons remain.
5. In the 3D Viewport, press **N**. Click the **MKSM** tab.

The panel should say **MKSM Bridge 0.24.1 - Start here**. Studio's EXE updater does not install Blender add-ons. Install this download in Blender separately.

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

## 4. Make the textures ready

Choose one route.

### A. One-texture helper — experimental

Use this for an opaque body. It does not transfer weights or increase the game's texture resolution.

1. Select **only the new body meshes**.
2. Click **Make one game texture (experimental)**.
3. Wait. The Bridge makes copies and packs their colors into one original-size game texture.
4. Click **Check texture result**.
5. Look at the prepared body in Material Preview. If it is black, blurry or wrong, **stop and fix the materials**. Do not export a broken result.

Original meshes remain in the scene. The selected new source meshes are hidden; prepared copies are selected. A small game texture can lose detail. Automatic baking still has problem cases. Use the manual route if the result is wrong.

This helper is **body-only**. Extra skinned parts, such as Liu Kang's dragon, need to be included through the selected-mesh export below. Parts sharing a texture may need manual material work.

### B. Manual materials — keep separate game texture slots

1. Assign the original MKSM materials to the new meshes.
2. Put your new texture images into those materials.
3. Match each image's width and height to its original game texture slot.
4. Adjust the new character's UV map so the textures line up.
5. If two materials share one game texture slot, use the same image for both.

Renaming a new material does not give it the original game's material information. Use the exported game materials. Do not overwrite a texture still needed by the dragon or another extra part without checking that part too.

## 5. Export from Blender — choose ONE button

### Normal route: GLB

**Used the one-texture helper, and only need its prepared body?** Click **Export prepared body (.glb)**. This exports the latest prepared body and game skeleton.

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
