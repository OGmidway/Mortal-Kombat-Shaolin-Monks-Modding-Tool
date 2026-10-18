# Xbox recomp patches

[Home](../README.md) · [Download Studio 0.28.2](https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/releases/tag/v0.28.2)

1. Open **Home → Xbox Recomp Patches**.
2. Browse to your supported Windows Xbox recomp EXE and choose **Review EXE**.
3. Select **Disable HDR** and/or **Reduce glossy reflections**. Both together reproduce the preset tested on Scorpion.
4. Choose **Save patched EXE** and a new filename.
5. Close the running recomp, launch the saved copy, and select your usual ISO.

No ISO rebuild is needed for these EXE patches. Studio preserves the original, refuses unknown builds and existing output files, and writes a hash-verified patch report. Uncheck options to restore their original behavior in another saved copy.

The current patch definitions recognize two exact recomp builds and their supported patched variants. They do not support every recomp version. Gloss/reflection changes affect shared materials and may change scenery. Individual options and all scenes have not been comprehensively gameplay tested.

## ISO replacements are a separate workflow

Use Studio's model, texture and supported audio replacement workflows, then **Build Game ISO** to create a separate modded Xbox ISO. Asset compatibility still depends on the native format and game revision. The experimental **Patch Xbox ISO** recipe changes Xbox executable instructions on disc; it is not a substitute for patching a recomp's precompiled Windows code. PS2 PNACH codes are not automatically portable to Xbox.

No game files are included with Studio.
