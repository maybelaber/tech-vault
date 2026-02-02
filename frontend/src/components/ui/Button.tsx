import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-all active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900 disabled:pointer-events-none disabled:opacity-50 min-h-[44px] min-w-[44px] touch-manipulation",
  {
    variants: {
      variant: {
        primary:
          "bg-emerald-500 text-white hover:bg-emerald-400 shadow-lg shadow-emerald-500/25",
        secondary:
          "bg-slate-700/80 text-slate-100 hover:bg-slate-600/80 border border-slate-600/50",
        ghost: "text-slate-300 hover:bg-slate-800/80 hover:text-slate-100",
        outline:
          "border border-slate-500/50 text-slate-200 hover:bg-slate-800/60",
      },
      size: {
        sm: "px-3 py-2 text-sm rounded-lg",
        md: "px-5 py-2.5 text-base",
        lg: "px-6 py-3 text-lg rounded-xl",
        icon: "p-2.5",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      ref={ref}
      className={twMerge(clsx(buttonVariants({ variant, size, className })))}
      {...props}
    />
  )
);
Button.displayName = "Button";

export { Button, buttonVariants };
