# Getting started

[Home](../README.md) · [Full feature checklist](FEATURES.md)

## What you need

- Windows x64 and a writable folder for the extracted application.
- Your own Shaolin Monks PS2 ISO, or an extracted folder containing its game files.
- Free space for exports and a second ISO if you plan to build mods.
- Optional: Blender for 3D editing; PCSX2 and your own BIOS for game testing; Godot 4 for an independent project.

The application includes its .NET runtime. Internet access is needed for updates, not ordinary local browsing or editing. Native compatibility research and animation profiles primarily target the tested USA PS2 revision.

## First launch

1. Download the Windows ZIP from [Releases](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/latest).
2. Extract it. Keep the accompanying notices and licenses.
3. Run **MKSM Studio.exe**. The title bar shows your version.
4. Choose **Open game ISO**. Select a real `.iso`, not a ZIP containing one.
5. Wait for the collection to load. Choose a category or enter a file number in search.
6. Click a resource to see its preview and available actions.

**Open folder** is for already extracted game files. When you choose **Build ISO…**, select the matching original ISO when prompted. Your staged folder edits will be included.

## Understanding the screen

| Area | What it does |
|---|---|
| Collection on the left | Searches/filters resources. Some entries retain numeric IDs because their original purpose/name is not recovered. |
| Main preview | Displays the selected model, textures, audio or information. |
| Actions above the preview | Changes with the file. A character can offer Save for Blender, Import character and Animations. |
| Edit workshop | Opens/saves projects and manages staged changes. |
| Advanced tools | Reveals native details, hex, strings, extraction and research controls. |
| Status at the bottom | Explains progress, errors and whether you are seeing an edited resource. |
| Check for updates | Checks the official release; becomes New update available when appropriate. |

Hold **Ctrl** to select multiple resources. Use **Export selected files…** for a batch. **Ctrl+F** focuses search, **Ctrl+S** saves the current project, and **F1** opens Home.

## Looking around a model or level

- Drag to orbit; Shift-drag to pan; scroll to zoom.
- **Fit view** brings the geometry back into view.
- **Fly around** enables a free camera. Use WASD and right-mouse look; the viewer displays its controls. **Stop flying** or **Esc** returns to normal viewing.
- **Surfaces…** hides walls, isolates a material or reveals geometry behind another surface.
- **Textures**, **Transparency**, **Outline view**, **Extra meshes** and **Show bones** change the preview.

Visibility choices can affect exports. Show the surfaces you intend to export. Some native alpha channels describe effects rather than ordinary opacity; switch Transparency off if parts become dark or invisible.

Raw positions is a research control. Leave it off for normal use. The viewer translates supported native coordinates to its viewing convention; unusual data may still need investigation.

## Three files you should not confuse

| File | Purpose |
|---|---|
| Original ISO | Unchanged game source. Studio does not edit it in place. |
| `.mksmproject` | Your saved staged edits. Reopen against the matching game source. |
| New modded ISO | A separately built image containing project changes. Test this in PCSX2. |

Exporting a GLB does not install it into the game. Importing/staging the supported native edit and building a new ISO completes that workflow.
