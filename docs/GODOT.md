# One character, separate animations in Godot 4

[Home](../README.md) · [Animation Lab](ANIMATIONS.md)

## 1. Export the model once

Select the original character in Studio and export a rigged GLB. Import it into Godot as a scene. Keep skeleton names, hierarchy, scale and rest pose intact. Use an inherited/wrapper scene for scripts, collision and animation control.

## 2. Export separate clips

Open Animation Lab for **that same character/rig**. Choose **Animation only (GLB)**, select the FPS and use Save clip or Save all clips. Copy desired GLBs into your Godot project. The character mesh is not repeated per animation.

## 3. Import each as a library

1. Select the animation GLB in FileSystem.
2. Set **Import As → AnimationLibrary** in Import settings.
3. Match animation import/bake FPS to the Studio export, for example **60**.
4. Keep **Remove Immutable Tracks OFF**.
5. **Reimport**; restart the editor if requested.

Studio keys rest poses for bones absent from the native clip. Retaining those tracks lets a new clip reset bones left in a previous pose. Settings are per file: verify every added animation. Changing FPS does not recover an unknown original game playback rate.

## 4. Load libraries onto the character

1. Add/select its **AnimationPlayer**.
2. Open **Animation → Manage Animations** and load the animation-library GLB.
3. Give each library a distinct name, such as `idle`, `walk` or `combat`.
4. Set AnimationPlayer's **Root Node** to the scene root from which exported track paths resolve.
5. Select the library/clip and play. Add more libraries similarly.

Do not instantiate animation-only GLBs as additional visible character scenes. Their skeleton definitions describe tracks; the visible character comes from the original model scene.

## 5. Loops and animation states

Configure a clip's **Loop Mode** in the GLB's advanced animation import settings and reimport. Idle, walk, run and falling clips usually loop; landings/one-shot attacks usually do not. Direct changes to generated imported resources may be overwritten by reimport.

An **AnimationTree** can reference the AnimationPlayer. Create states such as Idle, Walk, Run, Jump, Fall, Land and Attack, assigning library/clips to them. The controller chooses transitions from speed, ground contact and input. Studio supplies data; it does not automatically create a playable Godot controller.

If the clip moves its original root, choose whether to consume root motion or make an in-place adaptation. Combining controller movement with unhandled root translation can double movement or cause sliding.

## Troubleshooting

- **No movement:** verify AnimationPlayer root and track paths to the visible skeleton.
- **Stale pose:** keep Remove Immutable Tracks OFF on all clips and reimport.
- **Wrong size/orientation:** match model and animation import transforms.
- **Different character distorted:** names alone are insufficient; different rest poses/proportions need retargeting or adaptation.
- **Cannot return animation-only file to Studio:** use Character + animation with native companions for the Blender/native workflow.

Godot menu placement can vary by minor version. See [Godot's animation-library import guide](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html#using-animation-libraries).
