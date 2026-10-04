# Engine research: verified findings and remaining work

October 2026 update: [separate discovery maps](RESEARCH_MAPS.md) and [experimental native SFD import](MOVIES.md) are available in Studio 0.27.13. Game playback validation remains open.

[Home](../README.md) · [Roadmap](ROADMAP.md)

Status at Studio 0.26.0: research results below are not a deployed game patch. Studio's UI/settings update does not raise game memory, polygon or texture limits.

## Why a replacement can preview correctly and fail in game

Two distinct problems have been reproduced in diagnostic execution and captured memory analysis:

1. Native character conversion can reuse a staging region before it has finished reading model metadata from that region. A larger replacement can overwrite input that later conversion steps still need.
2. A later animation allocation can exceed the remaining player-pool capacity. Failed allocation handling can then allow a copy into unintended memory. Fixing conversion alone does not establish adequate memory for animations and gameplay.

These are not evidence of a single removable polygon-count flag. Neighboring allocations must retain their ownership and bounds. Enlarging an existing pool descriptor without moving its neighbors is not a safe solution.

## What has been checked

- Preserving CJ's needed metadata allows the diagnostic native converter to return in the default player pool.
- A native preserved-directory iterator produces the same 2,082,084 output bytes as the host-iterator diagnostic reference. This is not an exact match to every byte of the separate disjoint-input control; residual collision-area bytes were investigated separately.
- Native span copying/relocation was checked on 179 skeleton groups across 91 original model assets, including interleaved named and opaque bone-property records.
- The combined metadata-preservation path passed its skeleton-poisoning/property-counter check on 87 of 91 original assets. Four remain unsupported because of other packet/layout or diagnostic scratch-capacity cases.
- Native temporary allocation, real skeleton copying, property reading and release were exercised together, including rejected-copy cleanup.
- Bone linked-list pointers cannot universally be treated as contiguous record boundaries. Rebuilt CJ data includes a final bone link that skips far ahead to mesh data.
- Independent decoding of the shared UI cursor and select samples matches Studio's new local PCM output exactly.

The converter fixtures still include host-built layouts, synthetic preservation storage and selected service/transform substitutes. They do not execute the whole game, graphics processor or physical SPU. Passing them does not certify gameplay, every character, arbitrary textures or arbitrary file sizes.

## Still required before a memory-fix release

- Complete native metadata planning, storage ownership and activation lifetime throughout the loader.
- Handle remaining rigid/collision layouts and validate all required references.
- Account for animation and other allocations that coexist with character data.
- Propagate allocation failures safely without corrupting unrelated memory.
- Integrate the verified changes into the tool's build workflow, then perform fresh gameplay tests.

Longer-term work includes sound-bank editing/re-encoding, stage geometry and collision, scripts, camera behavior and additional engine formats. Camera findings are being retained; verified ultrawide support and a full level editor are not part of 0.26.0. Full engine reconstruction or porting remains a long-term objective, not a completed feature.
