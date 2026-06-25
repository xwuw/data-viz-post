#!/usr/bin/env python3
"""Generate reusable 900x1200 grain/noise backgrounds for data-viz-post.

The presets mirror seeds/background-presets.md. Outputs are deterministic for a
given preset and seed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


W, H = 900, 1200


def hex_rgb(value: str) -> np.ndarray:
    value = value.lstrip("#")
    return np.array([int(value[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def smooth_noise(rng: np.random.Generator, width: int, height: int, scale: float, blur: float) -> np.ndarray:
    small = rng.normal(0, 1, (max(4, int(height * scale)), max(4, int(width * scale))))
    small = (small - small.min()) / (small.max() - small.min())
    im = Image.fromarray(np.uint8(small * 255), "L").resize((width, height), Image.Resampling.BICUBIC)
    im = im.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(im).astype(np.float32) / 255


def add_grain(
    img: np.ndarray,
    rng: np.random.Generator,
    strength: float,
    chroma: float,
    speckles: float,
    dark: bool,
) -> np.ndarray:
    mono = rng.normal(0, strength, (H, W, 1))
    color = rng.normal(0, strength * chroma, (H, W, 3))
    out = img + mono + color
    if speckles:
        mask = rng.random((H, W)) < speckles
        if dark:
            out[mask] *= rng.uniform(0.25, 0.55, size=(mask.sum(), 1))
        else:
            out[mask] = out[mask] * 0.55 + rng.uniform(210, 255, size=(mask.sum(), 1)) * 0.45
    return np.clip(out, 0, 255)


def finish(img: np.ndarray, path: Path, contrast: float, saturation: float, blur: float = 0.0) -> Path:
    out = Image.fromarray(np.uint8(np.clip(img, 0, 255)), "RGB")
    if blur:
        out = out.filter(ImageFilter.GaussianBlur(blur))
    out = ImageEnhance.Contrast(out).enhance(contrast)
    out = ImageEnhance.Color(out).enhance(saturation)
    path.parent.mkdir(parents=True, exist_ok=True)
    out.save(path, quality=96)
    return path


def random_color_field(
    *,
    seed: int,
    base: str,
    palette: list[str],
    out_path: Path,
    contrast: float,
    saturation: float,
    grain: float,
    blur: float = 0.0,
    dark: bool = True,
) -> Path:
    rng = np.random.default_rng(seed)
    img = np.zeros((H, W, 3), dtype=np.float32) + hex_rgb(base)
    fields = [
        smooth_noise(rng, W, H, scale=0.030, blur=118),
        smooth_noise(rng, W, H, scale=0.055, blur=78),
        smooth_noise(rng, W, H, scale=0.095, blur=46),
    ]
    field_mix = 0.48 * fields[0] + 0.34 * fields[1] + 0.18 * fields[2]
    field_mix = (field_mix - field_mix.min()) / (field_mix.max() - field_mix.min())
    img *= 0.72 + 0.46 * field_mix[..., None]

    colors = [hex_rgb(c) for c in palette]
    yy, xx = np.mgrid[0:H, 0:W]
    xn = xx / W
    yn = yy / H
    for _ in range(18):
        cx = rng.uniform(-0.22, 1.22)
        cy = rng.uniform(-0.18, 1.18)
        rx = rng.uniform(0.18, 0.58)
        ry = rng.uniform(0.14, 0.44)
        softness = rng.uniform(0.85, 2.15)
        alpha = rng.uniform(0.18, 0.58)
        color = colors[rng.integers(0, len(colors))]
        d = ((xn - cx) / rx) ** 2 + ((yn - cy) / ry) ** 2
        mask = np.exp(-d * softness)
        mask *= 0.72 + 0.42 * fields[rng.integers(0, len(fields))]
        img = img * (1 - alpha * mask[..., None]) + color * (alpha * mask[..., None])

    angle = rng.uniform(-0.8, 0.8)
    direction = np.clip((xn * np.cos(angle) + yn * np.sin(angle) + 0.20), 0, 1)
    img = img * (0.84 + 0.28 * direction[..., None])
    img = add_grain(img, rng, strength=grain, chroma=0.45, speckles=0.0007, dark=dark)
    return finish(img, out_path, contrast=contrast, saturation=saturation, blur=blur)


def active_warm_white_red_paper(seed: int, out_path: Path) -> Path:
    rng = np.random.default_rng(seed)
    img = np.zeros((H, W, 3), dtype=np.float32) + hex_rgb("#fbf6ef")
    yy, xx = np.mgrid[0:H, 0:W]
    xn = xx / W
    yn = yy / H

    wash = smooth_noise(rng, W, H, scale=0.04, blur=96)[..., None]
    img = img * (0.99 + 0.035 * wash)

    for x, y, color, rx, ry, alpha, softness in [
        (0.78, 0.12, "#f4c8c0", 0.50, 0.28, 0.32, 1.35),
        (0.12, 0.30, "#f2d0c8", 0.48, 0.36, 0.24, 1.45),
        (0.52, 0.86, "#eaa49c", 0.40, 0.24, 0.34, 1.55),
        (0.86, 0.62, "#fffaf4", 0.44, 0.30, 0.42, 1.60),
        (0.10, 0.84, "#fffaf4", 0.46, 0.34, 0.36, 1.55),
    ]:
        d = ((xn - x) / rx) ** 2 + ((yn - y) / ry) ** 2
        mask = np.exp(-d * softness)[..., None]
        img = img * (1 - alpha * mask) + hex_rgb(color) * (alpha * mask)

    img = add_grain(img, rng, strength=4.5, chroma=0.16, speckles=0.00035, dark=False)
    return finish(img, out_path, contrast=1.035, saturation=0.92)


def red_top_paper_wash(seed: int, out_path: Path) -> Path:
    rng = np.random.default_rng(seed)
    img = np.zeros((H, W, 3), dtype=np.float32) + hex_rgb("#f4efe8")
    yy, xx = np.mgrid[0:H, 0:W]
    yn = yy / H

    top = np.clip(1 - yn / 0.46, 0, 1)[..., None]
    top = top ** 1.65
    img = img * (1 - 0.72 * top) + hex_rgb("#d92e2c") * (0.72 * top)

    rosy = np.clip(1 - np.abs(yn - 0.36) / 0.34, 0, 1)[..., None]
    img = img * (1 - 0.22 * rosy) + hex_rgb("#efb6b0") * (0.22 * rosy)

    paper = smooth_noise(rng, W, H, scale=0.055, blur=74)[..., None]
    img = img * (0.965 + 0.06 * paper)
    img = add_grain(img, rng, strength=5.0, chroma=0.12, speckles=0.0003, dark=False)
    return finish(img, out_path, contrast=1.02, saturation=0.88)


PRESETS = {
    "active-warm-white-red-paper": {
        "seed": 205,
        "filename": "background-white-red.png",
        "render": active_warm_white_red_paper,
    },
    "dark-violet-random-soft": {
        "seed": 201,
        "filename": "dark-violet-random-soft.png",
        "kwargs": {
            "base": "#0c0e18",
            "palette": ["#090a12", "#15172b", "#3b2fe4", "#6d3cff", "#d98dff", "#25203d"],
            "contrast": 1.22,
            "saturation": 1.18,
            "grain": 12,
            "dark": True,
        },
    },
    "indigo-magenta-random-soft": {
        "seed": 202,
        "filename": "indigo-magenta-random-soft.png",
        "kwargs": {
            "base": "#061052",
            "palette": ["#020735", "#061c87", "#2c2ee6", "#934cff", "#f294ff", "#f7c0ff"],
            "contrast": 1.20,
            "saturation": 1.18,
            "grain": 12,
            "dark": True,
        },
    },
    "muted-data-card-soft": {
        "seed": 204,
        "filename": "muted-data-card-soft.png",
        "kwargs": {
            "base": "#f4f1ec",
            "palette": ["#fbfaf7", "#dee2f7", "#b8c1e8", "#e8c3cb", "#d9cec2", "#2a3146"],
            "contrast": 1.12,
            "saturation": 0.96,
            "grain": 8,
            "dark": False,
        },
    },
    "red-top-paper-wash": {
        "seed": 206,
        "filename": "red-top-paper-wash.png",
        "render": red_top_paper_wash,
    },
}


def render_preset(name: str, out_dir: Path, seed_override: int | None = None) -> Path:
    preset = PRESETS[name]
    seed = seed_override if seed_override is not None else preset["seed"]
    out_path = out_dir / preset["filename"]
    if "render" in preset:
        return preset["render"](seed, out_path)
    return random_color_field(seed=seed, out_path=out_path, **preset["kwargs"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="active-warm-white-red-paper")
    parser.add_argument("--seed", type=int, default=None, help="Override the preset seed.")
    parser.add_argument("--out-dir", type=Path, default=Path.cwd())
    parser.add_argument("--list", action="store_true", help="List available presets and exit.")
    args = parser.parse_args()

    if args.list:
        for name, preset in PRESETS.items():
            print(f"{name}\tseed={preset['seed']}\tfilename={preset['filename']}")
        return

    print(render_preset(args.preset, args.out_dir, args.seed))


if __name__ == "__main__":
    main()
