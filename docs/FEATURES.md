# Feature checklist and current boundaries

[Home](../README.md) · [Roadmap](ROADMAP.md) · [Validation](VALIDATION.md) · [Previous builds](PREVIOUS_BUILDS.md)

Current application: **0.25.4**. Checked means implemented for supported data. **Experimental** means the workflow exists but needs preview and game testing. Unchecked items are not promised by this release.

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
- [x] Input validation and native preview; supported character/model-image imports stage together.
- [x] Three-bone draw batching and triangle checks in the shared replacement compiler (0.25.2).
- [x] Reject incompatible rebuilt batches in native import and before ISO writing; preserve byte-exact original records.
- [x] One prepared Kratos/Reptile replacement reported working in-game. See [validation scope](VALIDATION.md).
- [ ] Arbitrary new bones, hierarchies or replacement rigs.
- [ ] Unlimited meshes or removal of PS2 runtime limits.
- [ ] Full gameplay certification of arbitrary imported characters.

### Weapons and rigid objects (0.25.4)

- [x] Dedicated **Import weapon / object** workshop for supported unskinned type-0 geometry.
- [x] Copy another supported game model ID and its selected texture set into the destination slots.
- [x] Blender Bridge 0.23 weapon/object export without an armature.
- [x] **Experimental:** rebuild new vertices, triangles, normals, UVs and same-dimension material images; retain native attachment records and rebuild local bounds.
- [x] Review before staging, save/reload projects and rebuild ISO.
- [ ] All rigid/level/attachment encodings; collision, hitbox and weapon behavior editing.
- [ ] Gameplay confirmation of the new weapon workflows.

See [Weapons and objects](WEAPONS_AND_OBJECTS.md) for the **0443 → 0121** example.

## 4. Animation Lab

- [x] Bank discovery and recovered game-linked profiles.
- [x] Play, pause, scrub, loop, FPS selection and skeleton/textured preview.
- [x] Supported clip decoding and investigated root/rotation corrections.
- [x] One clip or a bank in individual numbered folders.
- [x] **Character + animation** exports for Blender/native editing.
- [x] **Animation only (GLB)** without repeated geometry/textures.
- [x] Selected-clip/full-bank details, hex and ASCII strings.
- [x] **Experimental:** edited types 1, 3, 6 and supported type-11 revision 2.
- [x] Delete old keys and author new motion on the original rig; import supported new lengths and whole-frame keys.
- [x] Select the intended take from a GLB containing multiple actions; match Blender FPS in the import dialog (0.25.3).
- [x] Recover missing Custom Properties only after complete, unique bone-name/hierarchy/bind-pose verification.
- [x] Show explicit import/staging errors and identify the selected action in the result.
- [x] Native type-11 clips display **Higher precision (already active)**; other disabled cases explain why.
- [x] Reimport native `.bin` banks and automatically stage them in the selected game resource.
- [x] Choose a game destination for standalone loaded banks; retained staged edits appear after reload.
- [x] Accept channel growth within verified game mappings; optional **Ignore bone-count difference** for explicit experiments, without retargeting.
- [x] **Experimental:** higher-precision eligible type-6 edits on verified USA profiles, with matching ISO compatibility patch.
- [ ] Automatic retargeting between arbitrary rigs/rest poses.
- [ ] Complete event/camera, transition and world-motion equivalence.
- [ ] All encodings or arbitrary subframe authoring.

## 5. Textures

- [x] Supported native texture preview and image export.
- [x] Same-dimension PNG replacement, palette conversion and supported smaller texture levels.
- [ ] General texture resizing or tested 4096 × 4096 in-game textures.

## 6. Audio and native loops

- [x] Supported audio preview/export.
- [x] WAV-to-ADX encoding and native ADX import at the destination rate/channel count.
- [x] Native loop endpoints in seconds or samples; intro-once and repeated-section preview.
- [x] Longer/shorter track replacement inside mapped AFS collections while preserving neighboring tracks.
- [x] Project persistence, individual track restore, bank undo and ISO rebuilding.
- [x] Standalone native ADX export with supported loop metadata.
- [ ] Installation of recovered AFS banks without mapped live resource IDs; other sound-bank formats.
- [ ] Automatic adjustment of game events/cutscenes to a longer sound.

See [Audio workshop](AUDIO.md) for conversion, loop placement and supported formats.

## 7. Advanced inspection

- [x] Native metadata, hex and readable strings for supported resources.
- [x] Animation Lab's own Advanced tools tab with selected-clip/full-bank scope.
- [x] Native resource extraction, stored-byte saving and resource index export.
- [x] Same-size hex overwrite from a file, game resource, current destination or pasted hex.
- [x] Byte offsets or one-based 16-byte line ranges, selected animation clip/full-bank scopes, before/after review and paged results.
- [x] Available native format validation, project staging/undo and patched-copy export with a transfer report.
- [ ] Hex insertion/deletion, automatic pointer repair or bone retargeting.
- [ ] Complete meaning/editing support for every unknown record.

## 8. Projects, rebuilding and testing

- [x] Stage, save/load, undo and restore original resource.
- [x] Project/source validation.
- [x] Supported native replacements can grow/shrink in byte size.
- [x] Rebuild archive placement into a separate ISO.
- [x] Build ISO only or build and boot; no emulator required to save an ISO.
- [x] Zero-edit builds produce an unchanged ISO copy.
- [x] Use current staged edits without first saving a project.
- [x] Verify installed resource bytes.
- [x] Launch selected PCSX2 with a separate test profile.
- [ ] Automatic proof of correct behavior throughout gameplay.

A bigger archive entry and greater in-game capacity are different issues. Relocation solves where the bytes go. It does not expand PS2 memory, texture hardware or internal buffers. Larger character imports must still fit format and practical runtime limits.

## 9. Distribution and updates

- [x] Self-contained Windows x64 EXE without application source/PDBs.
- [x] Gold dragon EXE/window icon; red/black/gold interface.
- [x] Startup and manual update checks.
- [x] Higher-version checks, signed manifests and payload validation.
- [x] In-app download, install and relaunch.
- [x] Temporary previous-EXE backup and recovery for failed startup; automatic old-build cleanup after confirmed successful startup.
- [x] Separate Blender bridge download (0.22 remains compatible with 0.25.3 workflows).
- [x] Centered looping gold author credits for OGmidway, RelaxDirk and Z mods.
- [x] Previous Builds index, with automatic release-packaging maintenance.

The core source is private; a compiled executable cannot guarantee protection against reverse engineering.

## Validation scope

The [validation record](VALIDATION.md) distinguishes historic corpus checks, current automated/UI/ISO checks, and reported gameplay. The Kratos replacement now has an in-game success report. The newly imported Kabal motion has preview/project/ISO verification; its gameplay test remains pending.

A working resource is not proof of every game revision, rig, encoding or gameplay situation. Use the [roadmap](ROADMAP.md) for the unfinished work and include specific resource IDs when reporting a problem.
