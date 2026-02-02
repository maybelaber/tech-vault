# React + TypeScript Setup

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
