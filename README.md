# data-viz-post

LatePost-style data visualization skill for turning news material, PDFs, screenshots, links, and datasets into chart prompts, generated images, or HTML cards.

## Workflow

![data-viz-post workflow](assets/workflow.png)

## Output Modes

- **AI gen mode**: split the story into chart sections, produce image-2/gpt-image-2 prompts, then generate images after user confirmation.
- **HTML card mode**: use seaborn/matplotlib to generate precise charts, then compose a fixed 900×1200px vertical HTML card.

## Main Files

- `data-viz-post.md`: skill instructions and workflow.
- `assets/style-reference-1.md`: LatePost-style visual reference.
- `references/checklist.md`: publication and prompt QA checklist.
