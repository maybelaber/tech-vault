# React Hooks Cheatsheet

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
