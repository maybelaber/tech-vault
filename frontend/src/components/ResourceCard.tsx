import { useNavigate } from "react-router-dom";
import { Card, CardContent } from "./ui/Card";
import { Badge } from "./ui/Badge";
import type { Resource } from "../api/recommendations";

interface ResourceCardProps {
  resource: Resource;
}

export function ResourceCard({ resource }: ResourceCardProps) {
  const navigate = useNavigate();
  const typeLabel =
    resource.resource_type === "doc"
      ? "Doc"
      : resource.resource_type === "blueprint"
        ? "Blueprint"
        : "Snippet";
  const technologyName = resource.technology?.name ?? "—";
  const skillLevelName = resource.skill_level?.name ?? "—";

  return (
    <Card
      className="p-4 h-full flex flex-col transition-transform hover:scale-[1.02] cursor-pointer focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 focus:ring-offset-slate-900"
      role="button"
      tabIndex={0}
      onClick={() => navigate(`/resources/${resource.id}`)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          navigate(`/resources/${resource.id}`);
        }
      }}
    >
      <CardContent className="p-0 flex flex-col gap-2 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="tech">{technologyName}</Badge>
          <Badge variant="level">{skillLevelName}</Badge>
          <Badge variant="outline" className="shrink-0 text-[10px]">
            {typeLabel}
          </Badge>
        </div>
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-sm font-semibold text-slate-100 line-clamp-2 flex-1 min-w-0">
            {resource.title}
          </h3>
        </div>
        {resource.description && (
          <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
            {resource.description}
          </p>
        )}
        <div className="mt-auto flex items-center gap-2 text-xs text-slate-500">
          <span>★ {resource.average_rating}</span>
          <span>·</span>
          <span>{resource.ratings_count} ratings</span>
        </div>
      </CardContent>
    </Card>
  );
}
