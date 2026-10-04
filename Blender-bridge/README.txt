MKSM BLENDER BRIDGE 0.25.2
Author: OG Midway. Contributors: RelaxDirk and Z mods.

INSTALL / UPDATE
Extract the ZIP. Blender > Edit > Preferences > Add-ons > Install from Disk.
Choose Blender-bridge/io_mksm_studio.py. Enable MKSM Studio Bridge.
Restart Blender after replacing an older add-on. Press N > MKSM.
Panel should say MKSM Bridge 0.25.2. Supports Blender 4.2 or later.
Install separately: the Studio EXE updater does not update Blender add-ons.

GEOMETRY REDUCTION PREVIEW
1. Select your new mesh objects; keep the original game skeleton unchanged.
2. Optional: reduce replacement geometry > Triangle budget (selected meshes).
3. Allowed surface change (%) defaults to 1% of each mesh's bounding diagonal.
4. Optional equal-weight seam welding reconnects effectively coincident points.
5. Click Preview reduced geometry on copies. Original meshes are hidden, kept.
6. Check silhouette, UV seams and joint poses. Read Geometry reduction report.
7. If rejected, increase the triangle budget or allowed surface change.
8. To undo the preview, select a reduced copy and click Discard preview.
9. Select approved preview meshes for texture setup or character export.

Reduction uses geometric edge collapse, preserves UV/material layers and
interpolates bone weights on copies. It does not silently remove influences
to satisfy the game's three-bone triangle palette. Use the separate weight
cleanup preview if needed. Keep its 25% removal limit until inspecting poses.
The cleanup now checks cumulative loss correctly and handles difficult
triangle palettes first, preventing cascading avoidable removals.

The geometry check samples vertices and face centers in both directions.
It is not a mathematical surface bound or an animation/texture guarantee.
Thin disconnected details may need a higher budget or manual adjustment.
GLB UV seams and native draw batches can increase compiled vertex counts.
Use Studio's compiled counts; this feature does not raise game memory limits.

Validation: Blender 4.2.22 fixture and Blender 5.2.2 real character checks;
source mesh/UV/weights and rig preservation; preview/discard; rejected
deviation, shape keys and missing weights; failure rollback; weight-cleanup
regressions on both versions. Game playback is not certified.

Read START_HERE.md for the complete character workflow.
