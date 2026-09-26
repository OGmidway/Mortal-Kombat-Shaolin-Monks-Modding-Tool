# Save changes, build an ISO, test the game

[Home](../README.md)

## A reliable first test

Begin with one recognizable change, such as a supported texture recolor. Confirm the original ISO boots, save the edit, build a new ISO and check that asset in-game. This establishes a working source/project/emulator setup before complex replacements.

## 1. Stage and save

Supported texture, shape and native replacements enter the editing project. Animation imports first live in lab preview: choose **Add animation to project** to stage them.

**Save project…** writes a `.mksmproject`. **Open project…** validates it against the source game. The project is the edit collection, not an ISO. Use **Undo last change** for the selected resource or **Restore original** to remove its staged edit. **Export edited files…** saves standalone native copies. Save before closing/updating.

## 2. Use the correct native path

**Import Blender edits…** returns shape/UV edits. **Import character…** rebuilds supported character replacements. **Replace game file…** stages a supported already-rebuilt native resource. Select the intended original resource ID, not a nearby guess.

Rebuilt supported resources may grow/shrink in byte size; the builder relocates their archive data. This removes exact whole-resource byte-size equality, not mesh, dimension or codec constraints.

## 3. Build a separate ISO

1. Open the original ISO and saved project.
2. Review staged resources/previews.
3. Choose **Build & play…**.
4. Select a new output ISO path with enough free space.
5. Let rebuilding and verification finish. An incomplete output is not a playable image.
6. Keep the original ISO/project for comparison and recovery.

The builder updates supported archive placement and ISO extents and verifies installed bytes. Tagged higher-precision animation edits require the matching supported compatibility patch. An unvalidated game executable revision is not treated as equivalent.

## 4. Launch PCSX2

Choose your PCSX2 executable in the testing workflow. A separate test profile keeps test settings/memory cards separate from normal defaults. Configure your own BIOS and controls as needed.

**Test in PCSX2…** can boot an existing ISO. **Build & play…** installs current staged edits into a new one. PCSX2, BIOS and game files are not included.

## 5. Verify gameplay

A successful rebuild establishes that supported bytes were installed and passed the builder's checks. It does not prove correct behavior in all gameplay situations.

For characters, test standing, movement, attacks, damage, attachments and transitions. For animations, test transitions into/out of the clip. For textures, compare distances, effects and lighting. Use an unmodified baseline.

Record source revision, original IDs, edit type and failure point. Test one change at a time to identify the cause.
