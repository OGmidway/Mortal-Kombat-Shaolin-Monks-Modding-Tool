# MKSM Studio 0.27.11 — Taskbar & Sidebar Clipping Fix

- Maximized Studio and Workshop windows now use the current monitor's usable working area, keeping the Windows taskbar from covering bottom sidebar buttons. Bounds use native pixel coordinates rather than a primary-monitor-only height limit.
- The waving sidebar flag is clipped below the live GitHub profile-card bounds. Its top edge no longer peeks above the profile. The protected region follows layout changes.
- Normal restore dimensions and saved 70–125% UI scale are retained. Existing crimson icons, fonts, Workshop ratings, background video/audio, particles, flag animation and fog are unchanged.

Validation covered actual maximized Studio and Workshop windows against Windows monitor work-area rectangles at the current display scale, restore size, 70%/125% UI scale, four synthetic taskbar/monitor layouts including negative coordinates, and rendered banner pixels above/below the protected profile region. Packaged EXE icons and signed channel packages are checked before publication.

---

# MKSM Studio 0.27.10 — Interface Scale & Windows Icon Refresh

- Settings > Appearance > Interface Scale adds a 70–125% size control with live preview, percentage readout and a 100% reset. Save keeps the choice across restarts; closing without saving restores the previous size.
- Fullscreen now creates more workspace instead of automatically enlarging the interface. Smaller windows fit their available space. Studio, Community Workshop and themed dialogs use the same scale; title-bar controls keep their normal size.
- Both actual EXEs contain the black/crimson dragon icon. Updates now notify Windows about the file and directory, invalidate cached icon associations, and request Windows' icon refresh. Settings > Application > Refresh Windows Application Icon provides the same action if Explorer still shows its cached gold icon. No icon-cache files are deleted and Explorer is not restarted.
- MK fonts, Workshop ratings/sorting, scrolling model portraits, separate signed update channels, movie/audio, particles, banner and fog are retained.

Validation covered live preview/cancel/save/reopen, minimized/maximized/restored windows, small-window fitting, Workshop/dialog scaling, unchanged title-bar height, closed-window cleanup, actual executable icons, signed package hashes and source update replacement/rollback. No new game-memory patches are included.

---

# MKSM Studio 0.27.9 — Crimson Polish & Workshop Ratings

- Redder crimson throughout Studio, Workshop and dialogs; matching OG Midway text and glow. Ordinary Home instructions and section labels are neutral white. Card numbers 01 / 02 / 03 remain crimson.
- MK4 and all 14 bundled font choices resolve from the EXE's own WPF resources using the correct family aliases. Font changes apply when settings are saved.
- The actual Windows executable includes the crimson dragon icon at seven sizes. Successful public/source replacements notify Explorer about that file's changed icon.
- A torn vertical MKSM banner gently waves behind the sidebar, with moving fog at the bottom. Banner and fog have separate switches; Animate Background Effects and the refresh-rate setting control motion.
- Workshop model portraits keep rotation and Shift-drag panning. Mouse-wheel scrolling reads the page without changing camera zoom; full editor zoom is retained.
- Workshop offers Most Popular, Most Downloaded, Recently Updated and My Uploads browsing. Most Popular ranks net likes, then likes, downloads and recent updates.
- Shared Like / Dislike counts use GitHub reactions on each listing. Sign in to vote, switch your vote, or click the chosen thumb again to clear it. Your choice is restored from GitHub; only your own thumb reactions are changed. Feedback animation respects the motion setting.
- Subscribe is now Follow Updates, with clear wording: it compares published file versions on Refresh and does not download files automatically.
- Existing background movie/audio, particle effects, announcements, mod packs, owner permissions and separate signed public/source updates are retained.

Validation covered font resolution, preview wheel behavior, rating changes and restoration, pagination, cancellation, unavailable ratings, animation lifecycle, packaged executable icons, signed packages and source replacement/rollback. No live mod ratings were changed during tests. Experimental game-memory patches and online-user counting are not included.

---

# MKSM Studio 0.27.8 — Crimson Interface & Workshop Downloads

