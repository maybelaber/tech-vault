# Figma Components

Build reusable UI in Figma with variants and auto-layout.

## Component anatomy

| Part          | Description                    |
|---------------|--------------------------------|
| Main component| Base with default props        |
| Variants      | Property combinations (e.g. size, state) |
| Instances     | Placed copies; override props |

## Naming variants

Use **Property name / Value** so dev handoff stays clear:

- `State / Default | Hover | Disabled`
- `Size / S | M | L`

## Auto-layout

1. Select frames → **Shift+A** (Auto layout).
2. Set direction (horizontal/vertical), spacing, padding.
3. Resizing: Hug contents or Fill container.

## Dev mode

Inspect CSS, copy as code, and sync with your design tokens.
