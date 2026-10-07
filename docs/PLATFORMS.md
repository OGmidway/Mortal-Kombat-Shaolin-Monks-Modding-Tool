# Choose your download

| Device | Download | Status |
|---|---|---|
| Windows x64 desktop/laptop | `MKSM-Studio-0.27.15-win-x64.zip` or EXE | Primary Windows build |
| Windows x64 handheld | Same Windows build; use Settings > Low-Power Visuals | Desktop interface; keyboard/mouse or equivalent input needed |
| Android with Winlator | `MKSM-Studio-0.27.15-portable-experimental-win-x64.zip` | Experimental Windows compatibility test, **not verified on Android** |
| Windows ARM | x64 build through Windows emulation | Untested |
| Native Android/iOS/Linux | None | No native build |

Extract the entire portable ZIP into a writable folder. Start with `Start Low Power.cmd`. If graphics fail, try `Start Software Rendering.cmd`; software rendering may be slower. `Start Studio.cmd` uses your saved preferences. Portable settings live beside the app in UserData. Always use a launcher; after an automatic update relaunch, close and reopen through it to retain the portable profile.

Low Power disables background video, sound, fog and glow and selects 15 FPS particles. Normal Settings can disable particles entirely. The extracted package includes the Windows .NET runtime; it does not remove WPF/Windows requirements. Winlator version, Android device, GPU driver and available memory can affect whether it starts. No performance or compatibility guarantee is established.

Use the private source ZIP only if invited; it includes its own Windows application and updater. Do not mix private and public executables.