- Gold interface accents replaced with vibrant crimson and pink highlights. Open Game ISO now matches the theme; neutral text stays readable.
- New red-and-black dragon icon for the executable, title bar and taskbar.
- Consistent headings, tabs, scrollbars, message frames, buttons and borders.
- Community Workshop cards and mod details show GitHub file-download totals for the currently published version. Counts are cached briefly; unavailable statistics never block browsing or downloads.
- Download totals count the main mod file only, including direct downloads and uncached 3D-preview fetches. Companion textures and cover images are excluded. Counts are not unique users or lifetime totals across older versions.
- Background movie, audio controls, particles with Off / 15 / 30 / 60 FPS, once-only announcements and manual review remain available.
- Public and private source builds retain separate signed update channels and installation replacement.

Live online-user counting is deferred. Experimental engine/memory patches are not included.

---

# MKSM Studio 0.27.7 — Interface & Community Refresh

- OG Midway is the sole author. RelaxDirk and Z mods are credited separately as contributors.
- Application title, executable metadata, header, Blender helper and project pages use the updated credits.
- Dark integrated title bar with standard window controls; clean rounded outlines replace silver bevels. Buttons highlight with a red glow.
- Red author shimmer/pulse, black panels and restrained gold accents.
- Community Workshop has wrapping mod cards, clear mod titles, compact creator credits and a framed model/image preview.
- GitHub profile panel shows your account avatar. Click your name to open GitHub; account refresh reloads the picture. Permissions still come from the authenticated account.
- Faster particles with Off / 15 / 30 / 60 FPS in Appearance (default 60). Cached drawing brushes and frame-synchronized rendering reduce allocation overhead. Background video playback stays independent.
- Settings are organized into Appearance, Audio and Application. Volume controls retain percentages and live preview; Save stays visible.
- Choose among 14 bundled font styles from the MK font collection, or load a TTF/OTF. MK4 is the default; system font is also available. Reopen Studio after saving a font change. This collection does not include a separately verified MK9 font.
- Green dragon notification beside sidebar Patch Notes for unread release notes, and beside Update Available after a newer release is detected. Slow pulse respects animation settings; reading notes clears it.
- Owner-only source control publishes Message of the Day or custom Patch Notes to all builds. Notifications appear once per publication on next launch, or within two minutes while active and not editing a modal operation. Offline failures do not block Studio.
- Public and private source builds keep separate signed update channels and the existing installation-replacement behavior.

Typed announcements support preview, a red-and-gold temple-style frame, scrolling and keyboard controls. New-version notes and announcements show once; sidebar buttons reopen them for review. Exact in-game font extraction is not included.

This release changes presentation, announcements and credits. Experimental engine/memory patches are not included.

---

# MKSM Studio 0.27.6 — Persistent Source Updates

- Source updates now replace the original application and Source folder. Existing shortcuts reopen the newest version.
- Updates launched by the previous source updater automatically hand off to the original installation.
- Previous executable is removed; local source edits are preserved in a Source-backup folder.
- Locked executable failures restore the original Source folder and keep the original executable.
- Public updates already replace the original executable in place; that behavior is retained.

---

# MKSM Studio 0.27.5 — Sidebar Layout

- Full-height left sidebar containing GitHub account, Studio branding and navigation / game library.
- Continuous vertical divider separates the sidebar from the editing workspace.
- Background movie, dragon and ambient effects stay on the right side.
- Adjusted spacing and compact-window scaling while retaining the existing controls and theme.
- Includes Community Mod Packs and administrator listing removal from the previous updates.

Visually checked on the home screen and model viewer at 1060x700 and 1920x1080. Public and private source update channels remain separate.

---

# MKSM Studio 0.27.4 — Community Mod Packs

- Create one `.mksmmodpack` from multiple files and publish it to Community Workshop without an ISO or gameplay test.
- Assign a destination game file ID to each replacement. Include native models, textures, animation banks and audio, or Studio-ready GLB/character packages.
- Download packs unchanged, or use **Apply Pack to Project** with a game open. Review all replacements and existing-edit conflicts before applying.
- Every file is checked before the group is staged. A failed file blocks the whole pack. The original ISO stays untouched; build a new ISO after applying.
- **Import Mod Pack...** also opens a downloaded local pack.

