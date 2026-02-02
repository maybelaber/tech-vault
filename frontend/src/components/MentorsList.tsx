import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { fetchMentors } from "../api/mentors";
import { Card, CardContent } from "./ui/Card";
import { Badge } from "./ui/Badge";

export default function MentorsList() {
  const [mentors, setMentors] = useState<{ name: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError(null);
        const list = await fetchMentors();
        if (!cancelled) {
          setMentors(list.map((m) => ({ name: m.name })));
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load mentors");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <p className="text-slate-400 text-sm py-4">Loading mentors…</p>
    );
  }

  if (error) {
    return (
      <p className="text-red-400 text-sm py-4" role="alert">
        {error}
      </p>
    );
  }

  if (mentors.length === 0) {
    return (
      <p className="text-slate-500 text-sm py-4">No mentors yet.</p>
    );
  }

  return (
    <ul className="space-y-3">
      {mentors.map((mentor, i) => (
        <motion.li
          key={mentor.name}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.04 }}
        >
          <Card className="p-4">
            <CardContent className="p-0 flex items-center gap-3">
              <Badge variant="tech">{mentor.name}</Badge>
            </CardContent>
          </Card>
        </motion.li>
      ))}
    </ul>
  );
}
