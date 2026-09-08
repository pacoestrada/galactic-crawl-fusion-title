# Galactic Crawl

An editable **DaVinci Resolve 21 Fusion title** with perspective scrolling text, horizon fading and a procedural starfield.

**v0.1.0-beta.1 is an initial testing release.** Syntax, references and package integrity have been checked. Installation, Inspector behavior and actual rendering in Resolve have **not** been verified yet.

![Mathematical reference preview, not rendered in Resolve](docs/galactic-crawl-preview.png)

The image and [30-second animation](https://github.com/pacoestrada/galactic-crawl-fusion-title/raw/refs/heads/main/docs/galactic-crawl-preview.mp4) are reference simulations, not Fusion renders. Their caption is not part of the installed title.

## Download and install

1. [Download Galactic-Crawl.drfx](https://github.com/pacoestrada/galactic-crawl-fusion-title/releases/download/v0.1.0-beta.1/Galactic-Crawl.drfx) from the [beta release](https://github.com/pacoestrada/galactic-crawl-fusion-title/releases/tag/v0.1.0-beta.1).
2. Open a Resolve project and switch to the **Fusion** page.
3. Drag the downloaded `.drfx` onto Fusion and confirm installation.
4. Find **Galactic Crawl** under **Edit → Effects Library → Titles**. Restart Resolve if needed.
5. Use a 1920 × 1080 landscape timeline and a **60–90 second** title clip for the first test.

Do not unzip the installer or use GitHub's source archive as the installer. This is a pre-release; links intentionally target the version tag instead of `releases/latest`.

For manual Linux installation, download the `.setting` release asset, rename it to `Galactic Crawl.setting`, copy it to the following folder and restart Resolve:

```text
~/.local/share/DaVinciResolve/Fusion/Templates/Edit/Titles/
```

Use only one installation method to avoid duplicates.

## Controls

The Inspector labels are in Spanish. See the [complete control tables](README.md#qué-puedes-editar).

- Story text, font/style, size and RGBA text color.
- Speed, horizon height, perspective, column width, horizon fade, initial position and travel distance.
- Star density, brightness, size and distribution seed.
- RGB space color and overall background opacity.

Set **Opacidad del fondo** to **0** and place your own image or video on a lower track to replace the background. There is no file picker in the Inspector. Background opacity leaves the text unchanged.

The default font is **DejaVu Sans Bold**, not bundled. Choose an installed font if unavailable. The text canvas is fixed at 1920 × 4096; use manual line breaks and start with about 20–25 short lines. Longer stories may require smaller text, a different start position and a different travel distance.

Lengthening the clip slows the animation at unchanged settings. The final 8% fades the text; the starfield remains. Stars are static and procedural, with no external image dependency.

## Validation and feedback

Portable checks run in GitHub Actions, including a Lua parse, graph checks, package integrity, source parity and SHA-256 verification. The installed Fusion Lua reader also accepted the settings table. None of these checks proves correct rendering.

See [VALIDATION.md](VALIDATION.md), the [download-to-Resolve test guide](docs/TESTING.md), and [architecture notes](docs/ARCHITECTURE.md). Report problems using the [bug report form](https://github.com/pacoestrada/galactic-crawl-fusion-title/issues/new?template=bug_report.yml).

Target platform: Resolve 21 on Linux. Free/Studio runtime behavior, other operating systems and other frame formats remain unverified.

## License

Design, direction and publication: **Paco Estrada**. Implementation and documentation developed with assistance from OpenAI Codex. Released under the [MIT License](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md).

[Documentación completa en español](README.md)
