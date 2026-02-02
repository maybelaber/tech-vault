import { apiClient } from "./client";

export interface MentorRead {
  id: string;
  name: string;
  role: string;
  username: string | null;
}

export interface ProfileStats {
  resources_count: number;
  ratings_count: number;
  team_count: number;
}

export interface UserProfile {
  id: string;
  telegram_id: number;
  username: string | null;
  first_name: string | null;
  last_name: string | null;
  team_id: string | null;
  skill_level_id: string | null;
  created_at: string;
  updated_at: string;
  stats: ProfileStats;
  skills: string[];
  mentors: MentorRead[];
  /** true = "Your Mentors" (from favorites), false = "Recommended Mentors" (fallback) */
  mentors_personalized: boolean;
}

export async function fetchProfile(): Promise<UserProfile> {
  const { data } = await apiClient.get<UserProfile>("/profile");
  return data;
}
