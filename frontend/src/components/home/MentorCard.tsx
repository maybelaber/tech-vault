export interface MentorCardProps {
  name: string;
  role: string;
  avatarUrl?: string | null;
}

const avatarUrlForName = (name: string) =>
  `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&size=96`;

export function MentorCard({ name, role, avatarUrl }: MentorCardProps) {
  const src = avatarUrl ?? avatarUrlForName(name);

  return (
    <article className="flex w-[160px] shrink-0 flex-col items-center rounded-xl border border-white/10 bg-slate-800/40 p-4 shadow-xl backdrop-blur-sm snap-start">
      <img
        src={src}
        alt=""
        className="h-14 w-14 rounded-full border-2 border-slate-600/50 object-cover ring-2 ring-white/5"
      />
      <h3 className="mt-3 truncate w-full text-center text-sm font-medium text-slate-100">
        {name}
      </h3>
      <p className="mt-0.5 text-xs text-slate-400 truncate w-full text-center">
        {role}
      </p>
    </article>
  );
}
