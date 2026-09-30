# Community Mod Packs

## Upload a pack

1. Open **Community Workshop → Create / Upload Mod Pack**.
2. Click **Add Files...** and select multiple files.
3. Enter **Replace Game File ID** for each file. Check IDs suggested from filenames.
4. For a GLB or character package containing textures, enter its **Texture ID** too. For native texture BINs, add each as its own row instead.
5. Save a new `.mksmmodpack` file, then enter the listing title, description, version and optional cover image. Publish.

No game ISO or emulator test is required to upload. Destination IDs are required for packs so recipients know where each file goes. File IDs are archive resource numbers, not filenames on your PC.

## Install a pack

1. Open your own game ISO in Studio.
2. Select a Workshop pack and click **Apply Pack to Project...**, or use **Import Mod Pack...** for a local download.
3. Wait for all files to be checked. Review the destination list. Existing edits that would be replaced are marked.
4. Click **Apply All Replacements**. Save your project, then **Build ISO**.

Cancelling or a failed validation leaves the project unchanged. Applying stages edits together; it does not overwrite the original ISO. Existing per-resource undo is retained. Downloads alone never change a project.

## Supported contents

- Ready-to-import native game files: models, texture banks, animation banks, audio banks and other numbered archive resources accepted by Studio's native replacement path.
- Studio-ready character/rigid-object GLBs, compiled against the selected original destination at installation.
- `.mksmcharacter` bundles, checked against their original model and texture hashes.

GLBs must already meet the existing Studio import requirements. Raw PNG/WAV files are not automatically converted by packs. Rebuild nested audio tracks into their containing bank before packaging. A pack cannot target the same resource twice, including a character's companion texture destination.

Packs currently replace existing numbered archive resources; they do not add new archive entries or replace arbitrary ISO files such as the executable. Limits are 100 files, 200 MB compressed and 384 MB expanded. Existing native resource and runtime limitations still apply. Test the rebuilt ISO to confirm gameplay compatibility.
