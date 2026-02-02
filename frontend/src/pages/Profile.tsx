import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Card, CardContent } from "../components/ui/Card";
import { Avatar, AvatarImage, AvatarFallback } from "../components/ui/Avatar";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { fetchProfile, type UserProfile, type MentorRead } from "../api/profile";
import { Send } from "lucide-react";

function mentorAvatarUrl(mentor: MentorRead): string {
  const name = mentor.name.trim() || "Mentor";
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&size=128`;
}

export default function Profile() {
  const { user: authUser } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchProfile();
        if (!cancelled) setProfile(data);
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load profile");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const displayName = profile
    ? [profile.first_name, profile.last_name].filter(Boolean).join(" ") ||
      profile.username ||
      "User"
    : authUser
      ? [authUser.first_name, authUser.last_name].filter(Boolean).join(" ") ||
        authUser.username ||
        "User"
      : "User";

  if (loading) {
    return (
      <div className="py-6 flex items-center justify-center min-h-[40vh]">
        <p className="text-slate-400">Loading profile…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-6">
        <p className="text-red-400" role="alert">
          {error}
        </p>
      </div>
    );
  }

  const stats = profile?.stats ?? {
    resources_count: 0,
    ratings_count: 0,
    team_count: 0,
  };
  const skills = profile?.skills ?? [];
  const mentors = profile?.mentors ?? [];

  return (
    <div className="py-6">
      <section className="mb-8">
        <Card className="p-4">
          <div className="flex items-center gap-4">
            <Avatar size="xl">
              <AvatarImage src={undefined} />
              <AvatarFallback name={displayName} />
            </Avatar>
            <div className="min-w-0 flex-1">
              <h2 className="text-lg font-semibold text-slate-100 truncate">
                {displayName}
              </h2>
              {(profile?.username ?? authUser?.username) && (
                <p className="text-sm text-slate-400">
                  @{profile?.username ?? authUser?.username}
                </p>
              )}
            </div>
          </div>
        </Card>
      </section>

      <section className="mb-8">
        <h3 className="text-base font-semibold text-slate-100 mb-2">Stats</h3>
        <Card className="p-4">
          <CardContent className="p-0 flex flex-wrap gap-4 text-sm">
            <div>
              <span className="text-slate-500">Resources</span>
              <p className="text-slate-200 font-medium">
                {stats.resources_count}
              </p>
            </div>
            <div>
              <span className="text-slate-500">Ratings</span>
              <p className="text-slate-200 font-medium">{stats.ratings_count}</p>
            </div>
            <div>
              <span className="text-slate-500">Team</span>
              <p className="text-slate-200 font-medium">{stats.team_count}</p>
            </div>
          </CardContent>
        </Card>
      </section>

      <section className="mb-6">
        <h3 className="text-base font-semibold text-slate-100 mb-2">
          Skills / Technologies
        </h3>
        {skills.length === 0 ? (
          <p className="text-slate-500 text-sm">
            No skills detected from favorites yet.
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {skills.map((skill) => (
              <Badge key={skill} variant="tech">
                {skill}
              </Badge>
            ))}
          </div>
        )}
      </section>

      <section>
        <h3 className="text-base font-semibold text-slate-100 mb-2">
          {profile?.mentors_personalized ? "Your Mentors" : "Recommended Mentors"}
        </h3>
        {mentors.length === 0 ? (
          <p className="text-slate-500 text-sm py-4">No mentors yet.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {mentors.map((mentor) => (
              <Card
                key={mentor.id}
                className="p-4 bg-slate-800/80 border-white/10"
              >
                <CardContent className="p-0 flex flex-col gap-3">
                  <div className="flex items-center gap-3">
                    <Avatar size="lg">
                      <AvatarImage src={mentorAvatarUrl(mentor)} />
                      <AvatarFallback name={mentor.name} />
                    </Avatar>
                    <div className="min-w-0 flex-1">
                      <p className="font-semibold text-slate-100 truncate">
                        {mentor.name}
                      </p>
                      <p className="text-sm text-slate-400">{mentor.role}</p>
                    </div>
                  </div>
                  {mentor.username ? (
                    <a
                      href={`https://t.me/${mentor.username}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex"
                      aria-label={`Contact ${mentor.name} via Telegram`}
                    >
                      <Button variant="secondary" size="sm" className="w-full">
                        <Send className="h-4 w-4 mr-1.5" />
                        Contact via Telegram
                      </Button>
                    </a>
                  ) : (
                    <Button variant="secondary" size="sm" disabled className="w-full">
                      <Send className="h-4 w-4 mr-1.5" />
                      Contact via Telegram
                    </Button>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
