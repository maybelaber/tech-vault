import { Card, CardContent } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { Heart } from "lucide-react";

// TODO: replace with real data from API
const favorites: unknown[] = [];

export default function TeamFavorites() {
  return (
    <div className="py-6">
      <h2 className="text-lg font-semibold text-slate-100 mb-1">Team Favorites</h2>
      <p className="text-slate-400 text-sm mb-4">
        Favorites from your team (5-star picks). Yours highlighted.
      </p>
      {favorites.length === 0 ? (
        <EmptyState
          icon={Heart}
          title="No favorites yet"
          description="Save the most important technologies and mentors here for quick access."
          actionLabel="Explore Vault"
          actionLink="/vault-search"
        />
      ) : (
        <Card className="p-4">
          <CardContent className="p-0">
            {/* List of favorites when data is available */}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
