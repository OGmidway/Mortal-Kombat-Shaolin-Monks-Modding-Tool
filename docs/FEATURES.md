# Feature checklist and current boundaries

[Home](../README.md)

Checked means implemented for supported data. **Experimental** means the workflow exists but needs preview and game testing. Unchecked items are not promised by this release.

## 1. Opening and finding resources

- [x] Direct PS2 ISO reading without mounting/extraction.
- [x] Extracted game folder browsing.
- [x] Category filters, text/ID search and multi-selection.
- [x] Supported nested resource discovery and extraction.
- [x] Save indices and export reports.
- [ ] Complete human-readable names/purposes for every resource.
- [ ] Verified full coverage of every platform, region and disc revision.

## 2. Models, levels and camera

- [x] Supported character and level geometry preview.
- [x] Textures, transparency, surface filtering and optional extras.
- [x] Original decoded skeleton display and rigged GLB export.
- [x] Original UVs, material identities and supported skin weights.
- [x] Body objects grouped by texture and skeleton.
- [x] Separate rigid attachments and optional extra meshes.
- [x] Orbit/pan/zoom, Fit view and free-flight camera.
- [x] Coordinate and bind-pose corrections for investigated layouts.
- [ ] Complete game rendering, lighting, effects and visibility logic.
- [ ] Guaranteed handling of all unknown scene records.

## 3. Blender character editing

- [x] Optional bridge, separately distributed as Python.
- [x] Shape/UV return with original topology, weights and mapping retained.
- [x] **Experimental:** replacement topology/weights compiled around original skeleton/material constraints.
- [x] Native model and supported material-image replacement packages.
- [x] Input validation and preview before staging.
- [ ] Arbitrary new bones, hierarchies or replacement rigs.
- [ ] Unlimited meshes or removal of PS2 runtime limits.
- [ ] Full gameplay certification of arbitrary imported characters.

## 4. Animation Lab

- [x] Reimport edited native `.bin` banks directly into the selected game bank, preserving native bytes and automatically staging them for ISO building.

- [x] Bank discovery and recovered game-linked profiles.
- [x] Play, pause, scrub, loop, FPS selection and skeleton/textured preview.
- [x] Supported clip decoding and investigated root/rotation corrections.
- [x] One clip or a bank in individual numbered folders.
- [x] **Character + animation** exports for Blender/native editing.
- [x] **Animation only (GLB)** without repeated geometry/textures.
- [x] Selected-clip/full-bank details, hex and ASCII strings.
- [x] **Experimental:** edited types 1, 3, 6 and supported type-11 revision 2.
- [x] Use Blender timing for supported length/key changes.
- [x] **Experimental:** higher-precision eligible type-6 edits on verified USA profiles, with matching ISO compatibility patch.
- [ ] Automatic retargeting between arbitrary rigs/rest poses.
- [ ] Complete event/camera, transition and world-motion equivalence.
- [ ] All encodings or arbitrary subframe authoring.

## 5. Textures, audio and inspection

- [x] Supported native texture preview and image export.
- [x] Same-dimension PNG replacement, palette conversion and supported smaller texture levels.
- [x] Supported audio preview/export.
- [x] WAV/ADX replacement with conversion to the original sample rate and channels.
- [x] Native ADX loop start/end in seconds or samples; intro-once and repeated-section preview.
- [x] Longer/shorter track replacement in mapped AFS collections, project persistence and ISO rebuilding.
- [x] Native details, hex and strings.
- [ ] General texture resizing or tested 4096 × 4096 in-game textures.
- [ ] Installation of recovered AFS banks without mapped live resource IDs; other sound-bank formats. See [Audio workshop](AUDIO.md).
- [ ] Editable support for every unknown resource.

## 6. Projects, rebuilding and testing

- [x] Stage, save/load, undo and restore original resource.
- [x] Project/source validation.
- [x] Supported native replacements can grow/shrink in byte size.
- [x] Rebuild archive placement into a separate ISO.
- [x] Verify installed resource bytes.
- [x] Launch selected PCSX2 with a separate test profile.
- [ ] Automatic proof of correct behavior throughout gameplay.

A bigger archive entry and greater in-game capacity are different issues. Relocation solves where the bytes go. It does not expand PS2 memory, texture hardware or internal buffers. Larger character imports must still fit format and practical runtime limits.

## 7. Distribution and updates

- [x] Self-contained Windows x64 EXE without application source/PDBs.
- [x] Gold dragon EXE/window icon; red/black/gold interface.
- [x] Startup and manual update checks.
- [x] Higher-version checks, signed manifests and payload validation.
- [x] In-app download, install and relaunch.
- [x] Temporary previous-EXE backup and recovery for failed startup; automatic old-build cleanup after confirmed successful startup.
- [x] Separate Blender bridge download.
- [ ] Guarantee that a compiled executable cannot be reverse-engineered.

## Validation scope

Historical checks covered 115 decoded skinned resources through Blender round trips and 91 recovered USA animation profiles for selected export/native paths. Actual Godot AnimationLibrary playback covered three rigs/six clips. These are specific checks, not every clip or gameplay situation.

This release adds updater and packaging checks. Its release notes identify current checks. A reproducible failing file ID/clip is more useful than assuming every character uses one layout.
