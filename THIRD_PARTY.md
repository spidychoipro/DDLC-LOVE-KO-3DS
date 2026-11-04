# Sources and third-party material

| Component | Source | Treatment |
|---|---|---|
| Doki Doki Literature Club! | https://ddlc.moe/ | Game assets are supplied locally; not included in this repository. |
| DDLC-LOVE 3DS release v1.1.9 | https://github.com/LukeZGD/DDLC-LOVE/releases/tag/v1.1.9 | User-supplied ZIP/CIA template. Lua changes are generated locally. Upstream GPL-3.0 code license is retained. |
| LovePotion 1.0.9 | https://github.com/lovebrew/lovepotion/tree/1.0.9 | Source location for the upstream prebuilt runtime; the C/C++ runtime is not rebuilt by this tool. |
| Korean patch 1.2 | https://sites.google.com/view/dokidokikor | User-supplied normal patch ZIP; translated dialogue, fonts and images are extracted and converted locally. Follow the original site's sharing instructions. |
| English comparison scripts | https://github.com/saber-nyan/ddlc-android/tree/f2a1c25a534cf5ad55f071ddb355b7807106c56a/game | Optional explicit download for text alignment; fixed commit and SHA-256 manifest; not executed or shipped here. |
| makerom 0.19.0 | https://github.com/3DSGuy/Project_CTR/releases/tag/makerom-v0.19.0 | User-supplied executable; not bundled. |
| mkromfs3ds | https://github.com/devkitPro/3dstools | User-supplied executable; not bundled. |
| Pillow / fonttools | https://pillow.readthedocs.io/ / https://fonttools.readthedocs.io/ | Build dependencies installed through requirements.txt. |

No Nintendo keys, DSP firmware, ROM images, emulator profiles, user saves, account credentials, or personal machine paths belong in this repository. The `.gitignore` excludes generated and private inputs.

The CIA packager uses the original decrypted homebrew executable and its permissions as a template. It updates metadata, title identifiers and RomFS hashes; it does not turn unsigned homebrew into an officially signed Nintendo title.

The build tools are independent implementations of data extraction, Unicode Hangul composition and local container assembly. Copyright in the original game and Korean translation remains with the respective creators.
