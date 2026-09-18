#!/usr/bin/env python3
"""Generate the labelled reference PNG and MP4 without using Resolve."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 960, 540
FPS, DURATION = 12, 30
VIEW_WIDTH, VIEW_HEIGHT = 800, 1800
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
YELLOW = (255, 205, 0, 255)
QUAD = ((400, 138), (560, 138), (970, 570), (-10, 570))


def homography(dst: tuple[tuple[float, float], ...], src: tuple[tuple[float, float], ...]) -> tuple[float, ...]:
    """Return Pillow's output-to-input perspective coefficients."""
    rows: list[list[float]] = []
    values: list[float] = []
    for (x, y), (u, v) in zip(dst, src):
        rows.extend(([x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]))
        values.extend((u, v))
    return tuple(np.linalg.solve(np.asarray(rows), np.asarray(values)))


def make_starfield() -> Image.Image:
    rng = np.random.default_rng(1977)
    frame = Image.new("RGB", (WIDTH, HEIGHT), (0, 1, 7))
    draw = ImageDraw.Draw(frame)
    for _ in range(310):
        x = int(rng.integers(0, WIDTH))
        y = int(rng.integers(0, HEIGHT))
        brightness = int(rng.integers(85, 230))
        radius = 1 if rng.random() < 0.93 else 2
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(brightness,) * 3)
    return frame


def make_text_plane() -> tuple[Image.Image, int]:
    lines = (ROOT / "docs/example-text-es.txt").read_text(encoding="utf-8").splitlines()
    font = ImageFont.truetype(str(FONT), 43)
    line_height = 66
    top_padding = 1_400
    plane = Image.new("RGBA", (VIEW_WIDTH, top_padding + len(lines) * line_height + 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(plane)
    for index, line in enumerate(lines):
        if not line:
            continue
        box = draw.textbbox((0, 0), line, font=font)
        x = (VIEW_WIDTH - (box[2] - box[0])) // 2
        draw.text((x, top_padding + index * line_height), line, font=font, fill=YELLOW, stroke_width=1)
    return plane, top_padding + len(lines) * line_height


def add_caption(frame: Image.Image) -> None:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    ImageDraw.Draw(frame).text(
        (15, HEIGHT - 23),
        "GALACTIC CRAWL · Vista orientativa · No renderizada en Resolve",
        font=font,
        fill=(125, 136, 155),
    )


def main() -> None:
    if not FONT.exists():
        raise SystemExit(f"Missing preview font: {FONT}")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required to generate the MP4 preview")

    background = make_starfield()
    plane, text_end = make_text_plane()
    transform = homography(
        QUAD,
        ((0, 0), (VIEW_WIDTH, 0), (VIEW_WIDTH, VIEW_HEIGHT), (0, VIEW_HEIGHT)),
    )
    clip = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(clip).polygon(QUAD, fill=255)
    fade = Image.new("L", (WIDTH, HEIGHT), 255)
    fade_pixels = fade.load()
    for y in range(HEIGHT):
        opacity = max(0, min(255, round((y - 138) / 80 * 255)))
        for x in range(WIDTH):
            fade_pixels[x, y] = opacity

    max_scroll = text_end - 70

    def frame_at(progress: float) -> Image.Image:
        scroll = round(max_scroll * progress)
        window = Image.new("RGBA", (VIEW_WIDTH, VIEW_HEIGHT), (0, 0, 0, 0))
        crop = plane.crop((0, scroll, VIEW_WIDTH, min(scroll + VIEW_HEIGHT, plane.height)))
        window.alpha_composite(crop, (0, 0))
        crawl = window.transform(
            (WIDTH, HEIGHT),
            Image.Transform.PERSPECTIVE,
            transform,
            resample=Image.Resampling.BICUBIC,
        )
        alpha = Image.composite(crawl.getchannel("A"), Image.new("L", (WIDTH, HEIGHT), 0), clip)
        alpha = Image.composite(alpha, Image.new("L", (WIDTH, HEIGHT), 0), fade)
        if progress > 0.92:
            alpha = alpha.point(lambda value: round(value * (1 - progress) / 0.08))
        crawl.putalpha(alpha)
        result = background.copy().convert("RGBA")
        result.alpha_composite(crawl)
        result = result.convert("RGB")
        add_caption(result)
        return result

    preview = frame_at(0.12)
    preview.save(ROOT / "docs/galactic-crawl-preview.png", optimize=True)

    process = subprocess.Popen(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{WIDTH}x{HEIGHT}",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(ROOT / "docs/galactic-crawl-preview.mp4"),
        ],
        stdin=subprocess.PIPE,
    )
    assert process.stdin is not None
    for number in range(FPS * DURATION):
        process.stdin.write(frame_at(number / (FPS * DURATION - 1)).tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("ffmpeg failed")


if __name__ == "__main__":
    main()