Limits: 100 input files, 200 MB compressed download and 384 MB expanded input. Existing native-format, rig, texture and game-memory restrictions still apply. Nested audio tracks must be provided as rebuilt native banks. Format validation is not gameplay validation.

Public and private source builds retain separate update channels.

---

# Release notes

## 0.27.3 — Standalone Community Workshop

- Share original GLB, BIN, PME2 or MKSM character files without opening an ISO, converting the model, or running the game. Optional companion texture BINs are supported.
- Download files to a chosen folder; installing them into a game is a separate manual step.
- Mod cards and a larger detail panel, optional pictures, and an interactive rest-pose model preview when no picture is supplied.
- Custom author display name with red, gold, blue, green, purple or white glow. Verified GitHub uploader remains visible separately.
- Creators can edit listing details, upload a new version, or remove their own listing. Owner moderation remains available to OGmidway.
- Shared GitHub account box on the main header/homepage, Workshop and updater windows. Existing credentials are restored; connected views display the username and already-signed-in status.
- 25 integrated checks passed with raw-file fixtures and mocked publishing/ownership mutations. Unsupported model previews remain downloadable. Public and private source channels updated together.


## 0.27.2 — Browser sign-in fix

- GitHub sign-in now opens a dedicated authorization dialog, with a selectable device code, Copy Code, Open GitHub and Copy Link controls.
- Studio opens the official GitHub device authorization page when the code arrives, fixing the noninteractive CLI flow that only printed a link.
- The dialog waits for authorization, shows errors, supports retry, and cancels the pending helper when closed.
- Applies to Community Workshop and private source-update sign-in. Public/private channels remain separate.
- 13 focused sign-in checks passed with a simulated authorization provider. A second user's successful live authorization still needs confirmation.


## 0.27.1 — Workshop uploads and preview images

- Upload prepared GLB characters, native character BIN/PME2 files, or existing MKSM character packages.
- Native models can include an optional texture BIN. The original destination character and texture set remain explicit.
- Add a PNG/JPG preview image, displayed beside the mod description.
- Larger Community Workshop button, in the top-right toolbar only.
- Public and private source builds updated together; update channels remain separate.
- 20 targeted checks passed. Beta model gameplay compatibility still needs testing; this patch does not raise engine limits.


## 0.27.0 - Community Workshop and bundled opening movie

- Community Workshop action in the top navigation: refresh, search, download, subscribe and add native character packages to editing projects.
- GitHub-backed publishing from Studio, creator version updates, and owner-only moderation of other creators' listings. Account permissions are checked online; no administrator credential is embedded in the EXE.
- Exact native source checks, package hashes, bounded downloads and grouped model/texture staging. Subscription changes are checked on workshop refresh; they never apply automatically.
- Complete converted opening movie included for automatic first-launch playback. Custom movie selection previews immediately; saved preferences remain respected.
- Title-case navigation labels, including Models & Levels, Textures & Materials, and Music & Sound.
- First workshop release: native character packages only. Live catalog/account checks and local/mocked publication tests passed; real creator upload/moderation and gameplay still need community testing. No sample character has been published automatically.


## 0.26.2 - Volume controls and responsive home sounds

Improved audio controls and Home navigation.

- Clear 0-100% volume readouts, larger slider handles, click-to-position, and one-percent minus/plus and keyboard steps.
- Live background-volume preview; closing without saving restores the old level.
- Responsive hover/select feedback only on Home. Settings and asset views remain quiet; explicit test-sound buttons still work.
- Removed the hover throttle and per-hover audio buffer setup.
- Join Discord directly below Build game ISO.

Existing modding features, bundled audio, MK4 font and continuous movie playback remain included. Blender Bridge is unchanged at 0.25.1.


## 0.26.1 — Archive styling and continuous background playback

