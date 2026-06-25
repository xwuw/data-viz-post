# HTML Card Style System

Use this file for HTML card mode after reading `references/html-card-examples/README.md`. The target is an editorial magazine data page, not a stack of UI cards.

## Adaptive Chart Plate Layouts

Do not reuse one identical chart plate size for every card. Select a plate geometry by chart type and data density. Treat the plate as page whitespace or a print inset, not as a rounded product card.

| Layout token | Use for | CSS geometry |
| --- | --- | --- |
| `wide-hero` | horizontal bar, lollipop, dumbbell, slopegraph | `left: 74px; top: 460px; width: 752px; height: 430px;` |
| `tall-flow` | Sankey, alluvial, ecosystem map, stakeholder map | `left: 64px; top: 400px; width: 772px; height: 560px;` |
| `radial-focus` | radial bar, rose, chord, circular network | `left: 92px; top: 430px; width: 716px; height: 500px;` |
| `area-narrative` | layered area, streamgraph, timeline | `left: 58px; top: 430px; width: 784px; height: 470px;` |
| `matrix-compact` | heatmap, scorecard grid, icon matrix | `left: 86px; top: 420px; width: 728px; height: 520px;` |
| `small-multiple` | small multiples, grouped panels | `left: 64px; top: 390px; width: 772px; height: 590px;` |
| `full-bleed-editorial` | dense timelines, streamgraphs, ecosystem maps that benefit from page integration | `left: 48px; top: 380px; width: 804px; height: 620px;` |

Rules:

- Keep every plate square-cornered: `border-radius: 0`.
- Keep every plate opaque: `background: #FFFCF6` or `#FFFFFF`.
- Vary the plate width, height, and vertical position according to the chart's visual grammar.
- Never center every chart in an identical rectangle across a multi-card set.
- Leave enough room for a bottom narrative sentence and source line.
- Reduce card feeling: avoid multiple framed boxes; use one main chart field, fine divider lines, direct labels, and page-level alignment.
- For magazine-like layouts, the chart can visually extend close to the plate boundary or align with the title block, as long as labels remain readable.

## Logo Placement

Use the bundled logo asset `assets/dt-insights-logo.png` in the lower-right logo area.

- Recommended CSS: `position: absolute; right: 72px; bottom: 58px; width: 124px; height: auto;`
- Acceptable width range: 112-140px, depending on source text length.
- Preserve transparency and original colors.
- Do not redraw, recolor, crop, stretch, outline, shadow, or place the logo inside a rounded container.
- Do not leave the old empty logo placeholder visible behind the logo.

## Professional Palette Tokens

Use one palette per card set. Red is for the main conclusion only.

| Token | Use for | Colors |
| --- | --- | --- |
| `latepost-core` | default comparison and ranking | `#C92816`, `#171717`, `#B8B2A8`, `#E6DED2`, `#8A8177` |
| `flow-muted` | Sankey/alluvial/chord | `#C92816`, `#2F5F5B`, `#8C8479`, `#C9C5BA`, `#E7DFD4` |
| `editorial-earth` | sector, finance, institution cards | `#C92816`, `#5B625C`, `#A88A4A`, `#C8BFAE`, `#2A2A28` |
| `cool-ink` | technology and research cards | `#C92816`, `#2F5668`, `#6D7A80`, `#B8C5C7`, `#171717` |
| `soft-heat` | heatmap and matrix cards | `#F4EDE4`, `#E8C7B8`, `#D98E76`, `#C92816`, `#681F17` |

Avoid:

- Default seaborn palettes such as `deep`, `bright`, `pastel`, `Set1`, `Paired`, `tab10` unless manually desaturated and reconciled with the card palette.
- Red/green binary palettes unless the data semantically requires gain/loss; even then use muted red and warm gray instead of traffic-light colors.
- High-saturation blue, green, purple, or orange against the warm paper background.
- Generic rainbow multi-series palettes and traffic-light red/green pairings.

## Chart Sophistication

Prefer higher-level editorial chart forms when the data structure supports them:

- Use lollipop, dot plot, ordered strip, dumbbell, slopegraph, or paired lollipop before default grouped bars.
- Use alluvial/Sankey/parallel sets for source-target-value flows.
- Use layered area, streamgraph, or horizon-style area before a plain multi-line chart when multiple time series overlap.
- Use radial bar, rose, chord, or circular network only when circular organization clarifies the relationships.
- Use heatmap, annotated tile matrix, small multiples, or scorecard grid for dense multi-metric comparisons.

Fall back to simple bars or lines only when the advanced form would obscure the conclusion.

## Matplotlib/Seaborn Baseline

```python
sns.set_theme(
    context="paper",
    style="ticks",
    font="Noto Sans CJK SC",
    rc={
        "axes.facecolor": "#FFFCF6",
        "figure.facecolor": "#FFFCF6",
        "axes.edgecolor": "#D8D0C4",
        "axes.labelcolor": "#5F5A52",
        "xtick.color": "#6F685F",
        "ytick.color": "#6F685F",
        "grid.color": "#ECE7DE",
        "grid.alpha": 0.32,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
    },
)
```

Only enable axis grid lines when they improve reading. For bar/ranking charts, prefer direct labels over visible grid lines.
