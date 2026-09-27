# Release notes

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
