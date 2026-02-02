import { useState } from "react";
import { Star } from "lucide-react";

const MAX_STARS = 5;

export interface StarRatingProps {
  /** Current user's rating (1-5), or null if not rated */
  value: number | null;
  /** Global average (for display, e.g. 4.2) */
  average: number;
  /** Callback when user clicks a star (1-5) */
  onRate?: (star: number) => void;
  /** If true, stars are not clickable and no hover effect */
  readonly?: boolean;
  /** Optional count of ratings for label */
  ratingsCount?: number;
}

export function StarRating({
  value,
  average,
  onRate,
  readonly = false,
  ratingsCount,
}: StarRatingProps) {
  const [hoverStar, setHoverStar] = useState<number | null>(null);
  const displayValue = readonly ? average : hoverStar ?? value ?? average;
  const effectiveValue = typeof displayValue === "number" ? displayValue : 0;

  const handleClick = (star: number) => {
    if (!readonly && onRate) onRate(star);
  };

  return (
    <div className="flex items-center gap-2 flex-wrap">
      <div
        className="flex items-center gap-0.5"
        role={readonly ? undefined : "slider"}
        aria-label={readonly ? `Rating: ${average} out of 5` : "Rate 1 to 5 stars"}
        aria-valuemin={1}
        aria-valuemax={MAX_STARS}
        aria-valuenow={value ?? undefined}
        onMouseLeave={() => !readonly && setHoverStar(null)}
      >
        {Array.from({ length: MAX_STARS }, (_, i) => {
          const star = i + 1;
          const filled = effectiveValue >= star;
          return (
            <button
              key={star}
              type="button"
              disabled={readonly}
              className={`
                p-0.5 rounded focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/50 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900
                ${!readonly ? "cursor-pointer hover:scale-110 transition-transform" : "cursor-default"}
              `}
              onMouseEnter={() => !readonly && setHoverStar(star)}
              onClick={() => handleClick(star)}
              aria-label={`${star} star${star > 1 ? "s" : ""}`}
              aria-pressed={value === star}
            >
              <Star
                className={`h-6 w-6 transition-colors ${
                  filled
                    ? "text-amber-400 fill-amber-400"
                    : "text-slate-500 fill-transparent"
                }`}
                aria-hidden
              />
            </button>
          );
        })}
      </div>
      <span className="text-sm text-slate-500">
        <span className="text-slate-300 font-medium">{Number(average).toFixed(1)}</span>
        {ratingsCount != null && (
          <>
            <span className="mx-1">·</span>
            <span>{ratingsCount} ratings</span>
          </>
        )}
      </span>
    </div>
  );
}
