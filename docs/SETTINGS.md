## Discord activity in 0.27.16

**Application > Show MKSM Studio activity in Discord** is enabled by default. It connects locally to Discord desktop and shares only Studio branding. Disable it to clear the activity. Discord must be running and its own Activity Privacy setting must allow sharing. No bot or Discord credentials are required. Connection failures do not block Studio; it retries in the background. Android/Winlator presence is unverified.

## Studio 0.27.14

- Fixed blank Workshop cards after resizing, scrolling and refreshing. Divider dragging previews the new width; cards reflow when released. The model camera stays steady.
- Workshop checks for new listings in the background after opening it: every 30 seconds signed in, every 2 minutes as a guest. Failed requests retain the library and back off. Selection, scroll anchor and unchanged previews survive refresh. Download totals refresh separately every 5 minutes, or on manual Refresh.
- Announcements check at startup, on returning to the app and every 10 seconds. Publishing updates the publisher's view immediately. GitHub caching and network conditions can still delay other clients; older Studio versions retain their old intervals. Messages remain once-per-publication and can be reopened.
- Background SFD/movie is off by default, including a one-time reset of the old default. The dragon and particles remain. Enable video in Settings if desired. Disabled media releases its decoder; muted menu music is not opened.
- Character replacement adds **Original head / hat / attachments…**. Explicitly hide unwanted original rigid parts while retaining skeleton and skinned surfaces. Selection persists in GLB/package exports and can be changed. Review the preview and test in game; this does not claim to fix every head texture or unsupported attachment.

# Settings and the new home screen

[Home](../README.md) · [Updates](UPDATES_AND_HELP.md)

1. Open **MKSM Studio.exe** and choose **Open game ISO** (or **Open folder** for extracted game files).
2. Use the left navigation to browse models, textures, music or your editing project.
3. Open **Settings** to turn presentation features on or off. Scroll down to **Save settings**.

## Your switches

- **Notify me about updates when Studio opens:** only newer signed releases prompt you to install. Background release checks continue even with notifications disabled. No forced installation.
- **Animate background effects:** stop decorative movement while keeping enabled artwork visible.
- **Floating particles** and **Red glow at the bottom:** independently show or hide each effect.
- **Play the opening movie:** enable or disable the video background.
- **Background audio:** choose **Game music**, **Opening movie audio**, or **Off**.
- **Show dragon background:** hide the dragon independently of video, particles and glow.
- **Keep playing when I switch to another app:** enabled by default; turn it off to pause when Studio loses focus.
- **Cursor / hover sounds** and **Click / select sounds:** independent switches for original-game feedback.
- **Background volume** controls the selected background audio. **Home menu sound volume** controls cursor/select sounds.

## Opening movie

The converted opening movie is included but disabled by default. Enable background video explicitly to play it. A missing previous movie path falls back to that bundled default. You can still prepare `Front/Movies/opening.sfd` from your own game folder or ISO. Conversion uses a local FFmpeg executable and runs outside the UI thread. If FFmpeg is missing, use **Choose FFmpeg converter**, then **Choose background movie** and select the SFD. You can also choose an MP4 or WMV directly. [FFmpeg's official download page](https://ffmpeg.org/download.html) links Windows builds. FFmpeg is a separate optional dependency, not included in Studio's EXE or updater.

Converted video is cached locally. The original game file stays unchanged. Choose **Opening movie audio** to hear its soundtrack, including with the video picture disabled. Only one background audio source plays at a time. Playback depends on Windows media support; if video cannot play, the dragon background remains usable.

## Music and interface sounds

The default `7051_000_mus_ambient_rc1.adx` soundtrack is packaged as MP3. Cursor and select effects are packaged as PCM WAV for immediate playback. In an audio preview, choose **Use this track as menu music** to replace the local menu soundtrack. This does not stage a game modification. The menu loops the full decoded track; it does not currently reproduce a selected track's custom internal ADX loop segment.

Shared sound events `SND_SHARED_SF_UI_CURSOR_MOVE` and `SND_SHARED_SF_UI_CURSOR_SELECT` are resolved from the supported retail shared sound header/bank. Unsupported bank layouts leave those sounds unavailable rather than choosing arbitrary samples. UI samples are cached for reuse. Use **Test hover sound** and **Test select sound** in Settings. If Windows accepts playback but you hear nothing, use **Open Windows sound mixer** and check the Studio volume and output device.

The background movie keeps playing while viewing assets. Playback continues when Studio loses focus unless you disable **Keep playing when I switch to another app**. Menu audio is included; the default opening movie is included.

## Appearance

Bundled MK fonts include the supplied Shaolin Monks font by Z Mods. Choose Settings → Appearance → Typography to change the interface font, or Load Another Font for a local TTF/OTF. Save applies the font immediately. Reset to Mortal Kombat 4 restores the default font. Home cards rearrange with available width; the interface scale remains independently adjustable.

Font credit: Mortal Kombat 4 Font v1.0, The Realm of Mortal Kombat (1997), sourced from [MKWarehouse](https://www.mortalkombatwarehouse.com/site/fonts/). Menu audio is from Mortal Kombat: Shaolin Monks.

## Help

Use **Join the MKSM Discord** in Settings: https://discord.gg/aJwRJxd4hh

Settings and presentation caches live under `%LOCALAPPDATA%/MKSM Studio`. These are separate from your ISO, projects and Blender files. The Blender add-on still installs separately.

## Volume controls (0.26.2)

Both bars show 0-100%. Drag the larger handle or click the bar to set a level. Use the minus/plus buttons or arrow keys for 1% steps. Background volume previews immediately. Save settings keeps the changes; closing without saving restores the previous volume. Use the explicit test buttons to hear the home-menu sound volume. Automatic hover/select sounds are limited to Home and do not play in Settings or asset previews. Join Discord is also available immediately below Build game ISO on Home.

Choosing a different background movie starts it immediately after preparation. Save settings keeps that movie; closing without saving restores the prior background.

On a fresh installation, Home hover/select sounds and background audio default to Off. Previously saved preferences remain in effect.

## Low-power visuals (0.27.13)

**Settings → Appearance → Low-Power Visuals** selects 15 FPS effects and disables fog/glow. Save settings to apply it. Video and audio choices remain unchanged; turn off background video separately on very limited graphics hardware. Sidebar cloth is cached, preview materials are shared/frozen, invisible effects stop rendering and Workshop cards recycle as you scroll. No blanket minimum-hardware or 60 FPS guarantee is implied.

Hover sounds, select sounds and background music default to Off for new settings. Existing saved choices are retained. Startup release metadata checks run in the background. Update Now opens installation, Remind Me Later prompts next launch, and Skip This Version suppresses that release only. Manual Check for Updates remains available. The notification toggle suppresses automatic prompts while background checks continue.
