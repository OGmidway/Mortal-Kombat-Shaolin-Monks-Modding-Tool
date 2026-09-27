<div align="center">

<img src="assets/icon.png" width="96" alt="MKSM Studio gold dragon icon">

# Mortal Kombat Shaolin Monks Modding Tool by OG Midway

**MKSM Studio — by OGmidway, RelaxDirk & Z mods**

Explore the game. Work with its characters and animations. Build a separate modded ISO to test your changes.

[**Download for Windows**](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/latest) · [Start here](docs/GETTING_STARTED.md) · [Feature checklist](docs/FEATURES.md) · [Report a problem](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/issues)

</div>

![MKSM Studio home screen](assets/studio.png)

## 1. What is MKSM Studio?

MKSM Studio is a Windows application for researching and modifying **Mortal Kombat: Shaolin Monks for PlayStation 2**. Open your own game ISO directly, browse supported resources, preview textured characters and their original skeletons, play native animations, export to Blender or Godot, and collect supported edits in a project. Build ISO writes a **new ISO** and can launch it in PCSX2.

You do not need to mount or unpack the ISO to begin. You do need your own game files. The download does not contain the game, a BIOS, character assets, or an emulator.

This is an independent, experimental modding tool. The best-tested workflows use the researched **USA PS2 revision**. Support for one resource or revision does not establish support for every version of the game.

## 2. Download and open

1. Open **[Releases](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/latest)**.
2. Download **MKSM-Studio-0.25.2-win-x64.zip** (or the newest equivalent Windows ZIP).
3. Extract the entire ZIP into a regular folder you can write to, such as `Documents/MKSM Studio`. Do not run it from inside the ZIP.
4. Double-click **MKSM Studio.exe**, recognizable by its gold dragon icon.
5. Click **Open game ISO** and select your Shaolin Monks PS2 ISO.

The Windows x64 runtime is included. Blender and PCSX2 are optional, separate applications. Download **MKSM-Blender-Bridge-0.22.zip** separately for the Blender editing workflow.

**Use the Windows download under release Assets.** GitHub's automatic **Source code (zip/tar.gz)** downloads contain this documentation repository, not the application.

## 3. Pick a workflow

| I want to… | Start here |
|---|---|
| Learn the interface and camera controls | [Getting started](docs/GETTING_STARTED.md) |
| See exactly what works and what is unfinished | [Feature checklist](docs/FEATURES.md) |
| Export a character with its skeleton, weights, textures and UVs | [Models and Blender](docs/MODELS_AND_BLENDER.md) |
| Replace character geometry or make shape edits | [Models and Blender](docs/MODELS_AND_BLENDER.md#returning-a-character-to-the-game) |
| Play, export or edit animation clips | [Animation Lab](docs/ANIMATIONS.md) |
| Use separate animations on one character in Godot 4 | [Godot guide](docs/GODOT.md) |
| Replace music/voices and set native ADX loop points | [Audio workshop](docs/AUDIO.md) |
| Replace an image or inspect native files | [Textures, audio and inspection](docs/ASSETS_AND_INSPECTION.md) |
| Save edits, rebuild an ISO and launch PCSX2 | [Projects and game testing](docs/PROJECTS_AND_TESTING.md) |
| Install a newer version from inside the app | [Updates and troubleshooting](docs/UPDATES_AND_HELP.md) |

## 4. At a glance

Checked items are implemented for supported data. They do not mean every game revision or every possible edit has been tested.

- [x] Open an ISO directly or browse an extracted game folder.
- [x] Preview supported textured models, levels and original skeletons.
- [x] Orbit, pan, zoom and fly around the 3D preview.
- [x] Export rigged GLB characters organized by texture, with UVs and weights.
- [x] Play and scrub supported native animation clips on the selected rig.
- [x] Save one clip or an organized bank of individual clip folders.
- [x] Export animation-only GLBs without repeated character geometry.
- [x] Return supported Blender character and animation edits to native resources.
- [x] Replace supported ADX audio, set exact loop points and rebuild its sound collection.
- [x] Stage changes in a saved project and rebuild a separate ISO.
- [x] Relocate supported rebuilt resources when their file size grows or shrinks.
- [x] Check GitHub for newer signed updates and install/relaunch from the app.
- [ ] Arbitrary texture resizing, including a general 4096 × 4096 in-game workflow.
- [ ] Unlimited polygon counts, texture memory, bones or native engine capacity.
- [ ] Automatic compatibility with any character rig, game revision or animation bank.
- [ ] Complete gameplay validation of every rebuilt character and animation.

See the [full checklist](docs/FEATURES.md) for supported, experimental and planned work.

## 5. Updates and source availability

The application checks for a newer release when opened. **New update available** appears only when a verified release has a higher version number. Choose **Install update** to download, verify, install and reopen the application. Save pending project edits when prompted. Failed checks do not prevent offline use.

This public repository contains documentation and release downloads. **The main application's C# source, build projects and debug symbols are not distributed here.** The optional Blender bridge is a separate Python add-on and is readable by design. A compiled executable is not a guarantee against reverse engineering.

## 6. Credits and support

**Tool authors: OGmidway, RelaxDirk & Z mods.** See [Credits and notices](docs/CREDITS.md) for research references, runtime licenses and dragon artwork attribution.

For a useful bug report, include the tool version, game region/revision, resource ID, steps to reproduce, and exact error. Share a screenshot or text report where helpful; do not upload an ISO, BIOS or extracted game archive. See [support details](docs/UPDATES_AND_HELP.md#reporting-a-problem).

Mortal Kombat and Shaolin Monks belong to their respective rights holders. This project is not an official game release.
