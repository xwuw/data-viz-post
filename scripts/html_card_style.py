#!/usr/bin/env python3
"""Reusable style tokens for data-viz-post HTML cards."""

from __future__ import annotations

import argparse
import json


CARD_SIZE = {"width": 900, "height": 1200}

FONT_STACKS = {
    "title": '"Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", "STSong", "SimSun", serif',
    "body": '"Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif',
    "number": '"Avenir Next", "Inter", "Helvetica Neue", Arial, sans-serif',
}

COLORS = {
    "paper": "#F8F7F4",
    "plate": "#FFFCF6",
    "ink": "#171717",
    "muted": "#8A8177",
    "hairline": "#D8D0C4",
    "grid": "#ECE7DE",
    "latepost_red": "#C92816",
}

LOGO = {
    "asset": "assets/dt-insights-logo.png",
    "right": 72,
    "bottom": 58,
    "width": 124,
}

PALETTES = {
    "latepost-core": ["#C92816", "#171717", "#B8B2A8", "#E6DED2", "#8A8177"],
    "flow-muted": ["#C92816", "#2F5F5B", "#8C8479", "#C9C5BA", "#E7DFD4"],
    "editorial-earth": ["#C92816", "#5B625C", "#A88A4A", "#C8BFAE", "#2A2A28"],
    "cool-ink": ["#C92816", "#2F5668", "#6D7A80", "#B8C5C7", "#171717"],
    "soft-heat": ["#F4EDE4", "#E8C7B8", "#D98E76", "#C92816", "#681F17"],
}

PLATE_LAYOUTS = {
    "wide-hero": {"left": 74, "top": 460, "width": 752, "height": 430},
    "tall-flow": {"left": 64, "top": 400, "width": 772, "height": 560},
    "radial-focus": {"left": 92, "top": 430, "width": 716, "height": 500},
    "area-narrative": {"left": 58, "top": 430, "width": 784, "height": 470},
    "matrix-compact": {"left": 86, "top": 420, "width": 728, "height": 520},
    "small-multiple": {"left": 64, "top": 390, "width": 772, "height": 590},
    "full-bleed-editorial": {"left": 48, "top": 380, "width": 804, "height": 620},
}

CHART_LAYOUT_MAP = {
    "bar": "wide-hero",
    "horizontal_bar": "wide-hero",
    "lollipop": "wide-hero",
    "dot_plot": "wide-hero",
    "dumbbell": "wide-hero",
    "slopegraph": "wide-hero",
    "sankey": "tall-flow",
    "alluvial": "tall-flow",
    "ecosystem": "tall-flow",
    "stakeholder": "tall-flow",
    "editorial_ecosystem": "full-bleed-editorial",
    "radial_bar": "radial-focus",
    "rose": "radial-focus",
    "chord": "radial-focus",
    "circular_network": "radial-focus",
    "area": "area-narrative",
    "streamgraph": "area-narrative",
    "horizon_area": "full-bleed-editorial",
    "timeline": "area-narrative",
    "dense_timeline": "full-bleed-editorial",
    "heatmap": "matrix-compact",
    "scorecard": "matrix-compact",
    "icon_matrix": "matrix-compact",
    "small_multiple": "small-multiple",
}


def layout_for(chart_type: str) -> dict[str, int]:
    token = CHART_LAYOUT_MAP.get(chart_type, "wide-hero")
    return PLATE_LAYOUTS[token]


def payload() -> dict[str, object]:
    return {
        "card_size": CARD_SIZE,
        "font_stacks": FONT_STACKS,
        "colors": COLORS,
        "logo": LOGO,
        "palettes": PALETTES,
        "plate_layouts": PLATE_LAYOUTS,
        "chart_layout_map": CHART_LAYOUT_MAP,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart-type", help="Print the plate layout for a chart type.")
    parser.add_argument("--palette", choices=sorted(PALETTES), help="Print one palette.")
    args = parser.parse_args()

    if args.chart_type:
        print(json.dumps(layout_for(args.chart_type), ensure_ascii=False, indent=2))
        return
    if args.palette:
        print(json.dumps(PALETTES[args.palette], ensure_ascii=False, indent=2))
        return
    print(json.dumps(payload(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
