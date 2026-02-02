import { motion } from "framer-motion";
import { FileText, Users } from "lucide-react";
import { useEffect, useState } from "react";
import { fetchMentors, type Mentor } from "../api/mentors";
import { fetchRecommendations, type Resource } from "../api/recommendations";
import { fetchResources } from "../api/resources";
import {
  FeedResourceCard,
  type ResourceTypeLabel,
} from "../components/home/FeedResourceCard";
import { HomeHeader } from "../components/home/HomeHeader";
import { MentorCard } from "../components/home/MentorCard";
import { EmptyState } from "../components/ui/EmptyState";

function resourceTypeToLabel(
  t: "doc" | "blueprint" | "snippet"
): ResourceTypeLabel {
  return t === "blueprint" ? "Blueprint" : t === "snippet" ? "Snippet" : "Doc";
}

function mapResourceToFeedItem(r: Resource): {
  id: string;
  title: string;
  type: ResourceTypeLabel;
  technology: string;
  level: string;
  rating: number | string;
  likes: number;
} {
  return {
    id: String(r.id),
    title: r.title,
    type: resourceTypeToLabel(r.resource_type),
    technology: r.technology?.name ?? "—",
    level: r.skill_level?.name ?? "—",
    rating: r.average_rating,
    likes: r.ratings_count,
  };
}

export default function Home() {
  const [mentors, setMentors] = useState<{ name: string; role: string }[]>([]);
  const [resources, setResources] = useState<
    {
      id?: string;
      title: string;
      type: ResourceTypeLabel;
      technology: string;
      level: string;
      rating: number | string;
      likes: number;
    }[]
  >([]);
  const [loadingMentors, setLoadingMentors] = useState(true);
  const [loadingResources, setLoadingResources] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchMentors();
        if (!cancelled) {
          setMentors(data.map((m: Mentor) => ({ name: m.name, role: "Mentor" })));
        }
      } catch {
        if (!cancelled) setMentors([]);
      } finally {
        if (!cancelled) setLoadingMentors(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        let data = await fetchRecommendations();
        if (data.length === 0) {
          data = await fetchResources({ limit: 5 });
        }
        if (!cancelled) {
          setResources(data.map(mapResourceToFeedItem));
        }
      } catch {
        try {
          const fallback = await fetchResources({ limit: 5 });
          if (!cancelled) setResources(fallback.map(mapResourceToFeedItem));
        } catch {
          if (!cancelled) setResources([]);
        }
      } finally {
        if (!cancelled) setLoadingResources(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="min-h-full bg-slate-900 pb-20">
      <div
        className="pointer-events-none fixed left-1/2 top-0 -translate-x-1/2 -translate-y-1/3 w-[120%] max-w-2xl rounded-full bg-gradient-to-b from-emerald-500/10 via-slate-900/0 to-slate-900/0 blur-3xl"
        aria-hidden
      />

      <div className="relative">
        <HomeHeader />

        <main>
          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="mb-8"
          >
            <h2 className="text-lg font-semibold text-slate-100 mb-1">
              Top Mentors
            </h2>
            <p className="text-sm text-slate-400 mb-4">
              Mentors and tech leads from your organization.
            </p>
            {loadingMentors ? (
              <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2 snap-x">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="h-[180px] w-[160px] shrink-0 snap-start rounded-xl bg-slate-800/40 animate-pulse border border-white/10"
                  />
                ))}
              </div>
            ) : mentors.length === 0 ? (
              <EmptyState
                icon={Users}
                title="No mentors yet"
                description="No recent updates. Mentors will appear here once added to the system."
              />
            ) : (
              <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2 snap-x">
                {mentors.map((m: { name: string; role: string }, i: number) => (
                  <MentorCard
                    key={`${m.name}-${i}`}
                    name={m.name}
                    role={m.role}
                  />
                ))}
              </div>
            )}
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.05 }}
            className="mb-8"
          >
            <h2 className="text-lg font-semibold text-slate-100 mb-1">
              Fresh Arrivals
            </h2>
            <p className="text-sm text-slate-400 mb-4">
              New and recommended resources for you.
            </p>
            {loadingResources ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="h-24 rounded-xl bg-slate-800/40 animate-pulse border border-white/10"
                  />
                ))}
              </div>
            ) : resources.length === 0 ? (
              <EmptyState
                icon={FileText}
                title="No recent updates"
                description="No recommended resources yet. Try the Search tab or check back later."
              />
            ) : (
              <div className="space-y-4">
                {resources.map((r) => (
                  <FeedResourceCard
                    key={r.id}
                    id={r.id}
                    title={r.title}
                    type={r.type}
                    technology={r.technology}
                    level={r.level}
                    rating={r.rating}
                    likes={r.likes}
                  />
                ))}
              </div>
            )}
          </motion.section>
        </main>
      </div>
    </div>
  );
}
