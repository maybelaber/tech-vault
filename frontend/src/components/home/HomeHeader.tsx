import { useAuth } from "../../contexts/AuthContext";

export function HomeHeader() {
  const { user } = useAuth();
  const displayName =
    user?.first_name ?? user?.username ?? "there";

  return (
    <header className="pt-safe-area-inset-top pb-6">
      <h1 className="text-2xl font-bold tracking-tight">
        <span className="bg-gradient-to-r from-slate-100 via-emerald-200/90 to-slate-200 bg-clip-text text-transparent">
          Hello, {displayName} 👋
        </span>
      </h1>
      <p className="mt-1 text-sm text-slate-400">
        Ready to expand your knowledge?
      </p>
    </header>
  );
}
