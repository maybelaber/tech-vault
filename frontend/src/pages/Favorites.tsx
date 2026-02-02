import { useState, useEffect } from "react";
import { Heart } from "lucide-react";
import { EmptyState } from "../components/ui/EmptyState";
import { ResourceCard } from "../components/ResourceCard";
import { fetchFavorites } from "../api/favorites";
import type { Resource } from "../api/recommendations";

export default function Favorites() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoading(true);
        const data = await fetchFavorites();
        if (!cancelled) setResources(data);
      } catch {
        if (!cancelled) setResources([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="py-6 flex items-center justify-center min-h-[40vh]">
        <p className="text-slate-400">Loading…</p>
      </div>
    );
  }

  return (
    <div className="py-6">
      <h2 className="text-lg font-semibold text-slate-100 mb-1">Favorites</h2>
      <p className="text-slate-400 text-sm mb-4">
        Resources you liked. Tap a card to open details.
      </p>
      {resources.length === 0 ? (
        <EmptyState
          icon={Heart}
          title="No favorites yet"
          description="Like resources on their detail page to see them here."
          actionLabel="Explore Vault"
          actionLink="/vault-search"
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {resources.map((resource) => (
            <ResourceCard key={resource.id} resource={resource} />
          ))}
        </div>
      )}
    </div>
  );
}
