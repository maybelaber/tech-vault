import { forwardRef, type HTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

const badgeVariants = cva(
  "inline-flex items-center rounded-lg px-2.5 py-0.5 text-xs font-medium border",
  {
    variants: {
      variant: {
        default:
          "border-slate-600/50 bg-slate-700/60 text-slate-200",
        tech: "border-emerald-500/40 bg-emerald-500/20 text-emerald-300",
        level: "border-amber-500/40 bg-amber-500/20 text-amber-300",
        outline: "border-slate-500/50 text-slate-400 bg-transparent",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant, ...props }, ref) => (
    <span
      ref={ref}
      className={twMerge(clsx(badgeVariants({ variant }), className))}
      {...props}
    />
  )
);
Badge.displayName = "Badge";

export { Badge, badgeVariants };
