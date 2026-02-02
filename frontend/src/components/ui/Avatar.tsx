import { forwardRef, type HTMLAttributes } from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

const avatarStyles =
  "relative flex shrink-0 overflow-hidden rounded-full border-2 border-slate-600/50 bg-slate-700 text-slate-200";

const sizeMap = {
  sm: "h-8 w-8 text-xs",
  md: "h-10 w-10 text-sm",
  lg: "h-14 w-14 text-lg",
  xl: "h-20 w-20 text-xl",
};

export interface AvatarProps extends HTMLAttributes<HTMLDivElement> {
  size?: keyof typeof sizeMap;
}

const Avatar = forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, size = "md", children, ...props }, ref) => (
    <div
      ref={ref}
      className={twMerge(clsx(avatarStyles, sizeMap[size], className))}
      {...props}
    >
      {children}
    </div>
  )
);
Avatar.displayName = "Avatar";

export interface AvatarImageProps extends HTMLAttributes<HTMLImageElement> {
  src?: string | null;
  alt?: string;
}

const AvatarImage = forwardRef<HTMLImageElement, AvatarImageProps>(
  ({ src, alt = "", className, ...props }, ref) =>
    src ? (
      <img
        ref={ref}
        src={src}
        alt={alt}
        className={twMerge("aspect-square h-full w-full object-cover", className)}
        {...props}
      />
    ) : null
);
AvatarImage.displayName = "AvatarImage";

function getInitials(name: string): string {
  return name
    .trim()
    .split(/\s+/)
    .map((s) => s[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

const AvatarFallback = forwardRef<
  HTMLSpanElement,
  HTMLAttributes<HTMLSpanElement> & { name?: string }
>(({ name, className, children, ...props }, ref) => (
  <span
    ref={ref}
    className={twMerge(
      "flex h-full w-full items-center justify-center font-semibold bg-slate-600/50",
      className
    )}
    {...props}
  >
    {children ?? (name ? getInitials(name) : "?")}
  </span>
));
AvatarFallback.displayName = "AvatarFallback";

export { Avatar, AvatarImage, AvatarFallback };
