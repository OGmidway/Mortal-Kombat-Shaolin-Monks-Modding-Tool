# Animation Lab

[Home](../README.md) · [Godot 4](GODOT.md) · [Blender setup](MODELS_AND_BLENDER.md)

## Play on the original rig

1. Select a rigged character and click **Animations…**.
2. Use its game-linked bank when a verified profile exists. Nearby IDs/manual bank choices do not prove compatibility.
3. Select a clip; search if necessary.
4. **Play**, pause or drag the timeline to a frame.
5. Use **Loop**, **Smooth motion**, **Preview FPS**, **Show bones**, **Textures** and **Follow character** as needed.
6. Use **Rest pose** to compare the original rig with the animated pose.

Preview FPS controls export/playback frame interpretation; it is not proof of the original game's speed. Choose the intended rate and keep it consistent. For 60 FPS, select **60** and use 60 in the destination application.

If a standing clip is upside down or distorted, verify the model/profile/bank combination first. Investigated native rotations/roots have corrections; incompatible or unverified layouts may need more research.

## Choose an export mode

| Mode | Contains | Use |
|---|---|---|
| **Character + animation** | Rigged character, supported textures/materials, one animation and native companions | Blender editing and native game return |
| **Animation only (GLB)** | Skeleton definition and one animation; no character mesh, textures, materials or repeated native snapshots | Separate libraries on one exported character |

Animation-only retains the skeleton definition because track paths need it. The visible character geometry is not duplicated.

## Save clips in separate folders

**Save clip…** exports the selected clip. **Save all clips…** creates numbered folders in original bank order, independent of search filtering.

```text
CharacterAnimations/
  animation-index.json
  READ_ME.txt
  0001_a00_stnd/
    0001_a00_stnd.glb
    ...companions for the export mode...
  0002_next_clip/
    0002_next_clip.glb
    ...
```

The number is the one-based source-bank position. The internal original name stays intact. Unsupported/incompatible clips are recorded with reasons in the index. Use a new destination to protect previous exports. Character + animation repeats native snapshots, so banks can take considerable space.

## Edit a native clip in Blender — experimental

1. Export **Character + animation** from a current Studio release.
2. Use the separate bridge's **Open Studio GLB**. It reads the companion manifest and sets the action/range.
3. Edit the original armature's action. Keep bones/hierarchy, frame 0 start and matching FPS. Bone scale/shear is unsupported.
4. Choose **Save Edited Animation for Studio**; export one active action.
5. Return to the same Studio model, bank, original clip and FPS.
6. Enable **Use Blender timing** for intentional length/key timing changes; otherwise retain native timing.
7. Choose **Higher precision** for an eligible packed clip if needed, then **Import edited clip…**.
8. Play/scrub the native result and inspect reported quantization/mesh differences.
9. For a bank opened from the game, a successful edited import is automatically added to the project. Close the lab and choose **Build ISO…**. Save the project to keep the edits for later. **Save native bank** writes a standalone replacement and compatibility report instead.

Game-backed imports are staged automatically after native validation. No-change imports preserve the bank without adding an edit. Standalone banks loaded from disk have no assumed game destination: save the edited bank, select its matching game bank in the Animation bank list, then use **Import native bank (.bin)…**. **Replace game file…** on the correct resource remains available. **Add animation to project** remains available for any pending game-backed edit.

## Reimport an edited native BIN bank

1. Save your edited bank in native `.bin` format. **Save native bank…** in Animation Lab writes this format; no GLB conversion is required.
2. Select its original destination in the **Animation bank** list.
3. Choose **Import native bank (.bin)…** and select your edited `.bin`.
4. Studio validates the bank, previews it and automatically adds the replacement to your project.
5. Close the lab and choose **Build ISO…**. Save the project if you want to retain the edits for another session.

This replaces the **whole selected bank**, preserving imported native bytes. The animation names and slot order must match the destination, and changed clips must have a supported layout and the original bone-channel count. Unknown clips can be retained unchanged. A BIN identical to the current bank adds no new edit. Required higher-precision compatibility markers remain intact and are detected by the ISO builder.

**Load bank file…** opens a standalone preview. To install that loaded bank, click **Add animation to project**, choose its matching original game bank, then click **Add bank to project**. Once staged, the button says **Bank added to project**; it is already included in the next build. Selecting another clip or changing playback controls does not edit the game. Test imported banks in gameplay after rebuilding.

## Native limits and higher precision

Editing supports decoded types 1, 3, 6 and type-11 revision 2 within validated layouts. Type 3 is root-translation-only. Type 6 has coarse packed rotations and bounded root positions. Eligible edited type-6 clips can convert to higher precision on verified USA profiles whose root channel maps only to bone 0.

That conversion requires the matching game compatibility patch. Studio detects its native marker and includes the supported patch during ISO building. It does not remove other engine limits; unsupported executable revisions cannot be treated as equivalent.

Whole-frame poses are evaluated; arbitrary subframe authoring is not captured. Preview does not reproduce every native event, camera, visibility, mirror/blend transition or world-motion behavior. Byte verification is not gameplay testing.

## Inspect the bytes

Enable **Advanced tools** inside Animation Lab. Choose selected clip or full bank, then details, hex or ASCII strings. Clip names live in the bank directory, so inspect the full bank to find them. Imported edits refresh the bytes. This is inspection, not an unrestricted hex patch editor.