- Aged-metal frames, MK4 title font, responsive archive cards and large-window scaling.
- Home added to left navigation and library; clearer model, material and audio section names.
- Bundled MP3 menu music and WAV cursor/select effects, available without first opening an ISO.
- Direct Windows interface-sound playback, routed hover handling, test buttons and volume-mixer shortcut.
- Separate dragon visibility and background audio selection: game music, movie audio or off.
- Background movie continues through asset previews and, by default, while another app has focus.
- Existing modding, rebuilding, signed updates and Blender Bridge 0.25.1 remain unchanged.

## 0.26.0 â€” Workshop presentation and settings

- New home navigation and clearer browse â†’ edit â†’ build workflow, retaining MKSM red, black, gold and dragon artwork.
- Startup update prompt only for a newer signed release; manual checks remain available.
- Opening-movie background with local SFD conversion through FFmpeg, or direct MP4/WMV selection.
- Menu music from the user's game, defaulting to 7051's ambient track; choose another previewed track.
- Native shared cursor-move and cursor-select samples decoded locally for hover/click feedback.
- Separate settings switches for video, music, interface sounds, particles, glow and animation; independent volume controls; Discord link.
- Cached media, delayed search filtering, bounded decorative refresh and pause-on-inactive/asset-preview behavior.
- No new engine memory patch or guarantee for oversized characters. See the research status for the confirmed failure mechanisms and remaining validation.


[Current download](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/latest) Â· [Previous builds](docs/PREVIOUS_BUILDS.md) Â· [Roadmap](docs/ROADMAP.md) Â· [Validation](docs/VALIDATION.md)

## 0.25.6 â€” Easier character material preparation

- Blender Bridge **0.24** adds **Prepare Character for MKSM**: select replacement meshes already weighted to the original rig. The bridge creates copies, generates a shared UV layout, bakes opaque base color into the largest native body texture slot, and assigns the original material ID.
- Preserves donor mesh positions, topology, weights and original scene materials/UVs. Selected source meshes are hidden in the viewport after preparation and remain available as a backup. The preparation report identifies the atlas size/material and warns about texture sharing with native attachments.
- Adds **Save Prepared Character for Studio**, which exports only the latest prepared copies and the original rig. Other hidden bodies are excluded.
- Checks missing textures, source mismatches, unsupported shaders/transparency, unapplied transforms/modifiers and the three-bone-per-triangle limit. Failures clean up temporary data and restore render settings.
- Adds preparation guidance in Studio's character workshop and exported Blender instructions. Keeps all previous weapon, hex, animation and updater fixes. Archives 0.25.5 under Previous Builds.

Install **MKSM-Blender-Bridge-0.24.zip separately**; Studio's in-app updater updates the Windows application, not your Blender installation. Restart Blender after replacing the add-on.

Validated in Blender 4.2.22 with two donor meshes/materials against three destination rigs (6412, Reptile 6732 and Kabal 6622), patterned UV placement, preserved source geometry/weights, failure cleanup, GLB/native compilation, skeleton checks and package reload. This release does not claim gameplay certification of automatically prepared characters. One native-size atlas can reduce detail; transparency, special shaders and attachments sharing the edited image may still require manual work.

## 0.25.5 â€” Missing weapon import button

Fixes the missing **Import weapon / objectâ€¦** toolbar button on rigid models, including **0121** and **0443**. The old visibility rule only showed the action for skinned characters.

- Shows the correct action for rigid models in normal and Advanced modes.
- Keeps unsupported object layouts disabled with an explanation.
- Retains character import and hides model actions when selecting textures.
- Verified the actual rendered toolbar and clicked it to open the weapon workshop; seven UI checks passed. No native import/build format changes.

Update inside Studio with **Check for updates â†’ Install update**, reopen your ISO, and select **0121**. The button is above the 3D preview, beside **Import Blender editsâ€¦**. Blender Bridge **0.23** remains current.

## 0.25.4 â€” Hex transfer and weapon/object editing

