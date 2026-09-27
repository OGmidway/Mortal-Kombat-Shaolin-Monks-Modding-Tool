# Transfer or write hex data

[Home](../README.md) · [Animation Lab](ANIMATIONS.md) · [Projects and ISO building](PROJECTS_AND_TESTING.md)

Available in **0.25.4**. Hex transfer overwrites existing bytes. It never inserts/deletes bytes or changes the selected resource's length. You can copy data between resources, including animation banks, or write your own byte values.

## 1. Choose the destination

- Main window: select a resource, enable **Advanced tools**, open **Hex**, then **Transfer hex data…**.
- Animation Lab: load a bank, open **Advanced tools → Hex**, choose **Selected clip** or **Full animation bank**, then **Transfer hex data…**.

The dialog states the destination scope and its starting offset. It reads the current edited/decoded resource, not compressed archive bytes. The main hex viewer's text limit does not limit the transfer dialog's addressable range.

## 2. Choose where the bytes come from

- **Source file…:** reads the exact bytes on disk. Extract decoded native data first if the file is an EWDF/compressed wrapper.
- **Game resource / Load ID:** reads that resource's current project version, including staged edits. Use the exact resource key displayed in the collection, such as `0121`.
- **Use destination as source:** copies from a snapshot of the destination. Overlapping copies are supported.
- **Enter / paste hex…:** enter complete byte pairs such as `DE AD BE EF`. Spaces, tabs and newlines are allowed. Do not paste row addresses or the ASCII column.

If the source is a recognized animation bank, its scope list also offers individual clips. Selecting a clip does not automatically identify equivalent bone tracks in another bank.

## 3. Select the exact range

| Mode | Source / destination fields | Amount |
|---|---|---|
| Byte offsets (hex) | Hexadecimal offsets relative to each selected scope. `10` means hex `0x10`, or 16 bytes. | Byte count, decimal by default; `0x` accepts hexadecimal. |
| Lines (16 bytes, 1-based) | Line 1 starts at the selected scope's first byte. Line 2 starts 16 bytes later. | Number of complete 16-byte lines. |

Example: copy source bytes `0x20` through `0x2F` over destination `0x80` through `0x8F`: choose byte mode, source `0x20`, destination `0x80`, byte count `16`.

For an animation clip, destination `0x0` means the clip's beginning, not the bank's beginning. The main inspector displays bank-relative addresses; subtract the clip start shown in the dialog when entering a clip-relative position. The review displays absolute resource/bank addresses for verification. ISO addresses are not used here.

Use byte mode for a partial final line. Negative, empty, overflowing and out-of-bounds ranges are rejected. Sources are limited to 256 MB; pasted hex is limited to 1 MB of decoded bytes.

## 4. Review and apply

Click **Review replacement**. Compare the before/after bytes and check the addresses, amount, changed-byte count and unchanged total size. Larger results are paged with **Previous bytes / Next bytes**. Changing a field invalidates the review.

- **Apply to project:** stages a valid resource for the next ISO build. Animation Lab refreshes the preview to these bytes. Save your project to retain the change across sessions; Undo/Restore in the main window can revert staged resources.
- **Apply to preview:** used for a standalone animation bank. Save the native bank or choose **Add animation to project** and assign its game destination.
- **Save patched copy…:** writes a separate native file plus `.hex-transfer.json` containing addresses, hashes and validation status. Saving alone does not stage anything. Existing files are never overwritten.

Malformed native results cannot be applied to the project. A raw patched copy can still be saved for research and is marked with its validation result. Recovered/nested resources without a mapped game destination are export-only. Supported mapped ADX tracks are repacked through their containing bank.

## What this does not do

Copying bytes does not repair pointers, checksums, animation slot references, bone orders or resource-specific lengths. Native animation slot names/order and changed-clip decoding are checked. Animation Lab retains its existing explicit bone-count option, but that option does not retarget motion. Unknown fields may pass available format checks and still behave incorrectly in-game.

For inserting frames, changing a clip duration through authored motion or replacing a whole bank with a different byte size, use the dedicated animation import workflow. Keep a project backup and test the rebuilt ISO fresh.
