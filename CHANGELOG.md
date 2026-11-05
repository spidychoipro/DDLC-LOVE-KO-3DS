# Changelog

## 0.2.7-beta — 2026-11-06

- Address the hardware-only first Korean warning freeze candidate by preparing font textures and quads before draw callbacks.
- Split the glyph atlas into 256x256 pages; preload ordinary text using 1.25 MiB plus the 0.25 MiB tutorial font.
- Prepare uncommon name glyphs during update and use prepared resources only during rendering.
- Add a regression forbidding GPU font uploads and quad allocation inside draw, plus a first-run startup log.
- Preserve title/save identity; CIA title version 9.
- Confirm on physical 3DS: the first Korean warning 10016 renders and A advances into the game; the same build runs in Azahar. Full-route completion remains unverified.

## 0.2.6-beta — 2026-11-04

- Preserve the original poem tutorial overlay, small pink frame, layout and outlined confirmation label.
- Replace only the English text areas with Korean, removing the full-screen redesign from 0.2.5.
- Retain the poem-return fix and dialogue translations; CIA title version 8.

## 0.2.5-beta — 2026-11-04

- Render the first poem-game tutorial in Korean instead of the English tutorial image.
- Prepare the next chapter before the first draw after poem completion and clear the previous background overlay.
- Convert dialogue expressions starting with a player/name variable, fixing 35 remaining English sentences.
- Audit all 9,943 static dialogue calls for ordinary English, allowing explicit names, paths and intentional glitch generators.
- Add a regression reproducing the old first return frame and checking the actual next-chapter script.
- CIA title version 7; retain the same Title ID and save identity.

## 0.2.4-beta — 2026-11-04

- Document the DDLC-only Azahar audio-stretching override for transient speed-up after native keyboard return; normal initial speed confirmed by the user.

- Stop title music and clear its queued audio before opening the native name keyboard.
- Defer music changes during name entry and scene loading until the first complete scene draw.
- Start only the final requested scene track on the following update; avoid restarting title music during loading.
- Restore title music normally when name entry is cancelled or rejected.
- Verify the stop/queue/play order in the Azahar 2126.1.2 game engine and 600 gameplay frames; also open the release content in Azahar 2126.2.
- Keep native timer APIs, title/save identity, input guard and system keyboard; CIA title version 6.

## 0.2.3-beta — 2026-11-04

- Fix the launch crash introduced by replacing the native timer API in 0.2.2.
- Preserve native timer functions and clamp elapsed time at game call sites.
- Keep the post-keyboard input guard and explicit skip behavior.
- Add a regression assertion that the engine timer function remains unchanged.
- Reproduced the 0.2.2 memory crash in Azahar 2126.1.2 and checked corrected startup plus 600 gameplay frames after the name callback.
- CIA title version 5; existing title and save identity retained.

## 0.2.2-beta — 2026-11-04

- Ignore stale keyboard/touch state after returning from the native name keyboard.
- Require a fresh X press or a touch starting inside the visible Skip button to skip.
- Reset automatic advance, skip state, dialogue pages and scene timers on New Game.
- Cap timer deltas after modal input and initialize the opening scene before drawing.
- Add regression tests reproducing the original skip and checking 600 frames after modal return.
- Clean generated build input between builds to keep ordinary dialogue font atlases small.
- Preserve the CIA Title ID/save identity; increment CIA title version to 4.

Azahar video was inspected; the new build has automated runtime tests but still needs interactive emulator and physical hardware verification.

## 0.2.1-beta — 2026-11-04

- Removed the custom in-game keyboard and custom Hangul composition runtime.
- New Game now opens Nintendo 3DS's native software keyboard directly.
- Preserve Korean, English and mixed UTF-8 names, including the last syllable.
- Added cancellation, validation and duplicate callback tests.
- Keep all 11,172 modern Hangul glyphs for name display.
- Preserve the same CIA Title ID/save identity; increment CIA title version to 3.

System keyboard languages depend on the installed applet and console environment. Physical hardware testing remains outstanding.

## 0.2.0-beta — 2026-11-04

- Added Korean text rendering, poetry/image localization and local CIA packaging.
- The experimental custom name keyboard from this version is superseded by 0.2.1.
