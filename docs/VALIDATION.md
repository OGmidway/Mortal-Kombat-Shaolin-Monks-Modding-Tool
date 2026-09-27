# What has been tested

[Home](../README.md) · [Features](FEATURES.md) · [Roadmap](ROADMAP.md) · [Release notes](../CHANGELOG.md)

This page records the evidence behind the current documentation, through **0.25.3**. It separates automated/tool checks from reported gameplay. A working preview, a byte-correct ISO and a working character in gameplay establish different things.

## Confirmed and reported gameplay

| Workflow | Result | Scope |
|---|---|---|
| Kratos replacing Reptile, model 6732 | The maintainer reported Kratos fully visible, running around and working in-game after the 0.25.2 mesh fix. | Confirms that prepared replacement and tested behavior. Other models, moves, attachments and circumstances need their own checks. |
| Blender animation → Studio → rebuilt game | A tester previously reported a successful animation replacement in-game. | A useful working baseline; not a claim that every codec, rig or custom action has been tested. |
| New Kabal custom-action import in 0.25.3 | Preview, project persistence and ISO output verified. | Gameplay confirmation for this new action is still pending. |

## Recent technical checks

| Area | Checked | What this does not establish |
|---|---|---|
| Character rendering fix, 0.25.2 | Retail palette dispatch/draw-gate behavior; corrected 5,165-triangle replacement in 57 accepted batches; original skeleton preservation; 118 untouched original model files retained; packaged EXE build and exact model/texture readback from ISO. | Unlimited mesh size or every native draw path/revision. |
| Animation import, 0.25.3 | 30 checks using a supplied three-action Blender GLB: take selection, complete rig verification without custom metadata, new lengths, unchanged neighboring clips, actual WPF preview/staging, project reopen, existing bridge/high-precision imports and rejection of incompatible skeletons. Final EXE import and ISO bank readback matched. | A gameplay test of the new Kabal motion or automatic retargeting. |
| Native bank imports, 0.24.5 | 29 checks covering a supplied Scorpion idle bank, reload/project persistence, mapped channel growth, explicit override and ISO readback. | Compatibility of arbitrary mismatched bone channels. |
| Audio, 0.25.0 | Native ADX header/loop handling, independent decoder comparison, project/UI round trips and rebuilt USA ISO. | Every game's sound event, transition or longer-track behavior. |
| Updater, 0.25.1 onward | Startup-confirmed cleanup and recovery checks; signed manifests/payloads; published asset hashes; older update client discovery of 0.25.3. | Windows Authenticode certification or an infallible network connection. |

## Earlier coverage retained in current workflows

- Character export/grouping research covered 115 decoded skinned resources through Blender round trips.
- Selected animation export/native paths were checked against 91 recovered USA game profiles.
- Actual Godot AnimationLibrary playback covered three rigs and six clips.
- Higher-precision work included actual Blender export fixtures, native evaluator checks, untouched-clip preservation and ISO compatibility-patch tests.

These are historical scoped checks, not a statement that the full corpus was rerun for every patch release. GLB is an interchange format; equivalent Unreal/Unity import behavior is not certified by the Godot tests.

## Reporting a new result

Include Studio version, game revision, model/bank/clip IDs, what you imported, the chosen action/FPS, and the behavior you tested. For a failure, include the exact error and the smallest useful reproduction. Do not upload game ISOs, BIOS files or full extracted archives.

After rebuilding, boot the newly built ISO fresh. A save state can retain resources loaded from an earlier build, so it is not a reliable first check of a replacement.
