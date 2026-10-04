# MKSM Blender Bridge 0.26.0

Author: OG Midway. Contributors: RelaxDirk and Z mods.

## Install

Extract this ZIP. In Blender, choose Edit > Preferences > Add-ons > Install from Disk, select io_mksm_studio.py, then enable MKSM Studio Bridge. Restart Blender after replacing an older add-on. In the viewport, press N and open MKSM. The panel should show 0.26.0. Tested with Blender 4.2.22 and 5.2.2. Studio's EXE updater does not install Blender add-ons.

## 1. Retarget Character

In Studio, export the ORIGINAL character slot with its textures using Save for Blender. Keep the GLB, original model, texture BIN and metadata together. Open its GLB with Open Game Character. Import your new character separately using Blender's importer for that format. Keep both skeletons; never rebuild or change the game skeleton's rest pose.

Select only your new character meshes. Choose their Source Skeleton and the original Game Skeleton. Put both rigs in Rest Position. Click Match Bones. Review every match, especially left/right, fingers, cloth and root bones. Select a row to change its game bone. Blend Two Game Bones supports splitting one source influence between two destinations.

Unknown weighted bones must be mapped before preview; ambiguous root and cloth names are deliberately not guessed. Suggestions cover native names, common MK9/Mixamo names and ValveBiped hands. They are suggestions, not proof of a correct match. This workflow uses existing authored weights. An unweighted model still needs weight painting first.

By default, your manually fitted shape stays in place. Optionally enable Fit Proportions for similarly aligned rest poses: it estimates scale from main body segments and adjusts the mesh using weighted joint offsets. It rejects major rest-pose misalignment instead of silently twisting the character. This is not an automatic A-pose/T-pose solver. Fingers, loose cloth and unusual proportions may need manual fitting.

Create the retarget preview. Originals are hidden and kept; the native skeleton is unchanged. Check shoulders, elbows, hips, knees, head, hands and garment overlap in several poses. Return to rest before exporting. Report opens the bone map, fit scale and native triangle-weight conflicts. Discard restores the originals. Already bound to the game skeleton? Skip retargeting.

## 2. Reduce Geometry

Select preview body meshes. Set a combined Triangle Budget and allowed Surface Change. Create Reduction Preview. Inspect silhouette, UV seams and joint poses. Report shows sampled surface change, counts and native weight conflicts; Discard restores the preceding meshes. Reconnect Matching Seams only welds effectively coincident points with matching weights. Surface sampling is not a guarantee of animation fidelity. Compiled game counts can exceed Blender counts because of UV seams and native batching.

## 3. Prepare Textures

Save a backup. Remove only obsolete reference body meshes from the working scene; retain the game skeleton and required native extras. Select the new body only. Prepare Game Textures uses available native slots; 0 means automatic. Hidden retained meshes still reserve their textures. Check the result in Material Preview. If every slot is reserved, review obsolete reference meshes rather than deleting required attachments. Skip this step if your materials already use the correct game slots and sizes.

## 4. Check & Export

The union of bone influences across a triangle must fit the native palette; limiting each vertex alone is insufficient. Preview Weight Cleanup makes copies, removes influences within your explicit Max Weight Removed limit, and reports the loss. Start at 25%; higher limits can visibly alter motion. Retargeting does not silently perform this cleanup. Inspect poses again after cleanup or reduction.

Select the new body and all required skinned extras. Export Selected Character (.glb). In Studio use Import Character for changed topology; Import Blender Edits is for topology-preserving edits. Check the compiled model, textures, old rigid head and spear/dragon attachments before rebuilding your ISO. The generic retargeter does not automatically remove rigid heads or restore special-move attachments; native attachment handling remains character-specific. The separately supplied Scorpion package contains its inspected head/spear corrections.

Keep an untouched ISO and test your replacement in gameplay and cutscenes. Passing export checks does not certify game playback or increase memory limits. This release was not validated through every animation or character. Reports are available in Blender's Text Editor.

Other existing weapon, animation and native package tools remain in their own panels. Native package export requires a compatible local Studio installation.