- Adds **Transfer hex dataâ€¦** to the main Advanced Hex tab and Animation Lab. Copy from game resources/files, reuse the current bytes, or paste hex. Select exact offsets or one-based 16-byte lines; destination length stays unchanged.
- Reviews before/after bytes, validates available native structures, rejects invalid/stale changes, and stages game-linked edits for ISO building. Standalone animation edits refresh preview; patched native copies include a transfer report.
- Adds **Import weapon / objectâ€¦** for fully decoded unskinned type-0 models. Copy an existing game model and texture set, or rebuild a Blender GLB with new vertices/triangles, normals, UVs and supported material images.
- Preserves native rigid attachment/transform records and rebuilds local bounds. Collision, hitboxes, attacks and character rigs are not authored by this workflow.
- Adds **Save Weapon / Object for Studio** in the separate **Blender Bridge 0.23** download. Existing character and animation workflows remain available.
- Adds step-by-step hex and weapon guides, including **0443 tiger-hook sword â†’ 0121 kama**, with **0442 â†’ 0120** textures. Archives 0.25.3 in Previous Builds.

Validated with actual Blender export, 18 supported rigid-resource round trips, WPF preview/staging, project save/reopen, byte-range failure cases and ISO resource readback. New weapon behavior and arbitrary hex edits still require gameplay testing. File resizing through hex editing is intentionally unsupported.

## Documentation refresh after 0.25.3

- Updates the overview, completed-feature hierarchy, roadmap, validation record and troubleshooting through 0.25.3.
- Records the reported in-game success of the corrected Kratos/Reptile replacement; leaves the newly imported Kabal action's gameplay result pending.
- Adds Previous Builds with release/download links and automatic index refresh during release packaging. Existing assets and update signatures are retained.
- This is a website/documentation update; the application remains 0.25.3.

## 0.25.3 â€” Blender animation re-import

- Adds an action/take selector when importing a GLB, so Blender files with several saved actions can replace the intended clip. The importer never silently chooses the first take in a multi-animation file.
- Supports completely new keyframes and a new duration on the original rig. The import dialog offers the take's length/new keys and matching Blender FPS.
- Recovers missing Blender Custom Properties only when the complete skin uniquely matches the selected native bone names, hierarchy and inverse bind matrices. Changed or ambiguous skeletons remain rejected.
- Labels native type-11 clips **Higher precision (already active)**. Eligible type-6 conversion remains available; other disabled cases have explanatory tooltips.
- Shows import failures in a dialog and identifies the imported action in the result. Project-staging failures are reported instead of appearing successful.

Validated using a supplied three-action Blender GLB, original and high-precision bridge exports, the Animation Lab preview, project save/reopen and native ISO readback. New motion still needs its own in-game test. The character mesh fix from 0.25.2 is retained.

## 0.25.2 â€” Character mesh draw compatibility

- Fixes character rebuilding that put replacement geometry into four-bone batches. The researched USA character draw path skips these batches, even though Studio can preview them.
- Automatically groups compatible replacement triangles into batches using at most three bones, preserving their weights.
- Rejects triangles that themselves reference more than three bones, with the mesh name and triangle number. Studio does not silently remove influences.
- Checks native character packages, native model replacements, and staged edits before writing an ISO. Unchanged original records are preserved.
- Adds the limit to the character workshop and Blender guide. Skeletons, textures and UVs are retained by this batching fix.

Validated against the game's palette dispatch and draw gate, the failing replacement, a corrected 5,165-triangle replacement, and 118 original native model files. This resolves an identified draw rejection; complete gameplay compatibility remains to be tested for each character. **Subsequent maintainer report:** the corrected Kratos replacement for Reptile 6732 is fully visible and moving in-game; this confirms that replacement, not all possible imports.

**Existing replacements:** update Studio, return to the original character's source export, then re-import your replacement GLB. Adjust weights if a triangle exceeds the limit. Old incompatible `.mksmcharacter` packages must be rebuilt; installing the update does not repair an existing ISO automatically. The Blender bridge is unchanged; point it at the updated Studio EXE when building a native package.

## 0.25.1 â€” Remove old builds after updating

- Deletes updater-created previous-version EXEs after the new application confirms successful startup.
- Cleans up older accumulated updater backups in the same installation folder, plus verified temporary installer/download EXEs for the completed update.
- Works when updating from an older helper: the new application also performs cleanup.
- Retains recovery on failed startup. Projects, settings, exports and game files are untouched.

## 0.25.0 â€” Audio replacement and native ADX loops

