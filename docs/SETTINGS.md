# Settings and the new home screen

[Home](../README.md) · [Updates](UPDATES_AND_HELP.md)

1. Open **MKSM Studio.exe** and choose **Open game ISO** (or **Open folder** for extracted game files).
2. Use the left navigation to browse models, textures, music or your editing project.
3. Open **Settings** to turn presentation features on or off. Scroll down to **Save settings**.

## Your switches

- **Check for updates when Studio opens:** only newer signed releases prompt you to install. No forced installation.
- **Animate background effects:** stop decorative movement while keeping enabled artwork visible.
- **Floating particles** and **Red glow at the bottom:** independently show or hide each effect.
- **Play the opening movie:** enable or disable the video background.
- **Background audio:** choose **Game music**, **Opening movie audio**, or **Off**.
- **Show dragon background:** hide the dragon independently of video, particles and glow.
- **Keep playing when I switch to another app:** enabled by default; turn it off to pause when Studio loses focus.
- **Cursor / hover sounds** and **Click / select sounds:** independent switches for original-game feedback.
- **Background volume** controls the selected background audio. **Home menu sound volume** controls cursor/select sounds.

## Opening movie

Studio prepares `Front/Movies/opening.sfd` from your own game folder or ISO. Conversion uses a local FFmpeg executable and runs outside the UI thread. If FFmpeg is missing, use **Choose FFmpeg converter**, then **Choose background movie** and select the SFD. You can also choose an MP4 or WMV directly. [FFmpeg's official download page](https://ffmpeg.org/download.html) links Windows builds. FFmpeg is a separate optional dependency, not included in Studio's EXE or updater.

Converted video is cached locally. The original game file stays unchanged. Choose **Opening movie audio** to hear its soundtrack, including with the video picture disabled. Only one background audio source plays at a time. Playback depends on Windows media support; if video cannot play, the dragon background remains usable.

## Music and interface sounds

The default `7051_000_mus_ambient_rc1.adx` soundtrack is packaged as MP3. Cursor and select effects are packaged as PCM WAV for immediate playback. In an audio preview, choose **Use this track as menu music** to replace the local menu soundtrack. This does not stage a game modification. The menu loops the full decoded track; it does not currently reproduce a selected track's custom internal ADX loop segment.

Shared sound events `SND_SHARED_SF_UI_CURSOR_MOVE` and `SND_SHARED_SF_UI_CURSOR_SELECT` are resolved from the supported retail shared sound header/bank. Unsupported bank layouts leave those sounds unavailable rather than choosing arbitrary samples. UI samples are cached for reuse. Use **Test hover sound** and **Test select sound** in Settings. If Windows accepts playback but you hear nothing, use **Open Windows sound mixer** and check the Studio volume and output device.

The background movie keeps playing while viewing assets. Playback continues when Studio loses focus unless you disable **Keep playing when I switch to another app**. Menu audio is included; the opening movie is prepared from your own game and is not included.

## Appearance

MK4 title lettering and scalable iron frames are included. The home cards rearrange with available width, and the main interface grows on large windows. Body text keeps its readable standard font. **Choose MK4 title font (.ttf)** lets you substitute a local font; save and reopen Studio to apply it. **Use default title font** restores the bundled MK4 font.

Font credit: Mortal Kombat 4 Font v1.0, The Realm of Mortal Kombat (1997), sourced from [MKWarehouse](https://www.mortalkombatwarehouse.com/site/fonts/). Menu audio is from Mortal Kombat: Shaolin Monks.

## Help

Use **Join the MKSM Discord** in Settings: https://discord.gg/aJwRJxd4hh

Settings and presentation caches live under `%LOCALAPPDATA%/MKSM Studio`. These are separate from your ISO, projects and Blender files. The Blender add-on still installs separately.

## Volume controls (0.26.2)

Both bars show 0-100%. Drag the larger handle or click the bar to set a level. Use the minus/plus buttons or arrow keys for 1% steps. Background volume previews immediately. Save settings keeps the changes; closing without saving restores the previous volume. Use the explicit test buttons to hear the home-menu sound volume. Automatic hover/select sounds are limited to Home and do not play in Settings or asset previews. Join Discord is also available immediately below Build game ISO on Home.
