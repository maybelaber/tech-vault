# Design Tokens in Figma

Use design tokens to keep colors, spacing, and typography consistent across products.

## Token structure

| Token type   | Example name      | Value   |
|-------------|-------------------|---------|
| Color       | `primary.500`     | #3B82F6 |
| Spacing     | `space.4`         | 16px    |
| Typography  | `font.heading.1`  | 24px    |

## Exporting from Figma

1. Create a **Variables** collection (e.g. "Brand").
2. Define modes for light/dark if needed.
3. Export via **Inspect** or plugins (e.g. Tokens Studio).

```json
{
  "color": {
    "primary": {
      "500": { "value": "#3B82F6", "type": "color" }
    }
  }
}
```

## Using in code

Map Figma variables to CSS custom properties or your design system config.
