import { useState, useEffect } from "react";
import { Search, Sparkles, Loader2 } from "lucide-react";
import { Card, CardContent } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { ResourceCard } from "../components/ResourceCard";
import { fetchRecommendations, type Resource } from "../api/recommendations";
import { fetchResources } from "../api/resources";
import { useDebounce } from "../hooks/useDebounce";

const DEBOUNCE_MS = 500;

export default function VaultSearch() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, DEBOUNCE_MS);

  const [recommendations, setRecommendations] = useState<Resource[]>([]);
  const [loadingRecs, setLoadingRecs] = useState(true);

  const [searchResults, setSearchResults] = useState<Resource[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const hasSearched = debouncedQuery.trim().length > 0;
  const isEmptyResults = hasSearched && searchResults.length === 0 && !isLoading;

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoadingRecs(true);
        const data = await fetchRecommendations();
        if (!cancelled) setRecommendations(data);
      } catch {
        if (!cancelled) setRecommendations([]);
      } finally {
        if (!cancelled) setLoadingRecs(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setSearchResults([]);
      setIsLoading(false);
      return;
    }
    let cancelled = false;
    setIsLoading(true);
    (async () => {
      try {
        const data = await fetchResources({ search: debouncedQuery });
        if (!cancelled) setSearchResults(data);
      } catch {
        if (!cancelled) setSearchResults([]);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [debouncedQuery]);

  return (
    <div className="py-6">
      <h2 className="text-lg font-semibold text-slate-100 mb-1">Vault Search</h2>
      <p className="text-slate-400 text-sm mb-4">
        Browse all docs, blueprints, snippets with filters.
      </p>
      <Card className="p-4 mb-4">
        <CardContent className="p-0 relative">
          <input
            type="search"
            placeholder="Search resources..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full rounded-lg border border-slate-600/50 bg-slate-800/50 px-4 py-3 pr-10 text-slate-100 placeholder:text-slate-500 focus:border-emerald-500/50 focus:outline-none focus:ring-1 focus:ring-emerald-500/50"
            aria-describedby={hasSearched && isLoading ? "search-loading" : undefined}
          />
          {hasSearched && isLoading && (
            <span
              id="search-loading"
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
              aria-label="Searching"
            >
              <Loader2 className="h-5 w-5 animate-spin" />
            </span>
          )}
        </CardContent>
      </Card>

      {!hasSearched ? (
        loadingRecs ? (
          <div
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
            aria-busy="true"
            aria-label="Loading recommendations"
          >
            {[1, 2, 3].map((i) => (
              <Card key={i} className="p-4 h-full animate-pulse">
                <CardContent className="p-0 space-y-3">
                  <div className="h-4 bg-slate-700/60 rounded w-3/4" />
                  <div className="h-3 bg-slate-700/40 rounded w-full" />
                  <div className="h-3 bg-slate-700/40 rounded w-1/2" />
                  <div className="h-3 bg-slate-700/40 rounded w-1/3 mt-2" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : recommendations.length === 0 ? (
          <EmptyState
            icon={Sparkles}
            title="Ready to explore?"
            description="Start typing above to search through documentation, mentors, and technologies."
          />
        ) : (
          <>
            <h2 className="text-lg font-semibold text-slate-200 mb-4">
              Recommended for You
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendations.map((resource) => (
                <ResourceCard key={resource.id} resource={resource} />
              ))}
            </div>
          </>
        )
      ) : isEmptyResults ? (
        <EmptyState
          icon={Search}
          title="No results found"
          description="Try adjusting your search query."
        />
      ) : isLoading ? (
        <div className="flex items-center justify-center py-12 text-slate-400" aria-busy="true">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {searchResults.map((resource) => (
            <ResourceCard key={resource.id} resource={resource} />
          ))}
        </div>
      )}
    </div>
  );
}
