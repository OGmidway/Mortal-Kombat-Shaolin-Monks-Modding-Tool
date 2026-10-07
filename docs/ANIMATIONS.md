## Studio 0.27.15 preview timing

Animation Lab previews use a fixed 60 FPS clock, independent of the Export/import FPS selector. The selector retains its previous 30 FPS default and controls file transfer timing only. Actual rendering depends on hardware and workload. Existing saved animations are not rewritten.

# Animation Lab

[Home](../README.md) · [Godot 4](GODOT.md) · [Blender setup](MODELS_AND_BLENDER.md) · [Validation](VALIDATION.md) · [Roadmap](ROADMAP.md)

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
3. Edit the original armature's action. You may delete **all original keyframes** and create your own animation. Keep the original bones, names, hierarchy and bind pose, start at frame 0, and keep FPS consistent. Bone scale/shear is unsupported.
4. Prefer **Save Edited Animation for Studio** in the bridge. Standard Blender GLB export also works when its complete skin/bind data remains intact. Enable **Custom Properties** to retain the original metadata; when it is missing, Studio verifies the entire rig before recovering its mapping.
5. Return to the same Studio model, bank and destination clip. Choose **Higher precision** first for an eligible packed clip if needed, then **Import edited clip…**.
6. In **Choose animation to import**, select your new action. A Blender GLB can contain the original idle plus other actions; choose the one you actually edited. For multiple takes, Studio requires an explicit choice.
7. Set the **FPS used when exporting from Blender**. Leave **Use this take's length and new keyframes** checked for newly authored motion or duration changes. Uncheck it only to edit the original stored poses. A selected take replaces one destination clip, not the whole bank.
8. Play/scrub the native result. The status identifies the imported take and destination; a failed import produces an explicit message. No-change imports also explain that another action may need selecting.
9. For a bank opened from the game, a successful edited import is automatically added to the project. Close the lab and choose **Build ISO…**. Save the project to keep the edits for later. **Save native bank** writes a standalone replacement and compatibility report instead.

Metadata recovery is not retargeting. Bone names alone are insufficient: every bone, its parent and its inverse bind matrix must uniquely match the selected original rig. Keep **Character + animation** exports for this workflow so skin/bind information is present. A GLB with another character's skeleton or missing bind data must be corrected/re-exported.

Game-backed imports are staged automatically after native validation. No-change imports preserve the bank without adding an edit. Standalone banks loaded from disk have no assumed game destination: save the edited bank, select its matching game bank in the Animation bank list, then use **Import native bank (.bin)…**. **Replace game file…** on the correct resource remains available. **Add animation to project** remains available for any pending game-backed edit.

## Reimport an edited native BIN bank

1. Save your edited bank in native `.bin` format. **Save native bank…** in Animation Lab writes this format; no GLB conversion is required.
2. Select its original destination in the **Animation bank** list.
3. Choose **Import native bank (.bin)…** and select your edited `.bin`.
4. Studio validates the bank, previews it and automatically adds the replacement to your project.
5. Close the lab and choose **Build ISO…**. Save the project if you want to retain the edits for another session.

This replaces the **whole selected bank**, preserving imported native bytes. The animation names and slot order must match the destination, and changed clips must have a supported layout. Different bone-channel counts are allowed when they fit the verified destination game-bank profile. For deliberate experiments, **Ignore bone-count difference** bypasses that count/profile restriction. It defaults to OFF, does not retarget bones, and does not bypass native structure or clip-name/order validation. Wrong channel mappings can distort animation or fail in-game.

Unknown clips can be retained unchanged. A BIN identical to the current bank adds no new edit. Required higher-precision compatibility markers remain intact and are detected by the ISO builder.

**Load bank file…** opens a standalone preview. To install that loaded bank, click **Add animation to project**, choose its matching original game bank, then click **Add bank to project**. Once staged, the button says **Bank added to project**; it is already included in the next build. Selecting another clip or changing playback controls does not edit the game. Test imported banks in gameplay after rebuilding.

## Preview, replacement and additional animations

- Selecting another clip, playing it, changing preview FPS or ticking Loop does **not** replace an animation in the game.
- **Import edited clip…** replaces the selected existing clip with the chosen Blender take. It can contain completely new motion; the source skeleton must still match.
- **Import native bank (.bin)…** replaces a whole existing bank. Clip names/order and supported structure are checked. **Load bank file…** alone is a preview until you assign/stage it.
- Putting another character's bank in a destination does not automatically retarget its bones. **Ignore bone-count difference** does not solve a wrong bone order or bind pose.
- Creating extra native clip slots and changing the game's references to use them is not implemented by these replacement controls. See the [roadmap](ROADMAP.md).

## Native limits and higher precision

Editing supports decoded types 1, 3, 6 and type-11 revision 2 within validated layouts. Type 3 is root-translation-only. Type 6 has coarse packed rotations and bounded root positions. Eligible edited type-6 clips can convert to higher precision on verified USA profiles whose root channel maps only to bone 0.

**Higher precision (already active)** means a selected type-11 clip already uses the finer native format. No extra conversion is needed; new imports retain it automatically. The disabled checkbox does not mean animation import is disabled. For other disabled cases, hover over the control for the reason; conversion requires a verified compatible game profile.

That conversion requires the matching game compatibility patch. Studio detects its native marker and includes the supported patch during ISO building. It does not remove other engine limits; unsupported executable revisions cannot be treated as equivalent.

Whole-frame poses are evaluated; arbitrary subframe authoring is not captured. Preview does not reproduce every native event, camera, visibility, mirror/blend transition or world-motion behavior. Byte verification is not gameplay testing.

## Inspect the bytes

Enable **Advanced tools** inside Animation Lab. Choose selected clip or full bank, then details, hex or ASCII strings. Clip names live in the bank directory, so inspect the full bank to find them. Imported edits refresh the bytes. This is inspection, not an unrestricted hex patch editor.

## Transfer specific native animation bytes

Animation Lab → **Advanced tools → Hex → Transfer hex data…** supports a selected clip or the full bank. A reviewed valid overwrite refreshes the preview and stages a game-linked bank. A standalone bank can be edited in preview, then saved as native BIN or assigned to a destination. See [Hex transfer](HEX_TRANSFER.md); copying bytes does not retarget bones or add animation slots.
