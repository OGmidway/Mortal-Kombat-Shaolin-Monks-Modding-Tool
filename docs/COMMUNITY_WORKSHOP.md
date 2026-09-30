# Community Workshop

[Home](../README.md) · [Characters](CHARACTER_START_HERE.md)

## Share a mod — no ISO required

1. Open Community Workshop at the top right. No game needs to be open.
2. Use the GitHub account box to sign in. Studio opens GitHub and shows a code with Copy Code and Copy Link buttons. Authorize GitHub CLI in your browser.
3. Click **Upload character** and choose `.glb`, `.bin`, `.pme2` or `.mksmcharacter`.
4. Enter a title and description. Add your author name and choose its glow color. You may include suggested model/texture IDs and game revision notes, but an ISO is not required.
5. Optionally attach a texture BIN and a PNG/JPG picture. Click **Publish publicly**.

Your file is shared unchanged. Workshop does not compile, convert, run, or test it against a game. Import requirements are checked later when a downloader chooses to install it. Individual files are limited to 200 MB. Raw GLBs get a basic header check; native BIN uploads are preserved as supplied.

Files are published in your public `MKSM-Workshop-Mods` GitHub release repository. The official Studio repository stores the listing. An existing private creator repository is never made public automatically. New listings appear without an approval queue.

## Browse and download

Select a mod card to see its author, title, description, picture or model preview. The verified GitHub uploader is shown separately from the creator's custom display name.

Without a picture, Studio downloads the file into its preview cache and tries to display its stored rest pose. GLB triangle meshes with embedded images, supported native character BINs and MKSM character packages are supported. It does not force every model into a T-pose. Unsupported, compressed or very large previews may be unavailable; the file can still be downloaded.

Click **Download Files...**, choose a folder, and Studio saves the original file, optional companion texture BIN and a readme in a new mod folder. It verifies download checksums. This does not change your game or editing project.

To install later, open your ISO in Studio, select the destination character, and use Import character for GLB/packages or Replace game file for native BINs. Import companion textures into the intended texture set. Save your project and build your ISO when ready.

## Edit or delete your own mod

Sign in with the account that uploaded it. **Edit Listing** changes the title, description, author name, glow and suggested destination without uploading the file again. **Upload new version** replaces the files or picture and requires a higher version number. Attach companion textures again when publishing a new version if they are still needed.

**Delete Listing** removes your listing from the Workshop by closing its GitHub issue. This does not erase files already downloaded or delete your separate GitHub release assets. Other users cannot edit or remove your listing. OGmidway retains owner moderation controls.

## Sign in once

The bordered account box appears at the top left of the application, including the homepage, and in Workshop/update windows. Connected views say **GitHub · Signed in as username** and **Already signed in**. GitHub CLI keeps credentials in its normal credential store; Studio restores the account when starting. Public application updates do not require login. Private source updates require an invited account.

## Subscriptions and compatibility

Subscribe marks a mod on this computer. Refresh detects changed file hashes; it does not install anything automatically. Old packaged listings remain readable. Raw-file listings require Studio 0.27.3 or newer.

The catalog reads up to the newest 1,000 open GitHub entries. GitHub availability and rate limits apply. Sharing a file does not guarantee game compatibility. User-reported beta native imports have succeeded; other models need their own testing.

## Validation

25 integrated checks cover no-ISO raw uploads, original-file downloads, companion textures, rest-pose previews, glow settings, creator-only edit/delete permissions and the shared account box. Publishing and mutations were tested with a mocked service; no sample mod was posted publicly. The earlier source-channel upgrade from 0.27.0 to 0.27.1 was verified through download, signature checks, extraction and application launch.

The left navigation now has a full metal-style enclosure and a red perimeter glow. The existing Settings > Glow option controls the aura.
