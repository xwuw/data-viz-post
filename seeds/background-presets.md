# Background Seed Presets

Use these presets when generating reusable noise/grain/liquid gradient backgrounds for HTML cards or AI-image prompts. Preserve the seed and visual intent unless the user explicitly asks to explore new backgrounds.

## active-warm-white-red-paper

- **Use for**: LatePost-style HTML card backgrounds with red/black/white charts.
- **Generator function**: `white_red_editorial`
- **Seed**: `205`
- **Canvas**: `900x1200`
- **Output filename used in current card workflow**: `background-white-red.png`
- **Visual intent**: warm white paper surface, small low-saturation red/pink area, no gray cast, light grain, editorial rather than decorative.
- **Base color**: `#fbf6ef`
- **Color masses**:
  - `#f4c8c0` at `(0.78, 0.12)`, radius `(0.50, 0.28)`, alpha `0.32`
  - `#f2d0c8` at `(0.12, 0.30)`, radius `(0.48, 0.36)`, alpha `0.24`
  - `#eaa49c` at `(0.52, 0.86)`, radius `(0.40, 0.24)`, alpha `0.34`
  - `#fffaf4` at `(0.86, 0.62)`, radius `(0.44, 0.30)`, alpha `0.42`
  - `#fffaf4` at `(0.10, 0.84)`, radius `(0.46, 0.34)`, alpha `0.36`
- **Noise**: smooth paper wash with `scale=0.04`, `blur=96`
- **Grain**: `strength=4.5`, `chroma=0.16`, `speckles=0.00035`, `dark=False`
- **Finish**: `contrast=1.035`, `saturation=0.92`, no blur

Do not add dark gray or black color masses to this preset; the chart layer already supplies black/gray data ink.
