import { Link } from "react-router-dom";
import { FileText, Layout, Code, Star, Heart } from "lucide-react";
import { Badge } from "../ui/Badge";

export type ResourceTypeLabel = "Doc" | "Blueprint" | "Snippet" | "Video";

export interface FeedResourceCardProps {
  id?: string;
  title: string;
  type: ResourceTypeLabel;
  technology: string;
  level: string;
  rating: number | string;
  likes: number;
}

const typeIcons: Record<ResourceTypeLabel, React.ComponentType<{ className?: string }>> = {
  Doc: FileText,
  Blueprint: Layout,
  Snippet: Code,
  Video: FileText,
};

const cardClassName =
  "block w-full text-left rounded-xl border border-white/10 bg-slate-800/40 p-4 shadow-lg backdrop-blur-sm transition-transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 focus:ring-offset-slate-900";

export function FeedResourceCard({
  id,
  title,
  type,
  technology,
  level,
  rating,
  likes,
}: FeedResourceCardProps) {
  const TypeIcon = typeIcons[type] ?? FileText;

  const content = (
    <>
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="tech">{technology}</Badge>
        <Badge variant="level">{level}</Badge>
      </div>
      <div className="mt-3 flex items-start gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-700/60 text-slate-300">
          <TypeIcon className="h-4 w-4" />
        </div>
        <h3 className="line-clamp-2 min-w-0 flex-1 text-sm font-semibold leading-tight text-slate-100">
          {title}
        </h3>
      </div>
      <div className="mt-3 flex items-center gap-4 text-xs text-slate-400">
        <span className="flex items-center gap-1">
          <Star className="h-3.5 w-3.5 text-amber-400" aria-hidden />
          <span>{typeof rating === "number" ? rating.toFixed(1) : rating}</span>
        </span>
        <span className="flex items-center gap-1">
          <Heart className="h-3.5 w-3.5 text-rose-400/80" aria-hidden />
          <span>{likes}</span>
        </span>
      </div>
    </>
  );

  if (id) {
    return (
      <Link to={`/resources/${id}`} className={cardClassName}>
        {content}
      </Link>
    );
  }
  return <article className={cardClassName}>{content}</article>;
}
