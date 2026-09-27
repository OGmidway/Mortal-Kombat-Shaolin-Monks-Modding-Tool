# Release notes

## 0.25.0 — Audio replacement and native ADX loops

- Adds **Replace audio & set loop points…** to the Audio tab.
- Imports PCM/float WAV and supported native ADX, matching the destination track's sample rate and channel count.
- Writes exact loop start/end points into native ADX, with seconds/sample inputs, waveform markers, intro-once playback and a three-pass loop preview.
- Rebuilds mapped AFS sound collections for longer or shorter tracks while preserving neighboring payloads, names and order.
- Includes audio edits in project save/load, track restore, bank undo, and ISO builds. Reopening a track previews its staged version.
- Saves standalone native ADX with loop metadata. Recovered banks without a mapped live resource ID support export but are clearly excluded from automatic ISO installation.
- Corrects ADX decoding to honor original predictor histories and coefficient truncation.
- Preserves native audio bytes when unchanged; eligible aligned loop edits avoid recompression.

Validated against an independent ADX decoder, original game headers, project/UI round trips and a rebuilt USA ISO. Runtime sound-event timing and music transitions still need gameplay testing. [Audio guide](docs/AUDIO.md).

## 0.24.5 — Native idle import and bone-count option

- Fixes native-bank imports that add channels already defined by the verified destination game rig, including Scorpion idle body/face channels.
- Adds **Ignore bone-count difference**, OFF by default, for explicit native-bank experiments. This does not retarget bones or bypass bank/clip structural checks.
- Keeps **Bank added to project** visible when a staged bank is reloaded or Animation Lab reopens.
- Shows an explicit message when a native import is rejected, so a failed import cannot be mistaken for a saved edit.


## 0.24.4 — Native animation bank import

- Adds **Import native bank (.bin)…** directly to Animation Lab.
- Imports an edited native bank into the selected game bank and stages it automatically for ISO rebuilding, without GLB conversion.
- Preserves native bytes and higher-precision compatibility markers.
- Validates clip names/order, changed clip layouts and bone-channel counts. Failed imports retain existing project edits.
- Enables **Add animation to project** for standalone loaded banks, with an explicit game-bank destination picker.
- Shows **Bank added to project** after automatic staging, explaining why no second Add is needed.


## 0.24.3 — Build ISO fixes

- **Build ISO…** is available after opening a game, even with no edits or selected resource.
- **Build ISO only** saves without PCSX2; **Build & boot in PCSX2** remains a separate option.
- Zero edits produce a byte-for-byte unchanged ISO copy.
- Extracted-folder sessions can build using their matching original ISO.
- Current staged edits are included without requiring a project save first. Validated character/texture imports and game-backed animation imports are staged automatically.
- Corrects the glowing author name to **Z mods**.
- Preserves source matching, output protection and replacement read-back checks.


## 0.24.2 — Zmods author credit

- Adds **Zmods** to the centered author credits with the same looping gold glow and shimmer.
- Updates application author metadata and public credits.
- Existing export, animation and editing behavior is unchanged.

## 0.24.1 — Clearer animation export name

- Renames **Animation only (Godot 4)** to **Animation only (GLB)**.
- Updates the tooltip, export progress messages and accompanying guide heading.
- The format, exported skeleton/animation data and Blender add-on are unchanged. Godot remains a documented import example.

## 0.24.0 — Public distribution and in-app updates

- Startup/manual update checks and New update available for a newer verified release.
- Signed EXE downloads, installation, automatic relaunch and previous-EXE recovery.
- Gold dragon EXE/window icon in seven sizes.
- Clean Windows package without C# source, build projects or PDBs.
- Separate optional Blender bridge 0.22 download.
- Beginner guides and detailed checklists distinguishing implemented/experimental/unfinished features.

Model, texture, animation, native-rebuild and ISO algorithms are retained from 0.23.0. Updater checks do not imply new gameplay validation of those algorithms.

## Earlier development

0.23 added animation-only GLBs for Godot 4 and explicit rest tracks. 0.22 added eligible higher-precision animation edits and corresponding game compatibility support. Earlier versions developed original rigs, texture-grouped exports, Blender native return, animation inspection, projects and separate ISO rebuilding.

Historical internal ZIPs can include application source and are not suitable public download packages.
