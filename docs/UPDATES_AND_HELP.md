# Updates and troubleshooting

[Home](../README.md)

## Update inside Studio

1. Open Studio online. It checks the official latest GitHub release in the background.
2. A verified newer version changes the button to **New update available**. **Check for updates** also works manually when no operation is busy.
3. Click **Install update** to download and verify.
4. Save pending project edits when asked. Canceling the save cancels installation.
5. Studio closes, applies the EXE and reopens automatically.

Only the application EXE is replaced. ISOs, projects and exported assets stay untouched. Reopen your game/project after relaunch. The optional Blender bridge is separate: install a newer bridge through Blender if release notes require it.

## Verification

The official repository is **OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool**. Studio reads `update.json` and `update.sig` from its latest public release. It verifies the publisher signature using its embedded public key, checks the version, and downloads the exact named EXE. Signed size, SHA-256 and executable version/product must match.

This update signature is separate from Windows Authenticode. This release does not claim a Microsoft-trusted code-signing certificate or guarantee no Windows reputation warning.

A failed check is not proof of being up to date. Offline use remains available. The updater refuses downgrades and uses GitHub's latest stable-release route.

## Folder and recovery behavior

Use a regular writable folder. Running inside a ZIP, protected folder or through a junction/symbolic link can prevent updates. Extract the full latest release into a new ordinary folder if necessary. Administrator elevation is not requested.

The updater temporarily keeps `MKSM Studio.previous-<id>.exe` for recovery. After the new application confirms successful startup, Studio deletes this old build and older updater-created backups in the same installation folder. It also removes the verified temporary download/helper EXEs for that completed update. Your projects, settings, game files and exports stay intact; unrelated files and manually downloaded release folders are not deleted. Locked files are retried briefly.

If the new application fails before acknowledging startup, the updater attempts to restore/reopen the previous version. A slow, still-running new process is not forcibly terminated; its recovery backup remains until startup is confirmed.

For manual recovery, close Studio and extract the desired complete release into a new folder. Keep ISOs/projects/exports. Older releases may not understand newer projects/native edits, so retain backups when changing versions.

## Common issues

| Problem | Next step |
|---|---|
| Update check fails | Check connectivity and retry later; GitHub availability can affect checks. |
| Verification fails | Do not run the incomplete file. Retry the official release; the existing EXE remains installed. |
| Cannot replace EXE | Close other instances, use a writable normal folder or extract a fresh full release. |
| No newer version | Latest verified release is the same or older; no reinstall needed. |
| Newer updater required | Download/extract the complete Windows ZIP manually. |
| Build ISO unavailable | Open a game ISO or extracted game folder and wait for any active operation to finish. Zero edits are allowed. Folder sources ask for the matching original ISO. |
| Model invisible/incomplete | Fit view; check Surfaces, Extra meshes, texture selection and Transparency. |
| Animation twists/flips | Verify original model, bank, profile and clip; record IDs if reproducible. |
| Blender return rejected | Use the correct shape/replacement/animation path and preserve companions/rig identities. |
| Godot tracks do nothing | Check root paths, skeleton names, transforms and Remove Immutable Tracks OFF. |

## Reporting a problem

Open an [issue](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/issues) with:

1. Studio and Windows version.
2. Game region/revision; ISO or extracted-folder source.
3. Resource ID, bank/clip and export/import mode.
4. Exact steps, expected/actual result and error text.
5. Useful screenshot or small non-game-data report.

Do not upload ISOs, BIOS, extracted archives, signing keys or unnecessary personal paths. IDs and reproduction steps are a good starting point.
