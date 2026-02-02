# TechVault Frontend — Folder Structure

```
src/
├── api/              # API client and endpoints
│   ├── client.ts
│   ├── auth.ts
│   ├── mentors.ts
│   └── ...
├── components/
│   ├── ui/           # Reusable UI primitives (dark theme)
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Avatar.tsx
│   │   └── index.ts
│   ├── Layout.tsx    # App shell: bottom nav + safe area
│   └── MentorsList.tsx
├── contexts/
│   └── AuthContext.tsx
├── pages/
│   ├── Login.tsx     # Centered logo + Telegram login
│   ├── Home.tsx      # Feed (resources) + Top Mentors
│   ├── Profile.tsx   # User info, stats, skills
│   ├── VaultSearch.tsx
│   ├── TeamFavorites.tsx
│   └── Recommendations.tsx
├── types/
├── App.tsx
├── main.tsx
└── index.css         # Tailwind + safe-area utilities
```

- **Layout:** No top header; fixed bottom nav (Home, Search, Favorites, Profile).
- **UI:** Glassmorphism cards, badges, avatar, buttons in `components/ui`.
- **Theme:** Dark (slate-900), rounded-xl, minimal borders.
