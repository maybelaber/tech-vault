#!/usr/bin/env python3
"""Generate dummy Markdown content for demo resources (design tokens, migrations, React, Figma, hooks)."""

import os

# backend/static/demo — same path used by main.py for StaticFiles mount at /demo
BACKEND_ROOT = os.path.join(os.path.dirname(__file__), "..")
DEMO_DIR = os.path.join(BACKEND_ROOT, "static", "demo")

FILES = {
    "design_tokens.md": """# Design Tokens in Figma

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
""",
    "postgresql_migrations.md": """# PostgreSQL Migrations

Best practices for schema changes with zero-downtime deployments.

## Naming convention

| Pattern        | Example                    |
|----------------|----------------------------|
| Create table   | `YYYYMMDD_create_users`    |
| Add column     | `YYYYMMDD_add_email_to_users` |
| Index          | `YYYYMMDD_idx_users_email` |

## Example migration (Alembic / raw SQL)

```sql
-- Add nullable column first (safe)
ALTER TABLE user_data.resources
  ADD COLUMN IF NOT EXISTS file_size_bytes BIGINT;

-- Backfill data, then add constraint if needed
-- ALTER TABLE user_data.resources ALTER COLUMN file_size_bytes SET NOT NULL;
```

## Rollback

Always write a reversible migration or document the rollback steps.
""",
    "react_typescript_setup.md": """# React + TypeScript Setup

Quick setup for a Vite + React + TypeScript app.

## Create project

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app && npm install
```

## Key config

| File           | Purpose                    |
|----------------|----------------------------|
| `tsconfig.json`| Strict mode, path aliases  |
| `vite.config.ts` | Build, env prefix `VITE_` |

## Typing props

```tsx
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  )
}
```

Enable `strict: true` in `tsconfig.json` for safer code.
""",
    # Alias for DB paths that use + (e.g. /demo/react_+_typescript_setup.md)
    # same content as react_typescript_setup.md, filled below
    "react_+_typescript_setup.md": None,
    "figma_components.md": """# Figma Components

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
""",
    "react_hooks_cheatsheet.md": """# React Hooks Cheatsheet

Quick reference for common hooks.

## useState

```tsx
const [count, setCount] = useState(0)
setCount((prev) => prev + 1)
```

## useEffect

| Dependency     | Behavior                    |
|----------------|-----------------------------|
| `[]`           | Run once on mount           |
| `[a, b]`       | Run when `a` or `b` changes |
| none           | Run after every render      |

```tsx
useEffect(() => {
  const sub = subscribe(id)
  return () => sub.unsubscribe()
}, [id])
```

## useMemo / useCallback

- **useMemo**: cache a computed value.
- **useCallback**: cache a function (e.g. for `useEffect` or child props).

```tsx
const list = useMemo(() => items.filter(Boolean), [items])
const onSave = useCallback(() => save(data), [data])
```
""",
}


def main() -> None:
    os.makedirs(DEMO_DIR, exist_ok=True)
    # Resolve alias: react_+_typescript_setup.md uses same content as react_typescript_setup.md
    if FILES.get("react_+_typescript_setup.md") is None:
        FILES["react_+_typescript_setup.md"] = FILES["react_typescript_setup.md"]
    for filename, content in FILES.items():
        if content is None:
            continue
        path = os.path.join(DEMO_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {path}")
    print(
        f"Done. {len([c for c in FILES.values() if c is not None])} files in {DEMO_DIR}")


if __name__ == "__main__":
    main()
