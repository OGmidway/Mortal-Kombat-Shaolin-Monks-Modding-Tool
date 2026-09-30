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
- **Menu music:** enable or mute the separate menu soundtrack.
- **Cursor / hover sounds** and **Click / select sounds:** independent switches for original-game feedback.
- **Background volume** controls menu music. **Interface sound volume** controls cursor/select sounds.

## Opening movie

Studio prepares `Front/Movies/opening.sfd` from your own game folder or ISO. Conversion uses a local FFmpeg executable and runs outside the UI thread. If FFmpeg is missing, use **Choose FFmpeg converter**, then **Choose background movie** and select the SFD. You can also choose an MP4 or WMV directly. [FFmpeg's official download page](https://ffmpeg.org/download.html) links Windows builds. FFmpeg is a separate optional dependency, not included in Studio's EXE or updater.

Converted video is cached locally. The original game file stays unchanged. Video audio is muted because menu music has its own track and volume control. Playback depends on Windows media support; if video cannot play, the dragon background remains usable.

## Music and interface sounds

The pictured `7051_000_mus_ambient_rc1.adx` is the preferred default. If unavailable, Studio looks for another named music track. In an audio preview, choose **Use this track as menu music** to replace the local menu soundtrack. This does not stage a game modification. The menu loops the full decoded track; it does not currently reproduce a selected track's custom internal ADX loop segment.

Shared sound events `SND_SHARED_SF_UI_CURSOR_MOVE` and `SND_SHARED_SF_UI_CURSOR_SELECT` are resolved from the supported retail shared sound header/bank. Unsupported bank layouts leave those sounds unavailable rather than choosing arbitrary samples. UI samples are cached for reuse.

The movie, music and effects pause when Studio loses focus. Asset previews pause the background presentation; return Home to resume it. Sound and movie preparation only occurs after opening your own game. No game media is shipped in public downloads.

## Help

Use **Join the MKSM Discord** in Settings: https://discord.gg/aJwRJxd4hh

Settings and presentation caches live under `%LOCALAPPDATA%/MKSM Studio`. These are separate from your ISO, projects and Blender files. The Blender add-on still installs separately.
