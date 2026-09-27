# Replace music and voices, with native loop points

[Home](../README.md) · [Feature checklist](FEATURES.md) · [Build an ISO](PROJECTS_AND_TESTING.md)

MKSM Studio 0.25.0 adds an **Audio workshop**. Replace a supported ADX track with your own WAV or ADX, select exactly where it loops, and include the replacement in a rebuilt game ISO. The loop is stored in the native ADX file.

## 1. Choose the sound to replace

1. Open your original game ISO or extracted game folder.
2. Select **Music & voices**, then choose an individual **Audio track**. Audio collections contain multiple tracks; select the track inside the collection.
3. Listen to identify the sound. Names such as `mus_`, `vo_` and `fx_` can help, but confirm by listening.
4. In the **Audio** tab, choose **Replace audio & set loop points…**.

The workshop shows the original track's sample rate and channel count. These are the destination format. The researched game uses 12,000, 24,000 and 48,000 Hz ADX tracks, with one or two channels.

## 2. Import your replacement

Choose **Choose WAV / ADX…**. Supported inputs:

- Uncompressed PCM WAV: 8-, 16-, 24- or 32-bit, mono or stereo.
- 32-bit floating-point WAV, mono or stereo.
- Supported unencrypted type-3 ADX, version 3 or 4, with 18-byte blocks.

WAV input rates from 8–192 kHz are accepted. Studio resamples to the original game track's rate and converts the channel count automatically. Stereo-to-mono uses an average; mono-to-stereo duplicates the channel. Use a prepared WAV when you need a particular mix. MP3, AAC and OGG import are not included in this release; convert those files to WAV first.

The replacement may be longer or shorter than the original. Its byte size does not need to match. **Use current game audio** returns to the track that was present when the workshop opened.

## 3. Set the loop section

Enable **Loop a section of this track**, then enter **Start** and **End**:

- **Seconds** is convenient for music editing. Decimal values are supported.
- **Samples** gives exact positions at the destination game sample rate.
- **Start at playhead** and **End at playhead** copy the current position from normal playback.
- **Loop entire track** sets Start to zero and End to the track's full length.

For example, set Start to **12.5 seconds** and End to **75 seconds**. Playback runs from the beginning to 75 seconds, then returns to 12.5 seconds on each repeat. The intro is heard once. Material after End is not part of the repeated section.

End is **exclusive**: the sample at End is where playback jumps back to Start. End must be after Start and within the track. If you replace a looped track with a shorter WAV, adjust any existing endpoints that are now outside it. WAV-embedded loop markers are not imported automatically; enter them in the workshop. Native ADX input brings its supported loop settings with it.

The waveform highlights the loop section; green marks Start and red marks End. Studio follows the original game's ADX block/sector alignment. An arbitrary sample-level start can require up to 31 silent samples of leading padding—less than 3 milliseconds at the observed game rates. Displayed endpoints remain relative to your imported audio; native ADX sample indices include that padding.

## 4. Preview what will be encoded

- **Listen once** plays the encoded track once. Drag the playhead slider to move through it.
- **Preview loop ×3** plays the intro, then three passes through the selected section. This previews the native ADX loop using the encoded samples. Playback stops after the third pass.
- **Pause** and **Stop** control playback. Use Listen once when placing markers from the playhead.

For a smooth seam, choose musically matching start/end positions and listen across the boundary. Loop points do not automatically crossfade or repair a discontinuity. Prepare any fades or seam edits in your audio editor first.

ADX is lossy. WAV imports and some loop changes require encoding. Unchanged compatible ADX is kept intact; compatible aligned loop edits can change metadata without recompressing the audio. Keep your original WAV for repeated revisions.

## 5. Put the audio into the game

1. Choose **Apply to project**. This stages the replacement immediately.
2. Close the workshop. The track preview now reads the staged version, including its loop settings.
3. Choose **Save project** to keep the edit for future sessions.
4. Choose **Build ISO…**, then **Build ISO only** or the PCSX2 launch option.
5. Test the appropriate scene, character sound or music transition in the game.

Most tracks live inside AFS audio collections. Studio rebuilds the containing collection, retains the other track payloads, names and order, and updates its offsets for longer/shorter sounds. Multiple replacements in one collection merge into one project resource. Restoring an individual track keeps edits to the other tracks. Undo follows the containing collection's edit history.

**Save native ADX…** writes a standalone game-format file with the loop metadata. Saving an ADX alone does not stage it in the open project; use **Apply to project** for that. **Save audio…** in the main preview exports decoded WAV instead.

## 6. Supported scope and remaining research

- [x] Native ADX encoding with destination sample rate and channel count.
- [x] Exact loop endpoints, intro-once playback and repeated-section preview.
- [x] Longer/shorter track replacement inside mapped AFS collections.
- [x] Project save/load, track restore, bank undo and ISO rebuilding.
- [x] Independent decoder verification and rebuilt-ISO byte read-back.
- [ ] Automatic installation of recovered AFS collections with no mapped live archive directory entry.
- [ ] Complete editing of every PS2 sound bank, codec or audio event.
- [ ] Automatic extension of dialogue/cutscene events to match a longer sound.
- [ ] Proof of every replacement's runtime behavior in the game.

The researched USA archive contains 7,643 discovered ADX tracks. Of these, 6,373 belong to collections with mapped live resource IDs. The other 1,270 were recovered from ten AFS collections in GAMEDATA.WAJ with no mapped live directory entry. Those tracks support workshop preparation and **Save native ADX**, but **Apply to project** is unavailable until their installation path is understood.

The app limits an input file or rebuilt native bank to 256 MB and total staged project resources to 1 GB. The ISO writer retains its disc-size checks. These are not promises about runtime memory: a game event can stop a longer sound, and the game can manage music transitions independently of a track's loop. Test your intended scene. No emulator texture-replacement feature is involved.
