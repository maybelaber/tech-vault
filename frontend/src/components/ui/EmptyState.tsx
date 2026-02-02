import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import type { LucideIcon } from "lucide-react";
import { Button } from "./Button";

export interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  actionLink?: string;
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  actionLabel,
  actionLink,
}: EmptyStateProps) {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="flex flex-col items-center justify-center h-[50vh] text-center px-4"
    >
      <div className="h-16 w-16 bg-slate-800/50 rounded-full flex items-center justify-center mb-4 ring-1 ring-white/10">
        <Icon className="h-8 w-8 text-slate-400" aria-hidden />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-slate-400 max-w-xs leading-relaxed mb-6">
        {description}
      </p>
      {actionLabel && actionLink && (
        <Button onClick={() => navigate(actionLink)}>{actionLabel}</Button>
      )}
    </motion.div>
  );
}
