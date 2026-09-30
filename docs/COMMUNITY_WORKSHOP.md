# Community Workshop

[Home](../README.md) · [Characters](CHARACTER_START_HERE.md) · [Build and test](PROJECTS_AND_TESTING.md)

## Download a character

1. Open your game ISO in Studio.
2. Click **Community Workshop** at the top.
3. Select a character. Check its destination model, texture set, game revision and creator's notes.
4. Click **Download + add to project**. Studio checks its checksum, native structure and exact original model/texture sources before staging the changes.
5. Close Workshop, review the character, **Save project**, then **Build ISO**.

**Download only** saves a package without changing your project. If an installed edit conflicts, Studio asks before replacing it. Workshop never writes directly over the original ISO. A package passing validation is not a guarantee that its size or gameplay behavior works in the engine.

The workshop starts empty until creators publish. Existing demonstration files on the developer's machine are not uploaded automatically.

## Subscribe and update

Subscribe remembers a listing on this computer. Opening Workshop or clicking Refresh fetches current listings, independently of Studio releases. A changed package hash is shown as a subscribed update. Download and apply it when you choose; no automatic replacement or background polling occurs.

## Publish your character

1. In the character replacement workshop, use **Save native copies** to obtain a `.mksmcharacter` package. A loose GLB cannot be published directly.
2. Open the original game revision used to create the package. Select the destination character and its matching texture set in Studio. Some native texture sets have identical bytes, so this selection identifies the intended destination.
3. Open Community Workshop and click **Sign in with GitHub**. Follow GitHub's browser/device sign-in. GitHub CLI is included; do not send a password or token to the workshop owner.
4. Click **Upload character** and choose the package.
5. Review the destination, title, version, description and game revision. Click **Publish publicly**.

Studio creates a public `MKSM-Workshop-Mods` repository under your GitHub account if it does not exist. It uploads the package as a release asset, then creates a workshop listing in the official Studio repository. If that repository already exists privately, Studio asks you to resolve that rather than changing visibility silently. Publishing shares the entire package, including its embedded Blender GLB and textures.

Uploads appear without an approval queue. Files are hosted under each creator's account. GitHub sign-in is needed for publishing/managing, but browsing and downloads are public. Packages are capped at 200 MB compressed and 384 MB expanded for this first release.

To update: select one of your listings, click **Upload new version**, choose the new package and enter a higher version such as `1.0.1`. Subscribers see a change after refresh. If the upload succeeds but listing creation fails, your GitHub download release and the local Workshop publish folder retain the package and listing text for recovery.

## Administrator controls

Sign in as **OGmidway**. Studio verifies the account's stable GitHub ID and administrator access to the official repository before showing removal controls for other creators' listings. This is enforced by GitHub permissions, not a secret button or a special public EXE.

**Remove listing** closes the listing; owner moderation also locks it. It disappears on the next refresh. Creators can remove their own listings. Removal does not erase packages already downloaded, existing projects, or the creator's separate download repository.

The owner source package is delivered privately, not as a public release asset. It includes the application source and a rebuild script. It contains no GitHub credentials or private update-signing keys.

## First-release boundaries

- Native character packages only; no general level/audio workshop yet.
- No thumbnails, ratings, comments UI, automatic subscription download or automatic mod installation.
- Lists the newest 1,000 open GitHub entries; a notice appears if the limit is reached.
- GitHub rate limits, availability and account permissions apply.
- Tested with native package fixtures, source conflicts, owner-role verification and live catalog reads. Creator publication/removal orchestration was tested against a mocked service; a real public character round trip has not yet been performed.
