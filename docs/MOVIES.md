# Experimental native SFD movie replacement

[Home](../README.md) · [Discovery maps](RESEARCH_MAPS.md)

Studio 0.27.13 imports already-created SFDs. Playback in the game is not verified. This first workflow keeps original resolution and strictly limits size, timing and stream layout.

1. Open your supported original USA PS2 ISO and choose **Movies & Cutscenes** on the left.
2. Select a movie. **Export Original SFD** preserves the original video and all embedded audio tracks.
3. Create a new SFD outside Studio. Keep the original native dimensions, frame rate, video format and audio stream layout. Make it smaller in bytes and no longer than the original. Studio does not include an SFD encoder.
4. Choose **Check Replacement SFD**. Select FFmpeg if prompted; ffprobe.exe must be beside it. The checker validates the source revision, stream headers, frame counts/timestamps, duration and full software decoding.
5. Choose **Stage Reviewed Replacement**. Save the editing project to retain the movie edit. **Restore Original Movie** removes it from the project.
6. **Build Game ISO** writes a new image, reruns movie validation, retains original movie LBAs, updates both ISO file lengths, clears remaining original allocation bytes and reads back the result. Character-window builds also include staged movie edits.
7. Fresh-boot your rebuilt image for testing. Older save states can retain original cached movie lengths.

Unknown or already-patched source revisions are rejected for import. Original export remains available for inspection. No unrestricted resolution, file size or duration support is claimed. A software-accepted movie can still fail the native CRI player; SFM2.29 versus the original SFM2.25 mux remains a compatibility question.

The native ISO build report records movie hashes, byte counts and original LBAs and leaves GamePlaybackVerified false. Passing offline checks does not establish in-game safety.
