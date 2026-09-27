# Roadmap and completed milestones

[Home](../README.md) · [Current features](FEATURES.md) · [Validation](VALIDATION.md) · [Previous builds](PREVIOUS_BUILDS.md)

This is the work list through **0.25.5**, not a release schedule. Checked milestones are delivered for the supported data. Unchecked items need implementation, research or further testing; they are not hidden features you can unlock with a setting.

## 1. Delivered foundation

- [x] Open a game ISO directly, browse supported resources, and export native data.
- [x] Red/black/gold interface, dragon artwork, and centered gold animated credits for OGmidway, RelaxDirk and Z mods.
- [x] Textured model/level preview, original skeletons, surface controls and free-flight camera.
- [x] Original native model snapshots plus rigged GLB exports organized by texture and skeleton.
- [x] Blender shape/UV editing and a separate replacement-character workflow.
- [x] Animation Lab playback, timeline, native-bank loading/import, GLB export and Advanced tools.
- [x] Separate animation-only GLBs and numbered folders for batch clip export.
- [x] Project persistence, variable-size resource relocation, separate ISO rebuild and PCSX2 launch.
- [x] Build-only and zero-edit ISO copying; a PCSX2 launch is optional.
- [x] Private core application distribution, optional readable Blender bridge and signed in-app updates.

## 2. Recent milestones

| Delivered | Result | Evidence / remaining scope |
|---|---|---|
| 0.24.4–0.24.5 | Native BIN bank import, explicit standalone-bank destination, allowed mapped channel growth and optional bone-count override | Staging/reload/project/ISO checks; the override does not retarget bones. |
| 0.25.0 | WAV-to-ADX conversion, destination rate/channels, exact loop section and longer/shorter audio replacement | Independent decoding and ISO checks; sound events and transitions still need gameplay coverage. |
| 0.25.1 | Old updater-created EXEs removed after successful startup | Recovery remains available if startup fails; GitHub release downloads remain available. |
| 0.25.2 | Replacement-character draw batches corrected | Kratos replacing Reptile 6732 was reported fully visible and moving in-game. This is one confirmed replacement, not certification of every model. |
| 0.25.3 | Choose a Blender action, import newly authored keys, recover missing metadata only against a verified complete rig, explain active high precision | Supplied Kabal GLB passed preview/project/ISO checks; its new motion still needs in-game testing. |

| 0.25.4 | Same-size hex transfer; rigid weapon/object workshop; Blender Bridge 0.23 object export | Animation/texture/project/UI checks, 18 rigid-resource round trips, actual Blender added-topology/material return and native weapon-copy ISO readback; weapon gameplay still pending. |

| 0.25.5 | Show the weapon/object import button for rigid models in normal and Advanced modes | Actual toolbar visibility/click/selection checks; no native format changes. |

## 3. Next: reliability and practical editing

- [ ] Collect reproducible character/animation failures with Studio version, game revision, resource IDs and chosen import mode.
- [ ] Expand gameplay checks across more replacement characters, including transitions, damage and attachments.
- [ ] Verify the newly imported Kabal actions in gameplay and record the result.
- [ ] Verify 0443 over 0121 in gameplay, including grip/orientation and weapon use.
- [ ] Extend rigid rebuilding beyond decoded unskinned type-0 parts; investigate collision/hitbox authoring separately.
- [ ] Improve diagnostics for difficult weights, unsupported tracks and model/animation source mismatches.
- [ ] Make complicated material/texture preparation easier while retaining the original native identities.
- [ ] Expand round-trip coverage across additional Blender versions and user export settings.

The mesh fix is in the shared importer. A CJ replacement would use the same original-rig, weight-transfer, material and ISO workflow as Kratos; a CJ result has not been verified here.

## 4. Deeper animation and scene research

- [ ] Recover more native animation layouts and unverified character/root mappings.
- [ ] Better reproduce animation transitions, runtime flags, mirroring and world motion.
- [ ] Research native event/camera authoring and timing behavior.
- [ ] Add entirely new animation slots and game references, beyond replacing existing clips/banks.
- [ ] Expand investigation of unusual level transforms, attachments, visibility records and orientation cases.
- [ ] Improve identification of numeric resources and their in-game use.

Existing coordinate/bind-pose corrections cover investigated layouts. An unchecked task here does not mean all characters or stages are currently broken.

## 5. Textures, audio and larger assets

- [ ] Research native texture resizing, mip levels, allocation and renderer requirements.
- [ ] Establish practical per-resource memory/geometry budgets through game testing.
- [ ] Recover the installation path for AFS collections that lack mapped live archive IDs.
- [ ] Investigate other sound banks/codecs and audio-event timing.
- [ ] Expand verified game revision/platform coverage.

Resource relocation already allows supported files to grow or shrink. General 4096 × 4096 textures, unlimited polygon counts, arbitrary skeleton replacement and removal of hardware limits are **not implemented promises**. Each requires separate format/runtime support, and hardware capacity remains finite.

## 6. Documentation and release history

- [x] Current feature checklist, beginner workflows and troubleshooting through 0.25.5.
- [x] Separate record of tool checks and reported gameplay outcomes.
- [x] Previous Builds index for published older releases.
- [x] Archive index maintenance during release packaging; existing downloads and signatures remain in their original releases.

For a specific problem, [open an issue](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/issues) with the details in [Updates and help](UPDATES_AND_HELP.md#reporting-a-problem).