- Adds **Replace audio & set loop pointsâ€¦** to the Audio tab.
- Imports PCM/float WAV and supported native ADX, matching the destination track's sample rate and channel count.
- Writes exact loop start/end points into native ADX, with seconds/sample inputs, waveform markers, intro-once playback and a three-pass loop preview.
- Rebuilds mapped AFS sound collections for longer or shorter tracks while preserving neighboring payloads, names and order.
- Includes audio edits in project save/load, track restore, bank undo, and ISO builds. Reopening a track previews its staged version.
- Saves standalone native ADX with loop metadata. Recovered banks without a mapped live resource ID support export but are clearly excluded from automatic ISO installation.
- Corrects ADX decoding to honor original predictor histories and coefficient truncation.
- Preserves native audio bytes when unchanged; eligible aligned loop edits avoid recompression.

Validated against an independent ADX decoder, original game headers, project/UI round trips and a rebuilt USA ISO. Runtime sound-event timing and music transitions still need gameplay testing. [Audio guide](docs/AUDIO.md).

## 0.24.5 â€” Native idle import and bone-count option

- Fixes native-bank imports that add channels already defined by the verified destination game rig, including Scorpion idle body/face channels.
- Adds **Ignore bone-count difference**, OFF by default, for explicit native-bank experiments. This does not retarget bones or bypass bank/clip structural checks.
- Keeps **Bank added to project** visible when a staged bank is reloaded or Animation Lab reopens.
- Shows an explicit message when a native import is rejected, so a failed import cannot be mistaken for a saved edit.


## 0.24.4 â€” Native animation bank import

- Adds **Import native bank (.bin)â€¦** directly to Animation Lab.
- Imports an edited native bank into the selected game bank and stages it automatically for ISO rebuilding, without GLB conversion.
- Preserves native bytes and higher-precision compatibility markers.
- Validates clip names/order, changed clip layouts and bone-channel counts. Failed imports retain existing project edits.
- Enables **Add animation to project** for standalone loaded banks, with an explicit game-bank destination picker.
- Shows **Bank added to project** after automatic staging, explaining why no second Add is needed.


## 0.24.3 â€” Build ISO fixes

- **Build ISOâ€¦** is available after opening a game, even with no edits or selected resource.
- **Build ISO only** saves without PCSX2; **Build & boot in PCSX2** remains a separate option.
- Zero edits produce a byte-for-byte unchanged ISO copy.
- Extracted-folder sessions can build using their matching original ISO.
- Current staged edits are included without requiring a project save first. Validated character/texture imports and game-backed animation imports are staged automatically.
- Corrects the glowing author name to **Z mods**.
- Preserves source matching, output protection and replacement read-back checks.


## 0.24.2 â€” Zmods author credit

- Adds **Zmods** to the centered author credits with the same looping gold glow and shimmer.
- Updates application author metadata and public credits.
- Existing export, animation and editing behavior is unchanged.

## 0.24.1 â€” Clearer animation export name

- Renames **Animation only (Godot 4)** to **Animation only (GLB)**.
- Updates the tooltip, export progress messages and accompanying guide heading.
- The format, exported skeleton/animation data and Blender add-on are unchanged. Godot remains a documented import example.

## 0.24.0 â€” Public distribution and in-app updates

- Startup/manual update checks and New update available for a newer verified release.
- Signed EXE downloads, installation, automatic relaunch and previous-EXE recovery.
- Gold dragon EXE/window icon in seven sizes.
- Clean Windows package without C# source, build projects or PDBs.
- Separate optional Blender bridge 0.22 download.
- Beginner guides and detailed checklists distinguishing implemented/experimental/unfinished features.

Model, texture, animation, native-rebuild and ISO algorithms are retained from 0.23.0. Updater checks do not imply new gameplay validation of those algorithms.

## Earlier development

0.23 added animation-only GLBs for Godot 4 and explicit rest tracks. 0.22 added eligible higher-precision animation edits and corresponding game compatibility support. Earlier versions developed original rigs, texture-grouped exports, Blender native return, animation inspection, projects and separate ISO rebuilding.

Historical internal ZIPs can include application source and are not suitable public download packages.
